import json
import pkg_resources
import os
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from rdflib import Graph, Namespace
from .. import RelationshipsSchema, State, EntityType, Relationship
from ..helpers import get_relationships_instructions, find_entities_type, find_relationship
from ..logger import custom_logger
from ..utils import find_rel_constraint, get_rel_definition, find_parents

brick_hierarchy_path = pkg_resources.resource_filename(
    __name__, os.path.join("..", "ontologies", "brick_hierarchy.json")
)

# Load the JSON file
with open(brick_hierarchy_path) as f:
    brick_hierarchy = json.load(f)

MAX_RETRIES = 3


def get_relationships(state: State, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determine relationships between building components using a language model.

    Args:
        state (State): The current state containing the user prompt and element hierarchy.
        config (dict): Configuration dictionary containing the language model.

    Returns:
        dict: A dictionary containing the grouped sensor paths.
    """

    custom_logger.eurac("🔗 Identifying related entities from the user prompt")

    user_prompt = state["user_prompt"]
    hierarchical_structure = state["elem_hierarchy"]

    # Convert building structure to a JSON string for better readability
    hierarchical_structure_json = json.dumps(hierarchical_structure, indent=2)

    # Get the model name from the config
    llm = config.get("configurable", {}).get("llm_model")

    # Enforce structured output
    structured_llm = llm.with_structured_output(RelationshipsSchema)
    # System message
    system_message = get_relationships_instructions.format(
        prompt=user_prompt
    )

    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
    )

    # Check the format of the entities in order to not break the graph.
    relationships = []
    for relationship in answer.relationships:
        relationships.append((relationship[0].replace(" ", "_"), (relationship[1].replace(" ", "_"))))

    # Build the skeleton of the entities as a dict
    entities_dict = {}
    for relationship in relationships:
        if relationship[0] not in entities_dict and relationship[0] != "":
            entities_dict[relationship[0]] = {
                "name": relationship[0],
                "type": None
            }

        if relationship[1] not in entities_dict and relationship[1] != "":
            entities_dict[relationship[1]] = {
                "name": relationship[1],
                "type": None
            }

    # Obtain all Brick entities to check if the entity type that will be identified is true
    def extract_keys(data, keys=None):
        if keys is None:
            keys = []

        for key, value in data.items():
            keys.append(key)
            if isinstance(value, dict):  # If the value is a nested dictionary, recurse
                extract_keys(value, keys)

        return keys

    all_brick_entities = extract_keys(brick_hierarchy)

    custom_logger.eurac("🔗 Identifying entity types")

    for entity in entities_dict:
        system_message = find_entities_type.format(
            user_prompt=user_prompt,
            hierarchical_structure=hierarchical_structure_json,
            entity=entity,
            relationships=relationships
        )

        structured_llm = llm.with_structured_output(EntityType)

        for attempt in range(MAX_RETRIES):
            answer = structured_llm.invoke([SystemMessage(content=system_message)])
            concept = answer.ontology_concept

            if concept == entity:
                entity_type = concept.split(".")[0]
            elif "." in concept:
                entity_type = concept.split(".")[-1]
            elif concept not in all_brick_entities:
                custom_logger.warning(f"Entity not recognized (attempt {attempt + 1}). Retrying...")
                continue
            else:
                entity_type = concept
            break
        else:
            # Fallback if all retries failed
            custom_logger.warning(f"Max retries reached for entity: {entity}. Using fallback type.")
            entity_type = entity.split(".")[0]

        entities_dict[entity]["type"] = entity_type

    # Adding the possible relationships for each entity extracted by the Brick ontology
    for entity in entities_dict:
        try:
            entities_dict[entity]["relationships"] = find_rel_constraint(entities_dict[entity]["type"])
        except Exception:
            # Drop the entity if it does not have a type
            print("Type not recognized for entity: ", entity)

    # Extract the super classes for each entity from the Brick ontology
    for entity in entities_dict:
        super_classes = find_parents(brick_hierarchy, entities_dict[entity]["type"])[1]
        entities_dict[entity]["super_classes"] = super_classes

    custom_logger.eurac("🔗 Getting relationships between building components")

    triples = []
    for relationship in relationships:

        subject = relationship[0]
        object = relationship[1]

        all_relationships = entities_dict[subject]["relationships"]
        object_type = entities_dict[object]["type"]
        object_superclasses = entities_dict[object]["super_classes"]
        object_constraint = [object_type] + object_superclasses

        # Extract the relationships that are valid for the entity type and its super classes
        valid_relationships = {}
        for rel_type in all_relationships:
            if any([constraint in all_relationships[rel_type]["constraints"] for constraint in object_constraint]):
                valid_relationships[rel_type] = all_relationships[rel_type]["definition"]

        if len(valid_relationships.keys()) == 0:
            valid_relationships = get_rel_definition()

        system_message = find_relationship.format(
            user_prompt=user_prompt,
            tuple=(subject, object),
            relationships=valid_relationships
        )

        structured_llm = llm.with_structured_output(Relationship)

        answer = structured_llm.invoke(
            [SystemMessage(content=system_message)]
            + [HumanMessage(content="Find the most appropriate relationships based on the user prompt provided.")]
        )

        valid = False
        for attempt in range(MAX_RETRIES):
            if answer.relationship in valid_relationships:
                valid = True
                break
            else:
                custom_logger.warning(f"The relationship is not valid. Trying again (attempt {attempt + 1}).")
                answer = structured_llm.invoke([SystemMessage(content=system_message)])

        if not valid:
            custom_logger.error("Failed to get a valid relationship after maximum retries.")

        if answer.relationship not in list(valid_relationships.keys()):
            answer.relationship = None

        triples.append((f"{subject}", f"{answer.relationship}", f"{object}"))

    # Append the triples identified to the graph
    graph = Graph()
    BLDG = Namespace("urn:Building#")
    BRICK = Namespace("https://brickschema.org/schema/Brick#")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    graph.bind("bldg", BLDG)
    graph.bind("brick", BRICK)
    graph.bind("rdf", RDF)

    for triple in triples:
        if triple[1] is not None:
            graph.add((BLDG[triple[0]], BRICK[triple[1]], BLDG[triple[2]]))

    for entity in entities_dict:
        if not entities_dict[entity]["type"] is None:
            graph.add((BLDG[entity], RDF.type, BRICK[entities_dict[entity]["type"]]))

    return {"relationships": triples, "graph": graph}
