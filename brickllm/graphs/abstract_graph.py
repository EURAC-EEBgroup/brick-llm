import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from langchain.chat_models.base import BaseChatModel
from langgraph.graph import StateGraph
from PIL import Image

from ..helpers.llm_models import _get_model


class AbstractBrickSchemaGraph(ABC):
    def __init__(self, model: Union[str, BaseChatModel] = "openai"):
        self.model = _get_model(model)
        self.workflow = None
        self.graph = None
        self.config = {"configurable": {"thread_id": "1", "llm_model": self.model}}
        self.result = None

    @abstractmethod
    def build_graph(self):
        """Build the graph by adding nodes and edges."""
        pass

    def compile_graph(self):
        """Compile the graph."""
        try:
            self.graph = self.workflow.compile()
        except Exception as e:
            raise ValueError(f"Failed to compile the graph: {e}")

    def _compiled_graph(self) -> StateGraph:
        """Check if the graph is compiled and return the compiled graph."""
        if self.graph is None:
            raise ValueError(
                "Graph is not compiled yet. Please compile the graph first."
            )
        return self.graph

    @abstractmethod
    def run(
        self, input_data: Dict[str, Any], stream: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Run the graph with the given input data."""
        pass

    def display(self, filename: str = "graph.png") -> None:
        """Display the compiled graph as an image."""
        if self.graph is None:
            raise ValueError(
                "Graph is not compiled yet. Please compile the graph first."
            )

        # Save the image to the specified file
        self.graph.get_graph().draw_mermaid_png(output_file_path=filename)

        # Open the image using PIL (Pillow)
        if os.path.exists(filename):
            with Image.open(filename) as img:
                img.show()
        else:
            raise FileNotFoundError(
                f"Failed to generate the graph image file: {filename}"
            )

    def get_state_snapshots(self) -> List[Dict[str, Any]]:
        """Get all the state snapshots from the graph execution."""
        all_states = []
        for state in self.graph.get_state_history(self.config):
            all_states.append(state)
        return all_states

    def save_ttl_output(self, output_file: str = "brick_schema_output.ttl") -> None:
        """Save the TTL output to a file."""
        if self.result is None:
            raise ValueError("No result found. Please run the graph first.")

        ttl_output = self.result.get("ttl_output", None)

        if ttl_output:
            with open(output_file, "w") as f:
                f.write(ttl_output)
        else:
            raise ValueError(
                "No TTL output found in the result. Please run the graph with a valid prompt."
            )
