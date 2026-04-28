"""
Fundamentals: construim embeddings cu TF-IDF (fara dependinte externe) si
aratam cum functioneaza similaritatea cosinus.

Pentru modele reale (sentence-transformers) vezi functia `real_embeddings_demo`
care se poate rula optional: python 01_embeddings/embeddings_fundamentals.py --real
"""
from __future__ import annotations

import math
import sys
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np


def _tokenize(t: str) -> List[str]:
    return [w.lower() for w in t.split() if w.strip()]


def build_tfidf(docs: List[str]) -> Tuple[np.ndarray, Dict[str, int]]:
    """Intoarce (X, vocab) unde X: [N, V] TF-IDF."""
    vocab: Dict[str, int] = {}
    for d in docs:
        for t in _tokenize(d):
            vocab.setdefault(t, len(vocab))

    N, V = len(docs), len(vocab)
    tf = np.zeros((N, V), dtype=np.float32)
    df = np.zeros(V, dtype=np.float32)
    for i, d in enumerate(docs):
        counts = Counter(_tokenize(d))
        for w, c in counts.items():
            j = vocab[w]
            tf[i, j] = c
            df[j] += 1
    idf = np.log((1 + N) / (1 + df)) + 1.0
    return tf * idf, vocab


def cosine(a: np.ndarray, b: np.ndarray, eps: float = 1e-12) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + eps))


def demo_cosine() -> None:
    docs = [
        "pisica neagra doarme pe canapea",
        "cainele alearga in parc",
        "pisicuta toarce multumita",
    ]
    X, _ = build_tfidf(docs)
    print("Matricea TF-IDF shape:", X.shape)
    print("cos(d0, d2) [pisica - pisicuta, vocab diferit]:", cosine(X[0], X[2]))
    print("cos(d0, d1) [pisica - caine]:", cosine(X[0], X[1]))


def real_embeddings_demo() -> None:
    """Optional: demonstreaza sentence-transformers daca e instalat."""
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:
        print("sentence-transformers indisponibil:", e)
        return
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb = model.encode([
        "Pisica neagra doarme pe canapea.",
        "Cainele alearga in parc.",
        "Felina toarce multumita.",
    ], normalize_embeddings=True)
    print("shape:", emb.shape)
    print("cos(0,2):", float(emb[0] @ emb[2]))
    print("cos(0,1):", float(emb[0] @ emb[1]))


if __name__ == "__main__":
    demo_cosine()
    if "--real" in sys.argv:
        real_embeddings_demo()
