from typing import List, Tuple

from pydantic.v1 import BaseModel, Field


# pydantic schemas
class ElemListSchema(BaseModel):
    elem_list: List[str]


class RelationshipsSchema(BaseModel):
    relationships: List[Tuple[str, ...]]


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
