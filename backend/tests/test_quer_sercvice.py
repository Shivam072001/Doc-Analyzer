import pytest
from unittest.mock import MagicMock
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService
from app.services.prompt_service import PromptService
from app.services.stats_service import StatsService
from app.config.config import Config

@pytest.fixture
def mock_llm_service():
    mock = MagicMock(spec=LLMService)
    mock.invoke.return_value = "Mocked LLM response"
    return mock

@pytest.fixture
def mock_vector_store_service():
    mock = MagicMock(spec=VectorStoreService)
    mock.query_vector_store.return_value = {"answer": "Mocked vector store response", "context": []}
    return mock

@pytest.fixture
def prompt_service():
    return PromptService()

@pytest.fixture
def stats_service():
    return StatsService()

def test_llm_service_invoke(mock_llm_service):
    query = "What is the meaning of life?"
    response = mock_llm_service.invoke(query)
    assert response == "Mocked LLM response"
    mock_llm_service.invoke.assert_called_once_with(query)

def test_vector_store_service_query(mock_vector_store_service, prompt_service):
    query = "Ask about a document"
    prompt_type = "qa"
    prompt = prompt_service.get_prompt(prompt_type)
    response = mock_vector_store_service.query_vector_store(query, prompt)
    assert response["answer"] == "Mocked vector store response"
    mock_vector_store_service.query_vector_store.assert_called_once_with(query, prompt)