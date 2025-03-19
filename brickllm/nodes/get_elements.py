from typing import Any, Dict
import json

from langchain_core.messages import HumanMessage, SystemMessage

from .. import ElemListSchema, State
from ..helpers import get_elem_instructions
from ..logger import custom_logger
from ..utils import get_brick_definition, get_hierarchical_info


def get_elements(state: State, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process the user prompt to identify elements within specified categories
    using a language model.

    Args:
        state (State): The current state containing the user prompt.
        config (dict): Configuration dictionary containing the language model.

    Returns:
        dict: A dictionary containing the list of identified elements.
    """
    custom_logger.eurac("🔍 Getting Brick entities from user prompt")

    user_prompt = state["user_prompt"]

    categories = ["Point", "Equipment", "Location", "Collection"]

    category_dict = {}
    # Get hierarchy info for each category
    for category in categories:
        parents, children = get_hierarchical_info(category)
        # category_dict[category] = children

        # get definition for each child
        children_dict = {}
        for child in children:
            children_dict[child] = get_brick_definition(child)

        category_dict[category] = children_dict

    # Get the model name from the config
    llm = config.get("configurable", {}).get("llm_model")

    # Enforce structured output
    structured_llm = llm.with_structured_output(ElemListSchema)
    entities_list = []

    for category in category_dict:
        category_dict_json = json.dumps(category_dict[category], indent=2)

        # System message
        system_message = get_elem_instructions.format(
            user_prompt=user_prompt, elements_dict=category_dict_json
        )

        # Generate question
        answer = structured_llm.invoke(
            [SystemMessage(content=system_message)]
        )

        entities_list.extend(answer.elem_list)

    entities_list = list(set(entities_list))

    # Subset the answer.elem_list to only include the ones that are in category_dict
    admitted_elements = []
    for category in category_dict:
        for child in category_dict[category]:
            admitted_elements.append(child)

    elem_list = [elem for elem in entities_list if elem in admitted_elements]

    return {"elem_list": elem_list}
