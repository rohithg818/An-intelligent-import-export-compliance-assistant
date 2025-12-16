# load_and_chunk_all_pdfs.py
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# ---------- Load PDF ----------
def load_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

# ---------- Chunk PDF ----------
def chunk_pdf(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return []

    text = load_pdf(path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_text(text)
