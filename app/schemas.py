from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ContainerBase(BaseModel):
    name: str

class ContainerCreate(ContainerBase):
    pass

class Container(ContainerBase):
    id: int
    
    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    container_id: int

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    file_path: str
    face_encodings: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        orm_mode = True

class VerificationSummary(BaseModel):
    container_id: int
    container_name: str
    images: List[Image]
    
    class Config:
        orm_mode = True