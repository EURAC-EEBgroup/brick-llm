from typing import Any, Dict, List, Union

from langchain.chat_models.base import BaseChatModel
from langgraph.graph import END, START, StateGraph

from .. import GraphConfig, State
from ..edges import validate_condition
from ..nodes import (
    get_elem_children,
    get_elements,
    get_relationships,
    get_sensors,
    schema_to_ttl,
    validate_schema,
)
from .abstract_graph import AbstractBrickSchemaGraph


class BrickSchemaGraph(AbstractBrickSchemaGraph):
    def __init__(self, model: Union[str, BaseChatModel] = "openai"):
        super().__init__(model)
        self.build_graph()
        self.compile_graph()

    def build_graph(self):
        self.workflow = StateGraph(State, config_schema=GraphConfig)

        # Build graph by adding nodes
        self.workflow.add_node("get_elements", get_elements)
        self.workflow.add_node("get_elem_children", get_elem_children)
        self.workflow.add_node("get_relationships", get_relationships)
        self.workflow.add_node("schema_to_ttl", schema_to_ttl)
        self.workflow.add_node("validate_schema", validate_schema)
        self.workflow.add_node("get_sensors", get_sensors)

        # Add edges to define the flow logic
        self.workflow.add_edge(START, "get_elements")
        self.workflow.add_edge("get_elements", "get_elem_children")
        self.workflow.add_edge("get_elem_children", "get_relationships")
        self.workflow.add_edge("get_relationships", "schema_to_ttl")
        self.workflow.add_edge("schema_to_ttl", "validate_schema")
        self.workflow.add_conditional_edges("validate_schema", validate_condition)
        self.workflow.add_edge("get_relationships", "get_sensors")
        self.workflow.add_edge("get_sensors", END)

    def run(
        self, input_data: Dict[str, Any], stream: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if "user_prompt" not in input_data:
            raise ValueError("Input data must contain a 'user_prompt' key.")

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
