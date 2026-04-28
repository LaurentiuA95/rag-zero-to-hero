"""
Fundamentals: metrici de retrieval si un faithfulness proxy.
"""
from __future__ import annotations

import math
import re
from typing import List, Optional, Set


def recall_at_k(rankings: List[List[int]], relevants: List[Set[int]], k: int) -> float:
    if not rankings:
        return 0.0
    hits = 0
    for r, rel in zip(rankings, relevants):
        top = r[:k]
        if any(d in rel for d in top):
            hits += 1
    return hits / len(rankings)


def mean_reciprocal_rank(
    rankings: List[List[int]], relevants: List[Set[int]], k: Optional[int] = None
) -> float:
    if not rankings:
        return 0.0
    s = 0.0
    for r, rel in zip(rankings, relevants):
        top = r if k is None else r[:k]
        for i, d in enumerate(top, start=1):
            if d in rel:
                s += 1.0 / i
                break
    return s / len(rankings)


def ndcg_at_k(rankings: List[List[int]], relevants: List[Set[int]], k: int) -> float:
    if not rankings:
        return 0.0
    total = 0.0
    for r, rel in zip(rankings, relevants):
        dcg = 0.0
        for i, d in enumerate(r[:k], start=1):
            if d in rel:
                dcg += 1.0 / math.log2(i + 1)
        m = min(k, len(rel))
        idcg = sum(1.0 / math.log2(i + 1) for i in range(1, m + 1)) if m else 0.0
        total += (dcg / idcg) if idcg else 0.0
    return total / len(rankings)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def faithfulness_score(claims: List[str], contexts: List[str]) -> float:
    if not claims:
        return 0.0
    joined = " ".join(_norm(c) for c in contexts)
    ok = sum(1 for cl in claims if _norm(cl) in joined)
    return ok / len(claims)


if __name__ == "__main__":
    print("recall:", recall_at_k([[1, 2, 3], [9, 1]], [{1}, {9}], k=2))
    print("mrr:", mean_reciprocal_rank([[3, 2, 1]], [{1}]))
    print("ndcg:", ndcg_at_k([[1, 2, 3]], [{1, 3}], k=3))
    print("faith:", faithfulness_score(["Pisica doarme."], ["Pisica doarme pe canapea."]))
