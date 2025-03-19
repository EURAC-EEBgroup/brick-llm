from typing import Any, Dict, List, Tuple

from typing_extensions import TypedDict

from rdflib import Graph

from .schemas import Sensor


# state for BrickSchemaGraph class
class State(TypedDict):
    user_prompt: str
    elem_list: List[str]
    elem_hierarchy: Dict[str, Any]
    relationships: List[Tuple[str, str]]
    graph :Graph
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
