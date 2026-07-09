from pydantic import BaseModel
from typing import Optional





class ItemSchema(BaseModel):
    name: str
    about: str
    price: int
    is_active: bool
    category_id: int



class ItemPatchSchema(BaseModel):
    name: Optional[str] = None
    about: Optional[str] = None
    price: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None

