# RAG Zero to Hero

Curs self-paced de Retrieval-Augmented Generation (RAG): de la embeddings si chunking pana la evaluare si RAG in productie. Fiecare modul combina **teorie** (README.md) cu **exercitii auto-evaluate** (`exercitii.py`). Pentru a debloca modulul urmator trebuie sa rezolvi toate exercitiile din modulul curent.

---

## Cum se parcurge cursul

1. Instaleaza dependintele (o singura data):
   ```bash
   pip install -r requirements.txt
   ```
2. Porneste runner-ul interactiv:
   ```bash
   python run.py
   ```
   Runner-ul iti spune la ce modul esti, ruleaza testele si deblocheaza urmatorul modul automat.
3. Alternativ, verifici manual un modul specific:
   ```bash
   python verify.py 01      # verifica modulul 01
   python verify.py all     # verifica toate modulele deblocate
   ```

### Mecanism de progresie

- Fiecare modul `NN_*` are `exercitii.py` cu functii stub marcate cu `raise NotImplementedError(...)`.
- `verify.py` importa `exercitii.py` din fiecare modul si ruleaza teste deterministe (seed fix, tolerante numerice).
- Modulul se **marcheaza trecut** scriind `progress/NN.done`.
- Un modul `NN+1` este accesibil doar daca `progress/NN.done` exista (controlat in `verify.py`).

---

## Continut

| # | Modul | Subiect |
|---|------|---------|
| 00 | `00_intro` | Ce e RAG, arhitectura, setup si sanity checks |
| 01 | `01_embeddings` | Embeddings textuale, similaritate cosinus, normalizare |
| 02 | `02_chunking` | Strategii de chunking: fix, sliding window, recursive, semantic |
| 03 | `03_vector_stores` | Vector store in-memory, indexare, filtrare metadata |
| 04 | `04_retrieval` | BM25, dense, hybrid retrieval, fusion (RRF) |
| 05 | `05_generation` | Prompt engineering pentru RAG, grounding, citari |
| 06 | `06_evaluation` | Metrici: Recall@k, MRR, nDCG, faithfulness, answer relevance |
| 07 | `07_advanced_retrieval` | Re-ranking, query rewriting, HyDE, multi-query |
| 08 | `08_production_rag` | Caching, observabilitate, cost, siguranta, latency |
| 09 | `09_proiect_final` | Proiect final end-to-end cu rubrica de evaluare |

---

## Cerinte

- Python >= 3.10
- ~2 GB spatiu pentru modele de embeddings descarcate local
- Nu ai nevoie de OpenAI/Anthropic API pentru a termina cursul; generarea foloseste un `MockLLM` determinist si, optional, orice HTTP endpoint compatibil.

Vezi [requirements.txt](./requirements.txt).

---

## Reguli de lucru

- **Nu edita `verify.py` ca sa treci testele.** Testele sunt deterministe si eroarea iti spune exact ce lipseste.
- Ruleaza `python run.py` ori de cate ori vrei un rezumat al progresului.
- Daca ramai blocat, citeste sectiunea "Debug tips" din README-ul modulului respectiv.

---

## Structura unui modul

```
NN_nume/
  README.md             # teorie concisa + notatie + trade-offs
  {topic}_fundamentals.py  # exemple runnable ("read & run")
  exercitii.py          # stub-uri de completat; importat de verify.py
```

Progresul tau se salveaza in `progress/*.done`. Pentru reset: `python run.py --reset`.
