# BrickLLM API Reference

Welcome to the API Reference for the `BrickLLM` library. This section of the documentation provides detailed information about the modules, classes, functions, and other components that make up the BrickLLM library.

## Overview

`BrickLLM` is a Python library designed to generate BrickSchema-compliant RDF files using Large Language Models (LLMs). It provides various utilities for parsing natural language building descriptions, extracting relevant components, and constructing a structured graph that represents the building and its systems.

This API reference covers all the essential modules and functions available in the library, including components for:

- **Element identification**
- **Relationship mapping**
- **TTL generation** (Turtle format RDF)
- **Ontology integration** (BrickSchema)

## Key Modules

- **Edges**: Validation of relationships (edges) between entities in the graph.
- **Graphs**: Handles the orchestration of graph-based operations with the BrickSchema.
- **Helpers**: Contains utility functions and predefined LLM prompts to aid in the generation process.
- **Nodes**: Specialized nodes that handle various tasks such as extracting elements, constructing hierarchies, and generating RDF files.
- **Ontologies**: Includes the BrickSchema ontology and hierarchical data.
- **Utils**: Utility functions for querying the BrickSchema and handling RDF data.

## How to Use the API Reference

- Navigate to individual modules and components via the side navigation or by clicking on the links in the module overview sections.
- Each module contains a breakdown of its functions, classes, and attributes, with descriptions and examples where applicable.

For an in-depth guide on how to use the library in practice, see the [Usage](../usage.md) section.

Happy coding!
