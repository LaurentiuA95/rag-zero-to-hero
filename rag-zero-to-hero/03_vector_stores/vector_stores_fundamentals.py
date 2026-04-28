"""
Fundamentals: vector store minim (flat index) cu metadata si pre-filter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class Entry:
    id: str
    vector: np.ndarray
    metadata: Dict[str, object] = field(default_factory=dict)


class InMemoryStore:
    def __init__(self, dim: int):
        self.dim = dim
        self._by_id: Dict[str, Entry] = {}

    def add(self, id: str, vector: np.ndarray, metadata: Optional[Dict] = None) -> None:
        v = np.asarray(vector, dtype=np.float32)
        if v.shape[-1] != self.dim:
            raise ValueError(f"dim mismatch: expected {self.dim}, got {v.shape[-1]}")
        self._by_id[id] = Entry(id, v, metadata or {})

    def search(
        self, query: np.ndarray, k: int, where: Optional[Dict] = None
    ) -> List[Tuple[str, float, Dict]]:
        q = np.asarray(query, dtype=np.float32)
        if q.shape[-1] != self.dim:
            raise ValueError("query dim mismatch")
        qn = np.linalg.norm(q) + 1e-12
        hits: List[Tuple[str, float, Dict]] = []
        for e in self._by_id.values():
            if where and not all(e.metadata.get(k_) == v_ for k_, v_ in where.items()):
                continue
            en = np.linalg.norm(e.vector) + 1e-12
            score = float(np.dot(q, e.vector) / (qn * en))
            hits.append((e.id, score, e.metadata))
        hits.sort(key=lambda x: x[1], reverse=True)
        return hits[:k]


if __name__ == "__main__":
    store = InMemoryStore(dim=3)
    store.add("a", np.array([1.0, 0.0, 0.0]), {"lang": "ro"})
    store.add("b", np.array([0.0, 1.0, 0.0]), {"lang": "en"})
    store.add("c", np.array([1.0, 1.0, 0.0]), {"lang": "ro"})
    print(store.search(np.array([1.0, 0.0, 0.0]), k=3))
    print(store.search(np.array([1.0, 0.0, 0.0]), k=3, where={"lang": "ro"}))
