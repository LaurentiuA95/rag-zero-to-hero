"""
Template de pornire pentru proiectul final.

Pasi sugerati:
  1. Importa componentele scrise de tine in modulele anterioare.
  2. Intr-o functie sample_corpus(), intoarce o lista de documente (dict cu "id", "text").
  3. In clasa RAGPipeline:
       - __init__ primeste index + llm
       - from_corpus(corpus) construieste totul
       - answer(question) face retrieval + generation si intoarce {text, citations}
  4. Ruleaza `python verify.py 09`.

Nota: poti copia functiile direct in 09_proiect_final/exercitii.py sau le poti importa
din module anterioare folosind importlib.
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent.parent


def _load(folder: str):
    path = ROOT / folder / "exercitii.py"
    spec = importlib.util.spec_from_file_location(folder, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[folder] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def example_skeleton() -> None:
    """Exemplu de cum iti poti construi clasa RAGPipeline."""
    m03 = _load("03_vector_stores")
    m04 = _load("04_retrieval")
    m05 = _load("05_generation")

    VectorStore = m03.VectorStore
    bm25_retrieve = m04.bm25_retrieve
    MockLLM = m05.MockLLM
    # etc.

    print("Store dim init:", VectorStore)
    print("BM25 callable:", callable(bm25_retrieve))
    print("MockLLM class:", MockLLM)


if __name__ == "__main__":
    example_skeleton()
