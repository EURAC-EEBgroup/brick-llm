from langchain_core.messages import HumanMessage, SystemMessage

from .. import State, ElemListSchema
from ..helpers import get_elem_instructions, _get_model
from ..utils import get_hierarchical_info, get_brick_definition


def get_elements(state: State, config):
    print("---Get Elements Node---")

    user_prompt = state["user_prompt"]

    categories = ['Point', 'Equipment', 'Location', 'Collection']

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
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(ElemListSchema)

    # System message
    system_message = get_elem_instructions.format(prompt=user_prompt, elements_dict=category_dict)

    # Generate question
    answer = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Find the elements.")])

    return {"elem_list": answer.elem_list}