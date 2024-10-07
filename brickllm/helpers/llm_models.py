from typing import Union
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from langchain.chat_models.base import BaseChatModel


def _get_model(model: Union[str, BaseChatModel]):
    """
    Get the LLM model based on the provided model type.

    Args:
        model (Union[str, BaseChatModel]): The model type as a string or an instance of BaseChatModel.

    Returns:
        BaseChatModel: The LLM model instance.
    """
    
    if isinstance(model, BaseChatModel):
        return model
    
    # Load environment variables
    load_dotenv()

    if model == "openai":
        return ChatOpenAI(temperature=0, model="gpt-4o")
    elif model == "anthropic":
        return ChatAnthropic(temperature=0, model="claude-3-sonnet-20240229")
    elif model == "fireworks":
        return ChatFireworks(temperature=0, model="accounts/fireworks/models/llama-v3p1-70b-instruct")
    else:
        raise ValueError(f"Unsupported model type: {model}")