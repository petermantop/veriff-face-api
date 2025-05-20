from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

database = f"sqlite:///{DATABASE_URL}"

engine = create_engine(
    database,
    connect_args={"check_same_thread": False},  # Required for multithreading
    poolclass=None,  # Explicitly disables connection pooling
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
