"""
Exercitii modulul 03 - Vector store in-memory cu filtrare pe metadata.

Implementeaza clasa `VectorStore` cu:
  - __init__(self, dim: int)
  - add(self, id: str, vector: np.ndarray, metadata: dict | None = None) -> None
      * ridica ValueError daca vector.shape[-1] != self.dim
      * metadata e optionala, default {}
  - search(self, query: np.ndarray, k: int, where: dict | None = None)
      * intoarce list[tuple[id, score, metadata]] sortat desc. dupa scor cosinus
      * `where` = pre-filter pe egalitate (toate cheile trebuie sa se potriveasca)

Scor = cosinus (calculat tu explicit).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple
from unittest import result

import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        # TODO: initializeaza structura ta interna (ex: dict id -> (vector, metadata))
        self._store = {}

    def add(
        self, id: str, vector: np.ndarray, metadata: Optional[Dict] = None
    ) -> None:
        # TODO: valideaza dim, stocheaza vectorul si metadata
        if vector.shape[0] != self.dim:
            raise ValueError("Dimensiune vector nepotrivita")
        if metadata is None:
            metadata = {}
        self._store[id] = vector, metadata

    def search(
        self,
        query: np.ndarray,
        k: int,
        where: Optional[Dict] = None,
    ) -> List[Tuple[str, float, Dict]]:
        # TODO: calculeaza cosinus pentru fiecare entry (filtrat de where), sorteaza desc, ia top-k
        rezultat = []
        for id, (vector, metadata) in self._store.items():
           if where is None or all(metadata[key] == value for key, value in where.items()):
                score = np.dot(query, vector) / (np.linalg.norm(query) * np.linalg.norm(vector))
                rezultat.append((id, score, metadata))
        sorted_rezultat = sorted(rezultat, key=lambda x: x[1], reverse=True)
        return sorted_rezultat[:k]
if __name__ == "__main__":
    s = VectorStore(dim=3)
    s.add("a", np.array([1.0, 0.0, 0.0]), {"lang": "ro"})
    s.add("b", np.array([0.0, 1.0, 0.0]), {"lang": "en"})
    s.add("c", np.array([1.0, 1.0, 0.0]), {"lang": "ro"})
    print(s.search(np.array([1.0, 0.0, 0.0]), k=3))
    print(s.search(np.array([1.0, 0.0, 0.0]), k=3, where={"lang": "ro"}))
