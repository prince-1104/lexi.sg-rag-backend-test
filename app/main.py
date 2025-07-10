from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import handle_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(req: QueryRequest):
    result = handle_query(req.query)
    return result