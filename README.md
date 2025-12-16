# 🚀 Import–Export Compliance Assistant (RAG-Based AI System)

This project is a full-stack **Retrieval-Augmented Generation (RAG)** application designed to answer import–export compliance questions using *verified policy documents only*. It delivers structured, hallucination-free answers and provides source references for every response.

Built by **Rohith G** and **Sharan Raj J**.

---

## ✨ Features

### 🔍 Retrieval-Augmented Generation (RAG)
- Vector search (SentenceTransformer: MiniLM-L6-v2)
- BM25 keyword matching
- Cross‑encoder reranking for high-precision relevance
- Merges, filters, and deduplicates document chunks

### 🤖 LLM Layer (Safe + Structured)
- Strict prompt rules to prevent hallucination  
- Answers **ONLY** using provided context  
- Rejects unsupported queries gracefully  
- Enforces structured output:
  - **Overview**
  - **Key Requirements**
  - **Procedure**
  - **Notes**

### ⚙️ Backend (FastAPI)
- `/chat` endpoint for answering queries
- RAG + LLM integration
- Metadata cleaning & source mapping
- Clean modular architecture

### 💬 Frontend (Custom Chat UI)
- Dark‑theme chat interface (HTML, CSS, JS)
- Loading animation (`•••`)
- Markdown-compatible message formatting
- Source cards with file name + category
- Enter‑key submit support

---

## 🏗️ Project Architecture

User Query → FastAPI → RAG Retrieval (Vector + BM25 + Reranking)
↓
Context Sent to LLM (Strict Prompting)
↓
Structured Answer + Sources Returned
↓
Frontend Renders Chat Output

yaml
Copy code

---

## 📦 Tech Stack

### Backend
- Python
- FastAPI
- ChromaDB (Persistent Vector Store)
- SentenceTransformer (MiniLM)
- Rank-BM25
- Cross Encoder (Reranking)
- Custom Prompt Engineering

### Frontend
- HTML / CSS / JavaScript
- Fetch API
- Responsive chat UI

---

## 📁 Folder Structure

backend/
│── main.py # FastAPI app + LLM prompt
│── rag.py # RAG pipeline (vector search + BM25 + rerank)
│── formatter.py # Cleans and structures LLM answers
│── llm.py # LLM wrapper
│── chroma_db/ # Vector store
frontend/
│── index.html # Chat UI
│── styles.css # Styling (dark theme)
│── script.js # API interaction

yaml
Copy code

---

## ▶️ Running the Project

### 1️⃣ Start Backend
```bash
cd backend
uvicorn main:app --reload
2️⃣ Open Frontend
Open index.html directly in your browser.

🧪 Example Queries
What documents are required for exporting goods from India?

What is an End-User Certificate (EUC)?

What post-shipment reporting is required under GAEIS?

Are there restrictions on exporting to UNSC-sanctioned destinations?

🧠 Key Highlights
Zero‑hallucination design

Highly controlled, enterprise‑grade prompt

Proper metadata usage and deduplication

Beautiful, intuitive UI

Real‑world application: compliance automation

👨‍💻 Contributors
Rohith G

Sharan

🌐 Portfolio
https://rohith-g-portfolio.netlify.app
