from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
from typing import List, Dict
from app.document_loader import load_documents


FAISS_INDEX_PATH = "vector_store/index.faiss"
METADATA_PATH = "vector_store/metadata.pkl"


model = SentenceTransformer("all-MiniLM-L6-v2") 

def build_faiss_index():
    
    print("🔄 Loading and embedding documents...")
    documents = load_documents("data/legal_docs")
    texts = [doc["text"] for doc in documents]

    # Embed all chunks
    embeddings = model.encode(texts, show_progress_bar=True)

    # Create FAISS index
    dim = len(embeddings[0])  # usually 384 for MiniLM
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and metadata
    os.makedirs("vector_store", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("✅ FAISS index created and saved.")

def search_similar_chunks(query: str, top_k: int = 5) -> List[Dict]:
    
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    # Embed the query
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        chunk = metadata[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["metadata"]["source"]
        })
    return results

def handle_query(query: str) -> Dict:
   
    retrieved_chunks = search_similar_chunks(query)

    # For now, just concatenate chunks (you'll replace this with real generation)
    combined_context = "\n\n".join([c["text"] for c in retrieved_chunks])
    fake_answer = f"Based on legal documents, here is the generated answer:\n\n{combined_context[:500]}..."

    return {
        "answer": fake_answer,
        "citations": retrieved_chunks
    }
