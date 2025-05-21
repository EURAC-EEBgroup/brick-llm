"""
Module containing the prompts used for the LLM models
"""

get_elem_instructions: str = """
You are an expert in recognizing elements from a given ontology dictionary (ONTOLOGY) in a natural language description of a building and/or energy systems (DESCRIPTION).\n
You are tasked with identifiying which elements of the ontology dictionary are present in the description.\n

# Resources Provided:
- ONTOLOGY: A hierarchical dictionary containing ontology entities with a description of each entity.

{elements_dict}

- DESCRIPTION: A natural language description of a building or energy systems.

{user_prompt}

# Your Objective:
- Identify and return all the semantic elements from the ontology dictionary that are also present in the DESCRIPTION. If no elements are found, return an empty list.
 """  # noqa

get_elem_children_instructions: str = """
    You are a semantic ontology expert and you are provided with a description (DESCRIPTION) which describes a building and/or energy systems.\n
    You are provided with a list of common elements organized in a hierarchy (ELEMENTS HIERARCHY).\n
    You are now asked to identify the elements in the hierarchy presents in the description.\n
    The elements provided are in the format of a hierarchy,
    eg: `Sensor -> Position_Sensor, Sensor -> Energy_Sensor`\n
    You must include only the elements in the list of elements provided.\n
    DO NOT repeat any elements and DO NOT include "->" in your response.\n

    DESCRIPTION: {prompt} \n
    ELEMENTS HIERARCHY: {elements_list} \n
    """  # noqa

get_relationships_instructions: str = """
    You are a semantic ontology expert and you are provided with a description (DESCRIPTION) that describes a building and/or energy systems.\n
    Your task is to determine the entities inside the description the relationships between these entities based on the context within the description.\n
    The relationships should reflect direct connections or associations as described or implied in the description.\n
    You must distinguish different entities of the same type, each entiity must be followed by a dot symbol (.) and a number to differentiate between enetities of the same type (e.g., Room.1, Room.2).\n
    An example of output is the following: [('Building.1', 'Floor.1'), ('Floor.1', 'Room.1'), ('Room.1', 'Temperature_Sensor.1'), ('Room.1', 'Temperature_Sensor.2'), ...]\n
    Ignore timeseries ID references.\n

    DESCRIPTION: {prompt}
    
"""  # noqa

find_entities_type = """
You are an expert in mapping ontology concepts (ONTOLOGY CONCEPTS) to entities extracted from a building or energy system description (DESCRIPTION).\n
You are provided with the building or energy system description to have the context (DESCRIPTION).\n
You are provided with the relationships you recognized between the entities in the descriptions (RELATIONSHIPS).\n
You are provided with the hierarchy of the ontology concepts (ONTOLOGY CONCEPTS).\n
Your job is to find the most appropriate ontology concept for an entity extracted from the building description. I will provide you with the name of an entitiy (ENTITY) and you have to find the related ontological concept, but only the most specific one form the hierarchy.\n

DESCRIPTION: {user_prompt}\n

RELATIONSHIPS: {relationships}\n

ONTOLOGY CONCEPTS: {hierarchical_structure}\n

Return only the most specific ontology concept from ONTOLOGY CONCEPTS hierarchy that better represent the ENTITY.\n
ENTIIY: {entity}\n
"""  # noqa

find_relationship = """
You are expert in extracting and linking semantic entities from a building or energy system description (DESCRIPTION) based on the constraints provided by an ontology.\n
In particular, your task is to link the entities already extracted in form of tuples (TUPLE), assigning a relationship between them.\n
You are provided with the description of the building or the energy system to have the context (DESCRIPTION).\n
You are provided with a tuple that contains the two entities linked (TUPLE).\n
You are also provided with a dictionary (RELATIONSHIPS) that contains the relationships admitted between the two entities. Each relationships is a dictionary where the key is the relationship and the value is the description.\n
Based on the DESCRIPTION, the entities in the TUPLE and the RELATIONSHIPS, you have to find the most appropriate relationship between the two entities.\n
Return only the relationship key that best fit the entities in the TUPLE.\n

DESCRIPTION: {user_prompt}

TUPLE: {tuple}

RELATIONSHIPS: {relationships}

Return only one relationship among RELATIONSHIPS that best link the entities in the TUPLE based on the context provided in the DESCRIPTION. Do not add any context to the response.\n
"""

get_sensors_instructions: str = """
    Your task is to complete a dictionary of sensors (SENSOR DICTIONARY) based on the information provided in a description of a building and/or energy systems (DESCRIPTION).\n
    
    DESCRIPTION:\n
    {prompt}\n
    
    SENSOR DICTIONARY:\n
    {sensor_structure}
    
    Your task is to identify in the DESCRIPTION either the identifier of the sensors (id) and/or their unit of measures (unit).\n
    
    For each sensor type, you can choose only between the unit of measures provided (UOM), choosing the most appropriate QUDT one for each type of sensor., if they are specified.\n
    
    UOM:\n
    {unit_of_measures}
    
    Regarding the identifiers (id), they can be provided in parentheses or brackets. If the timeseries is not provided, leave None in the dictionary 'id' field.\n
    Regarding the unit of measures, they can be provided in the description as a natural language. Return the most appropriate corresponding QUDT. If the unit of measure is not provided, leave None in the dictionary.\n
    Do not include information that are not mentioned in the DESCRIPTION.
"""

