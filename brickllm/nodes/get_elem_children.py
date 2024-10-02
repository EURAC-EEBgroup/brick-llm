from langchain_core.messages import HumanMessage, SystemMessage

from .. import State, ElemListSchema
from ..helpers import get_elem_children_instructions
from ..utils import get_children_hierarchy, create_hierarchical_dict, filter_elements
from ..helpers import _get_model


def get_elem_children(state: State, config):
    print("---Get Elem Children Node---")

    user_prompt = state["user_prompt"]
    categories = state["elem_list"]

    category_dict = {}
    for category in categories:
        children_list = get_children_hierarchy(category, flatten=True)
        children_string = "\n".join([f"{parent} -> {child}" for parent, child in children_list])
        category_dict[category] = children_string

    # Get the model name from the config
    model_name = config.get('configurable', {}).get("model_name", "fireworks")
    llm = _get_model(model_name)

    # Enforce structured output
    structured_llm = llm.with_structured_output(ElemListSchema)

    identified_children = []
    for category in categories:
        # if the category is not "\n", then add the category to the prompt
        if category_dict[category] != '':
              # System message
            system_message = get_elem_children_instructions.format(prompt=user_prompt, elements_list=category_dict[category])
            # Generate question
            elements = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Find the elements.")])
            identified_children.extend(elements.elem_list)
        else:
            identified_children.append(category)

    # Remove duplicates
    identified_children = list(set(identified_children))
    filtered_children = filter_elements(identified_children)

    # create hierarchical dictionary
    hierarchical_dict = create_hierarchical_dict(filtered_children, properties=True)

    return {"elem_hierarchy": hierarchical_dict}