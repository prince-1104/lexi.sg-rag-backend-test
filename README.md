## 🛠️ Setup

1. Clone the repo:
```bash
git clone https://github.com/yourname/lexi.sg-rag-backend-test
cd lexi.sg-rag-backend-test
```

## Create virtual environment:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


## 💡 Features

- ✅ FastAPI backend
- ✅ Embedding with `sentence-transformers`
- ✅ Vector store using FAISS
- ✅ Answer generation using OpenRouter 
- ✅ Returns citations with source text + filename
- ✅ React frontend like ChatGPT (optional)


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

