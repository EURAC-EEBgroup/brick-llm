from typing import Any, Dict, List, Union
from langgraph.graph import END, START, StateGraph

from .brickschema_graph import BrickSchemaGraph
from .. import GraphConfig, State
from ..helpers.llm_models import _get_model
from ..nodes import generation_local, validate_schema
from ..edges import validate_condition_local


class BrickSchemaGraphLocal(BrickSchemaGraph):
    def __init__(self, model):
        super().__init__(model)

        # Define a new graph
        self.workflow = StateGraph(state_schema=State,
                                   config_schema=GraphConfig)

        # Store the model
        self.model = _get_model(model)

        # Build graph by adding nodes
        self.workflow.add_node("generation_local", generation_local)
        self.workflow.add_node("validate_schema", validate_schema)

        # Add edges to define the flow logic
        self.workflow.add_edge(START, "generation_local")
        self.workflow.add_edge("generation_local", "validate_schema")
        self.workflow.add_conditional_edges("validate_schema", validate_condition_local)
        self.workflow.add_edge("validate_schema", END)

        try:
            self.graph = self.workflow.compile()
        except Exception as e:
            raise ValueError(f"Failed to compile the graph: {e}")

        # Update the config with the model
        self.config = {"configurable": {"thread_id": "1", "llm_model": self.model}}

        # Initialize the result
        self.result = None

    def run(self, instructions: str, prompt: str, stream: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Run the graph with the given user prompt and instructions.

        Args:
            instructions (str): the instructions for generating the model.
            prompt (str): The user prompt to run the graph.
            stream (bool): Stream the graph execution.

        Returns:
            result (dict): The result of the graph execution.
        """

        input_data = {"user_prompt": prompt, "instructions": instructions}

        if stream:
            events = []
            # Stream the content of the graph state at each node
            for event in self.graph.stream(
                    input_data, self.config, stream_mode="values"
            ):
                events.append(event)

            # Store the last event as the result
            self.result = events[-1]
            return events
        else:
            # Invoke the graph without streaming
            self.result = self.graph.invoke(input_data, self.config)
            return self.result
