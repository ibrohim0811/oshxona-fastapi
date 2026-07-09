from pydantic import BaseModel
from typing import Optional


class CategorySchema(BaseModel):
    id: int
    name: str



class CategoryCreateSchema(BaseModel):
    name: str



class CategoryPutSchema(BaseModel):
    name: str



class CategoryPatchSchema(BaseModel):
    name: Optional[str] = None