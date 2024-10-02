import json
from langgraph.graph import START, END, StateGraph
from .. import State, GraphConfig
from ..nodes import (
    get_elements, get_elem_children, get_relationships,
    schema_to_ttl, validate_schema, get_sensors
)
from ..edges import validate_condition
from PIL import Image
import os

from dotenv import load_dotenv
load_dotenv()

class BrickSchemaGraph:
    def __init__(self):
        """Initialize the StateGraph object and build the graph."""
        # Define a new graph
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
        
        # Compile graph
        try:
            self.graph = self.workflow.compile()
        except Exception as e:
            raise ValueError(f"Failed to compile the graph: {e}")
        
        # Hardcoding the thread_id for now
        self.config = {"configurable": {"thread_id": "1"}}

    def _compiled_graph(self):
        """Check if the graph is compiled and return the compiled graph."""
        if self.graph is None:
            raise ValueError("Graph is not compiled yet. Please compile the graph first.")
        return self.graph

    def display(self, filename="graph.png"):
        """Display the compiled graph as an image.
        
        Args:
            filename (str): The filename to save the graph image.
        """
        if self.graph is None:
            raise ValueError("Graph is not compiled yet. Please compile the graph first.")
        
        # Save the image to the specified file
        self.graph.get_graph().draw_mermaid_png(output_file_path=filename)

        # Open the image using PIL (Pillow)
        if os.path.exists(filename):
            with Image.open(filename) as img:
                img.show()
        else:
            raise FileNotFoundError(f"Failed to generate the graph image file: {filename}")

    def run(self, prompt, stream=False):
        """Run the graph with the given user prompt.

        Args:
            user_prompt (str): The user-provided natural language prompt.
            stream (bool): Whether to stream the execution (True) or run without streaming (False).
        """
        input_data = {"user_prompt": prompt}

        if stream:
            # Stream the content of the graph state at each node
            for event in self.graph.stream(input_data, self.config, stream_mode="values"):
                print(json.dumps(event, indent=2))
        else:
            # Invoke the graph without streaming
            result = self.graph.invoke(input_data, self.config)
            print(json.dumps(result, indent=2))
