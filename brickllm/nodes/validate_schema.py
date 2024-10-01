import random

from .. import State


def validate_schema(state: State):
    print("---Validate Schema Node---")

    # ttl_output = state["ttl_output"]

    # Validate the schema
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return {"is_valid": True}

    return {"is_valid": False}