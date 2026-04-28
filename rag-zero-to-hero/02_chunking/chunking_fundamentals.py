"""
Fundamentals: chunking strategies cu exemple reale.
Ruleaza: python 02_chunking/chunking_fundamentals.py
"""
from __future__ import annotations

from typing import List


SAMPLE = (
    "Introducere. RAG combina retrieval si generare.\n\n"
    "Retrieval cauta in baza de cunostinte.\n\n"
    "Generation folosesc un LLM peste contextul returnat."
)


def chunk_fixed(text: str, size: int) -> List[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def chunk_sliding(text: str, size: int, overlap: int) -> List[str]:
    assert 0 <= overlap < size, "overlap trebuie in [0, size)"
    step = size - overlap
    out = []
    i = 0
    while i < len(text):
        out.append(text[i : i + size])
        if i + size >= len(text):
            break
        i += step
    return out


def chunk_recursive(text: str, max_chars: int, separators: List[str]) -> List[str]:
    if len(text) <= max_chars:
        return [text.strip()] if text.strip() else []

    if not separators:
        # fallback: spargere fixa
        return chunk_fixed(text, max_chars)

    sep, rest = separators[0], separators[1:]
    parts = text.split(sep)
    out: List[str] = []
    for i, p in enumerate(parts):
        piece = p if i == len(parts) - 1 else p + sep.rstrip()
        if len(piece) <= max_chars:
            if piece.strip():
                out.append(piece.strip())
        else:
            out.extend(chunk_recursive(piece, max_chars, rest))
    return out


if __name__ == "__main__":
    print("--- fix, size=30 ---")
    for c in chunk_fixed(SAMPLE, 30):
        print(repr(c))

    print("\n--- sliding, size=30, overlap=10 ---")
    for c in chunk_sliding(SAMPLE, 30, 10):
        print(repr(c))

    print("\n--- recursive, max=40 ---")
    for c in chunk_recursive(SAMPLE, 40, ["\n\n", ". ", " "]):
        print(repr(c))
