
import json
from collections import defaultdict

from langchain_core.messages import HumanMessage, SystemMessage

from .. import State, RelationshipsSchema
from ..helpers import get_relationships_instructions, _get_model
from ..utils import build_hierarchy, find_sensor_paths


def get_relationships(state: State, config):
    print("---Get Relationships Node---")

    user_prompt = state["user_prompt"]
    building_structure = state["elem_hierarchy"]

    # Convert building structure to a JSON string for better readability
    building_structure_json = json.dumps(building_structure, indent=2)

    # Get the model name from the config
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(RelationshipsSchema)
    # System message
    system_message = get_relationships_instructions.format(prompt=user_prompt, building_structure=building_structure_json)

    # Generate question
    answer = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Find the relationships.")])

    try:
        tree_dict = build_hierarchy(answer.relationships)
    except Exception as e:
        print(f"Error building the hierarchy: {e}")

    # Group sensors by their paths
    sensor_paths = find_sensor_paths(tree_dict)
    grouped_sensors = defaultdict(list)
    for sensor in sensor_paths:
        grouped_sensors[sensor['path']].append(sensor['name'])
    grouped_sensor_dict = dict(grouped_sensors)

    return {"sensors_dict": grouped_sensor_dict}