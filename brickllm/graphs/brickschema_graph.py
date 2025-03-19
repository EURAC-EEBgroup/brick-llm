from typing import Any, Dict, List, Union

import rdflib
from langchain.chat_models.base import BaseChatModel
from langgraph.graph import END, START, StateGraph

from .. import GraphConfig, State
from ..edges import check_sensor_presence, validate_condition
from ..nodes import (
    get_elem_children,
    get_elements,
    get_relationships,
    get_sensors,
    schema_to_ttl,
    validate_schema,
    model_refactoring
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
        self.workflow.add_node("validate_schema", validate_schema)
        self.workflow.add_node("get_sensors", get_sensors)
        self.workflow.add_node("model_refactoring", model_refactoring)

        # Add edges to define the flow logic
        self.workflow.add_edge(START, "get_elements")
        self.workflow.add_edge("get_elements", "get_elem_children")
        self.workflow.add_edge("get_elem_children", "get_relationships")
        self.workflow.add_conditional_edges(
            "get_relationships",
            check_sensor_presence,
            {"get_sensors": "get_sensors", "validate_schema": "validate_schema"},
        )
        self.workflow.add_edge("get_sensors", "validate_schema")
        self.workflow.add_conditional_edges(
            "validate_schema",
            validate_condition,
            {"model_refactoring": "model_refactoring", "__end__": END})
        self.workflow.add_edge("model_refactoring", "validate_schema")

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
            ttl_output = self.result.get("graph", rdflib.Graph()).serialize(format="ttl")
            self.ttl_output = ttl_output
            return events
        else:
            self.result = self.graph.invoke(input_data, self.config)
            ttl_output = self.result.get("graph", rdflib.Graph()).serialize(format="ttl")
            self.ttl_output = ttl_output
            return self.result
