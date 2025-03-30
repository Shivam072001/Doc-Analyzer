from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from ..core.interfaces import VectorStoreServiceInterface
from ..config.config import Config
from .llm_service import LLMService
from .stats_service import StatsService
import os
import logging

llm_service = LLMService(Config.OLLAMA_MODEL)
stats_service = StatsService()

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

    def query_vector_store(self, query: str, prompt) -> dict:
        if self.vector_store is None:
            return {"answer": "Vector store not initialized."}

        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": self.search_k,
                "score_threshold": self.score_threshold,
            },
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
            logging.error(f"Error deleting document by ID: {e}")

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