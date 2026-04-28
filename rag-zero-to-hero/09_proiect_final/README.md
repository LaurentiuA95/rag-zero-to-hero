# Modulul 09 - Proiect final

## Obiectiv

Sa integrezi tot ce ai construit in 00-08 intr-un sistem RAG end-to-end, pe un corpus mic, cu evaluare automatizata.

## Ce livrezi

Un fisier `exercitii.py` care expune:

1. `sample_corpus() -> list[dict]`
   - Intoarce un corpus cu cel putin 6 documente. Fiecare doc are `{"id": str, "text": str}`.
   - Corpus-ul trebuie sa acopere cel putin doua subiecte distincte (de ex: istorie/literatura + stiinta).

2. `class RAGPipeline`
   - metoda de clasa: `RAGPipeline.from_corpus(corpus: list[dict]) -> RAGPipeline`
     construieste pipeline-ul: chunking (optional), indexare (vector store in-memory sau BM25), LLM mock.
   - metoda: `answer(question: str) -> dict` cu cheile `"text"` si `"citations"`.

## Criterii automatizate (din `verify.py`)

- `answer(...)` intoarce un dict cu `"text"` si `"citations"`.
- `citations` este nevid pentru query-urile de test.
- Raspunsuri **diferite** pentru intrebari pe subiecte diferite.

## Rubrica (pentru evaluare manuala / nota)

| Criteriu | Greutate | Ce verifici |
|----------|---------:|-------------|
| Corectitudine functionala | 30% | `answer` ruleaza, produce citari valide |
| Calitate retrieval | 20% | top-k contine docs cu raspunsul; Recall@3 >= 0.8 |
| Calitate raspuns | 20% | faithfulness proxy >= 0.9 pe test set |
| Modularitate cod | 15% | componente clare: Chunker, Index, Retriever, LLM, Orchestrator |
| Observabilitate | 10% | logging structurat, latente per etapa |
| Tests | 5% | pytest pentru componente critice |

## Arhitectura sugerata

```
RAGPipeline
  ├── corpus: list[dict]
  ├── chunker: functie (str -> list[str])   # recursive din modulul 02
  ├── index: VectorStore + BM25              # modulele 03 + 04
  ├── retriever.search(q, k)                 # hybrid + RRF
  ├── reranker (optional)                    # modulul 07
  ├── llm: MockLLM                           # modulul 05
  ├── generator.answer(q, ctx) -> dict       # build_rag_prompt + parse citations
  └── logger (structured)                    # modulul 08
```

Pentru proiect foloseste **componentele pe care le-ai scris tu** in modulele 02-08.

## Cum ruleaza verify.py

```python
Pipeline = _require(m, "RAGPipeline")
corpus = _require(m, "sample_corpus")()
pipe = Pipeline.from_corpus(corpus)

ans = pipe.answer("Cine a scris Luceafarul?")
# asteapta: dict cu "text" si "citations" (lista nevida)

ans2 = pipe.answer("Ce este fotosinteza?")
# asteapta: raspuns DIFERIT de cel de mai sus
```

## Extras (optional)

- Adauga un re-ranker cu `sentence-transformers/ms-marco-...`
- Evalueaza end-to-end cu metrici din modulul 06 pe un `eval_set.jsonl`
- Adauga o UI simpla (streamlit) pentru demo
- Inlocuieste MockLLM cu un LLM real (Anthropic/OpenAI/Ollama local)

## Debug tips

- Pastreaza totul in-memory (fara ChromaDB/FAISS) pana treci verify.py, apoi extinde.
- Daca `citations` iese gol, problema e la regex-ul din `answer_with_context`; pune `[doc_id]` la sfarsitul oricarui raspuns generat.
- Retrieval-ul hibrid se intampla pe indici (nu pe text): iti trebuie un `id -> text` map stabil.
