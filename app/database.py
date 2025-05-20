from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Construct the SQLAlchemy URL
DATABASE_URL = "sqlite:////home/kaspar/Documents/veriff-face-api/test.db"

engine = create_engine(
    DATABASE_URL,
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
