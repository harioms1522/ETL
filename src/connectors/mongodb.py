from typing import Dict, List, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

class MongoDBConnector:
    def __init__(self, uri: str):
        """Initialize MongoDB connection."""
        self.uri = uri
        self.client: Optional[MongoClient] = None
        self.db = None

    def connect(self) -> bool:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            # Verify connection
            self.client.admin.command('ping')
            return True
        except ConnectionFailure as e:
            console.print(f"[red]Failed to connect to MongoDB: {str(e)}")
            return False

    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()

    def get_collection(self, collection_name: str):
        """Get MongoDB collection."""
        if not self.client:
            raise ConnectionError("MongoDB connection not established")
        
        # Extract database name from URI or use default
        db_name = self.uri.split('/')[-1].split('?')[0] if '/' in self.uri else 'test'
        self.db = self.client[db_name]
        return self.db[collection_name]

    def get_collection_schema(self, collection_name: str) -> Dict[str, Any]:
        """Analyze collection schema."""
        collection = self.get_collection(collection_name)
        schema = {}
        
        # Sample documents to analyze schema
        sample_docs = collection.find().sort([('_id', -1)]).limit(100)
        
        for doc in sample_docs:
            for field, value in doc.items():
                if field not in schema:
                    schema[field] = {
                        'type': type(value).__name__,
                        'required': True,
                        'unique_values': set()
                    }
                schema[field]['unique_values'].add(str(value))
        
        # Convert sets to lists for JSON serialization
        for field in schema:
            schema[field]['unique_values'] = list(schema[field]['unique_values'])
        
        return schema

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get collection statistics."""
        collection = self.get_collection(collection_name)
        return collection.stats()

    def validate_connection(self) -> bool:
        """Validate MongoDB connection."""
        try:
            if not self.client:
                return self.connect()
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False

    def get_document_count(self, collection_name: str) -> int:
        """Get total document count in collection."""
        collection = self.get_collection(collection_name)
        return collection.count_documents({})

    def get_sample_documents(self, collection_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample documents from collection."""
        collection = self.get_collection(collection_name)
        return list(collection.find().limit(limit))

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect() 