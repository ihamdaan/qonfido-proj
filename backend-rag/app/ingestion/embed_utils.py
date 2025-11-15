from diskcache import Cache
from sentence_transformers import SentenceTransformer
import numpy as np
from app.settings import DISKCACHE_DIR, EMBED_MODEL

_model = None
_cache = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def _get_cache():
    global _cache
    if _cache is None:
        _cache = Cache(DISKCACHE_DIR)
    return _cache

def get_embedding(text: str) -> np.ndarray:
    cache = _get_cache()
    key = f"emb::{hash(text)}"
    emb = cache.get(key)
    if emb is not None:
        return np.array(emb)

    model = _get_model()
    emb = model.encode([text], show_progress_bar=False)[0]
    cache.set(key, emb.tolist())
    return np.array(emb)