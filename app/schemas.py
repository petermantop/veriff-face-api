from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ContainerBase(BaseModel):
    name: str

class ContainerCreate(ContainerBase):
    pass

class Container(ContainerBase):
    id: int
    
    class Config:
        from_attributes = True

class ImageBase(BaseModel):
    container_id: int

class ImageCreate(ImageBase):
    pass

class FaceEncoding(BaseModel):
    """A 128-dimensional face encoding vector."""
    encoding: List[float] = Field(..., description="128-dimensional face encoding vector")

class Image(ImageBase):
    id: int
    file_path: str
    face_encodings: Optional[List[List[float]]] = None
    
    class Config:
        from_attributes = True

class VerificationSummary(BaseModel):
    container_id: int
    container_name: str
    images: List[Image]
    
    class Config:
        from_attributes = True