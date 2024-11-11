import os
import re
from io import StringIO
from typing import Dict, List, Optional, Tuple, Union

import pkg_resources
import pyshacl
from rdflib import Graph, Namespace, URIRef
from rdflib.query import ResultRow

# Path to the Brick schema Turtle file
brick_ttl_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "Brick.ttl")
)
# Load the Brick schema Turtle file
g = Graph()
g.parse(brick_ttl_path, format="ttl")

# Define the namespaces from the prefixes
namespaces = {
    "brick": Namespace("https://brickschema.org/schema/Brick#"),
}


# Function to get the definition from the TTL file
def get_brick_definition(element_name: str) -> str:
    """
    Get the definition of an element from the Brick schema Turtle file.

    Args:
        element_name (str): The name of the element to get the definition for.

    Returns:
        str: The definition of the element, or "No definition available" if not found.
    """
    normalized_key = element_name.replace("_", "").lower()
    for prefix, namespace in namespaces.items():
        uri = namespace[element_name]
        for s, p, o in g.triples(
            (uri, URIRef("http://www.w3.org/2004/02/skos/core#definition"), None)
        ):
            return str(o)
        uri = namespace[normalized_key]
        for s, p, o in g.triples(
            (uri, URIRef("http://www.w3.org/2004/02/skos/core#definition"), None)
        ):
            return str(o)
    return "No definition available"


# Function to get the query result without using pandas
def get_query_result(query: str) -> List[Dict[str, str]]:
    """
    Execute a SPARQL query on the Brick schema graph and return the results.

    Args:
        query (str): The SPARQL query to execute.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the query results.
    """
    result = g.query(query)
    # Convert the result to a list of dictionaries where keys are the variable names
    query_vars = list(result.vars) if result.vars is not None else []
    data: List[Dict[str, Optional[str]]] = []
    for row in result:
        if isinstance(row, ResultRow):
            data.append(
                {str(var): str(row[var]) if row[var] else None for var in query_vars}
            )
    # Remove entries with None values and reset index
    cleaned_data = [
        {key: value for key, value in row.items() if value is not None} for row in data
    ]
    return cleaned_data


# Function to clean the result, extracting the needed part of the URI
def clean_result(data: List[str]) -> List[str]:
    """
    Extract the relevant part of a URI from a list of data.

    Args:
        data (List[str]): A list of URIs to clean.

    Returns:
        List[str]: A list of extracted parts from the URIs.
    """
    return [
        re.findall(r"#(\w+)", value)[0]
        for value in data
        if re.findall(r"#(\w+)", value)
    ]


# Function to create a SPARQL query for subclasses
def query_subclass(element: str) -> str:
    """
    Create a SPARQL query to find subclasses of a given element.

    Args:
        element (str): The element to find subclasses for.

    Returns:
        str: The SPARQL query string.
    """
    return f"SELECT ?subclass WHERE {{ brick:{element} rdfs:subClassOf ?subclass . }}"


# Function to create a SPARQL query for properties
def query_properties(element: str) -> str:
    """
    Create a SPARQL query to find properties of a given element.

    Args:
        element (str): The element to find properties for.

    Returns:
        str: The SPARQL query string.
    """
    return f"""
    SELECT ?property ?message ?path ?class WHERE {{
        brick:{element} sh:property ?property .
        ?property sh:message ?message ; sh:path ?path ;
                  sh:or/rdf:rest*/rdf:first ?constraint .
        ?constraint sh:class ?class .
    }}
    """


# Function to iteratively find subclasses
def iterative_subclasses(element: str) -> List[str]:
    """
    Iteratively find all subclasses of a given element.

    Args:
        element (str): The element to find subclasses for.

    Returns:
        List[str]: A list of subclasses.
    """
    subclasses: List[str] = []
    sub_class_data = get_query_result(query_subclass(element))
    subClass = (
        clean_result([row["subclass"] for row in sub_class_data])
        if sub_class_data
        else []
    )

    while subClass:
        subclasses.append(subClass[0])
        if subClass[0] in {
            "Collection",
            "Equipment",
            "Location",
            "Measureable",
            "Point",
        }:
            break
        sub_class_data = get_query_result(query_subclass(subClass[0]))
        subClass = (
            clean_result([row["subclass"] for row in sub_class_data])
            if sub_class_data
            else []
        )

    return subclasses


# General query function to retrieve properties and relationships
def general_query(element: str) -> Dict[str, Dict[str, Union[str, List[str]]]]:
    """
    Retrieve properties and relationships for a given element.

    Args:
        element (str): The element to retrieve properties and relationships for.

    Returns:
        Dict[str, Dict[str, Union[str, List[str]]]]: A dictionary containing properties and their constraints.
    """
    subclasses = iterative_subclasses(element)
    if not subclasses:
        return {}

    query_data = get_query_result(query_properties(subclasses[-1]))
    relationships: Dict[str, Dict[str, Union[str, List[str]]]] = {}

    for row in query_data:
        property_name = clean_result([row["path"]])[0]
        if property_name not in relationships:
            relationships[property_name] = {
                "message": row["message"],
                "constraint": clean_result([row["class"]]),
            }
        else:
            if isinstance(relationships[property_name]["constraint"], list):
                relationships[property_name]["constraint"].extend(
                    clean_result([row["class"]])
                )
            else:
                relationships[property_name]["constraint"] = clean_result(
                    [row["class"]]
                )

    return {"property": relationships}


def validate_ttl(ttl_file: str, method: str = "pyshacl") -> Tuple[bool, str]:
    """
    Validate a TTL file using the specified method.

    Args:
        ttl_file (str): The TTL file to validate.
        method (str): The method to use for validation. Default is 'pyshacl'.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating if the validation was successful and a validation report or error message.
    """
    # Load the ttl file
    output_graph = Graph()
    try:
        output_graph.parse(StringIO(ttl_file), format="ttl")
    except Exception as e:
        return False, f"Failed to parse the TTL file. Content: {e}"

    if method == "pyshacl":
        valid, results_graph, report = pyshacl.validate(
            output_graph,
            shacl_graph=g,
            ont_graph=g,
            inference="rdfs",
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
            meta_shacl=False,
            advanced=False,
            js=False,
            debug=False,
        )
        return valid, report
    else:
        return False, "Method not found"
