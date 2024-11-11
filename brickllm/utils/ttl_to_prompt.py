from typing import List, Tuple, Union

from langchain.chat_models.base import BaseChatModel
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage

from ..helpers import ttl_to_user_prompt
from ..schemas import TTLToBuildingPromptSchema


def ttl_to_building_prompt(
    ttl_file: str, llm: Union[Ollama, BaseChatModel]
) -> Tuple[str, List[str]]:

    # Enforce structured output
    structured_llm = llm.with_structured_output(TTLToBuildingPromptSchema)

    # System message
    system_message = ttl_to_user_prompt.format(ttl_script=ttl_file)

    # Generate question
    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
        + [HumanMessage(content="Generate the TTL.")]
    )

    return answer.building_description, answer.key_elements
