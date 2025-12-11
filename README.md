# Langchain Test

A test project for experimenting with LangChain using Ollama to run local models like qwen, deepseek-r1 and llama3.1. The project demonstrates basic chains and attempts at agent implementation with local models.

## Project Overview

The main goal is to understand LangChain chains and eventually implement agents with tools. Currently stuck at the chains phase due to the lack of `bind_tools()` method in the Ollama implementation.

This repository was created following a YouTube tutorial, but adapted to use Ollama instead of OpenAI. The basic chain functionality has been successfully implemented with local models.

## Features

- **Pet Name Generator**: Uses LangChain chains to generate creative pet names based on animal type and color
- **Streamlit UI**: Simple web interface for interacting with the pet name generator
- **Local Model Support**: Works with locally running Ollama models
- **Agent Experimentation**: Initial attempts at creating agents with tools (in progress)

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running on your system
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd langchain-test
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Ollama

- Install Ollama from [https://ollama.ai/](https://ollama.ai/)
- Start the Ollama service:
  ```bash
  ollama serve
  ```
- Pull the required model (deepseek-r1 is used by default):
  ```bash
  ollama pull deepseek-r1
  ```

### 5. Create Environment File (Optional)

Create a `.env` file in the root directory for any environment variables:
```bash
touch .env
```

## Running the Application

### Start the Streamlit App

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Pet Name Generator

1. Select an animal type from the sidebar (cat, dog, hamster, parrot, cow)
2. Enter the color of your pet
3. View the suggested pet names

### Testing Helper Functions

You can test the helper functions independently by running:

```bash
# Test the helper module directly
python langchain_helper.py
```

This allows you to test the core LangChain functionality without the Streamlit interface.

## Testing

Currently, the project doesn't have a formal test suite, but you can test functionality by:

1. **Testing the Helper Functions**:
   ```bash
   python -c "from langchain_helper import generate_pet_names; print(generate_pet_names('cat', 'black'))"
   ```

2. **Testing Agent Functionality** (experimental):
   ```bash
   python -c "from langchain_helper import langchain_agent; langchain_agent()"
   ```

## Current Limitations

- The agent implementation is limited by the lack of `bind_tools()` method in the Ollama implementation
- Tool binding for advanced agent functionality doesn't work as expected
- Currently focused on basic chain operations

## Project Structure

```
langchain-test/
├── main.py                 # Streamlit UI application
├── langchain_helper.py     # Core LangChain functionality
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── .venv/                  # Python virtual environment
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Key Dependencies

- **LangChain**: 1.1.3 (main framework)
- **langchain-ollama**: 1.0.0 (Ollama integration)
- **Streamlit**: 1.52.1 (web UI)
- **Wikipedia**: 1.4.0 (tool for agents)
- **Ollama**: 0.6.1 (local model runner)

## Contributing

This is a learning/experimental project. Feel free to fork and experiment with different models, chains, and agent implementations. 
