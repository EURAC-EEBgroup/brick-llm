from typing import TypedDict, Literal

# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai", "fireworks"]