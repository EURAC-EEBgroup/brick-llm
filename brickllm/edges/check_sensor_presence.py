from typing import Any, Dict, Literal

from ..utils import get_hierarchical_info
from ..logger import custom_logger


def check_sensor_presence(state: Dict[str, Any]) -> Literal["get_sensors", "schema_to_ttl"]:
    """
    Check if the sensors are present in the building structure.

    Args:
        state (Dict[str, Any]): The current state containing the sensor structure.

    Returns:
        Literal["get_sensors", "schema_to_ttl"]: The next node to visit.
    """

    custom_logger.eurac("📡 Checking for sensor presence")

    elem_list = state.get("elem_list", [])

    parents, children = get_hierarchical_info("Point")

    children_dict = {}
    for child in children:
        children_dict[child] = get_hierarchical_info(child)[1]

    # Flatten the dictionary in a list
    children_list = [elem for sublist in children_dict.values() for elem in sublist]

    is_sensor = False

    for elem in elem_list:
        if elem in children_list:
            is_sensor = True

    if is_sensor:
        return "get_sensors"
    else:
        return "schema_to_ttl"
