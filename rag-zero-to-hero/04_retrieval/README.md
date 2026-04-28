# Modulul 04 - Retrieval

## Obiectiv

Sa intelegi cele trei strategii de retrieval (sparse, dense, hybrid) si cum sa combini rezultatele cu Reciprocal Rank Fusion.

## Sparse (BM25)

BM25 = TF-IDF cu doua corectii: saturatie (k1) si normalizare pe lungime (b). Scor pentru un termen `t` intr-un doc `d`:

```
score(d, t) = IDF(t) * (f(t, d) * (k1 + 1)) / (f(t, d) + k1 * (1 - b + b * |d|/avgdl))
```

- `f(t, d)` = frecventa termenului `t` in `d`
- `|d|` = lungimea doc-ului (in tokens)
- `avgdl` = media pe corpus
- `k1 ~ 1.2-2.0`, `b ~ 0.75`

Puncte tari: rapid, zero setup, excelent pentru match lexical exact (nume, coduri, acronime).
Puncte slabe: zero semantica; "doctor" si "medic" nu sunt echivalenti fara lematizare.

## Dense

Folosesti un encoder textual (modulul 01) si cauti in vector store (modulul 03). Avantaj: prinzi sinonime si parafraze. Dezavantaj: rateaza match-uri exacte pe termeni rari care n-au fost vazuti in training.

## Hybrid

Combina scorurile sparse si dense. Doua scheme comune:

### 1. Linear combination
```
score_final = alpha * score_dense + (1 - alpha) * score_sparse_normalized
```
Problema: scorurile BM25 si cos sunt pe scale diferite; trebuie normalizate (min-max, z-score). Delicat.

### 2. Reciprocal Rank Fusion (RRF)

Nu combini scoruri, combini **ranguri**. Pentru un document `d` care apare pe pozitia `r_i` intr-unul din cele `L` liste:

```
RRF(d) = sum_i 1 / (k + r_i)
```

`k = 60` e default in literatura. Robust: scala-agnostic, usor de implementat.

Avantaj major: nu ai nevoie de un parametru `alpha` care depinde de corpus.

## Comparatie rapida

| Strategie | Pro | Contra | Setup |
|-----------|-----|--------|-------|
| BM25 | rapid, fara model | fara semantica | Lowercase + tokenize |
| Dense | semantica | model + vector index | Encoder + store |
| Hybrid (RRF) | best of both | cost 2x la retrieval | amandoua |

## Exercitii in acest modul

1. `bm25_retrieve(docs, query, k) -> list[int]` - folosind `rank_bm25.BM25Okapi` (sau implementare proprie), intoarce indicii top-k.
2. `reciprocal_rank_fusion(rankings, k=60)` - dand o lista de liste de indici, intoarce o lista finala de indici ordonati dupa scor RRF descendent.

Note:
- Tokenizarea in BM25: lowercase + split pe cuvinte. Pentru corpusul de test, `text.lower().split()` e suficient.
- In RRF, documentele care apar doar intr-o lista au scor mai mic decat cele care apar in toate - asa trebuie.

## Debug tips

- `rank_bm25.BM25Okapi` primeste lista de liste de tokens la init: `BM25Okapi([["pisica", "neagra", ...], ...])`.
- `get_scores(query_tokens)` intoarce scoruri pe toate documentele.
- Pentru RRF, foloseste un `dict[int, float]` acumulator si sorteaza la final.
