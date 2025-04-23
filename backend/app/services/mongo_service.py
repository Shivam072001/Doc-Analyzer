# services/mongo_service.py
from ..config.config import Config
import logging
from bson.objectid import ObjectId
from flask import current_app
from datetime import datetime
from ..models.document_metadata import DocumentMetadata  # Import the DocumentMetadata class

class MongoService:
    def __init__(self, db):
        self.db = db
        self.collection = self.db[Config.MONGO_COLLECTION]

    def insert_document_metadata(self, document_metadata: DocumentMetadata):
        try:
            result = self.collection.insert_one(document_metadata.to_dict())
            return result.inserted_id
        except Exception as e:
            logging.error(f"Error inserting document metadata into MongoDB: {e}")
            return None

    def get_all_documents_metadata(self):
        try:
            metadata_list = list(self.collection.find())
            return [DocumentMetadata.from_dict(data) for data in metadata_list]
        except Exception as e:
            logging.error(f"Error fetching all document metadata from MongoDB: {e}")
            return []

    def get_document_metadata_by_name(self, name: str):
        try:
            data = self.collection.find_one({"name": name})
            if data:
                return DocumentMetadata.from_dict(data)
            return None
        except Exception as e:
            logging.error(f"Error fetching document metadata by name from MongoDB: {e}")
            return None

    def delete_document_metadata_by_name(self, name: str):
        try:
            result = self.collection.delete_one({"name": name})
            return result.deleted_count
        except Exception as e:
            logging.error(f"Error deleting document metadata by name from MongoDB: {e}")
            return None

    def get_document_metadata_by_id(self, doc_id: str):
        try:
            data = self.collection.find_one({"_id": ObjectId(doc_id)})
            if data:
                return DocumentMetadata.from_dict(data)
            return None
        except Exception as e:
            logging.error(f"Error fetching document metadata by ID from MongoDB: {e}")
            return None