import json
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

import pkg_resources

from .query_brickschema import general_query

# Path to the JSON file
brick_hierarchy_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "brick_hierarchy.json")
)

# Load the JSON file
with open(brick_hierarchy_path) as f:
    data = json.load(f)


# Function to recursively find parents
def find_parents(
    current_data: Dict[str, Any], target: str, parents: List[str] = None
) -> Tuple[bool, List[str]]:
    """
    Recursively find the parent nodes of a target node in a hierarchical data structure.

    Args:
        current_data (dict): The current level of the hierarchy to search.
        target (str): The target node to find parents for.
        parents (list, optional): Accumulated list of parent nodes. Defaults to None.

    Returns:
        tuple: A tuple containing a boolean indicating if the target was found and a list of parent nodes.
    """
    if parents is None:
        parents = []
    for key, value in current_data.items():
        if key == target:
            return True, parents
        if isinstance(value, dict):
            found, result = find_parents(value, target, parents + [key])
            if found:
                return True, result
    return False, []


# Function to get the children of a node
def get_children(current_data: Dict[str, Any], target: str) -> List[str]:
    """
    Get the children of a target node in a hierarchical data structure.

    Args:
        current_data (dict): The current level of the hierarchy to search.
        target (str): The target node to find children for.

    Returns:
        list: A list of child nodes.
    """
    if target in current_data:
        return list(current_data[target].keys())
    for key, value in current_data.items():
        if isinstance(value, dict):
            children = get_children(value, target)
            if children:
                return children
    return []


# Function to flatten the hierarchy
def flatten_hierarchy(
    current_data: Dict[str, Any],
    parent: str = None,
    result: List[Tuple[str, str]] = None,
) -> List[Tuple[str, str]]:
    """
    Flatten a hierarchical data structure into a list of parent-child tuples.

    Args:
        current_data (dict): The current level of the hierarchy to flatten.
        parent (str, optional): The parent node. Defaults to None.
        result (list, optional): Accumulated list of parent-child tuples. Defaults to None.

    Returns:
        list: A list of tuples representing parent-child relationships.
    """
    if result is None:
        result = []
    for key, value in current_data.items():
        if parent:
            result.append((parent, key))
        if isinstance(value, dict):
            flatten_hierarchy(value, key, result)
    return result


# Main function to get hierarchy info
def get_hierarchical_info(key: str) -> Tuple[List[str], List[str]]:
    """
    Get the hierarchical information of a node, including its parents and children.

    Args:
        key (str): The target node to get information for.

    Returns:
        tuple: A tuple containing a list of parent nodes and a list of child nodes.
    """
    # Get parents
    found, parents = find_parents(data, key)
    # Get children
    children = get_children(data, key)
    return (parents, children)


# Function to recursively get all children and subchildren
def get_all_subchildren(current_data: Dict[str, Any], target: str) -> Dict[str, Any]:
    """
    Recursively get all children and subchildren of a target node.

    Args:
        current_data (dict): The current level of the hierarchy to search.
        target (str): The target node to find children for.

    Returns:
        dict: A dictionary representing the subtree of the target node.
    """
    if target in current_data:
        return current_data[target]
    for key, value in current_data.items():
        if isinstance(value, dict):
            result = get_all_subchildren(value, target)
            if result:
                return result
    return {}


# Main function to get hierarchy dictionary
def get_children_hierarchy(
    key: str, flatten: bool = False
) -> Union[Dict[str, Any], List[Tuple[str, str]]]:
    """
    Get the hierarchy of children for a target node, optionally flattening the result.

    Args:
        key (str): The target node to get children for.
        flatten (bool, optional): Whether to flatten the hierarchy. Defaults to False.

    Returns:
        dict or list: A dictionary representing the hierarchy or a list of parent-child tuples if flattened.
    """
    if flatten:
        return flatten_hierarchy(get_all_subchildren(data, key))
    return get_all_subchildren(data, key)


