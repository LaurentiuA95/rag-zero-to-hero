"""
Exercitii modulul 08 - Production RAG.

Implementeaza:

  1. class LRUCache
        __init__(self, capacity: int)
        get(self, key) -> Optional[value]   # None daca lipseste, refreshuieste pozitia
        put(self, key, value) -> None       # adauga/actualizeaza, evict LRU daca depaseste capacitatea
     Semantica: un `get` face cheia "most recently used". `put` pentru cheie existenta o reimprospateaza.

  2. class TokenBudget
        __init__(self, max_tokens: int)
        fit(self, items: list[str]) -> list[str]
     Ia stringurile in ordine; un string "costa" `len(s.split())` tokens; sare peste stringurile
     care nu ar incapea si continua (nu se opreste la primul skip). Rezultatul final respecta `max_tokens`.

  3. redact_pii(text: str) -> str
     Inlocuieste email-urile cu "<EMAIL>" si numerele de telefon cu "<PHONE>".
     Regex-uri sugerate (sunt conservatoare):
        email: r"[\\w.+-]+@[\\w-]+\\.[\\w.-]+"
        phone: r"\\+?\\d[\\d \\-().]{6,}\\d"
"""
from __future__ import annotations

import re
from collections import OrderedDict
from typing import List, Optional


class LRUCache:
    def __init__(self, capacity: int):
        # TODO
        raise NotImplementedError

    def get(self, key) -> Optional[object]:
        # TODO
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO
        raise NotImplementedError


class TokenBudget:
    def __init__(self, max_tokens: int):
        # TODO
        raise NotImplementedError

    def fit(self, items: List[str]) -> List[str]:
        # TODO
        raise NotImplementedError


def redact_pii(text: str) -> str:
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    c = LRUCache(2)
    c.put("a", 1); c.put("b", 2); c.get("a"); c.put("c", 3)
    print("b ->", c.get("b"), "(asteptat None)")
    print(TokenBudget(20).fit(["aaaa bbbb"] * 4))
    print(redact_pii("Contact: laur@example.com sau +40 711 222 333"))
