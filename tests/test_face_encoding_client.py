import pytest
from unittest.mock import patch, mock_open, AsyncMock
from app.face_encoding_client import FaceEncodingClient

@pytest.mark.asyncio
async def test_get_face_encodings_success():
    """Test successful retrieval of face encodings."""
    # Create a client instance
    client = FaceEncodingClient(base_url="http://test-service:8000")
    
    # Mock image path
    image_path = "/path/to/test_image.jpg"
    
    # Mock face encodings response
    mock_encodings = [[0.1, 0.2, 0.3] + [0.0] * 125]
    
    # Mock the file existence check
    with patch('os.path.exists', return_value=True):
        # Mock the file open operation
        mock_file = mock_open(read_data=b'fake_image_data')
        with patch('builtins.open', mock_file):
            # Mock the httpx AsyncClient
            with patch('httpx.AsyncClient') as mock_client:
                # Configure the mock response
                mock_response = AsyncMock()
                mock_response.status_code = 200
                # Make json() return a regular value, not a coroutine
                mock_response.json = lambda: mock_encodings
                
                # Configure the mock client
                mock_client_instance = AsyncMock()
                mock_client_instance.__aenter__.return_value = mock_client_instance
                mock_client_instance.post.return_value = mock_response
                mock_client.return_value = mock_client_instance
                
                # Call the method under test
                result = await client.get_face_encodings(image_path)
                
                # Verify the result
                assert result == mock_encodings
                
                # Verify the client was called correctly
                # Use the actual file object that was passed to post
                mock_client_instance.post.assert_called_once()
                call_args = mock_client_instance.post.call_args
                assert call_args[0][0] == "http://test-service:8000/v1/selfie"
                assert call_args[1]['timeout'] == 30.0
                assert 'file' in call_args[1]['files']

@pytest.mark.asyncio
async def test_get_face_encodings_file_not_found():
    """Test handling of non-existent image file."""
    # Create a client instance
    client = FaceEncodingClient(base_url="http://test-service:8000")
    
    # Mock image path
    image_path = "/path/to/nonexistent_image.jpg"
    
    # Mock the file existence check to return False
    with patch('os.path.exists', return_value=False):
        # Mock the logger to verify error logging
        with patch('app.face_encoding_client.logger.error') as mock_logger:
            result = await client.get_face_encodings(image_path)
            
            # Verify the result is None
            assert result is None
            
            # Verify the error was logged
            mock_logger.assert_called_once_with(f"Image file not found: {image_path}")

@pytest.mark.asyncio
async def test_get_face_encodings_service_error():
    """Test handling of service errors."""
    # Create a client instance
    client = FaceEncodingClient(base_url="http://test-service:8000")
    
    # Mock image path
    image_path = "/path/to/test_image.jpg"
    
    # Mock the file existence check
    with patch('os.path.exists', return_value=True):
        # Mock the file open operation
        mock_file = mock_open(read_data=b'fake_image_data')
        with patch('builtins.open', mock_file):
            # Mock the httpx AsyncClient
            with patch('httpx.AsyncClient') as mock_client:
                # Configure the mock response for error
                mock_response = AsyncMock()
                mock_response.status_code = 500
                mock_response.text = "Internal Server Error"
                
                # Configure the mock client
                mock_client_instance = AsyncMock()
                mock_client_instance.__aenter__.return_value = mock_client_instance
                mock_client_instance.post.return_value = mock_response
                mock_client.return_value = mock_client_instance
                
                # Mock the logger to verify error logging
                with patch('app.face_encoding_client.logger.error') as mock_logger:
                    # Call the method under test
                    result = await client.get_face_encodings(image_path)
                    
                    # Verify the result is None
                    assert result is None
                    
                    # Verify the error was logged
                    mock_logger.assert_called_once_with(
                        f"Error from Face Encoding service: {mock_response.status_code} - {mock_response.text}"
                    )