import httpx
import os
from typing import List, Optional
import logging
from app.config import FACE_ENCODING_SERVICE_URL

logger = logging.getLogger(__name__)

class FaceEncodingClient:
    """Client for interacting with the Face Encoding service."""
    
    def __init__(self, base_url: str = FACE_ENCODING_SERVICE_URL):
        self.base_url = base_url
        
    async def get_face_encodings(self, image_path: str) -> Optional[List[List[float]]]:
        """
        Send an image to the Face Encoding service and get back the face encodings.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of face encodings (128-dimensional vectors) or None if the request fails.
            Each face encoding is a list of 128 float values.
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
            
        try:
            # Prepare the file for upload
            with open(image_path, "rb") as f:
                files = {"file": f}
                
                # Make the request to the Face Encoding service
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/v1/selfie",
                        files=files,
                        timeout=30.0  # 30 seconds timeout
                    )
                    
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 400:
                        logger.error("More than 5 faces found in the image")
                        return None
                    else:
                        logger.error(f"Error from Face Encoding service: {response.status_code} - {response.text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error communicating with Face Encoding service: {str(e)}")
            return None