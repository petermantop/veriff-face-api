from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()


class VerificationContainer(Base):
    __tablename__ = 'verification_containers'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    container_id = Column(Integer, ForeignKey('verification_containers.id'), nullable=False)
    file_path = Column(String, nullable=False)
    face_encodings = Column(JSON)