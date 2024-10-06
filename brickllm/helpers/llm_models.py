from functools import lru_cache
from typing import Union

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from langchain.chat_models.base import BaseChatModel

def _get_model(model: Union[str, BaseChatModel]):
    if isinstance(model, BaseChatModel):
        return model
    
    if model == "openai":
        return ChatOpenAI(temperature=0, model="gpt-4o")
    elif model == "anthropic":
        return ChatAnthropic(temperature=0, model="claude-3-sonnet-20240229")
    elif model == "fireworks":
        return ChatFireworks(temperature=0, model="accounts/fireworks/models/llama-v3p1-70b-instruct")
    else:
        raise ValueError(f"Unsupported model type: {model}")