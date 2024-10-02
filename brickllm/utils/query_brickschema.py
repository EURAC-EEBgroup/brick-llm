import os
import re
from rdflib import Graph, URIRef, Namespace
import pkg_resources

# Path to the Brick schema Turtle file
brick_ttl_path = pkg_resources.resource_filename(__name__, os.path.join('..', 'ontologies', 'Brick.ttl'))
# Load the Brick schema Turtle file
g = Graph()
g.parse(brick_ttl_path, format='ttl')

# Define the namespaces from the prefixes
namespaces = {
    'brick': Namespace('https://brickschema.org/schema/Brick#'),
}

# Function to get the definition from the TTL file
def get_brick_definition(element_name: str) -> str:
    normalized_key = element_name.replace('_', '').lower()
    for prefix, namespace in namespaces.items():
        uri = namespace[element_name]
        for s, p, o in g.triples((uri, URIRef("http://www.w3.org/2004/02/skos/core#definition"), None)):
            return str(o)
        uri = namespace[normalized_key]
        for s, p, o in g.triples((uri, URIRef("http://www.w3.org/2004/02/skos/core#definition"), None)):
            return str(o)
    return "No definition available"

# Function to get the query result without using pandas
def get_query_result(query):
    result = g.query(query)
    # Convert the result to a list of dictionaries where keys are the variable names
    query_vars = list(result.vars)
    data = []
    for row in result:
        data.append({str(var): str(row[var]) if row[var] else None for var in query_vars})
    # Remove entries with None values and reset index
    cleaned_data = [
        {key: value for key, value in row.items() if value is not None} 
        for row in data
    ]
    return cleaned_data

# Function to clean the result, extracting the needed part of the URI
def clean_result(data):
    return [re.findall(r'#(\w+)', value)[0] for value in data if re.findall(r'#(\w+)', value)]

# Function to create a SPARQL query for subclasses
def query_subclass(element):
    return f"SELECT ?subclass WHERE {{ brick:{element} rdfs:subClassOf ?subclass . }}"

# Function to create a SPARQL query for properties
def query_properties(element):
    return f"""
    SELECT ?property ?message ?path ?class WHERE {{
        brick:{element} sh:property ?property .
        ?property sh:message ?message ; sh:path ?path ;
                  sh:or/rdf:rest*/rdf:first ?constraint .
        ?constraint sh:class ?class .
    }}
    """

# Function to iteratively find subclasses
def iterative_subclasses(element):
    subclasses = []
    sub_class_data = get_query_result(query_subclass(element))
    subClass = clean_result([row['subclass'] for row in sub_class_data]) if sub_class_data else []

    while subClass:
        subclasses.append(subClass[0])
        if subClass[0] in {'Collection', 'Equipment', 'Location', 'Measureable', 'Point'}:
            break
        sub_class_data = get_query_result(query_subclass(subClass[0]))
        subClass = clean_result([row['subclass'] for row in sub_class_data]) if sub_class_data else []

    return subclasses

# General query function to retrieve properties and relationships
def general_query(element):
    subclasses = iterative_subclasses(element)
    if not subclasses:
        return {}

    query_data = get_query_result(query_properties(subclasses[-1]))
    relationships = {}

    for row in query_data:
        property_name = clean_result([row['path']])[0]
        if property_name not in relationships:
            relationships[property_name] = {
                'message': row['message'],
                'constraint': clean_result([row['class']])
            }
        else:
            relationships[property_name]['constraint'].extend(clean_result([row['class']]))

    return {'property': relationships}
