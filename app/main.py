from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import handle_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",             
        "https://lexilegal-noober2026-8045s-projects.vercel.app/",  
        "https://lexilegal.doptonin.in",       
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(req: QueryRequest):
    result = handle_query(req.query)
    return result