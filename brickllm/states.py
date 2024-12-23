from typing import Any, Dict, List
from .schemas import Sensor

from typing_extensions import TypedDict


# state for BrickSchemaGraph class
class State(TypedDict):
    user_prompt: str
    elem_list: List[str]
    # elem_children_list: List[str]
    elem_hierarchy: Dict[str, Any]
    # relationships: List[Tuple[str, str]]
    rel_tree: Dict[str, Any]
    sensors_dict: Dict[str, List[str]]
    is_sensor: bool
    is_valid: bool
    validation_report: str
    validation_max_iter: int
    uuid_list: List[Sensor]
    ttl_output: str


# state for BrickSchemaGraphLocal class
class StateLocal(TypedDict):
    instructions: str
    user_prompt: str
    is_valid: bool
    validation_report: str
    validation_max_iter: int
    ttl_output: str
