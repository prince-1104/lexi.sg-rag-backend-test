#  lexi.sg-rag-backend-test 

This is the FastAPI-based Retrieval-Augmented Generation (RAG) backend for Lexi, a legal assistant that answers legal queries using semantic search over provided legal documents and LLM-based response generation.

>  Hosted at: [https://lexi-sg-rag-backend-test-caze.onrender.com](https://lexi-sg-rag-backend-test-caze.onrender.com)  
>  Frontend: [https://lexilegal.doptonin.in/](https://lexilegal.doptonin.in/)

## some sample que:

"What is the procedure to file a public interest litigation in India?"

"What are the fundamental rights guaranteed by the Indian Constitution?"

"Explain the doctrine of basic structure with reference to Indian Constitution."

"What are the legal grounds for divorce under Hindu Marriage Act?"


---
 Due to Render's free tier limitations, the server sleeps after a few minutes of inactivity.

It may take 10–30 seconds to "cold start" when first accessed after idle time.

If you encounter a delay or network error, please wait and retry your query.

---

## Features

- `/query` POST endpoint to ask legal questions
- Embedding-based similarity search using **FAISS**
- Text extraction from legal documents
- Uses **OpenRouter + open-source LLMs** for final answer generation
- Fully open-source and reproducible





## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prince-1104/lexi.sg-rag-backend-test.git
cd lexi.sg-rag-backend-test
```

## Create virtual environment:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt



## Sample Query
{
  "query": "Is insurer liable if transport vehicle had no permit?"
}
## Sample Output

{
  "answer": "No, insurer is not liable ...",
  "citations": [
    {
      "text": "...",
      "source": "Amrit Paul Singh v. TATA AIG.pdf"
    }
  ]
}




