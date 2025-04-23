import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from datetime import datetime
from ...config.config import Config  # Assuming you have a Config class


class DocumentDetailModel:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]
        self.document_details_collection = self.db['document_details']

    def insert_document_detail(self, name: str, size: int, upload_date: datetime, file_type: str, url: str):
        document_detail = {
            "name": name,
            "size": size,
            "upload_date": upload_date,
            "type": file_type,
            "url": url,
            "user_id": None,
            "category": None,
            "sub_category": None
        }
        result = self.document_details_collection.insert_one(document_detail)
        return str(result.inserted_id)  # Return the string representation of ObjectId

    def delete_document_detail_by_id(self, document_id: str):
        try:
            object_id = ObjectId(document_id)
            result = self.document_details_collection.delete_one({"_id": object_id})
            return result.deleted_count
        except Exception as e:
            logging.error(f"Error deleting document detail with ID {document_id}: {e}")
            return 0

    def get_document_detail_by_id(self, document_id: str):
        try:
            object_id = ObjectId(document_id)
            detail = self.document_details_collection.find_one({"_id": object_id})
            if detail:
                detail['_id'] = str(detail['_id'])
            return detail
        except Exception as e:
            logging.error(f"Error getting document detail with ID {document_id}: {e}")
            return None

    def list_document_details(self) -> list[dict]:
        """Lists all document details from the MongoDB collection, converting ObjectId to string."""
        details = list(self.document_details_collection.find({}, {'_id': True, 'name': True, 'size': True, 'upload_date': True, 'type': True, 'url': True, 'user_id': True, 'category': True, 'sub_category': True}))
        for detail in details:
            detail['_id'] = str(detail['_id'])
        return details
    
    def clear_db(self):
        """Clears all data from the MongoDB database used by the application."""
        try:
            delete_result = self.document_details_collection.delete_many({})
            logging.info(f"Successfully cleared {delete_result.deleted_count} documents from the 'document_details' collection.")

            # You can add logic here to clear other collections if needed

            print(f"Successfully cleared the MongoDB database '{Config.MONGO_DB_NAME}'.")

        except Exception as e:
            logging.error(f"Error clearing the MongoDB database: {e}")
            print(f"An error occurred while clearing the MongoDB database: {e}")
        finally:
            if 'client' in locals() and client:
                client.close()