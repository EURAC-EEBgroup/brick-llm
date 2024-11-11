from dotenv import load_dotenv

from brickllm.graphs import BrickSchemaGraphLocal

# Load environment variables
load_dotenv()

# Specify the instructions for local processing
instructions = """
Your job is to generate a RDF graph in Turtle format from a description of energy systems and sensors of a building in the following input, using the Brick ontology.
### Instructions:
- Each subject, object of predicate must start with a @prefix.
- Use the prefix bldg: with IRI <http://my-bldg#> for any created entities.
- Use the prefix brick: with IRI <https://brickschema.org/schema/Brick#> for any Brick entities and relationships used.
- Use the prefix unit: with IRI <http://qudt.org/vocab/unit/> and its ontology for any unit of measure defined.
- When encoding the timeseries ID of the sensor, you must use the following format: ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId 'timeseriesID' ].
- When encoding identifiers or external references, such as building/entities IDs, use the following schema: ref:hasExternalReference [ a ref:ExternalReference ; ref:hasExternalReference ‘id/reference’ ].
- When encoding numerical reference, use the schema [brick:value 'value' ; \n brick:hasUnit unit:'unit' ] .
-When encoding coordinates, use the schema brick:coordinates [brick:latitude "lat" ; brick:longitude "long" ].
The response must be the RDF graph that includes all the @prefix of the ontologies used in the triples. The RDF graph must be created in Turtle format. Do not add any other text or comment to the response.
"""

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

# Create an instance of BrickSchemaGraphLocal
brick_graph_local = BrickSchemaGraphLocal(model="llama3.1:8b-brick")

# Display the graph structure
brick_graph_local.display(filename="graph_local.png")

# Prepare input data
input_data = {"user_prompt": building_description, "instructions": instructions}

# Run the graph
result = brick_graph_local.run(input_data=input_data, stream=False)

# Print the result
print(result)

# Save the result to a file
brick_graph_local.save_ttl_output("my_building_local.ttl")
