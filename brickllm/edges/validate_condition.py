from typing import Any, Dict, Literal


def validate_condition(state: Dict[str, Any]) -> Literal["schema_to_ttl", "__end__"]:
    """
    Validate the condition for the next node to visit.

    Args:
        state (Dict[str, Any]): The current state containing the validation result.

    Returns:
        Literal["schema_to_ttl", "__end__"]: The next node to visit.
    """

    is_valid = state.get("is_valid", False)
    max_iter = state.get("validation_max_iter", 0)

    if max_iter > 0 and not is_valid:
        return "schema_to_ttl"

    return "__end__"
