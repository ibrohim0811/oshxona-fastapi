from pydantic import BaseModel
from typing import Optional


class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: str


class CustomerChemaid(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str



class CustomerSchemaPatch(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]