import os
from typing import Dict, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

console = Console()

def get_default_value(key: str) -> Optional[str]:
    """Get default value for environment variables."""
    defaults = {
        "MONGODB_URI": "mongodb://localhost:27017",
        "SQL_URI": "postgresql://user:password@localhost:5432/db",
        "BATCH_SIZE": "1000",
    }
    return defaults.get(key)

def validate_uri(uri: str, uri_type: str) -> bool:
    """Validate URI format."""
    if uri_type == "mongodb":
        return uri.startswith(("mongodb://", "mongodb+srv://"))
    elif uri_type == "sql":
        return any(uri.startswith(prefix) for prefix in [
            "postgresql://", "mysql://", "sqlite://", "mssql://"
        ])
    return True

def setup_environment() -> Dict[str, str]:
    """Interactive environment setup."""
    console.print(Panel.fit(
        "[bold cyan]ETL Tool Environment Setup[/bold cyan]\n"
        "This will help you configure the essential environment variables.",
        title="Setup Wizard"
    ))
    
    env_vars = {}
    
    # MongoDB URI
    mongodb_uri = Prompt.ask(
        "\n[bold]MongoDB Connection URI[/bold]",
        default=get_default_value("MONGODB_URI"),
        show_default=True
    )
    while not validate_uri(mongodb_uri, "mongodb"):
        console.print("[red]Invalid MongoDB URI format. Please try again.")
        mongodb_uri = Prompt.ask(
            "[bold]MongoDB Connection URI[/bold]",
            default=get_default_value("MONGODB_URI"),
            show_default=True
        )
    env_vars["MONGODB_URI"] = mongodb_uri
    
    # SQL URI
    sql_uri = Prompt.ask(
        "\n[bold]SQL Database Connection URI[/bold]",
        default=get_default_value("SQL_URI"),
        show_default=True
    )
    while not validate_uri(sql_uri, "sql"):
        console.print("[red]Invalid SQL URI format. Please try again.")
        sql_uri = Prompt.ask(
            "[bold]SQL Database Connection URI[/bold]",
            default=get_default_value("SQL_URI"),
            show_default=True
        )
    env_vars["SQL_URI"] = sql_uri
    
    # Batch Size
    batch_size = Prompt.ask(
        "\n[bold]Default Batch Size[/bold]",
        default=get_default_value("BATCH_SIZE"),
        show_default=True
    )
    while not batch_size.isdigit() or int(batch_size) <= 0:
        console.print("[red]Batch size must be a positive number.")
        batch_size = Prompt.ask(
            "[bold]Default Batch Size[/bold]",
            default=get_default_value("BATCH_SIZE"),
            show_default=True
        )
    env_vars["BATCH_SIZE"] = batch_size
    
    # Save to .env file
    if Confirm.ask("\n[bold]Save these settings to .env file?[/bold]"):
        with open(".env", "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        console.print("[green]Settings saved to .env file!")
    
    return env_vars

def load_environment() -> Dict[str, str]:
    """Load environment variables from .env file if it exists."""
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    return env_vars 