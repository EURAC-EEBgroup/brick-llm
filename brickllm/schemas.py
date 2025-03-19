from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


# pydantic schemas
class ElemListSchema(BaseModel):
    elem_list: List[str]


class RelationshipsSchema(BaseModel):
    relationships: List[Tuple[str, ...]]


class EntityType(BaseModel):
    ontology_concept: str = Field("The ontological concept")


class Relationship(BaseModel):
    relationship: str = Field("The relationship between the two entities")


class Sensor(BaseModel):
    name: str = Field("name of the sensor")
    id: Optional[str] = Field("Identifier of the sensor")
    unit: Optional[str] = Field("Unit of measure of the sensor")


class SensorSchema(BaseModel):
    sensors: List[Sensor] = Field("List of the sensors")


class TriplesSchema(BaseModel):
    triples: List[Tuple[str, ...]] = Field("List of tuples of type (str, str, str)")


class TTLSchema(BaseModel):
    ttl_output: str = Field(
        ..., description="The generated BrickSchema turtle/rdf script."
    )


class TTLToBuildingPromptSchema(BaseModel):
    building_description: str = Field(
        ..., description="The generated building description."
    )
    key_elements: List[str] = Field(
        ..., description="The generated list of key elements."
    )
