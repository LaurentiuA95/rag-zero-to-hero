# Modulul 07 - Advanced retrieval

## Obiectiv

Sa stapanesti cele trei tehnici care imbunatatesc cel mai mult RAG-ul in practica: re-ranking, multi-query expansion si HyDE (Hypothetical Document Embeddings).

## 1. Re-ranking

Ideea: retrieval-ul aduce `K` candidati (ex: K=50) si un **cross-encoder** (BERT-based) calculeaza un scor de relevanta pentru fiecare pereche `(query, doc)`. Apoi pastrezi top-k (ex: k=5).

Cross-encoder vs bi-encoder:

| | Bi-encoder (retrieval) | Cross-encoder (rerank) |
|---|------------------------|------------------------|
| Arhitectura | encodeaza query si doc separat | concatenare `[CLS] q [SEP] d` |
| Cost | O(1) per query (vectori precomputati) | O(K) per query (forward pass pe fiecare candidat) |
| Recall | mic la `k` mic | N/A (ia candidatii produsi de retriever) |
| Precision | mediu | foarte bun |

Modele tipice: `cross-encoder/ms-marco-MiniLM-L-6-v2`, `bge-reranker-base`. Cost: ~5-50ms per query pe CPU, ~1ms pe GPU.

### Pattern practic

```
retrieve(K=50) -> rerank(k=5) -> prompt_LLM(k=5)
```

In curs folosim un **rerank mock** determinist: scorul e `-|len(query) - len(doc)|`. Conceptul ramane acelasi; in productie swap-uiesti clasa.

## 2. Multi-query expansion

Ideea: o intrebare poate fi formulata in mai multe moduri. Cere LLM-ului sa genereze 3-5 **parafraze** ale intrebarii, face retrieval pentru fiecare, fuzioneaza (RRF) si pastreaza top-k.

Beneficiu: creste recall-ul cu 5-20% pe query-uri ambigue, cost ~3x la retrieval (neglijabil comparativ cu generarea).

Exemplu:
```
"Ce e RAG?" ->
  - "Defineste retrieval-augmented generation."
  - "RAG - ce inseamna?"
  - "Cum functioneaza retrieval-augmented generation?"
```

## 3. HyDE (Hypothetical Document Embeddings)

Intrebarea si documentul **nu sunt in acelasi spatiu semantic**: intrebarea e scurta si formulata interogativ, documentul e afirmativ. Encoder-ul vede similar doar intrebari similare.

HyDE rezolva asta: cere LLM-ului sa genereze un **pseudo-document** ("raspunde la intrebarea asta") si il foloseste ca query pentru embedding. Documentul real din corpus va avea embedding mai aproape de pseudo-doc decat de intrebare.

Pattern:
```
question -> LLM -> pseudo_doc -> embed(pseudo_doc) -> retrieve
```

Cost: un call LLM extra per query. Castig tipic: 3-10% recall.

Limite: pseudo-doc poate halucina informatii care **nu exista** in corpus; daca tipic raspunsul e "nu stiu", HyDE iti face rau.

## Combinari utile

```
query
  -> multi-query (N=3) -> retrieve_bm25 + retrieve_dense (K=50 each)
  -> RRF fusion
  -> rerank (k=5)
  -> prompt
```

Aceasta pipeline acopera 90% din imbunatatirile pe benchmark-uri publice (BEIR, MTEB).

## Exercitii in acest modul

1. `cross_encoder_rerank(query: str, candidates: list[tuple[int, str]], k: int) -> list[tuple[int, str]]`
   - Returneaza top-k candidati dupa scorul mock `-|len(query) - len(doc)|`.
   - Sortare descrescatoare dupa scor; la egalitate, stabil dupa ordinea originala.

2. `multi_query_expand(question: str, n: int) -> list[str]`
   - Intoarce `n` variante. Pentru exercitiu, e ok sa fie euristice:
       * intrebarea originala
       * "Defineste: " + question
       * "Ce inseamna " + ... etc.
   - Testul verifica `len >= n` si ca variantele pastreaza topicul (contin tokens din intrebare).

3. `hyde_pseudo_doc(question: str) -> str`
   - Construieste un string declarativ care ar putea fi raspuns la intrebare.
   - Testul verifica `len(split()) >= 10` (pseudo-doc nontrivial).
