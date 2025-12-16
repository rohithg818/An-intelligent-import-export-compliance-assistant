# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag import retrieve_context
from formatter import format_enterprise_answer
from llm import call_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.get("/")
def root():
    return {"status": "Import–Export Compliance Assistant Running"}

@app.post("/chat")
async def chat(payload: dict):
    query = payload.get("query", "").strip()

    if not query:
        return {"answer": "Please provide a valid query."}

    # ---- RAG retrieval ----
    rag_output = retrieve_context(query)
    context_docs = rag_output["documents"]
    meta_list    = rag_output["metadatas"]

    formatted_context = "\n\n".join(context_docs)

    # ---- FIXED LLM PROMPT (CORRECT INDENTATION + STRUCTURE) ----
    prompt = f"""
You are an Import–Export Compliance Assistant.

STRICT RULES:
1. Use ONLY the information present in the provided context.
2. If the context does NOT contain relevant information, reply exactly:
   "No relevant information found in the provided documents."
3. NEVER add, guess, or assume laws or procedures not found in the context.
4. NEVER mix import-only terms into export answers or vice‑versa.
5. Use ONLY the sections that contain real information from the context.

FORMAT RULES (MANDATORY):
- Each section MUST start on a new line.
- Section titles MUST be exactly:

**Overview**
1. ...

**Key Requirements**
1. ...

**Procedure**
1. ...

**Notes**
- ...

- Only include sections supported by context.
- NEVER merge multiple sections into a single paragraph.

Context:
{formatted_context}

Question:
{query}

Your structured answer:
"""

    # ---- LLM call ----
    llm_answer = call_llm(prompt)

    # ---- Final formatted response ----
    final_answer, cleaned_sources = format_enterprise_answer(
        query, llm_answer, meta_list
    )

    return {
        "query": query,
        "answer": final_answer,
        "sources": cleaned_sources
    }
