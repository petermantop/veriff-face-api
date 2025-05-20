from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import JSON

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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