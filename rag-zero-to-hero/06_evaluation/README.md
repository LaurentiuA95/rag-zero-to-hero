# Modulul 06 - Evaluation

## Obiectiv

Sa stii sa evaluezi cele doua componente ale unui RAG, **retrieval** si **generare**, cu metrici deterministe.

## Partea 1: Evaluarea retrieval-ului

Pentru un set `(query_i, relevant_i)` si sistemul intoarce un ranking `R_i`:

### Recall@k
Procentul de query-uri pentru care cel putin un document relevant apare in top-k.

```
Recall@k = (1/Q) * sum_i [any(d in top_k(R_i) for d in relevant_i)]
```

Simpla si robusta. Nu tine cont de ordinea in top-k.

### Precision@k
```
Precision@k = (1/Q) * sum_i |top_k(R_i) intersect relevant_i| / k
```

### Mean Reciprocal Rank (MRR)

Pentru primul document relevant la pozitia `r_i` (1-indexed):
```
MRR = (1/Q) * sum_i (1 / r_i)    [0 daca nu apare in top-k]
```

Penalizeaza rangurile mari. Bun pentru Q&A unde ne intereseaza sa avem raspunsul primul.

### nDCG@k

DCG tine cont de **gradul de relevanta** (0/1, sau 0..N) si de pozitie:

```
DCG@k = sum_{i=1..k} (2^rel_i - 1) / log2(i + 1)
IDCG@k = DCG@k pe rankingul ideal
nDCG@k = DCG@k / IDCG@k   (in [0, 1])
```

In curs folosim relevante binare (`rel ∈ {0, 1}`), deci `2^rel - 1 ∈ {0, 1}` si DCG devine suma de `1 / log2(i+1)` pe pozitiile cu relevant.

### Convention 1-indexed

In literatura, formulele sunt **1-indexed** (primul rezultat = pozitia 1). Atentie la implementare: `log2(1+1) = 1` la prima pozitie.

## Partea 2: Evaluarea raspunsului

### Faithfulness (grounding)

"Toate afirmatiile din raspuns au suport in contextele retrieved?"

```
faithfulness = |claims acoperite de context| / |claims total|
```

In practica: spargi raspunsul in propozitii-claims, pentru fiecare verifici (cu un LLM judge) daca e implicat de context. In curs folosim un proxy simplu: **inclusiune de string** (claim ⊆ concatenarea contextelor, dupa lower-case si normalizare whitespace).

### Answer relevance

"Raspunsul adreseaza efectiv intrebarea?" Variante:
- LLM-as-judge (cost, bias, variance).
- Embedding similarity intre intrebare si raspuns.
- ROUGE/BLEU vs un raspuns aur (nevoie de ground truth).

### Context relevance

"Contextele retrieved sunt utile pentru intrebare?" Poate fi evaluat cu recall@k pe seturi anotate sau cu LLM judge.

## Protocol reproducibil

- **Dataset cu ground truth**: un JSONL cu `{query, relevant_doc_ids, gold_answer?}`.
- **Seeds fixe** la orice componenta stohastica.
- **Split-uri**: dev pentru tuning, test pentru final; **nu** selecta modele pe test.
- **Confidence intervals**: bootstrap pe query-uri (n=1000 resample).
- **Ablatii**: modifica un singur parametru odata (k, chunker, encoder, prompt).
- **Raporteaza** media + interval de incredere 95%, nu doar punct.

## Exercitii in acest modul

1. `recall_at_k(rankings, relevants, k) -> float`
   - `rankings`: list[list[int]], `relevants`: list[set[int]].
2. `mean_reciprocal_rank(rankings, relevants, k=None) -> float`
   - Rang 1-indexed. `k=None` = fara taiere.
3. `ndcg_at_k(rankings, relevants, k) -> float`
   - Relevante binare (set-uri).
4. `faithfulness_score(claims, contexts) -> float`
   - Proxy: inclusiune string normalizata (lower-case + whitespace collapse).

## Debug tips

- nDCG: asigura-te ca `log2(i+1)` e cu `i` de la 1, nu 0.
- La IDCG, toate pozitiile relevante ideal sunt la inceput: primul relevant pe pozitia 1, etc. Pentru binary, IDCG@k cu m relevanti este `sum_{i=1..min(k,m)} 1/log2(i+1)`. Daca `m=0`, IDCG=0 si intoarce 0.
- faithfulness: normalizeaza spatiile inainte de `in` (ex: `re.sub(r"\s+", " ", ...).lower()`).
