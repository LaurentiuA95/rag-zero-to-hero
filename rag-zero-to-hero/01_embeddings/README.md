# Modulul 01 - Embeddings

## Obiectiv

Sa intelegi cum se transforma text in vectori densi si cum se compara acestia prin similaritate cosinus, inclusiv de ce e important sa normalizezi.

## Intuitie

Un encoder textual `f: text -> R^d` mapeaza propozitii in vectori astfel incat textele cu semantica apropiata ajung aproape unul de altul. Exemple tipice: `all-MiniLM-L6-v2` (d=384), `bge-small-en` (d=384), `text-embedding-3-small` (d=1536).

## Similaritatea cosinus

Pentru doi vectori `a, b in R^d`:

```
cos(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

Proprietati: `cos in [-1, 1]`; `1` = identici; `0` = ortogonali; `-1` = opusi. In practica, cei mai multi encoderi produc cos aproape mereu in `[0, 1]` pentru text natural.

### De ce normalizare L2?

Daca salvezi vectori deja normalizati (`||v||_2 = 1`), cos devine simplu **dot product**:

```
cos(a, b) = a . b  (cand ||a|| = ||b|| = 1)
```

Asta e strans legat de cum se implementeaza cautarea in vector stores: un dot product pe batch e o inmultire matriceala eficienta.

## Detaliu numeric

Evita diviziunea cu 0: daca `||v||_2 < eps`, returneaza `v` asa cum e (sau ridica exceptie, functie de politica). In exercitii folosim `eps = 1e-12`.

## Complexitate

- Similaritate `q` vs `N` documente: `O(N * d)` pentru brute force, fara index.
- Cu normalizare prealabila: aceeasi complexitate, dar **fara** costul radacinilor la runtime (le-ai platit la indexare).

## Bune practici

1. **Normalizeaza** embeddings o singura data la indexare.
2. **Salveaza dimensiunea `d`** langa vectori ca sa prinzi mismatch la search.
3. **Pastrati instruction prefix** daca encoder-ul o cere (`passage:` / `query:` pentru E5, BGE). Altfel, pierzi 3-10% pe recall.
4. **Batching**: calculeaza embeddings in batch (batch=32-128) pe CPU, `fp16` pe GPU.

## Pitfall: un embedding nu e "limba-agnostic" automat

Modelele multilingve (`paraphrase-multilingual-MiniLM`, `bge-m3`) au seturi diferite de limbi acoperite. Daca indexezi RO si cauti EN, ai nevoie fie de traducere, fie de model multilingv.

## Exercitii in acest modul

Implementezi in `exercitii.py`:

1. `cosine_similarity(a, b) -> float`
2. `l2_normalize(v) -> np.ndarray` (gestioneaza norma 0)
3. `top_k_similar(query, db, k) -> (indices, scores)` - intoarce sortat descrescator

Nu ai nevoie de model real pentru aceste exercitii: lucrezi pe `np.ndarray` date ca input.

## Debug tips

- Daca `cosine(a, a) != 1` dar e ~`0.9999`, cauza e probabil `float32`. `top_k` foloseste `np.argsort` - atentie la ordinea stabila pe scoruri egale; testele noastre nu lovesc egal.
- `top_k` trebuie sa intoarca `(np.ndarray, np.ndarray)` sau `(list, list)` - ambele merg, testul foloseste `list(...)`.
