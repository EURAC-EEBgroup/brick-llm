from dotenv import load_dotenv

from brickllm.graphs import BrickSchemaGraph

# Load environment variables
load_dotenv()

# Specify the user prompt
building_description = """
The building (external ref: 'OB103'), with coordinates 33.9614, -118.3531, has a total area of 500 m². It has three zones, each with its own air temperature sensor.
The building has an electrical meter that monitors data of a power sensor. An HVAC equipment serves all three zones and its power usage is measured by a power sensor.

Timeseries IDs and unit of measure of the sensors:
- Building power consumption: '1b3e-29dk-8js7-f54v' in watts.
- HVAC power consumption: '29dh-8ks3-fvjs-d92e' in watts.
- Temperature sensor zone 1: 't29s-jk83-kv82-93fs' in celsius.
- Temperature sensor zone 2: 'f29g-js92-df73-l923' in celsius.
- Temperature sensor zone 3: 'm93d-ljs9-83ks-29dh' in celsius.
"""

# Create an instance of BrickSchemaGraph with a predefined provider
brick_graph = BrickSchemaGraph(model="openai")

# Display the graph structure
brick_graph.display(file_name="graph_openai.png")

# Prepare input data
input_data = {"user_prompt": building_description}

# Run the graph
result = brick_graph.run(input_data=input_data, stream=False)

# Print the result
print(result)

# save the result to a file
brick_graph.save_ttl_output("my_building.ttl")
