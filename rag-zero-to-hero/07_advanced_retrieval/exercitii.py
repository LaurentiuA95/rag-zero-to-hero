"""
Exercitii modulul 07 - Advanced retrieval.

Implementeaza:

  1. cross_encoder_rerank(query: str, candidates: list[tuple[int, str]], k: int)
         -> list[tuple[int, str]]
     - candidates: list de (doc_id, doc_text)
     - scor MOCK: score(q, d) = -abs(len(q) - len(d))
     - intoarce top-k candidati sortati desc. dupa scor (stabil pe id la egalitate)

  2. multi_query_expand(question: str, n: int) -> list[str]
     - intoarce n reformulari ale intrebarii
     - test-ul verifica ca lista contine tokens relevanti din intrebare

  3. hyde_pseudo_doc(question: str) -> str
     - intoarce un pseudo-document declarativ
     - test-ul verifica ca pseudo-doc-ul are >= 10 cuvinte
"""
from __future__ import annotations

from typing import List, Tuple


def cross_encoder_rerank(
    query: str, candidates: List[Tuple[int, str]], k: int
) -> List[Tuple[int, str]]:
    # TODO
    raise NotImplementedError


def multi_query_expand(question: str, n: int) -> List[str]:
    # TODO
    raise NotImplementedError


def hyde_pseudo_doc(question: str) -> str:
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    cands = [(0, "lungime mult prea mare"), (1, "pisoi"), (2, "pisica")]
    print(cross_encoder_rerank("pisica", cands, k=2))
    print(multi_query_expand("Ce e RAG?", n=3))
    print(hyde_pseudo_doc("Ce e RAG?"))
