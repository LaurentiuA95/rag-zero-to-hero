"""
Exercitii modulul 06 - Evaluation.

Implementeaza:

  1. recall_at_k(rankings: list[list[int]], relevants: list[set[int]], k: int) -> float
     - Procentul de query-uri pentru care cel putin un relevant apare in top-k.

  2. mean_reciprocal_rank(rankings: list[list[int]], relevants: list[set[int]], k: int | None = None) -> float
     - Media lui 1/rang (primul rang relevant in lista). 1-indexed.
     - Daca niciun document relevant nu apare in lista, contributia e 0.

  3. ndcg_at_k(rankings: list[list[int]], relevants: list[set[int]], k: int) -> float
     - Relevante binare. IDCG = DCG al rankingului ideal (toti relevantii la inceput).
     - Formula: DCG@k = sum_{i=1..k} 1/log2(i+1) pentru pozitiile cu relevant.

  4. faithfulness_score(claims: list[str], contexts: list[str]) -> float
     - Returneaza |claims care apar (dupa normalizare whitespace+lowercase) in "\\n".join(contexts)| / |claims|.
     - Daca claims == [] intoarce 0.0.
"""
from __future__ import annotations

import math
import re
from typing import List, Optional, Set


def recall_at_k(rankings: List[List[int]], relevants: List[Set[int]], k: int) -> float:
    # TODO
    raise NotImplementedError


def mean_reciprocal_rank(
    rankings: List[List[int]],
    relevants: List[Set[int]],
    k: Optional[int] = None,
) -> float:
    # TODO
    raise NotImplementedError


def ndcg_at_k(
    rankings: List[List[int]],
    relevants: List[Set[int]],
    k: int,
) -> float:
    # TODO
    raise NotImplementedError


def faithfulness_score(claims: List[str], contexts: List[str]) -> float:
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    print("recall:", recall_at_k([[1, 2, 3]], [{1}], 3))
    print("mrr:", mean_reciprocal_rank([[9, 1, 2]], [{1}]))
    print("ndcg:", ndcg_at_k([[1, 2, 3]], [{1}], 3))
    print("faith:", faithfulness_score(["abc"], ["abc def"]))
