# backend/rag.py

import re
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from reranker import cross_encoder_rerank


# ─────────────────────────────────────────────
# Load SAME embedding model used in DB creation
# ─────────────────────────────────────────────
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ─────────────────────────────────────────────
# Connect to ChromaDB
# ─────────────────────────────────────────────
client = PersistentClient(path="chroma_db")
collection = client.get_collection("import_export_laws")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def tokenize(text):
    return re.findall(r"\w+", text.lower()) if isinstance(text, str) else []


def bm25_search(query, documents):
    if not documents:
        return []

    tokenized_docs = [tokenize(d) for d in documents]
    bm25 = BM25Okapi(tokenized_docs)
    scores = bm25.get_scores(tokenize(query))

    ranked = sorted(zip(scores, documents), reverse=True)
    return [doc for _, doc in ranked[:10]]


# ─────────────────────────────────────────────
# MAIN RAG PIPELINE
# ─────────────────────────────────────────────
def retrieve_context(query, top_k=5):

    # 1️⃣ Embed & Query Vector DB
    emb = embedder.encode([query]).tolist()
    hits = collection.query(query_embeddings=emb, n_results=top_k)

    # 2️⃣ Normalize output → flat doc+meta list
    raw = []
    for doc, meta in zip(hits["documents"], hits["metadatas"]):
        if isinstance(doc, list):
            for chunk in doc:
                raw.append({"document": chunk, "metadata": meta})
        else:
            raw.append({"document": doc, "metadata": meta})

    docs_only = [r["document"] for r in raw]

    # 3️⃣ BM25 lexical recall
    bm25_docs = bm25_search(query, docs_only)

    # 4️⃣ Merge & dedupe docs (BM25 first, then vector docs)
    merged = []
    seen = set()

    # Add BM25 docs
    for d in bm25_docs:
        if d not in seen:
            seen.add(d)
            meta = next((x["metadata"] for x in raw if x["document"] == d), {})
            merged.append({"document": d, "metadata": meta})

    # Add embedding hits
    for item in raw:
        d = item["document"]
        if d not in seen:
            seen.add(d)
            merged.append(item)

    # 5️⃣ Cross-encoder reranking
    reranked = cross_encoder_rerank(query, merged, top_k)

    # 6️⃣ Prepare final output
    final_docs = [x["document"] for x in reranked]
    final_meta = [x["metadata"] for x in reranked]

    return {
        "documents": final_docs,
        "metadatas": final_meta
    }
