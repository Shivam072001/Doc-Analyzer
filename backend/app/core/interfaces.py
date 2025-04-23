from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DocumentServiceInterface(ABC):
    @abstractmethod
    def list_documents(self, file_type: str) -> List[str]:
        """Lists documents of a specific type."""
        pass
    
    def list_document_details(self) -> list[dict]:
        """
        Lists details of all documents of a specific type.

        Args:
            file_type (str): The type of the documents to list (e.g., "pdf", "docx", "csv", "xlsx").

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a document
                            and contains the following keys:
                - "file_name" (str): The name of the file without the extension.
                - "file_size" (int): The size of the file in bytes.
                - "file_type" (str): The file extension (e.g., "pdf", "docx").
                - "upload_date" (str): The last modification timestamp of the file in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM or YYYY-MM-DDTHH:MM:SSZ).
                            Returns an empty list if the directory for the given file type
                            does not exist or is empty.
        """
    pass

    @abstractmethod
    def upload_document(self, file) -> Dict[str, Any]:
        """Uploads a document of any supported type."""
        pass

    @abstractmethod
    def delete_document(self, file_name: str, file_type: str) -> None:
        """Deletes a specific document."""
        pass

    @abstractmethod
    def get_document_dir(self, file_type: str) -> Optional[str]:
        """Gets the directory for a specific document type."""
        pass

    @abstractmethod
    def clear_document_directory(self, file_type: str) -> None:
        """Clears the directory for a specific document type."""
        pass

class LLMServiceInterface(ABC):
    @abstractmethod
    def invoke(self, query: str) -> str:
        pass

class VectorStoreServiceInterface(ABC):
    @abstractmethod
    def initialize_vector_store(self) -> None:
        pass

    @abstractmethod
    def add_documents(self, documents: List, source: str) -> None:
        pass

    @abstractmethod
    def query_vector_store(self, query: str, prompt: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_documents_by_source(self, source: str) -> None:
        pass

    @abstractmethod
    def delete_document_by_id(self, doc_id: str) -> None:
        pass

    @abstractmethod
    def clear_vector_store(self) -> None:
        pass

    @abstractmethod
    def list_documents(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_document_count(self) -> int:
        pass

class PromptServiceInterface(ABC):
    @abstractmethod
    def get_prompt(self, prompt_type: str):
        pass

    @abstractmethod
    def get_serializable_prompts(self) -> Dict[str, str]:
        pass

class StatsServiceInterface(ABC):
    @abstractmethod
    def update_usage_counts(self, documents: List) -> None:
        pass

    @abstractmethod
    def get_document_usage_percentage(self) -> Dict[str, Dict[str, float]]:
        pass

    @abstractmethod
    def get_query_usage_percentage(self) -> Dict[str, Dict[str, float]]:
        pass

    @abstractmethod
    def create_context_with_metadata(self, documents: List) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def clear_chat_history(self) -> None:
        pass

    @abstractmethod
    def update_chat_history(self, human_message: str, ai_message: str) -> None:
        pass