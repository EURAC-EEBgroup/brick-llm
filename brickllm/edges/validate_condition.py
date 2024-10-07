from typing import Literal

# from langgraph.graph import END


def validate_condition(state) -> Literal["schema_to_ttl", "__end__"]:
    """
    Validate the condition for the next node to visit.

    Args:
        state (State): The current state containing the validation result.

    Returns:
        Literal["schema_to_ttl", "__end__"]: The next node to visit.
    """

    is_valid = state.get("is_valid")
    max_iter = state.get("validation_max_iter")

    if max_iter > 0 and not is_valid:
        return "schema_to_ttl"

    return "__end__"
