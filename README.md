# RAG Retrieval System

## Assignment Context

This project fulfills **Assignment Option #1: Mini RAG with Financial Data** from Qonfido's assessment. The assignment required building a RAG pipeline handling both textual FAQs and quantitative fund data with lexical and semantic retrieval modes.

## What Is Delivered in this REPO:

### Core Requirements ✅
1. **Data Preparation**: Ingested both FAQ and performance datasets, created embeddings for textual data, and converted numerical metrics into searchable text format
2. **Retrieval Modes**: 
   - ✅ Lexical Search (BM25)
   - ✅ Semantic Search (vector embeddings)
3. **Query Handling**: Retrieves relevant context and returns structured responses with sources
4. **Interface**: FastAPI endpoint exposed at `/query` accepting user queries and retrieval method selection

### Bonus Features ✅
- ✅ **Hybrid Search**: Combined lexical + semantic retrieval with weighted scoring
- ✅ **Disk Caching**: Implemented for embeddings and retrieval results

### Additional Enhancements (Beyond Requirements) ⭐✅

To demonstrate end-to-end product thinking and improve evaluation experience, I went beyond the assignment scope:

1. ⭐ **Interactive Frontend**: Built Streamlit UI for real-time query testing without API calls
2. ⭐ **Deployment**: Deployed both backend and frontend for remote access (no local setup needed for reviewers)
3. ⭐ **Advanced Numeric Retrieval**: Added fourth retrieval method specifically optimized for scaled numerical data and rank-based queries (industry best practice)
4. ⭐ **LLM Integration**: Purchased $5 OpenRouter credits to enable smooth LLM-powered answer generation during evaluation (avoids rate limiting issues)

**Note**: These extras were implemented post-assignment to enhance demonstration quality and reviewer experience.

## Project Overview

This system implements a multi-strategy RAG pipeline combining FastAPI backend for document retrieval and Streamlit frontend for interactive querying. The retrieval layer supports lexical (BM25), semantic (vector embeddings), hybrid, and numeric ranking methods.

## Design Rationale

**Backend / Frontend Separation**: Isolates retrieval logic from UI, enabling independent scaling and component replacement.

**Multiple Retrieval Strategies**: Provides flexibility between speed (lexical) and semantic accuracy (embeddings), with hybrid combining both strengths.

**Disk Caching**: Improves performance for repeated queries by caching embeddings and results, reducing redundant computation.

**Interactive UI**: Streamlit frontend allows rapid experimentation with different retrieval strategies and immediate feedback.

## Trade-offs & Assumptions

### Trade-offs

**Accuracy vs Latency**: Semantic/hybrid retrieval produces more relevant results but requires embedding generation and ANN search. Lexical is faster but may miss semantic matches.

**Complexity vs Simplicity**: Supporting multiple strategies increases architectural complexity (more modules, configuration) but provides flexibility for different query types.

**Caching vs Freshness**: Disk caching improves speed but risks returning stale results if underlying data changes.

**General vs Domain-specific**: Built generically for text retrieval rather than heavily tuned for finance domain; domain-specific optimization would increase accuracy but reduce portability.

### Assumptions

- Document corpus is moderate-sized (embedding + indexing feasible in memory/disk)
- Standard embeddings suffice for financial domain; specialized models not required
- Target is exploratory/demo usage, not production-grade high-throughput service
- Ports 8000 (backend) and 8501 (frontend) are available; adjustable if needed
- Documents are appropriately chunked/indexed at startup

## How to Run Locally

### Prerequisites
- Python 3.11.9+
- Git

### Clone Repository

```bash
git clone https://github.com/ihamdaan/qonfido-proj
cd qonfido-proj
```

### Backend Setup

```bash
cd backend-rag
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend available at: **http://localhost:8000**
API access route: **http://localhost:8000/query**

### Frontend Setup (Optional)

```bash
cd frontend-streamlit
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Frontend available at: **http://localhost:8501**

## Usage

**Via API**: Send POST requests to `http://localhost:8000/query` with query text and retrieval method (lexical/semantic/hybrid/numeric)

**Via UI**: Select retrieval method, enter query, view retrieved documents and generated answer

## Limitations & Future Considerations

- Single-query handling; high-traffic systems need batching, async retrieval, and optimized indices
- Embedding generation may bottleneck with significantly larger corpora; requires advanced ANN structures
- Frontend optimized for experimentation, not production (lacks authentication, logging, rate-limiting, etc)
- No domain-specific fine-tuning or re-ranking; critical applications (like: financial domain) need cross-encoder reranking and provenance tracking

## Summary

This repository implements a flexible, multi-strategy RAG system fulfilling all core assignment requirements plus bonus features. The design prioritizes flexibility and experimentation over production optimization. Additional enhancements (frontend, deployment, numeric retrieval, LLM credits) demonstrate end-to-end PRD and practical system design.

Production deployment at scale would require: advanced indexing, latency optimization, domain-specific tuning, and system hardening (authentication, monitoring, error handling).