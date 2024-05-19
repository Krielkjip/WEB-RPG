# WEB-RPG

## Requirements
- Python 3.12 installed on your system
- Any Browser

## Create a Virtual Environment (python 3.12)

To create a virtual environment, you can use the following commands. Ensure you select the created virtual environment
in your IDE if you're using one.

### General Command

```bash
python -m venv venv
```

### Windows-Specific Command

```bash
python3.12.exe -m venv venv
```

## Activate Virtual Environment

Activate the virtual environment to ensure all dependencies are installed within this isolated environment.

```bash
.\venv\Scripts\activate
```

## Install Dependencies

With the virtual environment activated, install the required dependencies using pip.

```bash
pip install -r requirements.txt
```

## Run the Server

Start the game server by running the following command:

```bash
python game_server.py
```

When the server started you need to go to this link:
http://127.0.0.1:8000

To quit the server press CTRL+C