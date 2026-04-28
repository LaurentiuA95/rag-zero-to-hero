"""
Exercitii modulul 05 - Generation.

Implementeaza:

  1. build_rag_prompt(question: str, contexts: list[dict]) -> str
     - contexts: fiecare element are cheile "id" si "text"
     - prompt-ul trebuie sa includa:
         * instructiunea (contine cuvantul "raspunde" si "doar pe baza contextului" sau echivalent)
         * fiecare context sub forma `[id] text`
         * intrebarea
         * un indicator de format (ex: "Raspuns:", "format JSON", etc.)

  2. class MockLLM cu metoda .complete(prompt: str) -> str
     - extrage contextele din prompt
     - extrage intrebarea din prompt
     - alege contextul cu overlap lexical maxim cu intrebarea
     - intoarce un string care contine un extras din context + citarea `[id]`

  3. answer_with_context(question: str, contexts: list[dict], llm) -> dict
     - construieste prompt-ul, apeleaza llm.complete(prompt), parseaza rezultatul
     - intoarce: {"text": <raspuns>, "citations": <lista id-uri citate>}
     - citations se extrage cu regex din raspuns: patternul este [id]
"""
from __future__ import annotations

import re
from typing import Dict, List


def build_rag_prompt(question: str, contexts: List[Dict]) -> str:
    """Construieste un prompt pentru RAG."""
    # TODO
    raise NotImplementedError


class MockLLM:
    """LLM determinist pentru exercitii. NU face generare reala."""

    def complete(self, prompt: str) -> str:
        # TODO: parseaza, alege contextul cu overlap maxim, intoarce <text> [id]
        raise NotImplementedError


def answer_with_context(question: str, contexts: List[Dict], llm) -> Dict:
    """Construieste prompt, apeleaza llm.complete, intoarce {text, citations}."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    ctx = [
        {"id": "doc1", "text": "Soarele este o stea."},
        {"id": "doc2", "text": "Luna orbiteaza Pamantul."},
    ]
    print(build_rag_prompt("Ce e Soarele?", ctx))
    print(answer_with_context("Ce e Soarele?", ctx, MockLLM()))
