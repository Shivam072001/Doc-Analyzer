import requests
import json
import logging
import uuid
import os
from typing import BinaryIO, Dict, Any, Optional, Union, List
from ..config.config import Config

class UploadthingService:
    """
    A service for uploading files to Uploadthing.
    
    This class handles both single file uploads and multipart uploads to Uploadthing,
    with proper error handling and logging.
    """
    
    def __init__(self, secret_key: Optional[str] = None, 
                 upload_api_url: Optional[str] = None,
                 upload_multipart_url: Optional[str] = None):
        """
        Initialize the UploadthingService.
        
        Args:
            secret_key: The Uploadthing API key.
            upload_api_url: The URL for the Uploadthing API.
            upload_multipart_url: The URL for multipart uploads.
        """
        self.secret_key = secret_key or Config.UPLOADTHING_TOKEN
        self.upload_api_url = upload_api_url or Config.UPLOADTHING_URL
        self.upload_multipart_url = upload_multipart_url or Config.UPLOADTHING_MULTIPART_URL
        
        self.logger = logging.getLogger(__name__)

    def _validate_configuration(self):
        """Validate that the required configuration is present."""
        if not self.secret_key:
            raise ValueError("Uploadthing API key is not configured.")
        if not self.upload_api_url:
            raise ValueError("Uploadthing API URL is not configured.")

    def _get_file_size(self, file: Any) -> int:
        """
        Get the size of a file object in bytes.
        
        Args:
            file: The file object to get the size of.
            
        Returns:
            The size of the file in bytes.
        """
        # Try different methods to get file size
        try:
            # If file has a 'size' attribute (like FastAPI's UploadFile)
            if hasattr(file, "size") and file.size is not None:
                return file.size
            
            # If file is a file-like object
            if hasattr(file, "seek") and hasattr(file, "tell"):
                current_pos = file.tell()
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(current_pos)  # Reset file position
                return size
                

            if hasattr(file, "fileno"):
                return os.fstat(file.fileno()).st_size
                
        except (OSError, AttributeError, IOError) as e:
            self.logger.warning(f"Could not determine file size directly: {e}")
            
        # Last resort: read the file content to determine size
        try:
            if hasattr(file, "read") and hasattr(file, "seek"):
                current_pos = file.tell()
                content = file.read()
                size = len(content)
                file.seek(current_pos)  # Reset file position
                return size
        except Exception as e:
            self.logger.error(f"Failed to determine file size: {e}")
            raise ValueError(f"Unable to determine file size: {e}")

    def upload(self, file: Any, size: Optional[int] = None, 
               custom_id: Optional[str] = None, acl: str = "public-read", 
               content_disposition: str = "inline", metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Upload a file to Uploadthing.
        
        Args:
            file: The file object to upload.
            size: The size of the file in bytes. If not provided, it will be determined automatically.
            custom_id: A custom ID for the file. If not provided, a UUID will be generated.
            acl: The access control list for the file (default: "public-read").
            content_disposition: The content disposition for the file (default: "inline").
            metadata: Optional metadata for the file.
            
        Returns:
            The URL of the uploaded file.
        """
        self._validate_configuration()
        
        # Get filename and content type from file object
        if hasattr(file, "filename"):
            filename = file.filename
        elif hasattr(file, "name"):
            filename = os.path.basename(file.name)
        else:
            # Generate a random filename if none is available
            filename = f"upload_{uuid.uuid4()}"
        
        if hasattr(file, "content_type"):
            content_type = file.content_type
        else:
            # Try to guess the content type based on file extension
            import mimetypes
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        
        # Determine file size if not provided
        if size is None:
            size = self._get_file_size(file)
        
        # Generate a custom ID if not provided
        if custom_id is None:
            custom_id = str(uuid.uuid4())
        
        self.logger.info(f"Uploading file: {filename}, Size: {size}, Type: {content_type}")
        
        # Prepare headers and data for the initial request
        headers = {
            "X-Uploadthing-Api-Key": self.secret_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "files": [
                {
                    "name": filename,
                    "size": size,
                    "type": content_type,
                    "customId": custom_id
                }
            ],
            "acl": acl,
            "metadata": metadata,
            "contentDisposition": content_disposition
        }
        
        try:
            # Step 1: Get upload details from Uploadthing
            self.logger.debug(f"Making initial request to {self.upload_api_url}")
            response = requests.post(
                self.upload_api_url, 
                headers=headers, 
                data=json.dumps(data),
                timeout=30
            )
            response.raise_for_status()
            upload_details = response.json()
            
            self.logger.debug(f"Upload details received: {upload_details}")
            
            # Validate response format
            if not upload_details or 'data' not in upload_details or not isinstance(upload_details['data'], list) or not upload_details['data']:
                self.logger.error(f"Unexpected response from Uploadthing: {upload_details}")
                raise ValueError("Invalid response format from Uploadthing.")
            
            file_data = upload_details['data'][0]
            
            if not file_data.get('url') or not file_data.get('fields'):
                self.logger.error(f"Missing required fields in response: {file_data}")
                raise ValueError("Missing required fields in Uploadthing response.")
            
            upload_url = file_data['url']
            fields = file_data['fields']
            file_url = file_data['fileUrl']
            
            # Step 2: Prepare multipart form data for actual upload
            if hasattr(file, "read"):
                # Ensure file is at the beginning
                if hasattr(file, "seek"):
                    file.seek(0)
                file_content = file.read()
            else:
                # If file is a path, open and read it
                with open(file, 'rb') as f:
                    file_content = f.read()
            
            # Prepare the multipart form data
            files = {'file': (filename, file_content, content_type)}
            
            # Step 3: Upload the file to the pre-signed URL
            self.logger.debug(f"Uploading file to {upload_url}")
            upload_response = requests.post(
                upload_url, 
                data=fields, 
                files=files,
                timeout=60  # Longer timeout for file upload
            )
            upload_response.raise_for_status()
            
            self.logger.info(f"File '{filename}' uploaded successfully to Uploadthing. URL: {file_url}")
            return file_url
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error communicating with Uploadthing: {str(e)}")
            if 'response' in locals() and hasattr(response, 'text'):
                self.logger.error(f"Response body: {response.text}")
            raise ValueError(f"Error during Uploadthing communication: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during Uploadthing upload: {str(e)}")
            raise ValueError(f"Unexpected error during Uploadthing upload: {str(e)}")

    def upload_multiple(self, files: List[Any], custom_ids: Optional[List[str]] = None, 
                        acl: str = "public-read", content_disposition: str = "inline", 
                        metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Upload multiple files to Uploadthing.
        
        Args:
            files: A list of file objects to upload.
            custom_ids: A list of custom IDs for the files. If not provided, UUIDs will be generated.
            acl: The access control list for the files (default: "public-read").
            content_disposition: The content disposition for the files (default: "inline").
            metadata: Optional metadata for the files.
            
        Returns:
            A list of URLs of the uploaded files.
        """
        if custom_ids and len(custom_ids) != len(files):
            raise ValueError("The number of custom_ids must match the number of files")
        
        file_urls = []
        for i, file in enumerate(files):
            custom_id = custom_ids[i] if custom_ids else None
            file_url = self.upload(
                file=file,
                custom_id=custom_id,
                acl=acl,
                content_disposition=content_disposition,
                metadata=metadata
            )
            file_urls.append(file_url)
        
        return file_urls

    def check_upload_status(self, polling_url: str, polling_jwt: str) -> Dict[str, Any]:
        """
        Check the status of an uploaded file.
        
        Args:
            polling_url: The URL to poll for status updates.
            polling_jwt: The JWT token for authentication.
            
        Returns:
            The response from the polling endpoint.
        """
        self._validate_configuration()
        
        headers = {
            "X-Uploadthing-Api-Key": self.secret_key,
            "Authorization": f"Bearer {polling_jwt}"
        }
        
        try:
            response = requests.get(polling_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking upload status: {str(e)}")
            if hasattr(response, 'text'):
                self.logger.error(f"Response body: {response.text}")
            raise ValueError(f"Error checking upload status: {str(e)}")