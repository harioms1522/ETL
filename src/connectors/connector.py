# this is a base class for all connectors
class Connector:
    def __init__(self, uri: str):
        self.uri = uri

    def connect(self):
        pass

    def validate_connection(self):
        pass    

    def disconnect(self):
        pass

    def get_collection(self, collection_name: str):
        pass

    def get_collection_schema(self, collection_name: str):
        pass

    def get_collection_stats(self, collection_name: str):
        pass

    def get_document_count(self, document_count_name: str):
        pass

    def get_sample_documents(self, collection_name: str):
        pass

    def get_data(self, collection_name: str):
        pass 

    def iterator(self, collection_name: str):
        pass    
    
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass    
    
    
    
    
    
