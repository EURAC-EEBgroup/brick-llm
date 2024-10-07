from typing import Any, List, Dict
from typing_extensions import TypedDict

# graph state
class State(TypedDict):
    user_prompt: str
    elem_list: List[str]
    # elem_children_list: List[str]
    elem_hierarchy: Dict[str, Any]
    # relationships: List[Tuple[str, str]]
    # rel_tree: Dict[str, Any]
    sensors_dict: Dict[str, List[str]]
    is_valid: bool
    validation_report: str
    validation_max_iter: int
    uuid_dict: Dict[str, Any]
    ttl_output: str
