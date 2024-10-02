from brickllm.graphs import BrickSchemaGraph

# Create an instance of BrickSchemaGraph
brick_graph = BrickSchemaGraph()
brick_graph.compile()

# Specify the user prompt
building_description = """
I have a building located in Bolzano.
It has 3 floors and each floor has 1 office.
There are 2 rooms in each office and each room has three sensors:
- Temperature sensor;
- Humidity sensor;
- CO sensor.
"""

# Display the graph
brick_graph.display()

# Run the graph without streaming
brick_graph.run(
    prompt=building_description,
    stream=False
)