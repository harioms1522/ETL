from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

class SQLConnector:
    def __init__(self, uri: str):
        """Initialize SQL connection."""
        self.uri = uri
        self.engine = None
        self.inspector = None

    def connect(self) -> bool:
        """Establish connection to SQL database."""
        try:
            self.engine = create_engine(self.uri)
            # Verify connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.inspector = inspect(self.engine)
            return True
        except SQLAlchemyError as e:
            console.print(f"[red]Failed to connect to SQL database: {str(e)}")
            return False

    def disconnect(self):
        """Close SQL connection."""
        if self.engine:
            self.engine.dispose()

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get table schema information."""
        if not self.inspector:
            raise ConnectionError("SQL connection not established")

        schema = {}
        
        # Get columns
        columns = self.inspector.get_columns(table_name)
        for column in columns:
            schema[column['name']] = {
                'type': str(column['type']),
                'nullable': column.get('nullable', True),
                'default': str(column.get('default', '')),
                'primary_key': column.get('primary_key', False)
            }
        
        # Get primary keys
        pk_constraint = self.inspector.get_pk_constraint(table_name)
        if pk_constraint['constrained_columns']:
            for col in pk_constraint['constrained_columns']:
                schema[col]['primary_key'] = True
        
        # Get foreign keys
        fk_constraints = self.inspector.get_foreign_keys(table_name)
        for fk in fk_constraints:
            for col in fk['constrained_columns']:
                if col in schema:
                    schema[col]['foreign_key'] = {
                        'referred_table': fk['referred_table'],
                        'referred_column': fk['referred_columns'][0]
                    }
        
        return schema

    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Get table statistics."""
        if not self.engine:
            raise ConnectionError("SQL connection not established")

        stats = {}
        
        # Get row count
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            stats['row_count'] = result.scalar()
            
            # Get table size (if supported by the database)
            try:
                result = conn.execute(text(f"SELECT pg_total_relation_size('{table_name}')"))
                stats['size_bytes'] = result.scalar()
            except:
                pass
        
        return stats

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists."""
        if not self.inspector:
            raise ConnectionError("SQL connection not established")
        return self.inspector.has_table(table_name)

    def is_table_compatible(self, table_name: str, collection_schema: Dict[str, Any]) -> bool:
        """Check if table is compatible with collection schema."""
        table_schema = self.get_table_schema(table_name)
        # check if table schema is a subset of collection schema
        return all(col in collection_schema for col in table_schema)
        # return table_schema == collection_schema

    def validate_connection(self) -> bool:
        """Validate SQL connection."""
        try:
            if not self.engine:
                return self.connect()
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False

    def get_sample_rows(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample rows from table."""
        if not self.engine:
            raise ConnectionError("SQL connection not established")

        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
            return [dict(row) for row in result]

    def create_table(self, table_name: str, schema: Dict[str, Any]) -> bool:
        """Create table with given schema."""
        if not self.engine:
            raise ConnectionError("SQL connection not established")

        try:
            # Generate CREATE TABLE statement
            columns = []
            for col_name, col_info in schema.items():
                col_def = f"{col_name} {col_info['type']}"
                if not col_info.get('nullable', True):
                    col_def += " NOT NULL"
                if col_info.get('primary_key', False):
                    col_def += " PRIMARY KEY"
                columns.append(col_def)

            create_stmt = f"CREATE TABLE {table_name} ({', '.join(columns)})"
            
            with self.engine.connect() as conn:
                conn.execute(text(create_stmt))
                conn.commit()
            return True
        except SQLAlchemyError as e:
            console.print(f"[red]Failed to create table: {str(e)}")
            return False

    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> bool:
        """Insert data into table."""
        if not self.engine:
            raise ConnectionError("SQL connection not established")

        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES ({', '.join([f':{key}' for key in data[0].keys()])})"))
                conn.commit()
            return True
        except SQLAlchemyError as e:
            console.print(f"[red]Failed to insert data: {str(e)}")
            return False

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect() 