from fastapi import APIRouter, Depends

from app.database import get_db
from sqlalchemy.orm import Session

from app import schemas, service

router = APIRouter()

@router.post("/containers/", response_model=schemas.Container)
def create_container(container: schemas.ContainerCreate, db: Session = Depends(get_db)):
    return service.create_container(db, container)