from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


if __name__ == "__main__":
    pdf_path = r"Data\acts\1.FTDR_Act_1992.pdf"
    print("Trying to load:", pdf_path)

    text = load_pdf(pdf_path)

    print("PDF LOADED SUCCESSFULLY")
    print("Text length:", len(text))
    print("\n--- SAMPLE TEXT ---\n")
    print(text[:1000])
