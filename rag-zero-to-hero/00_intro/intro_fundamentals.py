"""
Fundamentals: cum arata un "mini-RAG" end-to-end in ~50 de linii, fara dependinte externe.
Ruleaza: python 00_intro/intro_fundamentals.py

Este un exemplu didactic. Modulele urmatoare il inlocuiesc bucata cu bucata.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Chunk:
    id: str
    text: str


CORPUS = [
    Chunk("d1", "Luceafarul este o poezie de Mihai Eminescu publicata in 1883."),
    Chunk("d2", "Fotosinteza este procesul prin care plantele transforma lumina in energie."),
    Chunk("d3", "Mihai Eminescu este considerat poetul national al Romaniei."),
    Chunk("d4", "Apa fierbe la 100 de grade Celsius la presiune atmosferica standard."),
]


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9\u00C0-\u024F]+", text.lower())


def bow_vector(text: str, vocab: List[str]) -> List[float]:
    toks = tokenize(text)
    counts = {w: 0 for w in vocab}
    for t in toks:
        if t in counts:
            counts[t] += 1
    return [float(counts[w]) for w in vocab]


def cosine(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return num / (na * nb)


def retrieve(query: str, corpus: List[Chunk], k: int = 2) -> List[Tuple[Chunk, float]]:
    vocab = sorted({t for c in corpus for t in tokenize(c.text)} | set(tokenize(query)))
    qv = bow_vector(query, vocab)
    scored = [(c, cosine(qv, bow_vector(c.text, vocab))) for c in corpus]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


def generate_answer(question: str, contexts: List[Chunk]) -> str:
    # Generare extractiva naiva: alegem propozitia din context cu suprapunere maxima de cuvinte cu intrebarea.
    q_tokens = set(tokenize(question))
    best_sent, best_score, best_id = "", -1, ""
    for c in contexts:
        for sent in re.split(r"(?<=[.!?])\s+", c.text.strip()):
            s_tokens = set(tokenize(sent))
            score = len(q_tokens & s_tokens)
            if score > best_score:
                best_sent, best_score, best_id = sent, score, c.id
    return f"{best_sent} [sursa: {best_id}]"


if __name__ == "__main__":
    for q in ["Cine a scris Luceafarul?", "Ce este fotosinteza?"]:
        hits = retrieve(q, CORPUS, k=2)
        top = [c for c, _ in hits]
        print(f"Q: {q}")
        print(f"  top-k: {[c.id for c in top]}")
        print(f"  A: {generate_answer(q, top)}\n")
