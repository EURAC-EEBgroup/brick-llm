import os
import json
import pkg_resources
from typing import Any, Dict, Literal
from rdflib import Graph

from ..logger import custom_logger
from ..utils import get_hierarchical_info

ontology_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "Brick.ttl"))

hierarchy_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "brick_hierarchy.json"))
brick_hierarchy = json.load(open(hierarchy_path))


def check_sensor_presence(state: Dict[str, Any]) -> Literal["get_sensors", "validate_schema"]:
    """
    Check if the sensors are present in the building structure.

    Args:
        state (Dict[str, Any]): The current state containing the sensor structure.

    Returns:
        Literal["get_sensors", "schema_to_ttl"]: The next node to visit.
    """

    custom_logger.eurac("📡 Checking for sensor presence")

    graph = state["graph"]

    g = Graph()

    # Leave graph untouched to not add Brick in it
    if graph is not None:
        for triple in graph:
            g.add(triple)

    g.parse(ontology_path, format="turtle")

    # Query subclass of Point
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    
    SELECT ?point
    WHERE {
        ?point rdf:type/rdfs:subClassOf* brick:Point .
    }
    """

    res_query = g.query(query)

    if len(res_query) == 0:
        is_sensor = False
    else:
        is_sensor = True

    if is_sensor:
        return "get_sensors"
    else:
        return "validate_schema"
