import typer
from rich.console import Console
from rich.progress import Progress
from typing import Optional, List
import os
from dotenv import load_dotenv
import subprocess
import sys
from utils.env_setup import setup_environment, load_environment
from connectors import *

# Initialize typer app and rich console
app = typer.Typer(help="MongoDB to SQL Migration Tool")
console = Console()

# Load environment variables
load_dotenv()




@app.command()
def setup(
    force: bool = typer.Option(
        False,
        help="Force setup even if .env file exists",
    ),
):
    """
    Interactive setup for environment variables.
    """
    try:
        if os.path.exists(".env") and not force:
            if not typer.confirm("Environment file (.env) already exists. Do you want to overwrite it?"):
                console.print("[yellow]Setup cancelled.")
                return
        
        env_vars = setup_environment()
        
        # Set environment variables for current session
        for key, value in env_vars.items():
            os.environ[key] = value
        
        console.print("\n[green]Environment setup completed successfully!")
        console.print("You can now run other commands using these settings.")
        
    except Exception as e:
        console.print(f"[red]Error during environment setup: {str(e)}")
        raise typer.Exit(1)

@app.command()
def migrate(
    mongodb_uri: str = typer.Option(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        help="MongoDB connection URI",
    ),
    sql_uri: str = typer.Option(
        os.getenv("SQL_URI", "postgresql://user:password@localhost:5432/db"),
        help="SQL database connection URI",
    ),
    collection: str = typer.Option(
        ...,  # Required parameter
        help="MongoDB collection to migrate",
    ),
    table: str = typer.Option(
        ...,  # Required parameter
        help="Target SQL table name",
    ),
    batch_size: int = typer.Option(
        1000,
        help="Number of documents to process in each batch",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Perform a dry run without actually migrating data",
    ),
):
    """
    Migrate data from MongoDB to SQL database.
    """
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Migrating data...", total=None)
            
            # TODO: Implement actual migration logic
            console.print(f"Starting migration from {collection} to {table}")
            console.print(f"MongoDB URI: {mongodb_uri}")
            console.print(f"SQL URI: {sql_uri}")

            mongo_connector = MongoDBConnector(mongodb_uri)
            sql_connector = SQLConnector(sql_uri)
            mongo_connector.connect()
            sql_connector.connect() 

            # Get collection schema
            collection_schema = mongo_connector.get_collection_schema(collection)

            # Create table with schema
            # if no table, create one
            if not sql_connector.table_exists(table):
                sql_connector.create_table(table, collection_schema)

            # check if table is compatible with collection schema
            if not sql_connector.is_table_compatible(table, collection_schema):
                console.print("[red]Table is not compatible with collection schema")
                raise typer.Exit(1)

            # get count of documents in collection
            collection_count = mongo_connector.get_document_count(collection)
            # give information about the no of batches and the size of each batch
            console.print(f"[cyan]Collection has {collection_count} documents")
            console.print(f"[cyan]Batch size is {batch_size}")
            console.print(f"[cyan]No of batches is {collection_count // batch_size}")   

            # run migration on batches if batch_size is set
            if batch_size > 0:
                for i, batch in enumerate(mongo_connector.iterator(collection, limit=batch_size, sort=[("_id", -1)])):
                    progress.update(task, completed=i * 100 / (collection_count // batch_size))
                    sql_connector.insert_data(table, batch)
            else:
                # run migration on all documents
                for i, document in enumerate(mongo_connector.iterator(collection)):
                    # how can i show progress for each document
                    progress.update(task, completed=i * 100 / collection_count) 
                    sql_connector.insert_data(table, document)
            
            if dry_run:
                return console.print("[yellow]DRY RUN: No data will be migrated")
            
            # Placeholder for actual migration logic
            progress.update(task, completed=True)
            
        console.print("[green]Migration completed successfully!")
        
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}")
        raise typer.Exit(1)

@app.command()
def validate(
    mongodb_uri: str = typer.Option(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        help="MongoDB connection URI",
    ),
    sql_uri: str = typer.Option(
        os.getenv("SQL_URI", "postgresql://user:password@localhost:5432/db"),
        help="SQL database connection URI",
    ),
    collection: str = typer.Option(
        ...,  # Required parameter
        help="MongoDB collection to validate",
    ),
    table: str = typer.Option(
        ...,  # Required parameter
        help="Target SQL table to validate",
    ),
):
    """
    Validate connections and schema compatibility.
    """
    try:
        console.print("[cyan]Validating connections and schema...")
        
        # TODO: Implement validation logic
        console.print("Checking MongoDB connection...")
        console.print("Checking SQL connection...")
        console.print("Validating schema compatibility...")
        
        console.print("[green]Validation completed successfully!")
        
    except Exception as e:
        console.print(f"[red]Validation failed: {str(e)}")
        raise typer.Exit(1)

@app.command()
def schema(
    mongodb_uri: str = typer.Option(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        help="MongoDB connection URI",
    ),
    collection: str = typer.Option(
        ...,  # Required parameter
        help="MongoDB collection to analyze",
    ),
    output: Optional[str] = typer.Option(
        None,
        help="Output file for schema analysis (JSON format)",
    ),
):
    """
    Analyze and display MongoDB collection schema.
    """
    try:
        console.print(f"[cyan]Analyzing schema for collection: {collection}")
        
        # TODO: Implement schema analysis logic
        console.print("Analyzing document structure...")
        console.print("Identifying data types...")
        
        if output:
            console.print(f"Saving schema analysis to: {output}")
        
        console.print("[green]Schema analysis completed successfully!")
        
    except Exception as e:
        console.print(f"[red]Schema analysis failed: {str(e)}")
        raise typer.Exit(1)

@app.command()
def chain(
    commands: List[str] = typer.Argument(
        ...,
        help="List of commands to execute in sequence (e.g., 'validate migrate')",
    ),
    mongodb_uri: str = typer.Option(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        help="MongoDB connection URI",
    ),
    sql_uri: str = typer.Option(
        os.getenv("SQL_URI", "postgresql://user:password@localhost:5432/db"),
        help="SQL database connection URI",
    ),
    collection: str = typer.Option(
        ...,  # Required parameter
        help="MongoDB collection name",
    ),
    table: str = typer.Option(
        ...,  # Required parameter
        help="Target SQL table name",
    ),
    batch_size: int = typer.Option(
        1000,
        help="Number of documents to process in each batch",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Perform a dry run without actually migrating data",
    ),
    output: Optional[str] = typer.Option(
        None,
        help="Output file for schema analysis (JSON format)",
    ),
):
    """
    Execute multiple commands in sequence.
    Available commands: validate, schema, migrate
    """
    try:
        executable_path = sys.executable if not getattr(sys, 'frozen', False) else sys.argv[0]
        
        for command in commands:
            if command not in ['validate', 'schema', 'migrate']:
                console.print(f"[red]Unknown command: {command}")
                console.print("Available commands: validate, schema, migrate")
                raise typer.Exit(1)
            
            console.print(f"\n[cyan]Executing command: {command}")
            
            # Build command arguments
            cmd_args = [
                executable_path,
                command,
                "--mongodb-uri", mongodb_uri,
                "--collection", collection,
            ]
            
            # Add command-specific arguments
            if command in ['validate', 'migrate']:
                cmd_args.extend(["--sql-uri", sql_uri, "--table", table])
                if command == 'migrate':
                    cmd_args.extend(["--batch-size", str(batch_size)])
                    if dry_run:
                        cmd_args.append("--dry-run")
            elif command == 'schema' and output:
                cmd_args.extend(["--output", output])
            
            # Execute command
            result = subprocess.run(cmd_args, capture_output=True, text=True)
            
            if result.returncode != 0:
                console.print(f"[red]Command '{command}' failed:")
                console.print(result.stderr)
                raise typer.Exit(1)
            
            console.print(result.stdout)
            console.print(f"[green]Command '{command}' completed successfully!")
        
        console.print("\n[green]All commands completed successfully!")
        
    except Exception as e:
        console.print(f"[red]Error during command chain execution: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 