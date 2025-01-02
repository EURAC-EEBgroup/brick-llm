import json
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage

from .. import SensorSchema, State
from ..helpers import get_sensors_instructions
from ..logger import custom_logger


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
    sensor_structure = state["sensors_dict"]
    sensor_structure_json = json.dumps(sensor_structure, indent=2)

    # Get the model name from the config
    llm = config.get("configurable", {}).get("llm_model")

    # Enforce structured output
    structured_llm = llm.with_structured_output(SensorSchema)
    # System message
    system_message = get_sensors_instructions.format(
        prompt=user_prompt, sensor_structure=sensor_structure_json
    )

    # Generate question
    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
        + [HumanMessage(content="Complete the sensor structure.")]
    )

    return {"uuid_list": answer.sensors}
