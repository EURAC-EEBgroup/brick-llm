import json

from langchain_core.messages import HumanMessage, SystemMessage

from .. import State, TTLSchema
from ..helpers import schema_to_ttl_instructions, ttl_example, _get_model


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
    print(answer.ttl_output)

    return {"ttl_output": answer.ttl_output}