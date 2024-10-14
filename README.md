<p align="center">
  <img src="docs/assets/brickllm_banner.png" alt="BrickLLM" style="width: 100%;">
</p>

# 🧱 BrickLLM

BrickLLM is a Python library for generating RDF files following the BrickSchema ontology using Large Language Models (LLMs).

## Features

- Generate BrickSchema-compliant RDF files from natural language descriptions of buildings and facilities
- Support for multiple LLM providers (OpenAI, Anthropic, Fireworks)
- Customizable graph execution with LangGraph
- Easy-to-use API for integrating with existing projects

## 💻 Installation

You can install BrickLLM using pip:

``` bash
pip install brickllm
```

<details>
<summary><b>Development Installation</b></summary>

[Poetry](https://python-poetry.org/) is used for dependency management during development. To install BrickLLM for contributing, follow these steps:

``` bash
# Clone the repository
git clone https://github.com/EURAC-EEBgroup/brickllm-lib.git
cd brick-llm

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows

# Install Poetry and dependencies
pip install poetry
poetry install

# Install pre-commit hooks
pre-commit install
```

</details>

## 🚀 Quick Start

Here's a simple example of how to use BrickLLM:

``` python
from brickllm.graphs import BrickSchemaGraph

building_description = """
I have a building located in Bolzano.
It has 3 floors and each floor has 1 office.
There are 2 rooms in each office and each room has three sensors:
- Temperature sensor;
- Humidity sensor;
- CO sensor.
"""

# Create an instance of BrickSchemaGraph with a predefined provider
brick_graph = BrickSchemaGraph(model="openai")

# Display the graph structure
brick_graph.display()

# Run the graph
result = brick_graph.run(prompt=building_description, stream=False)

# Print the result
print(result)

# save the result to a file
brick_graph.save_ttl_output("my_building.ttl")
```

<details>
<summary><b>Using Custom LLM Models</b></summary>

BrickLLM supports using custom LLM models. Here's an example using OpenAI's GPT-4o:

``` python
from brickllm.graphs import BrickSchemaGraph
from langchain_openai import ChatOpenAI

custom_model = ChatOpenAI(temperature=0, model="gpt-4o")
brick_graph = BrickSchemaGraph(model=custom_model)

result = brick_graph.run(prompt=building_description, stream=False)
```
</details>

<details>
<summary><b>Using Local LLM Models</b></summary>
BrickLLM supports using local LLM models employing the [Ollama framework](https://ollama.com/). Currently, only our fine-tuned model is supported.
To learn how to download our fine-tuned model, read the documentation [here](https://prova.com/).

``` python
from brickllm.graphs import BrickSchemaGraphLocal

instructions = """
Your job is to generate a RDF graph in Turtle format from a description of energy systems and sensors of a building in the following input, using the Brick ontology.
### Instructions:
- Each subject, object of predicate must start with a @prefix.
- Use the prefix bldg3: with IRI <http://my-bldg-3#> for any created entities.
- Use the prefix brick: with IRI <https://brickschema.org/schema/Brick#> for any Brick entities and relationships used.
- Use the prefix unit: with IRI <http://qudt.org/vocab/unit/> and its ontology for any unit of measure defined.
- When encoding the timeseries ID of the sensor, you must use the following format: ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId 'timeseriesID' ].
- When encoding identifiers or external references, such as building/entities IDs, use the following schema: ref:hasExternalReference [ a ref:ExternalReference ; ref:hasExternalReference ‘id/reference’ ].
- When encoding numerical reference, use the schema [brick:value 'value' ; \n brick:hasUnit unit:'unit' ] .
-When encoding coordinates, use the schema brick:coordinates [brick:latitude "lat" ; brick:longitude "long" ].
The response must be the RDF graph that includes all the @prefix of the ontologies used in the triples. The RDF graph must be created in Turtle format. Do not add any other text or comment to the response.
"""

user_prompt = """
The building (external ref: 'OB103'), with coordinates 33.9614, -118.3531, has a total area of 500 m². It has three zones, each with its own air temperature sensor. 
The building has an electrical meter that monitors data of a power sensor. An HVAC equipment serves all three zones and its power usage is measured by a power sensor.

Timeseries IDs and unit of measure of the sensors:
- Building power consumption: '1b3e-29dk-8js7-f54v' in watts.
- HVAC power consumption: '29dh-8ks3-fvjs-d92e' in watts.
- Temperature sensor zone 1: 't29s-jk83-kv82-93fs' in celsius.
- Temperature sensor zone 2: 'f29g-js92-df73-l923' in celsius.
- Temperature sensor zone 3: 'm93d-ljs9-83ks-29dh' in celsius.
"""

# Create an instance of BrickSchemaGraphLocal with our fine-tuned model
brick_graph = BrickSchemaGraphLocal(model="llama3.1:8b-brick")

# Run the graph
result = brick_graph.run(instructions=instructions, prompt=user_prompt, stream=False)

# Print the results
print(result)

# save the result to a file
brick_graph.save_ttl_output("my_building.ttl")
```
</details>

## 📖 Documentation

For more detailed information on how to use BrickLLM, please refer to our [documentation](https://brickllm.com/docs).

## 🤝 Contributing

We welcome contributions to BrickLLM! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## 📜 License

BrickLLM is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact:

- Marco Perini <marco.perini@eurac.edu>
- Daniele Antonucci <daniele.antonucci@eurac.edu>

## Acknowledgements

BrickLLM is developed and maintained by the Energy Efficiency in Buildings group at EURAC Research.
