import chromadb
from sentence_transformers import SentenceTransformer


# ===============================
# 1. Load persistent Chroma DB
# ===============================
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="import_export_laws")

print("Chroma DB loaded")
print("Total chunks in DB:", collection.count())


# ===============================
# 2. Load embedding model
# ===============================
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded")


# ===============================
# 3. User query (improved)
# ===============================
query = (
    "Export policy and restrictions for lithium-ion batteries "
    "under ITC HS code in India"
)

print("\nUSER QUERY:")
print(query)


# ===============================
# 4. Convert query to embedding
# ===============================
query_embedding = embedder.encode([query]).tolist()


# ===============================
# 5. Similarity search with metadata filter
# ===============================
# We focus on ITC HS + Policy documents
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
    where={
        "source": {
            "$contains": "ITC"
        }
    }
)


# ===============================
# 6. Display retrieved chunks
# ===============================
print("\nTOP 5 RETRIEVED CHUNKS:\n")

documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]

if not documents:
    print("No relevant documents found.")
else:
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        print(f"\n--- Result {i + 1} ---")
        print(f"Source: {meta.get('source', 'Unknown')}\n")
        print(doc[:1200])  # limit output length
