from brickllm.graphs import BrickSchemaGraph
from langchain_openai import ChatOpenAI

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
custom_model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
brick_graph = BrickSchemaGraph(model=custom_model)

# Run the graph with the custom model
result = brick_graph.run(prompt=building_description, stream=False)

print(result)
print(result.get('elem_hierarchy', None))

ttl_output = result.get('ttl_output', None)

# Save the output to a file
if ttl_output:
    print(ttl_output)
    with open('output_custom.ttl', 'w') as f:
        f.write(ttl_output)