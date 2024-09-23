from functools import lru_cache
import random, json
from collections import defaultdict

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks

from brickllm.utils.states import State
from brickllm.utils.schemas import ElemListSchema, RelationshipsSchema, TTLSchema
from brickllm.utils.prompts import get_elem_instructions, get_elem_children_instructions, get_relationships_instructions, schema_to_ttl_instructions, ttl_example
from brickllm.helpers.query_brickschema import get_brick_definition
from brickllm.helpers.get_hierarchy_info import get_hierarchy_info, get_children_hierarchy, create_hierarchical_dict, build_hierarchy, find_sensor_paths, filter_elements


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model="gpt-4o")
    elif model_name == "anthropic":
        model =  ChatAnthropic(temperature=0, model="claude-3-sonnet-20240229")
    elif model_name == "fireworks":
        model = ChatFireworks(temperature=0, model="accounts/fireworks/models/llama-v3p1-70b-instruct")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    return model

def get_elements(state: State, config):
    print("---Get Elements Node---")

    user_prompt = state["user_prompt"]

    categories = ['Point', 'Equipment', 'Location', 'Collection']

    category_dict = {}
    # Get hierarchy info for each category
    for category in categories:
        parents, children = get_hierarchy_info(category)
        # category_dict[category] = children

        # get definition for each child
        children_dict = {}
        for child in children:
            children_dict[child] = get_brick_definition(child)

        category_dict[category] = children_dict

    # Get the model name from the config
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(ElemListSchema)

    # System message
    system_message = get_elem_instructions.format(prompt=user_prompt, elements_dict=category_dict)

    # Generate question
    answer = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Find the elements.")])

    return {"elem_list": answer.elem_list}

def get_elem_children(state: State, config):
    print("---Get Elem Children Node---")

    user_prompt = state["user_prompt"]
    categories = state["elem_list"]

    category_dict = {}
    for category in categories:
        children_list = get_children_hierarchy(category, flatten=True)
        children_string = "\n".join([f"{parent} -> {child}" for parent, child in children_list])
        category_dict[category] = children_string

    # Get the model name from the config
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(ElemListSchema)

    identified_children = []
    for category in categories:
        # if the category is not "\n", then add the category to the prompt
        if category_dict[category] != '':
              # System message
            system_message = get_elem_children_instructions.format(prompt=user_prompt, elements_list=category_dict[category])
            # Generate question
            elements = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Find the elements.")])
            identified_children.extend(elements.elem_list)
        else:
            identified_children.append(category)

    # Remove duplicates
    identified_children = list(set(identified_children))
    filtered_children = filter_elements(identified_children)

    # create hierarchical dictionary
    hierarchical_dict = create_hierarchical_dict(filtered_children, properties=True)

    return {"elem_hierarchy": hierarchical_dict}

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

def schema_to_ttl(state: State, config):
    print("---Schema To TTL Node---")

    user_prompt = state["user_prompt"]
    sensors_dict = state["sensors_dict"]
    elem_hierarchy = state["elem_hierarchy"]

    sensors_dict_json = json.dumps(sensors_dict, indent=2)
    elem_hierarchy_json = json.dumps(elem_hierarchy, indent=2)

    # Get the model name from the config
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(TTLSchema)

    # System message
    system_message = schema_to_ttl_instructions.format(
        prompt=user_prompt,
        sensors_dict=sensors_dict_json,
        elem_hierarchy=elem_hierarchy_json,
        ttl_example=ttl_example
    )

    # Generate question
    answer = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Generate the TTL.")])
    # print(answer.ttl_output)
    # strip the answer from the backticks
    # ttl_output = extract_ttl_content(answer.ttl_output)

    return {"ttl_output": answer.ttl_output}

def validate_schema(state: State):
    print("---Validate Schema Node---")

    ttl_output = state["ttl_output"]

    # Validate the schema
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return {"is_valid": True}

    return {"is_valid": False}

def get_sensors(state: State):
    print("---Get Sensor Node---")

    uuid_dict = {
        "Building#1>Floor#1>Office#1>Room#1": [
            {
                "name":"Temperature_Sensor#1",
                "uuid":"aaaa-bbbb-cccc-dddd",
            },
            {
                "name":"Humidity_Sensor#1",
                "uuid":"aaaa-bbbb-cccc-dddd",
            }
        ],
        "Building#1>Floor#1>Office#1>Room#2": [
            {
                "name":"Temperature_Sensor#2",
                "uuid":"aaaa-bbbb-cccc-dddd",
            },
            {
                "name":"Humidity_Sensor#2",
                "uuid":"aaaa-bbbb-cccc-dddd",
            }
        ],
    }
    return {"uuid_dict": uuid_dict}