# Function to filter elements based on the given conditions
def filter_elements(elements: List[str]) -> List[str]:
    """
    Filter elements based on their hierarchical relationships.

    Args:
        elements (list): A list of elements to filter.

    Returns:
        list: A list of filtered elements.
    """
    elements_info = {element: get_hierarchical_info(element) for element in elements}
    filtered_elements = []

    for element, (parents, children) in elements_info.items():
        # Discard elements with no parents and no children
        if not parents and not children:
            continue
        # Check if the element is a parent of any other element
        is_parent = any(element in p_list for p_list, _ in elements_info.values())
        if is_parent:
            continue
        filtered_elements.append(element)

    return filtered_elements


def create_hierarchical_dict(
    elements: List[str], properties: bool = False
) -> Dict[str, Any]:
    """
    Create a hierarchical dictionary from a list of elements, optionally including properties.

    Args:
        elements (list): A list of elements to include in the hierarchy.
        properties (bool, optional): Whether to include properties in the hierarchy. Defaults to False.

    Returns:
        dict: A dictionary representing the hierarchical structure.
    """
    hierarchy = {}

    for category in elements:
        parents, _ = get_hierarchical_info(category)
        current_level = hierarchy

        for parent in parents:
            if parent not in current_level:
                current_level[parent] = {}
            current_level = current_level[parent]

        # Finally add the category itself
        if category not in current_level:
            if properties:
                elem_property = general_query(category)
                if len(elem_property.keys()) == 0:
                    continue
                elem_property = elem_property["property"]
                # remove "message" key from the dictionary
                for prop in elem_property.keys():
                    elem_property[prop].pop("message")
                current_level[category] = elem_property
            else:
                current_level[category] = {}

    return hierarchy


def find_sensor_paths(
    tree: Dict[str, Any], path: List[str] = None
) -> List[Dict[str, str]]:
    """
    Find paths to sensor nodes in a hierarchical tree structure.

    Args:
        tree (dict): The hierarchical tree structure.
        path (list, optional): Accumulated path to the current node. Defaults to None.

    Returns:
        list: A list of dictionaries containing sensor names and their paths.
    """
    if path is None:
        path = []

    current_path = path + [tree["name"]]
    if "children" not in tree or not tree["children"]:
        if re.search(r"Sensor", tree["name"]):
            sensor_path = ">".join(current_path[:-1])
            return [{"name": tree["name"], "path": sensor_path}]
        return []

    sensor_paths = []
    for child in tree["children"]:
        sensor_paths.extend(find_sensor_paths(child, current_path))

    return sensor_paths


def build_hierarchy(relationships: List[Tuple[str, str]]) -> Dict[str, Any]:
    """
    Build a hierarchical tree structure from a list of parent-child relationships.

    Args:
        relationships (list): A list of tuples representing parent-child relationships.

    Returns:
        dict: A dictionary representing the hierarchical tree structure.
    """

    # Helper function to recursively build the tree structure
    def build_tree(node: str, tree_dict: Dict[str, List[str]]) -> Dict[str, Any]:
        return (
            {
                "name": node,
                "children": [build_tree(child, tree_dict) for child in tree_dict[node]],
            }
            if tree_dict[node]
            else {"name": node}
        )

    # Create a dictionary to hold parent-children relationships
    tree_dict = defaultdict(list)
    nodes = set()

    # Fill the dictionary with data from relationships
    for parent, child in relationships:
        tree_dict[parent].append(child)
        nodes.update([parent, child])

    # Find the root (a node that is never a child)
    root = next(
        node for node in tree_dict if all(node != child for _, child in relationships)
    )

    # Build the hierarchical structure starting from the root
    hierarchy = build_tree(root, tree_dict)
    return hierarchy


def extract_ttl_content(input_string: str) -> str:
    """
    Extract content between code block markers in a string.

    Args:
        input_string (str): The input string containing code blocks.

    Returns:
        str: The extracted content between the code block markers.
    """
    # Use regex to match content between ```python and ```
    match = re.search(r"```code\s*(.*?)\s*```", input_string, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
