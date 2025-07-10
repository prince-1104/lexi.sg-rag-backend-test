import os
import pdfplumber
from typing import List, Dict

def load_pdf_text(file_path: str) -> str:
    full_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text.strip())
    return "\n".join(full_text)

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def load_documents(directory: str) -> List[Dict]:
  
    all_chunks = []
    for filename in os.listdir(directory):
        if not filename.endswith(".pdf"):
            print(f"⚠️ Skipping unsupported file: {filename}")
            continue

        file_path = os.path.join(directory, filename)
        text = load_pdf_text(file_path)
        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": filename,
                    "chunk_id": i
                }
            })
    return all_chunks
