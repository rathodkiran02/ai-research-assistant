import os
from config import DOCUMENTS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents(directory: str = DOCUMENTS_DIR) -> list[dict]:
    """Load all .md, .txt, .pdf files from the documents directory."""
    docs = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith((".md", ".txt")):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({"filename": filename, "content": content})
        elif filename.endswith(".pdf"):
            docs.append({"filename": filename, "content": _load_pdf(filepath)})
    return docs


def _load_pdf(filepath: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Split documents into overlapping chunks."""
    chunks = []
    for doc in docs:
        text = doc["content"]
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append({
                    "source": doc["filename"],
                    "text": chunk_text.strip()
                })
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks
