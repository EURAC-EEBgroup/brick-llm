import json
from typing import Any, Dict
import os
import pkg_resources

from langchain_core.messages import HumanMessage, SystemMessage
from rdflib import Graph, Namespace, BNode, Literal, XSD

from .. import SensorSchema, State
from ..helpers import get_sensors_instructions
from ..logger import custom_logger
from ..utils import get_uom_dict

ontology_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "Brick.ttl"))


def get_sensors(state: State, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve sensor information for the building structure.

    Args:
        state (State): The current state.
        config (dict): Configuration dictionary containing the language model.
    Returns:
        dict: A dictionary containing sensor UUIDs mapped to their locations.
    """
    custom_logger.eurac("📡 Getting sensors information")

    user_prompt = state["user_prompt"]
    graph = state["graph"]

    g = Graph()
    g.parse(ontology_path, format="turtle")

    if graph is not None:
        for triple in graph:
            g.add(triple)

    # Create a dictionary to store the sensor informations
    sensor_dict = {}

    # Identify the Point entities in the graph
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX brick: <https://brickschema.org/schema/Brick#>

    SELECT ?point ?type
    WHERE {
        ?point rdf:type/rdfs:subClassOf* brick:Point .
        ?point rdf:type ?type .
    }
    """

    res_query = g.query(query)
    point_type_list = []
    for row in res_query:
        point_type_list.append(str(row['type']).split("#")[1])
        sensor_dict[str(row['point']).split("#")[1]] = {
            "name": str(row['point']).split("#")[1],
            "type": str(row['type']).split("#")[1],
            "id": None,
            "unit": None
        }

    point_type_list = list(set(point_type_list))
    uom_dict = get_uom_dict(point_type_list)

    sensor_structure_json = json.dumps(sensor_dict, indent=2)
    uom_dict_json = json.dumps(uom_dict, indent=2)
    # Get the model name from the config
    llm = config.get("configurable", {}).get("llm_model")

    # Enforce structured output
    structured_llm = llm.with_structured_output(SensorSchema)
    # System message
    system_message = get_sensors_instructions.format(
        prompt=user_prompt, sensor_structure=sensor_structure_json, unit_of_measures=uom_dict_json
    )

    # Generate question
    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
    )

    # Encode the sensor information in the graph
    sensors = answer.sensors

    BLDG = Namespace("urn:Building#")
    UNIT = Namespace("http://qudt.org/vocab/unit/")
    BRICK = Namespace("https://brickschema.org/schema/Brick#")
    REF = Namespace("https://brickschema.org/schema/Brick/ref#")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    graph.bind("bldg", BLDG)
    graph.bind("brick", BRICK)
    graph.bind("unit", UNIT)
    graph.bind("ref", REF)
    graph.bind("rdf", RDF)

    for sensor in sensors:
        timeseries_ref = BNode()
        if sensor.unit is not None and sensor.unit != "None":
            try:
                graph.add((BLDG[sensor.name], BRICK.hasUnit, UNIT[sensor.unit]))
            except:
                custom_logger.warning(f"Unit {sensor.unit} not found in QUDT")

        if sensor.id is not None:
            graph.add((BLDG[sensor.name], REF.hasExternalReference, timeseries_ref))
            graph.add((timeseries_ref, RDF.type, REF.TimeseriesReference))
            graph.add((timeseries_ref, REF.hasTimeseriesId, Literal(sensor.id, datatype=XSD.string)))

    return {"graph": graph, "sensor_dict": sensors}
