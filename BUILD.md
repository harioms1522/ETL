# Building the ETL Executable

This guide explains how to create a standalone executable for the ETL tool.

## Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)

## Step-by-Step Build Instructions

1. **Set up the virtual environment** (if not already done):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Create the executable**:
   ```bash
   pyinstaller --onefile src/cli.py --name etl
   ```

The executable will be created in the `dist` directory as:
- Windows: `dist/etl.exe`
- Linux/Mac: `dist/etl`

## Additional Build Options

### Add an Icon
To add a custom icon to the executable:
```bash
pyinstaller --onefile --icon=path/to/icon.ico src/cli.py --name etl
```

### Hide Console Window
If you don't want the console window to appear:
```bash
pyinstaller --onefile --noconsole src/cli.py --name etl
```

### Include Additional Data Files
If your application needs access to additional files:
```bash
pyinstaller --onefile --add-data "path/to/file;destination/in/executable" src/cli.py --name etl
```

## Troubleshooting

1. **Missing Dependencies**
   - If you encounter missing module errors, ensure all dependencies are listed in `requirements.txt`
   - Rebuild after updating dependencies

2. **File Not Found Errors**
   - Make sure all required files are included using `--add-data`
   - Check file paths in your code are relative to the executable location

3. **Large Executable Size**
   - This is normal for PyInstaller executables as they include Python runtime
   - Use `--exclude-module` to remove unnecessary modules

## Distribution

The executable in the `dist` directory can be distributed to users who don't have Python installed.
- Windows users can run `etl.exe` directly
- Linux/Mac users may need to make the file executable first: `chmod +x etl` 