"""
Exercitii modulul 04 - Retrieval.

Implementeaza:
  1. bm25_retrieve(docs, query, k)            -> list[int]
     - docs: list[str]; query: str (raw, ambele primite ca text)
     - tokenizeaza cu `text.lower().split()`
     - poti folosi `rank_bm25.BM25Okapi` sau sa-ti faci scorul manual
     - intoarce indicii documentelor ordonati descrescator dupa scor BM25, top-k

  2. reciprocal_rank_fusion(rankings, k_const=60, k=None) -> list[int]
     - rankings: lista de list[int] (ranguri produse de diferiti retrievers)
     - pentru fiecare doc si pentru fiecare lista in care apare, adauga 1 / (k_const + rang)
     - rangul incepe de la 1 (nu 0)
     - intoarce indicii sortati descrescator dupa scor RRF; daca `k` e dat, taie la top-k
"""
from __future__ import annotations

from typing import List, Optional


def bm25_retrieve(docs: List[str], query: str, k: int = 5) -> List[int]:
    """Intoarce indicii top-k documente ordonate dupa scor BM25."""
    # TODO: tokenizeaza si calculeaza BM25.
    text = "Pisica neagra sta pe acoperis."
    print(text.lower().split())
    docs = [
        "Pisica neagra sta pe acoperis.",
        "Cainele maro alearga in parc.",
        "Pisicile dorm mult.",
        "Parcul este verde si mare.",
    ]
    tokenized = []
    for doc in docs:
        tokenized.append(doc.lower().split())
    print(tokenized)

def reciprocal_rank_fusion(
    rankings: List[List[int]], k_const: int = 60, k: Optional[int] = None
) -> List[int]:
    """Combina mai multe ranking-uri prin RRF."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    docs = [
        "Pisica neagra sta pe acoperis.",
        "Cainele maro alearga in parc.",
        "Pisicile dorm mult.",
        "Parcul este verde si mare.",
    ]
    print("BM25:", bm25_retrieve(docs, "pisica", k=2))
    print("RRF:", reciprocal_rank_fusion([[2, 0, 3, 1], [0, 2, 1, 3]], k=4))
