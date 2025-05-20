# Veriff Face API

A minimal REST API service that allows clients to:
1. Create a verification container
2. Upload up to 5 images to that verification container
3. Fetch a verification summary containing every face's 128-dimensional vector

## Configuration

The application can be configured using environment variables:

- `DATABASE_URL`: Path to the SQLite database file (default: "/home/kaspar/Documents/veriff-face-api/test.db")
- `FACE_ENCODING_SERVICE_URL`: URL of the Face Encoding service (default: "http://localhost:8000")
- `UPLOAD_DIR`: Directory to store uploaded images (default: "uploads" directory in the project root)

You can set these variables in a `.env` file in the project root directory. See `.env.example` for an example.

## API Endpoints

### Create a Verification Container
```
POST /containers/
```
Request body:
```json
{
  "name": "container-name"
}
```

### Upload an Image to a Container
```
POST /containers/{container_id}/images/
```
Form data:
- `file`: The image file to upload

### Get Verification Summary
```
GET /containers/{container_id}/summary
```

## Running the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Running Tests

```bash
poetry run pytest
```

## Design Decisions

- The API is built using FastAPI for high performance and easy development
- SQLite is used as the database for simplicity, but can be easily replaced with another database
- Images are stored on the filesystem, and their paths are stored in the database
- The Face Encoding service is accessed via HTTP requests
- The API enforces a limit of 5 images per container

## Future Improvements

- Add authentication and authorization
- Add more comprehensive error handling
- Add more comprehensive logging
- Add more tests for edge cases