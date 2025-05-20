from typing import List
from pydantic import BaseModel

class ContainerBase(BaseModel):
    name: str

class ContainerCreate(ContainerBase):
    pass

class Container(ContainerBase):
    id: int