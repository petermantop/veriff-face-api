from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def create_container(db: Session, container: schemas.ContainerCreate):

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