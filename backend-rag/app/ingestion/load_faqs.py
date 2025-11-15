import pandas as pd
from pathlib import Path
from app.settings import DATA_DIR

FAQS_CSV = DATA_DIR / "faqs.csv"

def load_faqs(path: Path = FAQS_CSV) -> pd.DataFrame:
    df = pd.read_csv(path, sep=",")
    
    df = df.dropna(subset=["question", "answer"]).reset_index(drop=True)
    df["text"] = df["question"].str.strip() + "\n" + df["answer"].str.strip()
    df["source"] = df.index.map(lambda i: f"faq_{i}")
    return df[["source", "question", "answer", "text"]]