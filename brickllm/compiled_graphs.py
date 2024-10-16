from .graphs import BrickSchemaGraph, BrickSchemaGraphLocal

# compiled graph
brickschema_graph = BrickSchemaGraph()._compiled_graph()
brickschema_graph_local = BrickSchemaGraphLocal()._compiled_graph()
