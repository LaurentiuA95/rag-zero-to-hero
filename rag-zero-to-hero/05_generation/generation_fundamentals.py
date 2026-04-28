"""
Fundamentals: prompt building + MockLLM determinist + parser.
"""
from __future__ import annotations

import re
from typing import Dict, List


PROMPT_TMPL = """Esti asistent. Raspunde doar pe baza contextului de mai jos.
Daca raspunsul nu este in context, raspunde "Nu stiu".
Citeaza sursele prin id-urile lor in paranteze patrate, ex: [doc1].

Context:
{context}

Intrebare: {question}

Raspuns (o singura propozitie, urmata de citare [id]):"""


def build_prompt(question: str, contexts: List[Dict]) -> str:
    ctx = "\n".join(f"[{c['id']}] {c['text']}" for c in contexts)
    return PROMPT_TMPL.format(context=ctx, question=question)


_CTX_RE = re.compile(r"\[(\w+)\]\s*([^\[]+)")


def _parse_contexts(prompt: str) -> List[Dict]:
    block = prompt.split("Context:\n", 1)[-1].split("\nIntrebare:", 1)[0]
    return [{"id": m.group(1), "text": m.group(2).strip()} for m in _CTX_RE.finditer(block)]


def _parse_question(prompt: str) -> str:
    m = re.search(r"Intrebare:\s*(.+?)\n", prompt)
    return m.group(1).strip() if m else ""


def _tok(s: str) -> set:
    return set(re.findall(r"[\w]+", s.lower()))


class MockLLM:
    def complete(self, prompt: str) -> str:
        ctxs = _parse_contexts(prompt)
        q = _parse_question(prompt)
        qt = _tok(q)
        if not ctxs:
            return "Nu stiu."
        best = max(ctxs, key=lambda c: len(qt & _tok(c["text"])))
        # prima propozitie din context + citare
        first_sent = re.split(r"(?<=[.!?])\s+", best["text"].strip())[0]
        return f"{first_sent} [{best['id']}]"


if __name__ == "__main__":
    ctx = [
        {"id": "doc1", "text": "Soarele este o stea."},
        {"id": "doc2", "text": "Luna orbiteaza Pamantul."},
    ]
    p = build_prompt("Ce e Soarele?", ctx)
    print(p)
    print("LLM:", MockLLM().complete(p))
