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
