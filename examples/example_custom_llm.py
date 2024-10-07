from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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
- CO sensor.
"""

# Create an instance of BrickSchemaGraph with a custom model
custom_model = ChatOpenAI(temperature=0, model="gpt-4o")
brick_graph = BrickSchemaGraph(model=custom_model)

# Display the graph structure
brick_graph.display()

# Run the graph with the custom model
result = brick_graph.run(prompt=building_description, stream=False)

# Print the result
print(result)

# save the result to a file
brick_graph.save_ttl_output("my_building_custom.ttl")
