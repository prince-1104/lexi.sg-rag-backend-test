import os
import faiss
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from app.document_loader import load_documents

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

# Load OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Paths
FAISS_INDEX_PATH = "vector_store/index.faiss"
METADATA_PATH = "vector_store/metadata.pkl"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index():
    documents = load_documents("data/legal_docs")
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("vector_store", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(documents, f)

def search_similar_chunks(query: str, top_k: int = 5) -> List[Dict]:
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

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
    context = "\n\n".join([f"{c['text']}" for c in retrieved_chunks])

    prompt = f"""
You are a legal assistant. Based on the following legal text snippets, answer the user's question.
Always stay factual. If unsure, say "not found".

Legal Snippets:
{context}

User Question: {query}
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "answer": response.choices[0].message.content.strip(),
        "citations": retrieved_chunks
    }