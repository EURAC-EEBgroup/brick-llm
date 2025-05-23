from typing import Any, Dict

from ..logger import custom_logger
from ..utils import validate_ttl


def validate_schema(state) -> Dict[str, Any]:
    """
    Validate the generated TTL output against the BrickSchema.

    Args:
        state (State): The current state containing the TTL output and validation parameters.

    Returns:
        dict: A dictionary containing the validation status and report.
    """
    custom_logger.eurac("✅ Validating TTL schema")

    graph = state.get("graph", None)
    max_iter = state.get("validation_max_iter", 3)

    max_iter -= 1

    if graph is None:
        return {
            "is_valid": False,
            "validation_report": "Empty TTL output.",
            "validation_max_iter": max_iter,
        }

    is_valid, report = validate_ttl(graph)

    return {
        "is_valid": is_valid,
        "validation_report": report,
        "validation_max_iter": max_iter,
    }
