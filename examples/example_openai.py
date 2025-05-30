from dotenv import load_dotenv

from brickllm.graphs import BrickSchemaGraph

# Load environment variables
load_dotenv()

# Specify the user prompt
building_description = """
I have a building located in Bolzano.
It has 3 floors and each floor has 1 office.
There are 2 rooms in each office and each room has three sensors:
- Temperature sensor;
- Humidity sensor;
- CO2 sensor.
"""

# Create an instance of BrickSchemaGraph with a predefined provider
brick_graph = BrickSchemaGraph(model="openai")

# Display the graph structure
brick_graph.display(filename="graph_openai.png")

# Prepare input data
input_data = {"user_prompt": building_description}

# Run the graph
result = brick_graph.run(input_data=input_data, stream=False)

# Print the result
print(result)

# save the result to a file
brick_graph.save_ttl_output("my_building.ttl")

# Generate the building description from the generated ttl file
building_description, key_elements = brick_graph.ttl_to_building_description()

print("Generated building description:")
print(building_description)
print("--------------------------------")
print("Generated key elements:")
print(key_elements)
