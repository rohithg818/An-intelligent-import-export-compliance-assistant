# Import–Export Compliance Assistant (RAG-Based AI System)

A full-stack Retrieval-Augmented Generation (RAG) system designed to answer import–export compliance questions using verified policy documents only. The system produces structured, citation-backed responses and avoids hallucinations by enforcing strict context usage.

Built by Rohith G and Sharan Raj J.

---

## Demo
LinkedIn demo post:  
https://www.linkedin.com/posts/rohith-gopi-a26223353_ai-machinelearning-chromeextension-activity-7406387202022232066-CzWq

Portfolio:  
https://rohith-g-portfolio.netlify.app

---

## Problem
Import–export regulations are complex, fragmented across multiple policy documents, and difficult to query reliably. Traditional LLM-based chatbots often hallucinate or provide unverified answers, which is unacceptable for compliance-critical use cases.

---

## Solution
This project implements a controlled RAG pipeline that retrieves information strictly from verified policy documents and generates structured, source-backed responses. Unsupported queries are rejected gracefully to maintain reliability.

---

## Key Capabilities

### Retrieval-Augmented Generation (RAG)
- Dense vector search using SentenceTransformer (MiniLM-L6-v2)
- BM25 keyword-based retrieval
- Cross-encoder reranking for high-precision relevance
- Chunk merging, filtering, and deduplication

### LLM Layer (Controlled & Safe)
- Strict prompting to prevent hallucinations
- Responses generated only from retrieved context
- Unsupported queries are explicitly rejected
- Structured output format:
  - Overview
  - Key Requirements
  - Procedure
  - Notes

### Backend
- FastAPI-based API
- `/chat` endpoint for compliance queries
- Modular RAG pipeline integration
- Metadata cleaning and source mapping

### Frontend
- Custom chat UI built with HTML, CSS, and JavaScript
- Dark theme interface
- Loading indicator during response generation
- Markdown-compatible rendering
- Source cards displaying document name and category
- Keyboard-friendly input handling

---

## System Flow

User Query  
→ FastAPI Backend  
→ RAG Retrieval (Vector Search + BM25 + Reranking)  
→ Context sent to LLM (strict prompting)  
→ Structured answer with sources  
→ Frontend renders response  

---

## Tech Stack

### Backend
- Python
- FastAPI
- ChromaDB (persistent vector store)
- SentenceTransformer (MiniLM)
- Rank-BM25
- Cross-encoder reranker
- Custom prompt templates

### Frontend
- HTML, CSS, JavaScript
- Fetch API
- Responsive chat interface

---

## Project Structure

backend/
├── main.py # FastAPI app and request handling
├── rag.py # RAG pipeline (vector search, BM25, reranking)
├── formatter.py # Structured response formatting
├── llm.py # LLM wrapper
├── chroma_db/ # Persistent vector store

frontend/
├── index.html # Chat UI
├── styles.css # Dark theme styling
├── script.js # API interaction

yaml
Copy code

---

## Running the Project

### Start the backend
```bash
cd backend
uvicorn main:app --reload
Run the frontend
Open index.html directly in a browser.

Example Queries
What documents are required for exporting goods from India?

What is an End-User Certificate (EUC)?

What post-shipment reporting is required under GAEIS?

Are there restrictions on exporting to UN-sanctioned destinations?

Highlights
Hallucination-resistant design

Controlled, compliance-oriented prompting

Source-backed answers with metadata

Real-world regulatory use case

Clean, usable interface

Contributors
Rohith G

Sharan Raj J
