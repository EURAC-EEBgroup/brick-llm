from typing import TypedDict, Literal
from langgraph.graph import START, END, StateGraph

from brickllm.utils.states import State
from brickllm.utils.nodes import get_elements, get_elem_children, get_relationships, schema_to_ttl, validate_schema, get_sensors
from brickllm.utils.edges import validate_condition

# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai", "fireworks"]

# Define a new graph
workflow = StateGraph(State, config_schema=GraphConfig)
# Build graph
workflow = StateGraph(State)
workflow.add_node("get_elements", get_elements)
workflow.add_node("get_elem_children", get_elem_children)
workflow.add_node("get_relationships", get_relationships)
workflow.add_node("schema_to_ttl", schema_to_ttl)
workflow.add_node("validate_schema", validate_schema)
workflow.add_node("get_sensors", get_sensors)

# Logic
workflow.add_edge(START, "get_elements")
workflow.add_edge("get_elements", "get_elem_children")
workflow.add_edge("get_elem_children", "get_relationships")
workflow.add_edge("get_relationships", "schema_to_ttl")
workflow.add_edge("schema_to_ttl", "validate_schema")
workflow.add_conditional_edges("validate_schema", validate_condition)
workflow.add_edge("get_relationships", "get_sensors")
workflow.add_edge("get_sensors", END)

# Compile graph
graph = workflow.compile()