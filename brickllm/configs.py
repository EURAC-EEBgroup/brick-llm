from typing import Literal, TypedDict, Union

from langchain.chat_models.base import BaseChatModel


# Define the config
class GraphConfig(TypedDict):
    model: Union[Literal["anthropic", "openai", "fireworks"], BaseChatModel]