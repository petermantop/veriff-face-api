import httpx
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FaceEncodingClient:
    """Client for interacting with the Face Encoding service."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    async def get_face_encodings(self, image_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Send an image to the Face Encoding service and get back the face encodings.
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
                        f"{self.base_url}/encode",
                        files=files,
                        timeout=30.0  # 30 seconds timeout
                    )
                    
                    if response.status_code == 200:
                        return response.json()
                    else:
                        logger.error(f"Error from Face Encoding service: {response.status_code} - {response.text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error communicating with Face Encoding service: {str(e)}")
            return None