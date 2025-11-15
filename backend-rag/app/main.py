from fastapi import FastAPI
from .api.routes import router
from app.settings import OPENROUTER_API_KEY

app = FastAPI(title="Qonfido Mini RAG Backend")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}

# basic startup check
@app.on_event("startup")
async def startup_event():
    if not OPENROUTER_API_KEY:
        print("WARNING: OPENROUTER_API_KEY not set. LLM calls will fail.")