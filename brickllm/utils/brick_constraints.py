import json
from rdflib import Graph
from typing import Dict
import os
import pkg_resources

from brickllm.utils.get_hierarchy_info import find_parents
from brickllm.utils.query_brickschema import get_query_result, general_query

brick_ttl_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "Brick.ttl")
)
# Load the Brick schema Turtle file
g = Graph()
g.parse(brick_ttl_path, format="ttl")

hierarchy_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "brick_hierarchy.json"))
brick_hierarchy = json.load(open(hierarchy_path))


def get_rel_definition() -> Dict:
    """
    Get the definition of all the relationship properties in the Brick schema.
    Returns:
        Dict: A dictionary containing the relationship properties and their definitions.

    """

    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT *
    WHERE {
        ?property a owl:AsymmetricProperty .
        ?property skos:definition ?definition .
    }
    """

    result = g.query(query)

    properties = {}
    for row in result:
        property_name = row["property"].split("#")[-1]
        properties[property_name] = {
            "definition": str(row["definition"]),
        }

    return properties


def find_rel_constraint(element: str) -> Dict:
    """
    Get the relationship constraints for a given element in the Brick schema. It extracts all the constraints of
    all its parents.
    Args:
        element: the Brick class for which the relationship constraints are to be extracted.

    Returns:
        Dict: A dictionary containing the relationship constraints and the definition of the relationship for the given element.

    """

    definitions = get_rel_definition()
    parent_list = find_parents(brick_hierarchy, element)[1]

    query = """
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?path ?class
    WHERE {{
        brick:{element} sh:property ?property .
        ?property sh:path ?path .
        {{
            ?property sh:class ?class .
        }}
        UNION
        {{
            ?property sh:or ?orList .
            ?orList rdf:rest*/rdf:first ?nodeShape .
            ?nodeShape sh:class ?class .
        }}
    }}
    """

    # Append the element to the parent list
    elements = [element] + parent_list

    property_dict = {}

    for parent in elements:
        property_list = []
        query_res = get_query_result(query.format(element=parent))
        for row in query_res:
            property_list.append(row["path"].split("#")[-1])
        property_list = list(set(property_list))

        for property in property_list:
            list_classes = []
            for prop in query_res:
                if prop["path"].split("#")[-1] == property:
                    list_classes.append(prop["class"].split("#")[-1])
            if property in property_dict:
                for class_name in list_classes:
                    if not class_name in property_dict[property]["constraints"]:
                        property_dict[property]["constraints"].append(class_name)
            else:
                try:
                    definition = definitions[property]["definition"]
                except KeyError:
                    definition = "No definition found"
                property_dict[property] = {
                    "definition": definition,
                    "constraints": list_classes
                }

        if "Meter" in parent:
            property_dict["meters"] = {
                "definition": "the subject (of Meter class) meters the object.",
                "constraints": ["Location", "Equipment", "HVAC_Equipment"]
            }

        if "Location" in elements or "Collection" in elements or "Equipment" in elements or "HVAC_Equipment" in elements:
            property_dict["isMeteredBy"] = {
                "definition": "the subject is recorded by the object.",
                "constraints": ["Meter"]
            }

        if "Location" in elements:
            property_dict["isLocationOf"] = {
                "definition": "the subject is the location of the object.",
                "constraints": ["Location", "Collection", "Equipment", "HVAC_Equipment"]
            }

    return property_dict


def get_uom_dict(point_type_list) -> Dict:
    """
    Get the unit of measures for different Brick point types.
    Args:
        point_type_list: A list of Brick point types
    Returns:
        Dict: A dictionary containing the unit of measures for the given point types.

    """
    # Create a dictionary to store the unit of measures
    uom_dict = {}

    for point_type in point_type_list:
        dict_type = {}
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        PREFIX qudt: <http://qudt.org/schema/qudt/>
        PREFIX unit: <http://qudt.org/vocab/unit/>

        SELECT ?quantity ?unit ?description
        WHERE {{
            brick:{point_type} brick:hasQuantity ?quantity .
            ?quantity qudt:applicableUnit ?unit .
            ?unit a qudt:Unit .
            OPTIONAL {{ ?unit rdfs:label ?description . 
                        }}
        }}
        """
        res_query = g.query(query)
        for row in res_query:
            dict_type[str(row['unit']).split("/")[-1]] = {
                "QUDT": str(row['unit']).split("/")[-1],
                "description": str(row['description'])
            }
        uom_dict[point_type] = dict_type

    return uom_dict