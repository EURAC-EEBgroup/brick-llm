from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from rdflib import Graph
from io import StringIO

from .. import State, TTLSchema
from ..helpers import model_refactor_instructions
from ..logger import custom_logger


def model_refactoring(state: State, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refactor the model based on the validation report.

    Args:
        state (State): The current state containing the validation report.
        config (dict): Configuration dictionary containing the language model.

    Returns:
        dict: A dictionary containing the refactored model.
    """
    custom_logger.eurac("🔧 Refactoring the model")

    validation_report = state["validation_report"]
    graph = state["graph"]
    user_prompt = state["user_prompt"]

    # Get the model name from the config
    llm = config.get("configurable", {}).get("llm_model")

    # Enforce structured output
    structured_llm = llm.with_structured_output(TTLSchema)

    system_message = model_refactor_instructions.format(
        validation_report=validation_report,
        rdf_graph=graph.serialize(format="ttl"),
        user_prompt=user_prompt
    )

    # Generate question
    answer = structured_llm.invoke(
        [SystemMessage(content=system_message)]
    )

    try:
        graph = Graph().parse(StringIO(answer.ttl_output), format="ttl")
    except Exception:
        custom_logger.eurac("Refactoring failed.")

    return {"graph": graph}
