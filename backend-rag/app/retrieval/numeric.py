import re
import pandas as pd
from typing import List, Dict, Optional, Tuple
from ..ingestion.load_funds import load_funds


class NumericRetriever:
    METRIC_MAPPINGS = {
        "sharpe": "sharpe_ratio",
        "sharpe ratio": "sharpe_ratio",
        "risk-adjusted": "sharpe_ratio",
        "risk adjusted": "sharpe_ratio",
        
        "cagr": "cagr_3y",
        "return": "cagr_3y",
        "returns": "cagr_3y",
        "growth": "cagr_3y",
        
        "volatility": "volatility",
        "risk": "volatility",
        "variance": "volatility",
        "std": "volatility",
        "standard deviation": "volatility",
    }
    
    ASCENDING_KEYWORDS = [
        "lowest", "minimum", "min", "worst", "bottom", "least",
        "avoid", "not consider", "stay away", "don't invest"
    ]
    
    DESCENDING_KEYWORDS = [
        "highest", "maximum", "max", "best", "top", "most",
        "recommend", "consider", "invest", "outperform"
    ]
    
    def __init__(self):
        self.funds = load_funds()
        for col in ["sharpe_ratio", "cagr_3y", "volatility"]:
            if col in self.funds.columns:
                self.funds[col] = pd.to_numeric(self.funds[col], errors='coerce')
    
    
    def _extract_metric(self, query: str) -> Optional[str]:
        q = query.lower()
        
        for keyword, column in self.METRIC_MAPPINGS.items():
            if keyword in q:
                return column
        
        return None
    
    
    def _extract_direction(self, query: str) -> bool:
        q = query.lower()
        
        has_ascending = any(kw in q for kw in self.ASCENDING_KEYWORDS)
        has_descending = any(kw in q for kw in self.DESCENDING_KEYWORDS)
        
        if has_ascending and not has_descending:
            return True 
        else:
            return False  
    
    
    def _extract_threshold(self, query: str, metric: str) -> Optional[Tuple[str, float]]:
        q = query.lower()
        
        patterns = [
            (r'(?:above|over|greater than|more than|>)\s*(\d+\.?\d*)\s*%?', 'gt'),
            (r'(?:below|under|less than|<)\s*(\d+\.?\d*)\s*%?', 'lt'),
            (r'(?:at least|minimum)\s*(\d+\.?\d*)\s*%?', 'gte'),
            (r'(?:at most|maximum)\s*(\d+\.?\d*)\s*%?', 'lte'),
        ]
        
        for pattern, operator in patterns:
            match = re.search(pattern, q)
            if match:
                value = float(match.group(1))
                if '%' in q and value > 1:
                    value = value / 100
                return (operator, value)
        
        return None
    
    
    def _apply_threshold(self, df, metric: str, operator: str, value: float):
        if operator == 'gt':
            return df[df[metric] > value]
        elif operator == 'lt':
            return df[df[metric] < value]
        elif operator == 'gte':
            return df[df[metric] >= value]
        elif operator == 'lte':
            return df[df[metric] <= value]
        return df
    
    
    def _extract_top_k(self, query: str, default_k: int = 5) -> int:
        q = query.lower()
        
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        patterns = [
            r'top\s+(\d+)',
            r'(\d+)\s+(?:best|worst|top|bottom)',
            r'top\s+(\w+)',  
        ]
        
        for pattern in patterns:
            match = re.search(pattern, q)
            if match:
                num_str = match.group(1)
                if num_str in number_words:
                    return number_words[num_str]
                try:
                    return int(num_str)
                except ValueError:
                    continue
        
        return default_k
    
    
    def is_numeric_query(self, query: str) -> bool:
        metric = self._extract_metric(query)
        if not metric:
            return False
        
        q = query.lower()
        ranking_keywords = (
            self.ASCENDING_KEYWORDS + 
            self.DESCENDING_KEYWORDS + 
            ["compare", "rank", "sort", "order"]
        )
        
        has_ranking = any(kw in q for kw in ranking_keywords)
        has_threshold = self._extract_threshold(query, metric) is not None
        
        return has_ranking or has_threshold
    
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        metric = self._extract_metric(query)
        if not metric:
            return [] 
        
        if metric not in self.funds.columns:
            return []
        
        filtered_df = self.funds.copy()
        
        threshold = self._extract_threshold(query, metric)
        if threshold:
            operator, value = threshold
            filtered_df = self._apply_threshold(filtered_df, metric, operator, value)
            
            if len(filtered_df) == 0:
                return []
        
        query_k = self._extract_top_k(query, default_k=top_k)
        
        ascending = self._extract_direction(query)
        
        sorted_df = filtered_df.sort_values(metric, ascending=ascending)
        
        top_df = sorted_df.head(query_k)
        
        results = []
        for idx, (_, row) in enumerate(top_df.iterrows()):
            results.append({
                "score": 1.0 - (idx * 0.1),  # Slight score degradation by rank
                "source": {
                    "id": row.source,
                    "type": "fund",
                    "meta": {
                        "fund_name": row.fund_name,
                        "rank": idx + 1,
                        "metric": metric,
                        "metric_value": float(row[metric])
                    }
                },
                "text": row.text,
                "rank": idx + 1,
                "metric_value": float(row[metric])
            })
        
        return results
    
    
    def get_all_funds_sorted(self, metric: str = "sharpe_ratio", ascending: bool = False) -> List[Dict]:
        if metric not in self.funds.columns:
            return []
        
        sorted_df = self.funds.sort_values(metric, ascending=ascending)
        
        results = []
        for idx, (_, row) in enumerate(sorted_df.iterrows()):
            results.append({
                "score": 1.0,
                "source": {
                    "id": row.source,
                    "type": "fund",
                    "meta": {
                        "fund_name": row.fund_name,
                        "rank": idx + 1,
                        "metric": metric,
                        "metric_value": float(row[metric])
                    }
                },
                "text": row.text,
                "rank": idx + 1,
                "metric_value": float(row[metric])
            })
        
        return results