ttl_example: str = """
    @prefix bldg: <urn:Building#> .
    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix unit: <https://qudt.org/vocab/unit/> .
    @prefix ref: <https://brickschema.org/schema/Brick/ref#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    bldg:CO_sensor a brick:CO ;
        brick:hasUnit unit:PPM ;
        brick:isPointOf bldg:Milano_Residence_1 ;
        ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId 'dvfs-dfwde-gaw'^^xsd:string ; ref:storedAt bldg:example_db ]

    bldg:Indoor_humidity a brick:Relative_Humidity_Sensor ;
        brick:hasUnit unit:PERCENT ;
        brick:isPointOf bldg:livingroom ;
        ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId '23rs-432a-63cv'^^xsd:string ;
                ref:storedAt bldg:example_db ] .

    bldg:Indoor_temperature a brick:Air_Temperature_Sensor ;
        brick:hasUnit unit:DEG_C ;
        brick:isPointOf bldg:livingroom ;
        ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId  'rtg456789'^^xsd:string ;
                ref:storedAt bldg:example_db ] .

    bldg:external_temperature a brick:Air_Temperature_Sensor ;
        brick:hasUnit unit:DEG_C ;
        brick:isPointOf bldg:livingroom ;
        ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId   'art53678^^xsd:string' ;
                ref:storedAt bldg:example_db ] .

    bldg:example_db a brick:Database .

    bldg:Milano_Residence_1 a brick:Building ;
        brick:hasLocation [ brick:value "Milano"^^xsd:string ] .

    bldg: a brick:Room ;
        brick:isPartOf bldg:Milano_Residence_1 .

    bldg:livingroom a brick:Room ;
        brick:isPartOf bldg:Milano_Residence_1 .
"""  # noqa

schema_to_ttl_instructions: str = """
    You are an expert in generating ontology-based RDF graph from a user prompt, which describes a building or energy systems.\n
    You are provided with a dictionary containing the hierarchy of the building/energy systems components (COMPONENTS HIERARCHY) detected in the user prompt (USER PROMP).\n
    You are also provided with the relationships between the components (RELATIONSHIPS) identified in the user prompt.\n
    You are also provided with the list of the sensors (SENSOR LIST) identified in the user prompts, with additional information about uuid and unit of measures, if avaiable.
    
    Your task is to generate a RDF graph in Turtle format that is compliant with the hierarchy and relationships described in the input. Use only the elements identified in the COMPONENTS HIERARCHY and SENSOR LIST, connecting each entities with the appropriate properties (presented in each element of the hierarchy).\n
    DO NOT add information that are not present in the input.\n
    To encode the uuid of the sensors, use the following schema: 'sensor' ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId 'uuid'^^xsd:string .].\n
    To encode the unit of measure of the sensor, use the following schema: 'sensor' brick:hasUnit unit:UNIT, where unit is the @prefix of the unit ontology (@prefix unit: <http://qudt.org/vocab/unit/> .).\n
    Include all the @prefix declarations at the beginning of the output Turtle file.\n
    I provide you an example of the output Turtle: the TTL SCRIPT EXAMPLE is useful to understand the overall structure of the output, not the actual content. Do not copy any information from this example.\n
    TTL SCRIPT EXAMPLE: {ttl_example}\n
    
    # Inputs
    USER PROMPT: {prompt}\n
    
    COMPONENTS HIERARCHY: {elem_hierarchy}\n

    SENSOR LIST: {uuid_list}\n
"""  # noqa

model_refactor_instructions: str = """
    You are an expert in refactoring a RDF graph based on a validation report from the ontology and the natural language description of the RDF graph.\n
    You are provided with the following inputs:
    1. **RDF GRAPH**: The RDF graph generated from the user prompt that needs to be refactored.\n
    {rdf_graph}
    
    2. **VALIDATION REPORT**: A SHACL shapes validation report that identifies the issues in the RDF graph generated from the description.\n
    {validation_report}
    
    3: **DESCRIPTION**: The original description that was used to generate the RDF graph.\n
    {user_prompt}
    
    Your task is to refactor the RDF graph. Ensure that the refactored RDF graph is consistent with the original description and the entities and relationship of the Brick ontology, addressing all the validation errors.\n
"""

ttl_to_user_prompt: str = """
    You are a BrickSchema ontology expert tasked with generating a clear and concise description of a building or facility from a TTL script.

    Your output must follow these guidelines:
    - Focus on the key building characteristics, components and relationships present in the TTL
    - Maintain technical accuracy and use proper Brick terminology
    - Keep descriptions clear and well-structured
    - Only include information explicitly stated in the TTL script
    - If no TTL content is provided, return an empty string

    Eventually, the user can provide additional instructions to help you generate the building description.
    <additional_instructions>
    {additional_instructions}
    </additional_instructions>

    TTL script to analyze:
    <ttl_script>
    {ttl_script}
    </ttl_script>
"""  # noqa

prompt_template_local: str = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    {instructions}

    ### Input:
    {user_prompt}

    ### Response:
"""  # noqa
