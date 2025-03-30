from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DocumentServiceInterface(ABC):
    @abstractmethod
    def list_pdfs(self) -> List[str]:
        pass

    @abstractmethod
    def upload_pdf(self, file) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_pdf(self, file_name: str) -> None:
        pass

    @abstractmethod
    def clear_pdf_directory(self) -> None:
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
    def get_pdf_usage_percentage(self) -> Dict[str, Dict[str, float]]:
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