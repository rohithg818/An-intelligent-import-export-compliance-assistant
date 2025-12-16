# build_chroma_db.py
import os
import chromadb
from sentence_transformers import SentenceTransformer
from load_and_chunk_all_pdfs import chunk_pdf

print("\n🔹 LOADING EMBEDDING MODEL...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

print("🔹 INITIALIZING PERSISTENT CHROMA DB...")
client = chromadb.PersistentClient(path="../chroma_db") 
# NOTE: path is relative to scripts folder

collection = client.get_or_create_collection("import_export_laws")

# ---------- ALL PDF FILES + CATEGORY ----------
pdf_files = [
    ("Data/acts/1.FTDR_Act_1992.pdf", "FTDR Act, 1992", "acts"),
    ("Data/acts/2.Customs_Act_1962.pdf", "Customs Act, 1962", "acts"),

    ("Data/ftp/3.Foreign Trade Policy.pdf", "Foreign Trade Policy", "policy"),
    ("Data/hbp/4.DGFT Handbook of Procedures.pdf", "DGFT Handbook of Procedures", "policy"),

    ("Data/icegate/6.ICEGATE_Examination_Application_Advisory.pdf", "ICEGATE Examination Advisory", "icegate"),
    ("Data/icegate/6.ICEGATE_SEZONLINE_Duty_Payment_Manual.pdf", "ICEGATE SEZ Duty Payment", "icegate"),
    ("Data/icegate/6.ICEGATE_IGCR_User_Manual_v1_07.pdf", "ICEGATE IGCR Manual", "icegate"),

    ("Data/itc_hs/5.ITC (HS) – Export Policy.pdf", "ITC HS Export Policy", "itc_hs"),
    ("Data/itc_hs/5.ITC(HS)-Import Policy.pdf", "ITC HS Import Policy", "itc_hs"),

    ("Data/public_notices/4.DGFT Public Notice HBP.pdf", "DGFT Public Notice HBP", "public_notice"),
    ("Data/public_notices/4.DGFT Public Notice RoDTEP.pdf", "DGFT Public Notice RoDTEP", "public_notice"),
    ("Data/public_notices/4.DGFT Public Notice TRQ.pdf", "DGFT Public Notice TRQ", "public_notice"),
    ("Data/public_notices/4.DGFT Public Notices SION.pdf", "DGFT Public Notice SION", "public_notice"),

    ("Data/trade_documents/7.Trade_Document_Descriptions.pdf", "Trade Document Descriptions", "trade_documents"),
]


doc_id = collection.count()

print("\n==============================")
print("📌 STARTING CHROMA BUILD")
print("==============================")

for path, source, category in pdf_files:

    print(f"\n📄 Processing: {source}")
    chunks = chunk_pdf(path)
    filename = os.path.basename(path)

    if len(chunks) == 0:
        print("   ⚠ No text extracted → skipping")
        continue

    embeddings = embedder.encode(chunks).tolist()

    ids = [f"doc_{doc_id + i}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": source,
            "file_name": filename,
            "category": category,
            "chunk_index": i,
            "total_chunks": len(chunks)
        }
        for i in range(len(chunks))
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"   ✅ Stored {len(chunks)} chunks")
    doc_id += len(chunks)

print("\n==============================")
print("🎉 CHROMA DATABASE BUILD COMPLETE")
print(f"📌 Total documents stored: {collection.count()}")
print("==============================\n")
