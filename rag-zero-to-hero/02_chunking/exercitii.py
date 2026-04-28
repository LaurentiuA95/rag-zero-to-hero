"""
Exercitii modulul 02 - Chunking.

Implementeaza:
  1. chunk_fixed(text, size)                  -> list[str]
     - Imparti textul in bucati consecutive de `size` caractere. Ultima poate fi mai scurta.
     - Exemplu: chunk_fixed("abcdefghij", 3) == ["abc", "def", "ghi", "j"]

  2. chunk_sliding(text, size, overlap)       -> list[str]
     - Sliding window cu pas = size - overlap.
     - Ultimul chunk este cel care atinge sau depaseste ultimul caracter.
     - Constraint: 0 <= overlap < size.
     - Exemplu: chunk_sliding("abcdefghij", 4, 2) ==
                ["abcd", "cdef", "efgh", "ghij"]

  3. chunk_recursive(text, max_chars, separators) -> list[str]
     - Daca len(text) <= max_chars: intoarce [text.strip()] (daca e nevid).
     - Altfel: ia `separators[0]`, sparge textul, pentru fiecare parte:
         * daca e <= max_chars -> adaug-o (strip)
         * daca nu -> recursie cu `separators[1:]`
     - Daca nu mai ai separatori si chunk-ul e prea mare, cazi pe chunk_fixed(..., max_chars).

Toate functiile: strip() la final pentru fiecare chunk produs; fara chunks goale.
"""
from __future__ import annotations

from functools import partial
from typing import List


def chunk_fixed(text: str, size: int) -> List[str]:
    """Imparte textul in bucati consecutive de `size` caractere."""
    # TODO
    rezultat = []
    for i in range(0, len(text), size):
        chunk = text[i:i + size]
        rezultat.append(chunk.strip())
    return rezultat


def chunk_sliding(text: str, size: int, overlap: int) -> List[str]:
    """Sliding window cu pas = size - overlap."""
    # TODO: validare overlap >= 0 si overlap < size
    rezultat = []
    for i in range(0, len(text), size - overlap):
        chunk = text[i:i + size]
        rezultat.append(chunk.strip())
        if i + size >= len(text):
            break
    return rezultat


def chunk_recursive(text: str, max_chars: int, separators: List[str]) -> List[str]:
    """Chunking recursiv dupa o lista ordonata de separatori."""
    # TODO
    if len(text) <= max_chars:
        return [text.strip()]
    if not separators:
        return chunk_fixed(text, max_chars)
    parti = text.split(separators[0])
    rezultat = []
    for parte in parti:
        if len(parte) <= max_chars:
            rezultat.append(parte.strip())
        else:
            rezultat.extend(chunk_recursive(parte, max_chars, separators[1:]))
    return rezultat


if __name__ == "__main__":
    doc = "abcdefghij"
    print(chunk_fixed(doc, 3))
    print(chunk_sliding(doc, 4, 2))
    print(chunk_recursive(
        "Paragraf unu.\n\nParagraf doi are doua propozitii. Asta e a doua.\n\nFinal.",
        max_chars=40,
        separators=["\n\n", ". ", " "],
    ))
