from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from ..retrieval.lexical import LexicalRetriever
from ..retrieval.semantic import SemanticRetriever
from ..retrieval.hybrid import HybridRetriever
from ..core.context_builder import build_context, SYSTEM_PROMPT
from ..core.llm import generate_answer
from app.settings import TOP_K_LEXICAL, TOP_K_SEMANTIC


router = APIRouter()


_lex = LexicalRetriever()
_sem = SemanticRetriever()
_hybrid = HybridRetriever()


class QueryIn(BaseModel):
    query: str
    mode: Optional[str] = "hybrid" # lexical / semantic / hybrid


class QueryOut(BaseModel):
    answer: str
    sources: list
    reasoning: Optional[dict] = None


@router.post("/query", response_model=QueryOut)
async def query_endpoint(payload: QueryIn):
    query = payload.query
    mode = payload.mode.lower() if payload.mode else "hybrid"
    if mode == "lexical":
        retrieved = _lex.retrieve(query, top_k=TOP_K_LEXICAL)
    elif mode == "semantic":
        retrieved = _sem.retrieve(query, top_k=TOP_K_SEMANTIC)
    else:
        retrieved = _hybrid.retrieve(query, top_k=max(TOP_K_LEXICAL, TOP_K_SEMANTIC))


    context = build_context(query, retrieved)
    llm_resp = generate_answer(SYSTEM_PROMPT, query, context)


    print("retrieved: ", retrieved)
    sources = [ {"id": r["source"]["id"], "type": r["source"]["type"], "source_meta": r["source"].get("meta", {}), "source_text": r["text"], "score": r.get("score", 0.0)} for r in retrieved ]
    return {
    "answer": llm_resp["answer"],
    "sources": sources,
    "reasoning": llm_resp.get("reasoning_details")
    }