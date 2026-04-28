"""
Fundamentals: rerank mock + multi-query + HyDE.
"""
from __future__ import annotations

from typing import List, Tuple


def mock_cross_score(q: str, d: str) -> float:
    return -abs(len(q) - len(d))


def rerank(q: str, cands: List[Tuple[int, str]], k: int) -> List[Tuple[int, str]]:
    scored = [(mock_cross_score(q, d), i, d) for i, d in cands]
    scored.sort(key=lambda x: (-x[0], x[1]))  # stabil pe id
    return [(i, d) for _, i, d in scored[:k]]


def multi_query(question: str, n: int) -> List[str]:
    tpls = [
        "{q}",
        "Defineste: {q}",
        "Explica pe scurt: {q}",
        "{q} - detalii si exemple.",
        "Care este raspunsul la: {q}",
    ]
    out = [t.format(q=question.strip()) for t in tpls[:n]]
    if len(out) < n:
        out += [question] * (n - len(out))
    return out


def hyde(question: str) -> str:
    q = question.strip().rstrip("?") or "subiectul de interes"
    return (
        f"Acesta este un paragraf care raspunde la intrebarea '{q}'. "
        f"{q.capitalize()} este un concept tehnic care implica mai multe componente "
        f"si pasi concreti. Mai jos sunt detalii si exemple relevante care acopera "
        f"aspecte importante, intuitie, compromisuri si modul de utilizare in practica."
    )


if __name__ == "__main__":
    print(rerank("pisica", [(0, "lungime mult prea mare"), (1, "pisoi"), (2, "pisica")], k=2))
    print(multi_query("Ce e RAG?", n=3))
    print(hyde("Ce e RAG?"))
