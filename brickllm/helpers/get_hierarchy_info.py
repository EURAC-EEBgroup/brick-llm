import json, os, re
from collections import defaultdict
from brickllm.helpers.query_brickschema import general_query

brick_hierarchy_path = os.path.join(os.getcwd(), 'brick_hierarchy.json')

# Load the JSON file
with open(brick_hierarchy_path) as f:
    data = json.load(f)

# Function to recursively find parents
def find_parents(current_data, target, parents=None):
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
def get_children(current_data, target):
    if target in current_data:
        return list(current_data[target].keys())
    for key, value in current_data.items():
        if isinstance(value, dict):
            children = get_children(value, target)
            if children:
                return children
    return []

# Function to flatten the hierarchy
def flatten_hierarchy(current_data, parent=None, result=None):
    if result is None:
        result = []
    for key, value in current_data.items():
        if parent:
            result.append((parent, key))
        if isinstance(value, dict):
            flatten_hierarchy(value, key, result)
    return result

# Main function to get hierarchy info
def get_hierarchy_info(key):
    # Get parents
    found, parents = find_parents(data, key)
    # Get children
    children = get_children(data, key)
    return (parents, children)

# Function to recursively get all children and subchildren
def get_all_subchildren(current_data, target):
    if target in current_data:
        return current_data[target]
    for key, value in current_data.items():
        if isinstance(value, dict):
            result = get_all_subchildren(value, target)
            if result:
                return result
    return {}

# Main function to get hierarchy dictionary
def get_children_hierarchy(key, flatten=False):
    if flatten:
        return flatten_hierarchy(get_all_subchildren(data, key))
    return get_all_subchildren(data, key)

# Function to filter elements based on the given conditions
def filter_elements(elements):
    elements_info = {element: get_hierarchy_info(element) for element in elements}
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

def create_hierarchical_dict(elements, properties=False):
    hierarchy = {}

    for category in elements:
        parents, _ = get_hierarchy_info(category)
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

def find_sensor_paths(tree, path=None):
    if path is None:
        path = []

    current_path = path + [tree['name']]
    if 'children' not in tree or not tree['children']:
        if re.search(r'Sensor', tree['name']):
            sensor_path = '>'.join(current_path[:-1])
            return [{'name': tree['name'], 'path': sensor_path}]
        return []

    sensor_paths = []
    for child in tree['children']:
        sensor_paths.extend(find_sensor_paths(child, current_path))

    return sensor_paths

def build_hierarchy(relationships):
    # Helper function to recursively build the tree structure
    def build_tree(node, tree_dict):
        return {'name': node, 'children': [build_tree(child, tree_dict) for child in tree_dict[node]]} if tree_dict[node] else {'name': node}

    # Create a dictionary to hold parent-children relationships
    tree_dict = defaultdict(list)
    nodes = set()

    # Fill the dictionary with data from relationships
    for parent, child in relationships:
        tree_dict[parent].append(child)
        nodes.update([parent, child])

    # Find the root (a node that is never a child)
    root = next(node for node in tree_dict if all(node != child for _, child in relationships))

    # Build the hierarchical structure starting from the root
    hierarchy = build_tree(root, tree_dict)
    return hierarchy

def extract_ttl_content(input_string: str) -> str:
  # Use regex to match content between ```python and ```
  match = re.search(r"```code\s*(.*?)\s*```", input_string, re.DOTALL)
  if match:
      return match.group(1).strip()
  return ""
