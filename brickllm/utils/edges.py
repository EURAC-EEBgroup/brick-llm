import random
from typing import Literal
from langgraph.graph import END

def validate_condition(state) -> Literal["schema_to_ttl", "__end__"]:

    # Often, we will use state to decide on the next node to visit
    is_valid = state.get("is_valid", False)
    max_iter = state.get("validation_max_iter", 1)

    if max_iter > 0 and not is_valid:
        state["validation_max_iter"] = max_iter - 1
        return "schema_to_ttl"

    return END