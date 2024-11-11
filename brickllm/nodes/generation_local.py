from typing import Any, Dict

from .. import StateLocal
from ..helpers import prompt_template_local
from ..utils import extract_rdf_graph


def generation_local(state: StateLocal, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate the RDF graph using the local LLM from a prompt containing the building description and the instruction

    Args:
        state (StateLocal): The current state containing the user prompt and the instructions.
        config (dict): Configuration dictionary containing the language model.

    Returns:
        dict: A dictionary containing the output generated.
    """

    print("---One shot generation with local LLM Node---")

    instructions = state["instructions"]
    user_prompt = state["user_prompt"]

    llm = config.get("configurable", {}.get("llm_model"))["llm_model"]

    message = prompt_template_local.format(
        instructions=instructions, user_prompt=user_prompt
    )

    answer = llm.invoke(message)
    ttl_output = extract_rdf_graph(answer)

    return {"ttl_output": ttl_output}
