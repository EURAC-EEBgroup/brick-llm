from typing import Any, Dict

from ..utils import validate_ttl


def validate_schema(state) -> Dict[str, Any]:
    """
    Validate the generated TTL output against the BrickSchema.

    Args:
        state (State): The current state containing the TTL output and validation parameters.

    Returns:
        dict: A dictionary containing the validation status and report.
    """
    print("---Validate Schema Node---")

    ttl_output = state.get("ttl_output", None)
    max_iter = state.get("validation_max_iter", 2)

    max_iter -= 1

    if ttl_output is None:
        return {
            "is_valid": False,
            "validation_report": "Empty TTL output.",
            "validation_max_iter": max_iter,
        }

    is_valid, report = validate_ttl(ttl_output)

    return {
        "is_valid": is_valid,
        "validation_report": report,
        "validation_max_iter": max_iter,
    }
