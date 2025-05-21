from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from brickllm.graphs import BrickSchemaGraph

# Load environment variables
load_dotenv()

# Specify the user prompt
building_description = """
I have a building located that  is composed by 2 floors. 
Each floor is composed by 1 room.
The room at the first floor has three sensors:
- Temperature sensor (°C) (ID: "hfws-xdf2");
- Humidity sensor (ID: "regs-452z");
- CO2 sensor (PPM) (ID: "gwq2-FH53).

The room at the second floor has two sensors:
- Temperature sensor (°C) (ID: "542c-743s");
- CO2 sensor (PPM) (ID: "deqz-63sr).

A general meter is installed in the building,  and collects the data of all the sensors in the building.
"""

# Create an instance of BrickSchemaGraph with a custom model
custom_model = ChatOpenAI(temperature=0, model="gpt-4o-mini")
brick_graph = BrickSchemaGraph(model=custom_model)

# Display the graph structure
brick_graph.display()

# Prepare input data
input_data = {"user_prompt": building_description}

# Run the graph with the custom model
result = brick_graph.run(input_data=input_data, stream=False)

# Print the result
print(result["graph"].serialize())

# save the result to a file
brick_graph.save_ttl_output("my_building_custom.ttl")

# Generate the building description from the generated ttl file
building_description, key_elements = brick_graph.ttl_to_building_description()

print("Generated building description:")
print(building_description)
print("--------------------------------")
print("Generated key elements:")
print(key_elements)
