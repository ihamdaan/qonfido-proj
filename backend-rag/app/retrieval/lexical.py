from rank_bm25 import BM25Okapi
from ..ingestion.load_faqs import load_faqs
from ..ingestion.load_funds import load_funds


class LexicalRetriever:
    def __init__(self):
        faqs = load_faqs()
        funds = load_funds()
        self.faqs = faqs
        self.funds = funds
        self.corpus = list(faqs["text"]) + list(funds["text"])
        tokenized = [doc.split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized)


    def retrieve(self, query: str, top_k: int = 5):
        tokens = query.split()
        scores = self.bm25.get_scores(tokens)
        top_n = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_n:
            snippet = self.corpus[idx]
            if idx < len(self.faqs):
                row = self.faqs.iloc[idx]
                source = {"id": row.source, "type": "faq", "meta": {"question": row.question}}
            else:
                fidx = idx - len(self.faqs)
                row = self.funds.iloc[fidx]
                source = {"id": row.source, "type": "fund", "meta": {"fund_name": row.fund_name}}

            results.append({"score": float(scores[idx]), "source": source, "text": snippet})

        return results
