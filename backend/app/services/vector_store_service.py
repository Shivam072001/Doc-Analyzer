from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from ..core.interfaces import VectorStoreServiceInterface
from ..config.config import Config
from .llm_service import LLMService
from .stats_service import StatsService
from .prompt_service import PromptService  # Import PromptService
import os
import logging
from typing import Optional, List
import random

llm_service = LLMService(Config.OLLAMA_MODEL)
stats_service = StatsService()
prompt_service = PromptService() # Instantiate PromptService

class VectorStoreService(VectorStoreServiceInterface):
    _instance = None

    def __new__(cls, db_folder=None, chunk_size=None, chunk_overlap=None, score_threshold=None, search_k=None):
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            cls._instance.db_folder = db_folder or Config.DB_FOLDER
            cls._instance.chunk_size = chunk_size or Config.CHUNK_SIZE
            cls._instance.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
            cls._instance.score_threshold = score_threshold or Config.SCORE_THRESHOLD
            cls._instance.search_k = search_k or Config.SEARCH_K
            cls._instance.embedding = FastEmbedEmbeddings()
            cls._instance.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=cls._instance.chunk_size,
                chunk_overlap=cls._instance.chunk_overlap,
                length_function=len,
                is_separator_regex=False
            )
            cls._instance.vector_store = cls._instance._initialize_vector_store()
        return cls._instance

    def _initialize_vector_store(self):
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
            logging.info(f"Created vector store directory: {self.db_folder}")
        try:
            vector_store = Chroma(persist_directory=self.db_folder, embedding_function=self.embedding)
            if not vector_store.get():
                logging.info("Vector store is empty or not properly initialized.")
            return vector_store
        except Exception as e:
            logging.error(f"Error initializing vector store: {e}")
            return None

    def initialize_vector_store(self) -> None:
        self.vector_store = self._initialize_vector_store()

    def add_documents(self, documents, source: str) -> None:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        chunks = self.text_splitter.split_documents(documents)
        for chunk in chunks:
            chunk.metadata = {"source": source}
        try:
            Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_folder)
            # Re-initialize the vector store to pick up the new documents
            self.vector_store = Chroma(persist_directory=self.db_folder, embedding_function=self.embedding)
            logging.info(f"Added {len(chunks)} chunks from {source} to vector store.")
        except Exception as e:
            logging.error(f"Error adding documents to vector store: {e}")

    def query_vector_store(self, query: str, prompt, selected_files: Optional[List[str]] = None) -> dict:
        if self.vector_store is None:
            return {"answer": "Vector store not initialized."}

        search_kwargs = {
            "k": self.search_k,
            "score_threshold": self.score_threshold,
        }

        if selected_files:
            search_kwargs["where"] = {"source": {"$in": selected_files}}

        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs=search_kwargs,
        )

        retriever_prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                (
                    "human",
                    "Given the above conversation, generate a search query to lookup in order to get information relevant to the conversation",
                ),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm=llm_service.llm, retriever=retriever, prompt=retriever_prompt
        )
        document_chain = create_stuff_documents_chain(LLMService(Config.OLLAMA_MODEL).llm, prompt)
        retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

        # Assuming chat_history is managed by the stats service
        chat_history = stats_service.get_chat_history()
        result = retrieval_chain.invoke({"input": query, "chat_history": chat_history})
        return result

    def delete_documents_by_source(self, source: str) -> None:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        try:
            db_data = self.vector_store.get()
            metadatas = db_data.get("metadatas", [])
            ids = db_data.get("ids", [])
            docs_to_delete = [id for id, metadata in zip(ids, metadatas) if metadata.get("source", "").strip().lower() == source.strip().lower()]
            if docs_to_delete:
                self.vector_store.delete(docs_to_delete)
                self.vector_store.persist()
                logging.info(f"Deleted {len(docs_to_delete)} documents with source: {source}")
            else:
                logging.info(f"No documents found for source: {source}")
        except Exception as e:
            logging.error(f"Error deleting documents by source: {e}")

    def delete_document_by_id(self, doc_id: str) -> None:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        try:
            self.vector_store.delete([doc_id])
            self.vector_store.persist()
            logging.info(f"Deleted document with ID: {doc_id}")
        except Exception as e:
            logging.error(f"Error deleting document by ID: {doc_id}")

    def clear_vector_store(self) -> None:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        try:
            db_data = self.vector_store.get()
            ids = db_data.get("ids", [])
            if ids:
                self.vector_store.delete(ids)
                self.vector_store.persist()
                logging.info("Successfully deleted all documents from vector store.")
            else:
                logging.info("No documents found in vector store to delete.")
        except Exception as e:
            logging.error(f"Error clearing vector store: {e}")

    def list_documents(self) -> list[dict[str, str]]:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        try:
            db_data = self.vector_store.get()
            metadatas = db_data.get("metadatas", [])
            documents = [{"source": metadata.get("source", "Unknown")} for metadata in metadatas]
            return documents
        except Exception as e:
            logging.error(f"Error listing documents: {e}")
            return []

    def get_document_count(self) -> int:
        if self.vector_store is None:
            self.vector_store = self._initialize_vector_store()
        try:
            db_data = self.vector_store.get()
            return len(db_data.get("metadatas", []))
        except Exception as e:
            logging.error(f"Error getting document count: {e}")
            return 0

    def generate_suggestive_questions(self, prompt_type: str, selected_files: Optional[List[str]] = None, num_questions: int = 5) -> List[str]:
        if self.vector_store is None:
            logging.warning("Vector store not initialized, cannot generate suggestive questions.")
            return []

        prompt = prompt_service.get_prompt(prompt_type)
        if not prompt:
            logging.warning(f"Prompt type '{prompt_type}' not found, cannot generate suggestive questions.")
            return []

        all_documents_data = self.vector_store.get()
        if not all_documents_data or not all_documents_data.get('ids'):
            logging.info("No documents in vector store to generate suggestive questions from.")
            return []

        document_texts = all_documents_data.get('documents', [])
        metadatas = all_documents_data.get('metadatas', [])

        filtered_document_texts = []
        if selected_files:
            for text, metadata in zip(document_texts, metadatas):
                if metadata and metadata.get('source') in selected_files:
                    filtered_document_texts.append(text)
            if not filtered_document_texts:
                logging.info("No documents found matching the selected files for question generation.")
                return []
        else:
            filtered_document_texts = document_texts

        sample_size = min(num_questions, len(filtered_document_texts))
        if not filtered_document_texts:
            return []
        sampled_documents = random.sample(filtered_document_texts, sample_size)

        question_generation_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an AI that generates suggestive questions based on document content and a given prompt style."),
            ("human", """Generate {num_questions} potential questions that a user might ask about the following document content, keeping in mind the style and focus of the '{prompt_type}' prompt:

            Document Content:
            {document_content}

            Prompt Style:
            {prompt_style}

            Questions:"""),
        ])

        generated_questions = []
        for doc_content in sampled_documents:
            question_generation_prompt = question_generation_prompt_template.format_messages(
                num_questions=1, # Generate one question per document sample
                document_content=doc_content,
                prompt_style=prompt.template, # Assuming prompt has a 'template' attribute
                prompt_type=prompt_type
            )
            try:
                response = llm_service.invoke(question_generation_prompt[0].content)
                # Basic splitting of response into lines, removing empty ones
                questions = [q.strip() for q in response.strip().split('\n') if q.strip()]
                generated_questions.extend(questions)
            except Exception as e:
                logging.error(f"Error generating suggestive questions: {e}")

        return generated_questions[:num_questions] # Return up to the requested number of questions