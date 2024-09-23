import os, re
from rdflib import Graph, URIRef, Namespace
import pandas as pd

brick_ttl_path = os.path.join(os.getcwd(), 'Brick.ttl')
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

def get_query_result(query):
    return pd.DataFrame(g.query(query), columns=g.query(query).vars).astype(str).dropna().reset_index(drop=True)

def clean_result(data):
    return [re.findall(r'#(\w+)', value)[0] for value in data]

def query_subclass(element):
    return f"SELECT ?subclass WHERE {{ brick:{element} rdfs:subClassOf ?subclass . }}"

def query_properties(element):
    return f"""
    SELECT ?property ?message ?path ?class WHERE {{
        brick:{element} sh:property ?property .
        ?property sh:message ?message ; sh:path ?path ;
                  sh:or/rdf:rest*/rdf:first ?constraint .
        ?constraint sh:class ?class .
    }}
    """

def iterative_subclasses(element):
    subclasses = []
    subClass = clean_result(get_query_result(query_subclass(element)).iloc[:, 0])
    while subClass:
        subclasses.append(subClass[0])
        if subClass[0] in {'Collection', 'Equipment', 'Location', 'Measureable', 'Point'}:
            break
        subClass = clean_result(get_query_result(query_subclass(subClass[0])).iloc[:, 0])
    return subclasses

def general_query(element):
    subclasses = iterative_subclasses(element)
    if not subclasses:
        return {}

    query_result = get_query_result(query_properties(subclasses[-1]))
    query_result.columns = ['property', 'message', 'path', 'class']
    relationships = {}

    for _, row in query_result.iterrows():
        property_name = clean_result(pd.Series([row['path']]))[0]
        if property_name not in relationships:
            relationships[property_name] = {
                'message': str(row['message']),
                'constraint': clean_result(pd.Series([row['class']]))
            }
        else:
            relationships[property_name]['constraint'].extend(clean_result(pd.Series([row['class']])))

    return {'property': relationships}