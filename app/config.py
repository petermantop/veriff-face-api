import os
from urllib.parse import unquote
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "home/kaspar/Documents/veriff-face-api/test.db")

# Face Encoding Service configuration
FACE_ENCODING_SERVICE_URL_RAW = unquote(os.getenv("FACE_ENCODING_SERVICE_URL", "http://localhost:8000"))
FACE_ENCODING_SERVICE_URL = FACE_ENCODING_SERVICE_URL_RAW.replace(r"\x3a", ":")

# Upload directory configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"))