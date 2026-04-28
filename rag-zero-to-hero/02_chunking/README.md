# Modulul 02 - Chunking

## Obiectiv

Sa stii sa spargi documente lungi in unitati indexabile (`chunks`), stiind de ce alegi o strategie sau alta.

## De ce conteaza

- LLM-urile au **context window** finit. Chiar si la 200k tokens, costul scaleaza liniar.
- Similaritatea cosinus pe **pasaje scurte** e mai precisa decat pe documente intregi: media diluator.
- Chunks **prea mici** pierd contextul si dau raspunsuri fragmentate; **prea mari** diluteaza relevanta si cresc costul.

## Strategii

### 1. Fix size
Imparti stringul in bucati de `N` caractere sau `N` tokens. Simplu, rapid, agnostic la continut. Problema: rupe in mijloc de propozitie.

### 2. Sliding window (cu overlap)
Aceeasi idee dar cu suprapunere de `O` caractere intre chunks consecutive. Cresti recall-ul pentru ca entitatile de la marginea unui chunk apar si in urmatorul.

Parametri tipici: `size = 512 tokens`, `overlap = 64-128 tokens`.

Numar de chunks: `n = ceil((L - overlap) / (size - overlap))`.

### 3. Recursive (aka "structural")
Incerci separatori **in ordine** (ex: `"\n\n"`, `". "`, `" "`). Daca un chunk iese peste `max_chars`, il spargi cu urmatorul separator, recursiv. Pastreaza cat mai mult structura semantica (paragrafe, propozitii).

### 4. Semantic chunking
Imparti textul in propozitii, calculezi embedding pentru fiecare, si unesti propozitii consecutive atat timp cat similaritatea ramane peste un prag. Mai scump (nevoie de embeddings la pre-procesare), dar lucreaza pe granite "topic shift".

### 5. Token-aware + structural
In practica, combini: spargi pe paragrafe, apoi forcezi `max_tokens` cu un tokenizer real (tiktoken, sentencepiece).

## Trade-offs

| Strategie | Cost | Context pastrat | Cand folosesti |
|-----------|------|-----------------|----------------|
| Fix | O(L) | Slab | Baseline rapid, log-uri, cod |
| Sliding | O(L) | Mediu | Text narativ cu entitati-cheie |
| Recursive | O(L log L) amortizat | Bun | Docs tehnice, FAQ, wiki |
| Semantic | O(L) + embeddings | Foarte bun | Continut lung, multi-topic |

## Pitfall-uri

- **Table/cod** tratat ca text natural: rupi sintaxa. Solutie: pre-procesare care extrage tabelele in CSV si codul in blocuri separate.
- **Duplicari**: sliding-window cu overlap produce duplicate aproape-exacte la indexare. Scor post-retrieval poate fi dominat de duplicate. Mitigare: deduplicare cu MinHash/SimHash sau jaccard pe token-set.
- **Chunks prea scurte** (< 50 tokens) primesc embedding slab. Forteaza un `min_len`.

## Exercitii in acest modul

1. `chunk_fixed(text, size)` - imparte in bucati de dimensiune `size`; ultima poate fi mai mica.
2. `chunk_sliding(text, size, overlap)` - sliding window, `overlap < size`; acopera intreg textul.
3. `chunk_recursive(text, max_chars, separators)` - imparte recursiv pana cand niciun chunk nu depaseste `max_chars`. Daca niciun separator nu reduce dimensiunea si chunk-ul e tot prea mare, cazi pe `chunk_fixed` ca fallback.

## Debug tips

- Teste folosesc `size=3, 4, overlap=2` - verifica ca numerotarea ferestrelor porneste de la 0 si se opreste cand `start + size >= len(text)`.
- Pentru recursive: pastreaza separatorul `". "` **cu spatiul**. Nu elimina separatori din text daca nu e necesar; dar asigura-te ca nu ramane whitespace artificial la marginea chunk-urilor (`strip()` la final).
