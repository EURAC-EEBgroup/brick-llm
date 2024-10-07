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
