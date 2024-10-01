
from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model="gpt-4o")
    elif model_name == "anthropic":
        model =  ChatAnthropic(temperature=0, model="claude-3-sonnet-20240229")
    elif model_name == "fireworks":
        model = ChatFireworks(temperature=0, model="accounts/fireworks/models/llama-v3p1-70b-instruct")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    return model