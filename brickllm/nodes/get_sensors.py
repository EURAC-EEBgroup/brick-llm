from typing import Any, Dict

from .. import State


def get_sensors(state: State) -> Dict[str, Any]:
    """
    Retrieve sensor information for the building structure.

    Args:
        state (State): The current state.

    Returns:
        dict: A dictionary containing sensor UUIDs mapped to their locations.
    """
    print("---Get Sensor Node---")

    uuid_dict = {
        "Building#1>Floor#1>Office#1>Room#1": [
            {
                "name": "Temperature_Sensor#1",
                "uuid": "aaaa-bbbb-cccc-dddd",
            },
            {
                "name": "Humidity_Sensor#1",
                "uuid": "aaaa-bbbb-cccc-dddd",
            },
        ],
        "Building#1>Floor#1>Office#1>Room#2": [
            {
                "name": "Temperature_Sensor#2",
                "uuid": "aaaa-bbbb-cccc-dddd",
            },
            {
                "name": "Humidity_Sensor#2",
                "uuid": "aaaa-bbbb-cccc-dddd",
            },
        ],
    }
    return {"uuid_dict": uuid_dict}
