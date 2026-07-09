from pydantic import BaseModel
from typing import Optional



class OrderSchemaid(BaseModel):
    id: int
    status: str
    customer_id: int

class OrderSchema(BaseModel):
    status: str
    customer_id: int


class OrderCreateSchema(BaseModel):
    status: str
    customer_id: int



class OrderSchemaPatch(BaseModel):
    status: Optional[str] = None
    customer_id: Optional[int] = None    