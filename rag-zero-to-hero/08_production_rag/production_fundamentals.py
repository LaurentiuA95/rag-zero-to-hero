"""
Fundamentals: LRU cache, token budgeting, redactare PII.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from typing import List


class LRU:
    def __init__(self, capacity: int):
        self.c = capacity
        self.d: "OrderedDict[str, object]" = OrderedDict()

    def get(self, k):
        if k not in self.d:
            return None
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v) -> None:
        if k in self.d:
            self.d.move_to_end(k)
        self.d[k] = v
        while len(self.d) > self.c:
            self.d.popitem(last=False)


class Budget:
    def __init__(self, max_tokens: int):
        self.max = max_tokens

    def fit(self, items: List[str]) -> List[str]:
        out, used = [], 0
        for s in items:
            t = len(s.split())
            if used + t > self.max:
                continue
            out.append(s)
            used += t
        return out


EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d \-().]{6,}\d")


def redact(text: str) -> str:
    text = EMAIL.sub("<EMAIL>", text)
    text = PHONE.sub("<PHONE>", text)
    return text


if __name__ == "__main__":
    c = LRU(2)
    c.put("a", 1); c.put("b", 2); _ = c.get("a")
    c.put("c", 3)
    print("LRU b:", c.get("b"))
    print("budget:", Budget(20).fit(["aaaa bbbb"] * 4))
    print("redact:", redact("mail a@b.ro tel +40 711 222 333"))
