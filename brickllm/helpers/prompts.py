"""
Module containing the prompts used for the LLM models
"""

get_elem_instructions: str = """
    You are a BrickSchema ontology expert and you are provided with a user prompt which describes a building or facility.\n
    You are provided with a list of common elements that can be used to describe a building or facility.\n
    You are also provided with the elements description to understand what each element represents.\n
    You are now asked to identify the elements presents in the user prompt, even if not explicitly mentioned.\n
    USER PROMPT: {prompt} \n
    ELEMENTS: {elements_dict} \n
    """

get_elem_children_instructions: str = """
    You are a BrickSchema ontology expert and you are provided with a user prompt which describes a building or facility.\n
    You are provided with a list of common elements that can be used to describe a building or facility.\n
    You are now asked to identify the elements presents in the user prompt.\n
    The elements provided are in the format of a hierarchy,
    eg: `Sensor -> Position_Sensor, Sensor -> Energy_Sensor`\n
    You must include only the elements in the list of common elements provided.\n
    DO NOT repeat any elements and DO NOT include "->" in your response.\n

    USER PROMPT: {prompt} \n
    ELEMENTS HIERARCHY: {elements_list} \n
    """

get_relationships_instructions: str = """
    You are a BrickSchema ontology expert and are provided with a detailed description of a building or facility.\n
    You are also provided with a hierarchical structure of identified building components.\n
    Your task is to determine the relationships between these components based on the context within the building description and the provided hierarchical structure.\n
    The relationships should reflect direct connections or associations as described or implied in the prompt.\n
    Each element must be followed by a dot symbol (.) and a number to differentiate between elements of the same type (e.g., Room.1, Room.2).\n
    An example of output is the following: [('Building.1', 'Floor.1'), ('Floor.1', 'Room.1'), ('Building.1','Floor.2'), ...]\n
    DO NOT add relationships on the output but only the components names, always add first the parent and then the child.\n
    If an element has no relationships, add an empty string in place of the missing component ("Room.1","").\n
    Hierarchical structure: {building_structure}\n
    USER PROMPT: {prompt}
"""

ttl_example: str = """
    @prefix bldg: <urn:Building#> .
    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix prj: <http://example.com/Project#> .

    bldg:CO_sensor a brick:CO ;
        brick:hasTag bldg:hour ;
        brick:hasUnit bldg:PPM ;
        brick:isPointOf bldg: ;
        brick:timeseries [ brick:hasTimeseriesId bldg:jkj4432uz43 ;
                brick:storedAt bldg:example_DB ] .

    bldg:Indoor_humidity a brick:Relative_Humidity_Sensor ;
        brick:hasTag bldg:hour ;
        brick:hasUnit bldg:PERCENT ;
        brick:isPointOf bldg:livingroom ;
        brick:timeseries [ brick:hasTimeseriesId bldg:hfrt56478 ;
                brick:storedAt bldg:example_DB ] .

    bldg:Indoor_temperature a brick:Air_Temperature_Sensor ;
        brick:hasTag bldg:hour ;
        brick:hasUnit bldg:DEG_C ;
        brick:isPointOf bldg:livingroom ;
        brick:timeseries [ brick:hasTimeseriesId bldg:rtg456789 ;
                brick:storedAt bldg:example_DB ] .

    bldg:external_temperature a brick:Air_Temperature_Sensor ;
        brick:hasTag bldg:hour ;
        brick:hasUnit bldg:DEG_C ;
        brick:isPointOf bldg:livingroom ;
        brick:timeseries [ brick:hasTimeseriesId bldg:art53678 ;
                brick:storedAt bldg:example_DB ] .

    bldg:example_db a brick:Database .

    prj:ThermoIot a brick:Site .

    bldg:Milano_Residence_1 a brick:Building ;
        brick:buildingPrimaryFunction [ brick:value "Residential" ] ;
        brick:hasLocation [ brick:value "Milano" ] ;
        brick:isPartOf prj:ThermoIot .

    bldg: a brick:Room ;
        brick:isPartOf bldg:Milano_Residence_1 .

    bldg:livingroom a brick:Room ;
        brick:isPartOf bldg:Milano_Residence_1 .
"""

schema_to_ttl_instructions: str = """
    You are a BrickSchema ontology expert and you are provided with a user prompt which describes a building or facility.\n
    You are provided with a dictionary containing the detected components in the building description.\n
    You are also provided with the hierarchical structure of the building components with their constraints BrickSchema compliant.\n
    Your task is to generate a valid TTL (turtle) script that captures the hierarchy and relationships described in the input.\n
    DO NOT add information that are not present in the input.\n
    DO NOT add uuids or database id in the TTL if not specified in the prompt.\n
    You must keep the enumeration with the hashtag for each component otherwise it will not be possible to recognize the components.\n
    The TTL SCRIPT EXAMPLE is useful to understand the overall structure of the output, not the actual content.\n
    TTL SCRIPT EXAMPLE: {ttl_example}\n

    COMPONENTS HIERARCHY: {elem_hierarchy}\n

    USER DESCRIPTION: {prompt}\n

    COMPONENTS DICT: {sensors_dict}\n
"""

prompt_template_local: str = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    {instructions}

    ### Input:
    {user_prompt}

    ### Response:
"""
