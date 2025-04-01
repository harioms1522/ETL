from src.connectors.connector import Connector

class Migrator:
    # this will be a higher level class that will be used to migrate data from mongodb to sql
    # it will be responsible for:
    # - validating the data
    # - migrating the data
    # - logging the data
    # - reporting the data
    
    # target and source connectors are passed as arguments
    def __init__(self, target_connector: Connector, source_connector: Connector):
        self.target_connector = target_connector
        self.source_connector = source_connector
        self.target_connector.connect()
        self.source_connector.connect()


    def migrate(self, source_table: str, target_table: str, batch_size: int = 1000):
        

        pass
    

    # it will also have a method to validate the data
    # it will also have a method to report the data
    # it will also have a method to log the data
    # it will also have a method to migrate the data
    # it will also have a method to validate the data
    # it will also have a method to report the data
    # it will also have a method to log the data