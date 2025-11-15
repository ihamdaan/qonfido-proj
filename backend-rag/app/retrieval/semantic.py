import faiss
import numpy as np
from ..ingestion.load_faqs import load_faqs
from ..ingestion.load_funds import load_funds
from ..ingestion.embed_utils import get_embedding
from app.settings import FAISS_INDEX_PATH


class SemanticRetriever:
    def __init__(self):
        self.faqs = load_faqs()
        self.funds = load_funds()
        self.corpus = list(self.faqs["text"]) + list(self.funds["text"])
        self.ids = list(self.faqs["source"]) + list(self.funds["source"])
        self.index = None
        self._build_index()


    def _build_index(self):
        if FAISS_INDEX_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                return
            except Exception:
                pass
        embs = [get_embedding(t).astype(np.float32) for t in self.corpus]
        dim = embs[0].shape[0]
        xb = np.vstack(embs)
        index = faiss.IndexFlatIP(dim) 
        faiss.normalize_L2(xb)
        index.add(xb)
        faiss.write_index(index, str(FAISS_INDEX_PATH))
        self.index = index


    def retrieve(self, query: str, top_k: int = 5):
        q_emb = get_embedding(query).astype(np.float32)
        faiss.normalize_L2(np.expand_dims(q_emb, axis=0))
        D, I = self.index.search(np.expand_dims(q_emb, axis=0), top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0:
                continue
            text = self.corpus[idx]
            source_id = self.ids[idx]
            typ = "faq" if str(source_id).startswith("faq_") else "fund"
            meta = {}
            if typ == "faq":
                row = self.faqs[self.faqs["source"] == source_id].iloc[0]
                meta = {"question": row.question}
            else:
                row = self.funds[self.funds["source"] == source_id].iloc[0]
                meta = {"fund_name": row.fund_name}
            results.append({"score": float(score), "source": {"id": source_id, "type": typ, "meta": meta}, "text": text})
        return results