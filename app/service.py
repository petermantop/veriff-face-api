import os
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app import models, schemas
from app.face_encoding_client import FaceEncodingClient
from app.config import UPLOAD_DIR
from typing import List

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize the Face Encoding client
face_encoding_client = FaceEncodingClient()

def create_container(db: Session, container: schemas.ContainerCreate):
    """Create a new verification container."""
    existing_container = db.query(models.VerificationContainer).filter(
        models.VerificationContainer.name == container.name
    ).first()
    
    if existing_container:
        raise HTTPException(status_code=400, detail="Container with this name already exists")
    
    # If no duplicate found, create the new container
    db_container = models.VerificationContainer(name=container.name)
    db.add(db_container)
    db.commit()
    db.refresh(db_container)
    return db_container

def get_container(db: Session, container_id: int):
    """Get a container by ID."""
    container = db.query(models.VerificationContainer).filter(
        models.VerificationContainer.id == container_id
    ).first()
    
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    
    return container

async def upload_image(db: Session, container_id: int, file: UploadFile):
    """Upload an image to a verification container and process it with Face Encoding service."""
    # Check if container exists
    container = get_container(db, container_id)
    
    # Check if container already has 5 images
    image_count = db.query(models.Image).filter(
        models.Image.container_id == container_id
    ).count()
    
    if image_count >= 5:
        raise HTTPException(status_code=400, detail="Container already has the maximum of 5 images")
    
    # Create a unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Process the image with Face Encoding service
    face_encodings = await face_encoding_client.get_face_encodings(file_path)
    
    # Create a new image record in the database
    db_image = models.Image(
        container_id=container_id,
        file_path=file_path,
        face_encodings=face_encodings
    )
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    return db_image

def get_verification_summary(db: Session, container_id: int):
    """Get a verification summary for a container."""
    # Check if container exists
    container = get_container(db, container_id)
    
    # Get all images for the container
    images = db.query(models.Image).filter(
        models.Image.container_id == container_id
    ).all()
    
    # Create the verification summary
    summary = schemas.VerificationSummary(
        container_id=container.id,
        container_name=container.name,
        images=images
    )
    
    return summary