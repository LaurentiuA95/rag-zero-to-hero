"""
Fundamentals: BM25 + dense (TF-IDF) + hybrid cu RRF pe un corpus mic.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Sequence

import numpy as np


def tokenize(text: str) -> List[str]:
    return text.lower().split()


def bm25_scores(
    corpus: Sequence[Sequence[str]],
    query: Sequence[str],
    k1: float = 1.5,
    b: float = 0.75,
) -> np.ndarray:
    N = len(corpus)
    avgdl = np.mean([len(d) for d in corpus]) if corpus else 0.0
    df: Dict[str, int] = defaultdict(int)
    for d in corpus:
        for t in set(d):
            df[t] += 1

    scores = np.zeros(N, dtype=np.float32)
    for i, d in enumerate(corpus):
        dl = len(d) or 1
        tf: Dict[str, int] = defaultdict(int)
        for t in d:
            tf[t] += 1
        for t in query:
            if t not in df:
                continue
            idf = np.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
            num = tf[t] * (k1 + 1)
            den = tf[t] + k1 * (1 - b + b * dl / (avgdl or 1))
            scores[i] += idf * num / den
    return scores


def rrf(rankings: List[List[int]], k_const: int = 60, k: int | None = None) -> List[int]:
    acc: Dict[int, float] = defaultdict(float)
    for ranking in rankings:
        for r, idx in enumerate(ranking, start=1):
            acc[idx] += 1.0 / (k_const + r)
    ordered = sorted(acc.items(), key=lambda x: x[1], reverse=True)
    idxs = [i for i, _ in ordered]
    return idxs if k is None else idxs[:k]


if __name__ == "__main__":
    docs = [
        "pisica neagra sta pe acoperis",
        "cainele maro alearga in parc",
        "pisicile dorm mult",
        "parcul este verde si mare",
    ]
    q = tokenize("pisica in parc")
    toks = [tokenize(d) for d in docs]
    s = bm25_scores(toks, q)
    print("BM25 scores:", s)
    print("BM25 top:", np.argsort(-s))
    fused = rrf([[0, 2, 3, 1], [2, 0, 1, 3]], k=4)
    print("RRF fused:", fused)
