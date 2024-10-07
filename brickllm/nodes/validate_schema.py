from .. import State
from ..utils import validate_ttl


def validate_schema(state: State):
    print("---Validate Schema Node---")

    ttl_output = state.get("ttl_output", None)

    if ttl_output is None:
        return {"is_valid": False, "validation_report": "Empty TTL output."}
    
    is_valid, report = validate_ttl(ttl_output)

    return {"is_valid": is_valid, "validation_report": report}