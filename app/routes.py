from fastapi import APIRouter, Depends, UploadFile, File, Path
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas, service
from typing import List

router = APIRouter()

@router.post("/containers/", response_model=schemas.Container)
def create_container(container: schemas.ContainerCreate, db: Session = Depends(get_db)):
    """Create a new verification container."""
    return service.create_container(db, container)

@router.get("/containers/{container_id}", response_model=schemas.Container)
def get_container(container_id: int = Path(..., description="The ID of the container to retrieve"), 
                 db: Session = Depends(get_db)):
    """Get a container by ID."""
    return service.get_container(db, container_id)

@router.post("/containers/{container_id}/images/", response_model=schemas.Image)
async def upload_image(
    container_id: int = Path(..., description="The ID of the container to upload to"),
    file: UploadFile = File(..., description="The image file to upload"),
    db: Session = Depends(get_db)
):
    """Upload an image to a verification container."""
    return await service.upload_image(db, container_id, file)

@router.get("/containers/{container_id}/summary", response_model=schemas.VerificationSummary)
def get_verification_summary(
    container_id: int = Path(..., description="The ID of the container to get the summary for"),
    db: Session = Depends(get_db)
):
    """Get a verification summary for a container."""
    return service.get_verification_summary(db, container_id)