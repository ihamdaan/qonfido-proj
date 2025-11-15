# RAG Retrieval System

A Retrieval-Augmented Generation (RAG) system with multiple search strategies and an interactive Streamlit frontend.

## Project Structure

```
.
├── backend-rag/           # FastAPI backend with retrieval methods
└── frontend-streamlit/    # Streamlit web interface
```

## Features

The backend implements **3 major retrieval methods + 1 additional retrieval method**:

1. **Lexical Search** - Traditional keyword-based retrieval using BM25
2. **Semantic Search** - Vector-based similarity search using embeddings
3. **Hybrid Search** - Combines lexical and semantic approaches for optimal results
4. **Numeric Search** - Rank-based queries for scaled numerical data (industry best practice, not in assignment requirements)

*Note: Disk caching is implemented for improved performance.*

## Setup Instructions

### Prerequisites
- Python 3.11.9
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

OR

DOWNLOAD IT DIRECTLY FROM THE REPO LINK

### 2. Backend Setup

#### macOS/Linux

```bash
cd backend-rag

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload
```

#### Windows

```bash
cd backend-rag

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload
```

The backend will run on **http://localhost:8000**

### 3. Frontend Setup

Open a **new terminal window** and navigate to the project root:

#### macOS/Linux

```bash
cd frontend-streamlit

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

#### Windows

```bash
cd frontend-streamlit

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

The frontend will run on **http://localhost:8501**

## Usage

1. Ensure the backend is running (http://localhost:8000)
2. Open the Streamlit interface (http://localhost:8501)
3. Select your preferred retrieval method
4. Enter your query and view results

## API Documentation

Once the backend is running, visit **http://localhost:8000/query** for interactive API route.

## Deactivating Virtual Environments

When done, deactivate the virtual environment in each terminal:

```bash
deactivate
```

## Troubleshooting

- **Port conflicts**: If ports 8000 or 8501 are in use, modify the port numbers in the run commands
- **Connection errors**: Ensure the backend is running before starting the frontend
- **Module not found**: Verify you've activated the virtual environment and installed requirements

---

*For issues or contributions, please open an issue or pull request.*