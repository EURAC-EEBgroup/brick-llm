# Overview

BrickLLM is a Python library designed to generate RDF (Resource Description Framework) files that comply with the BrickSchema ontology using Large Language Models (LLMs). The library leverages advanced natural language processing capabilities to interpret building descriptions and convert them into structured, machine-readable formats suitable for building automation and energy management systems.

## Main Features

- **Multi-provider LLM Support**: Supports multiple LLM providers, including OpenAI, Anthropic, and Fireworks AI.
- **Natural Language to RDF Conversion**: Converts natural language descriptions of buildings and facilities into BrickSchema-compliant RDF.
- **Customizable Graph Execution**: Utilizes LangGraph for flexible and customizable graph-based execution of the conversion process.
- **Ontology Integration**: Incorporates the BrickSchema ontology for accurate and standardized representation of building systems.
- **Extensible Architecture**: Designed with modularity in mind, allowing for easy extension and customization.

## How It Works

1. **User Input**: The process begins with a natural language description of a building or facility provided by the user.

2. **LLM Processing**: The description is processed by a selected LLM to extract relevant building components and their relationships.

3. **Graph Execution**: The extracted information is passed through a series of nodes in a graph structure:
   - **Element Identification**: Identifies building elements from the user prompt.
   - **Hierarchy Construction**: Builds a hierarchical structure of the identified elements.
   - **Relationship Mapping**: Determines relationships between the components.
   - **TTL Generation**: Converts the structured data into Turtle (TTL) format, which is a serialization of RDF.

4. **Output Generation**: The final output is a BrickSchema-compliant RDF file in TTL format, representing the building's structure and systems.
