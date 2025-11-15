import pandas as pd
from pathlib import Path
from app.settings import DATA_DIR

FUNDS_CSV = DATA_DIR / "funds.csv"

def format_fund_row(row: pd.Series) -> str:
    return (
    f"Fund {row.fund_id} {row.fund_name} in category {row.category} "
    f"has 3-year CAGR of {row['cagr_3yr (%)']}%, volatility of {row['volatility (%)']}%, "
    f"and Sharpe ratio of {row.sharpe_ratio}."
    )

def load_funds(path: Path = FUNDS_CSV) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t" if "\t" in open(path).read() else ",")
    
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=["fund_id"]) # minimal
    df = df.reset_index(drop=True)
    df["text"] = df.apply(format_fund_row, axis=1)
    df["source"] = df.fund_id
    return df[["source", "fund_id", "fund_name", "category", "text", "cagr_3yr (%)", "volatility (%)", "sharpe_ratio"]]