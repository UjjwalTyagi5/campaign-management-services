from pydantic import BaseModel, Field
from typing import List

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config:
        orm_mode = True
