# MongoDB to SQL Migration Tool

A command-line tool for migrating data from MongoDB to SQL databases.

## Features

- Migrate data from MongoDB to SQL databases
- Schema analysis and validation
- Support for various SQL databases (PostgreSQL, MySQL, etc.)
- Progress tracking and reporting
- Dry-run capability
- Connection validation
- Schema compatibility checking

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mongodb-to-sql
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

1. Migrate data:
```bash
python src/cli.py migrate --mongodb-uri="mongodb://localhost:27017" --sql-uri="postgresql://user:password@localhost:5432/db" --collection="users" --table="users"
```

2. Validate connections and schema:
```bash
python src/cli.py validate --mongodb-uri="mongodb://localhost:27017" --sql-uri="postgresql://user:password@localhost:5432/db" --collection="users" --table="users"
```

3. Analyze MongoDB schema:
```bash
python src/cli.py schema --mongodb-uri="mongodb://localhost:27017" --collection="users" --output="schema.json"
```

## Usage Examples

### Basic Commands

1. **Validate connections and schema**:
   ```bash
   etl validate --collection my_collection --table my_table
   ```

2. **Analyze schema**:
   ```bash
   etl schema --collection my_collection --output schema.json
   ```

3. **Migrate data**:
   ```bash
   etl migrate --collection my_collection --table my_table --batch-size 1000
   ```

### Chain Commands

Execute multiple commands in sequence:

1. **Basic chain**:
   ```bash
   etl chain validate migrate --collection my_collection --table my_table
   ```

2. **Full chain with all options**:
   ```bash
   etl chain schema validate migrate \
       --collection my_collection \
       --table my_table \
       --mongodb-uri mongodb://localhost:27017 \
       --sql-uri postgresql://user:password@localhost:5432/db \
       --batch-size 1000 \
       --dry-run \
       --output schema.json
   ```

Available commands for chaining:
- `validate`: Check connections and schema compatibility
- `schema`: Analyze MongoDB collection schema
- `migrate`: Transfer data from MongoDB to SQL


### Environment Variables

You can set the following environment variables to avoid typing them in the command line:

- `MONGODB_URI`: MongoDB connection URI
- `SQL_URI`: SQL database connection URI

### Command Options

#### migrate
- `--mongodb-uri`: MongoDB connection URI
- `--sql-uri`: SQL database connection URI
- `--collection`: MongoDB collection to migrate
- `--table`: Target SQL table name
- `--batch-size`: Number of documents to process in each batch (default: 1000)
- `--dry-run`: Perform a dry run without actually migrating data

#### validate
- `--mongodb-uri`: MongoDB connection URI
- `--sql-uri`: SQL database connection URI
- `--collection`: MongoDB collection to validate
- `--table`: Target SQL table to validate

#### schema
- `--mongodb-uri`: MongoDB connection URI
- `--collection`: MongoDB collection to analyze
- `--output`: Output file for schema analysis (JSON format)

## Development

### Project Structure

```
mongodb-to-sql/
├── src/
│   ├── __init__.py
│   ├── cli.py           # CLI interface
│   │   ├── __init__.py
│   │   ├── connectors/
│   │   │   ├── __init__.py
│   │   │   ├── mongodb.py   # MongoDB connector
│   │   │   └── sql.py       # SQL connector
│   │   ├── transformers/
│   │   │   ├── __init__.py
│   │   │   └── schema.py    # Schema transformation logic
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py # Validation utilities
│   ├── tests/
│   ├── requirements.txt
│   ├── setup.py
│   └── README.md
```

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 