from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
from ..core.interfaces import StatsServiceInterface

class StatsService(StatsServiceInterface):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatsService, cls).__new__(cls)
            cls._instance.pdf_usage_count = {}
            cls._instance.query_usage_count = {}
            cls._instance.chat_history = []
        return cls._instance

    def get_chat_history(self):
        return self.chat_history

    def update_usage_counts(self, documents: List) -> None:
        for doc in documents:
            pdf_source = doc.metadata.get("source")
            if pdf_source:
                self.pdf_usage_count[pdf_source] = self.pdf_usage_count.get(pdf_source, 0) + 1
                self.query_usage_count[pdf_source] = self.query_usage_count.get(pdf_source, 0) + 1

    def get_pdf_usage_percentage(self) -> Dict[str, Dict[str, float]]:
        total_queries = sum(self.pdf_usage_count.values())
        return {
            pdf: {
                "count": count,
                "percentage": (count / total_queries * 100) if total_queries > 0 else 0,
            }
            for pdf, count in self.pdf_usage_count.items()
        }

    def get_query_usage_percentage(self) -> Dict[str, Dict[str, float]]:
        total_queries = sum(self.query_usage_count.values())
        return {
            pdf: {
                "count": count,
                "percentage": (count / total_queries * 100) if total_queries > 0 else 0,
            }
            for pdf, count in self.query_usage_count.items()
        }

    def create_context_with_metadata(self, documents: List) -> List[Dict[str, str]]:
        contexts = []
        for doc in documents:
            metadata = doc.metadata
            contexts.append({
                "source": metadata.get("source", "Unknown"),
                "page_content": doc.page_content
            })
        return contexts

    def clear_chat_history(self) -> None:
        self.chat_history = []

    def update_chat_history(self, human_message: str, ai_message: str) -> None:
        self.chat_history.append(HumanMessage(content=human_message))
        self.chat_history.append(AIMessage(content=ai_message))