"""
Module containing the prompts used for the LLM models
"""

get_elem_instructions: str = """
    You are an expert in indentifying semantic elements in a natural language prompt hich describes a building and/or energy systems.\n
    You are provided with a dictionary containing the entities of an ontology (ELEMENTS) in a hierarchical way, which can be used to describe the building and/or the energy systems. 
    You are also provided with the elements description to understand what each element represents.\n
    You are now asked to identify the entities of the ENTITIES dictionary presented in the user prompt (USER PROMPT), choosing the most specific one if it is possible among the ones provided. Return the entities of ENTITIES (with the proper underscores) presented in the USER PROMPT.\n
    USER PROMPT: {prompt} \n
    ENTITIES: {elements_dict} \n
    """  # noqa

get_elem_children_instructions: str = """
    You are a semantic ontology expert and you are provided with a user prompt (USER PROMPT) which describes a building and/or energy systems.\n
    You are provided with a list of common elements organized in a hierarchy (ELEMENTS HIERARCHY).\n
    You are now asked to identify the elements in the hierarchy presents in the user prompt.\n
    The elements provided are in the format of a hierarchy,
    eg: `Sensor -> Position_Sensor, Sensor -> Energy_Sensor`\n
    You must include only the elements in the list of common elements provided.\n
    DO NOT repeat any elements and DO NOT include "->" in your response.\n

    USER PROMPT: {prompt} \n
    ELEMENTS HIERARCHY: {elements_list} \n
    """  # noqa

get_relationships_instructions: str = """
    You are a semantic ontology expert and you are provided with a user prompt (USER PROMPT) that describes a building and/or energy systems.\n
    You are also provided with a hierarchical structure (HIERARCHICAL STRUCTURE) of the identified building or energy systems components in the prompt.\n
    Your task is to determine the relationships between these components based on the context within the building description and the provided hierarchical structure.\n
    The relationships should reflect direct connections or associations as described or implied in the prompt.\n
    Each element must be followed by a dot symbol (.) and a number to differentiate between elements of the same type (e.g., Room.1, Room.2).\n
    An example of output is the following: [('Building.1', 'Floor.1'), ('Floor.1', 'Room.1'), ('Building.1','Floor.2'), ...]\n
    DO NOT add relationships on the output but only the components names, always add first the parent and then the child.\n
    If an element has no relationships, add an empty string in place of the missing component ("Room.1","").\n
    HIERARCHICAL STRUCTURE: {building_structure}\n
    USER PROMPT: {prompt}
"""  # noqa


get_sensors_instructions: str = """
    You are an expert in identifying information in a natural language prompt (USER PROMPT) that describes a building and/or energy systems.\n
    Your task is to map information about sensors in the building into the provided hierarchical sensor structure (HIERARCHICAL SENSOR STRUCTURE).\n
    You must look in the USER PROMPT for finding the UUID of the sensors and their unit of measures, if provided. If these information ar not provided in the USER PROMPT, return the HIERARCHICAL SENSOR STRUCTURE as it is.\n
    The UUID of the sensors may be explicitly provided in the USER PROMPT or may be inferred from the context (they may be in parentheses or brackets).\n
    To encode the unit of measures, use the names defined by the QUDT ontology.\n
    Complete the HIERARCHICAL SENSOR STRUCTURE with the "uuid" and "unit" fields for each sensor, if provided in the USER PROMPT.\n
    Remember, only provide units and ID if explicitly provided in the user prompt! If those information are not provided, return the dictionary with the empty field.
    USER PROMPT: {prompt}
    HIERARCHICAL SENSOR STRUCTURE: {sensor_structure}
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
    You are also provided with the list of the sensors (SENSOR LIST) identified in the user prompts, with additional information about uuid and unit of measures, if avaiable.
    Your task is to generate a RDF graph in Turtle format that is compliant with the hierarchy and relationships described in the input. Use only the elements identified in the COMPONENTS HIERARCHY and SENSOR LIST, connecting each entities with the appropriate properties (presented in each element of the hierarchy).\n
    DO NOT add information that are not present in the input.\n
    To encode the uuid of the sensors, use the following schema: 'sensor' ref:hasExternalReference [ a ref:TimeseriesReference ; ref:hasTimeseriesId 'uuid'^^xsd:string .].\n
    To encode the unit of measure of the sensor, use the following schema: 'sensor' brick:hasUnit unit:UNIT, where unit is the @prefix of the unit ontology (@prefix unit: <http://qudt.org/vocab/unit/> .).\n
    Include all the @prefix declarations at the beginning of the output Turtle file.\n
    I provide you an example of the output Turtle: the TTL SCRIPT EXAMPLE is useful to understand the overall structure of the output, not the actual content. Do not copy any information from this example.\n
    TTL SCRIPT EXAMPLE: {ttl_example}\n

    COMPONENTS HIERARCHY: {elem_hierarchy}\n

    USER PROMPT: {prompt}\n

    SENSOR LIST: {uuid_list}\n
"""  # noqa

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
