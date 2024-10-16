from typing import Any, Dict, List, Union

from langchain.chat_models.base import BaseChatModel
from langgraph.graph import START, StateGraph

from .. import GraphConfig, StateLocal
from ..edges import validate_condition_local
from ..nodes import generation_local, validate_schema
from .abstract_graph import AbstractBrickSchemaGraph


class BrickSchemaGraphLocal(AbstractBrickSchemaGraph):
    def __init__(self, model: Union[str, BaseChatModel]):
        super().__init__(model)
        self.build_graph()
        self.compile_graph()

    def build_graph(self):
        self.workflow = StateGraph(StateLocal, config_schema=GraphConfig)

        # Build graph by adding nodes
        self.workflow.add_node("generation_local", generation_local)
        self.workflow.add_node("validate_schema", validate_schema)

        # Add edges to define the flow logic
        self.workflow.add_edge(START, "generation_local")
        self.workflow.add_edge("generation_local", "validate_schema")
        self.workflow.add_conditional_edges("validate_schema", validate_condition_local)

    def run(
        self, input_data: Dict[str, Any], stream: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if "user_prompt" not in input_data or "instructions" not in input_data:
            raise ValueError(
                "Input data must contain both 'user_prompt' and 'instructions' keys."
            )

        if stream:
            events = []
            for event in self.graph.stream(
                input_data, self.config, stream_mode="values"
            ):
                events.append(event)
            self.result = events[-1]
            return events
        else:
            self.result = self.graph.invoke(input_data, self.config)
            return self.result
