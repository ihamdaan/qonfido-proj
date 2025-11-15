from .lexical import LexicalRetriever
from .semantic import SemanticRetriever
from .numeric import NumericRetriever
from app.settings import HYBRID_ALPHA, TOP_K_LEXICAL, TOP_K_SEMANTIC

class HybridRetriever:
    def __init__(self):
        self.lex = LexicalRetriever()
        self.sem = SemanticRetriever()
        self.num = NumericRetriever()

    def retrieve(self, query: str, top_k: int = 10, alpha: float = HYBRID_ALPHA):

        if self.num.is_numeric_query(query):
            num_results = self.num.retrieve(query, top_k=top_k)
            
            if num_results:
                faq_context = self.sem.retrieve(query, top_k=3)
                faq_only = [r for r in faq_context if r["source"]["type"] == "faq"]
                return num_results + faq_only

        lex_res = self.lex.retrieve(query, top_k=TOP_K_LEXICAL)
        sem_res = self.sem.retrieve(query, top_k=TOP_K_SEMANTIC)

        lex_scores = [r["score"] for r in lex_res]
        sem_scores = [r["score"] for r in sem_res]
        max_lex = max(lex_scores) if lex_scores else 1.0
        max_sem = max(sem_scores) if sem_scores else 1.0

        candidates = {}
        for r in lex_res:
            sid = r["source"]["id"]
            candidates[sid] = {
                "source": r["source"],
                "text": r["text"],
                "lex_score": r["score"],
                "sem_score": 0.0
            }

        for r in sem_res:
            sid = r["source"]["id"]
            if sid not in candidates:
                candidates[sid] = {
                    "source": r["source"],
                    "text": r["text"],
                    "lex_score": 0.0,
                    "sem_score": r["score"]
                }
            else:
                candidates[sid]["sem_score"] = r["score"]

        fused = []
        for sid, v in candidates.items():
            norm_lex = v["lex_score"] / max_lex if max_lex else 0.0
            norm_sem = v["sem_score"] / max_sem if max_sem else 0.0

            score = (1 - alpha) * norm_lex + alpha * norm_sem

            fused.append({
                "score": float(score),
                "source": v["source"],
                "text": v["text"],
                "lex_score": v["lex_score"],
                "sem_score": v["sem_score"]
            })

        fused_sorted = sorted(fused, key=lambda x: x["score"], reverse=True)

        return fused_sorted[:top_k]
