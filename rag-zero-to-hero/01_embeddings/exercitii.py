"""
Exercitii modulul 01 - Embeddings (lucram pe np.ndarray dati ca input).

Implementeaza:
  1. cosine_similarity(a, b)        -> float in [-1, 1]
  2. l2_normalize(v)                 -> np.ndarray cu norma 1 (sau 0-vector daca v == 0)
  3. top_k_similar(query, db, k)     -> (indices, scores), sortate desc. dupa scor
"""
from __future__ import annotations

from typing import Tuple

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray, eps: float = 1e-12) -> float:
    """Similaritate cosinus intre doi vectori 1D.

    Hint: foloseste np.dot si np.linalg.norm; adauga `eps` la numitor pentru stabilitate.
    """
    # TODO
    numarator = np.dot(a, b)
    numitor = np.linalg.norm(a) * np.linalg.norm(b)
    return numarator / (numitor + eps)

def l2_normalize(v: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Intoarce v / ||v||_2. Daca ||v||_2 < eps, intoarce v nemodificat (sau zero).

    Atentie: foloseste astype(float) daca vrei sa fii sigur ca nu divizi integer.
    """
    # TODO
    norma = np.linalg.norm(v)
    if norma < eps:
        return v
    return v / norma


def top_k_similar(
    query: np.ndarray, db: np.ndarray, k: int
) -> Tuple[np.ndarray, np.ndarray]:
    """Intoarce (indices, scores) pentru top-k randuri din `db` similare cu `query`.

    - `query`: shape (d,)
    - `db`:    shape (N, d)
    - returns:
        indices: shape (k,) int
        scores:  shape (k,) float, sortat descrescator

    Implementeaza cu scoruri cosinus. Poti folosi cosine_similarity sau vectorizat.
    """
    # TODO
    scores = []
    for row in db:
        scores.append(cosine_similarity(row, query))
    scores = np.array(scores)
    sorted_indices = np.argsort(-scores)
    top_k_indices = sorted_indices[:k]
    top_k_scores = scores[top_k_indices]
    return top_k_indices, top_k_scores

if __name__ == "__main__":
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.5, 0.5, 0.0])
    print("cos(a, b) =", cosine_similarity(a, b))
    print("norm(a) =", np.linalg.norm(l2_normalize(a)))
    db = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    print(top_k_similar(np.array([1.0, 0.0]), db, k=2))
