from sqlalchemy.orm import Session
from app import models, schemas

def create_container(db: Session, container: schemas.ContainerCreate):
    db_container = models.VerificationContainer(name=container.name)
    db.add(db_container)
    db.commit()
    db.refresh(db_container)
    return db_container