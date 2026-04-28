"""
Exercitii modulul 09 - Proiect final RAG end-to-end.

Livrabil:
  - sample_corpus() -> list[dict]: cel putin 6 documente pe >= 2 subiecte
  - class RAGPipeline:
        @classmethod
        def from_corpus(cls, corpus: list[dict]) -> "RAGPipeline"
        def answer(self, question: str) -> dict   # {"text": ..., "citations": [...]}

Constrangeri:
  - Citations nevid pentru query-urile din verify.py.
  - Raspunsuri diferite pentru intrebari pe subiecte diferite.

Hint: ai voie sa folosesti MockLLM-ul din modulul 05 si componentele din 02-08.
Te poti uita in `template_proiect.py` pentru cum sa incarci module din alt folder.
"""
from __future__ import annotations

from typing import Dict, List


def sample_corpus() -> List[Dict]:
    """Intoarce un corpus mic cu >= 6 documente pe >= 2 subiecte.

    Format: [{"id": str, "text": str}, ...]
    """
    # TODO
    raise NotImplementedError


class RAGPipeline:
    def __init__(self, *args, **kwargs):
        # TODO: stocheaza componente (index, llm, etc.)
        raise NotImplementedError

    @classmethod
    def from_corpus(cls, corpus: List[Dict]) -> "RAGPipeline":
        # TODO: construieste pipeline-ul din corpus
        raise NotImplementedError

    def answer(self, question: str) -> Dict:
        # TODO: retrieval -> prompt -> LLM -> parse -> {"text", "citations"}
        raise NotImplementedError


if __name__ == "__main__":
    p = RAGPipeline.from_corpus(sample_corpus())
    print(p.answer("Cine a scris Luceafarul?"))
    print(p.answer("Ce este fotosinteza?"))
