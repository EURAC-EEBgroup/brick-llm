import logging
from typing import List, Optional, Tuple, Union

from langchain.chat_models.base import BaseChatModel
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage

from ..helpers import ttl_to_user_prompt
from ..schemas import TTLToBuildingPromptSchema

logger = logging.getLogger(__name__)


def ttl_to_building_prompt(
    ttl_file: str,
    llm: Union[Ollama, BaseChatModel],
    additional_instructions: Optional[str] = None,
) -> Tuple[str, List[str]]:

    # Enforce structured output
    structured_llm = llm.with_structured_output(TTLToBuildingPromptSchema)

    # System message
    system_message = ttl_to_user_prompt.format(
        ttl_script=ttl_file, additional_instructions=additional_instructions
    )

    logger.info("Generating building description and key elements from the TTL file.")
    # Generate question
    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
        + [HumanMessage(content="Generate the TTL.")]
    )

    return answer.building_description, answer.key_elements
