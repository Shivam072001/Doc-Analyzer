from langchain_ollama import OllamaLLM
from ..core.interfaces import LLMServiceInterface

class LLMService(LLMServiceInterface):
    def __init__(self, model_name):
        self.llm = OllamaLLM(model=model_name)

    def invoke(self, query: str) -> str:
        return self.llm.invoke(query)