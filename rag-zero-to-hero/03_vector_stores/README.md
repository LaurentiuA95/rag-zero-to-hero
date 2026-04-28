# Modulul 03 - Vector stores

## Obiectiv

Sa intelegi contractul minim al unui vector store si sa implementezi unul in memorie cu filtrare pe metadata.

## Contract minimal

Orice vector store expune:

- `add(id, vector, metadata)` - insereaza un vector cu un identificator unic si metadata optionala.
- `search(query, k, where=None)` - intoarce top-k `(id, score, metadata)`, optional filtrat.
- `delete(id)`, `upsert(id, ...)` - opereaza pe id stabil.

Dincolo de contract, diferentele apar la:
- **structura de index**: flat (brute force), IVF, HNSW, PQ
- **distante**: cosinus, dot, L2
- **filtrare**: pre-filter vs post-filter (impact pe recall/latency)
- **durabilitate**: in-memory vs disk vs remote

## Structuri de index (intuitie)

| Index | Recall | Latenta | Memorie | Build | Observatii |
|-------|--------|---------|---------|-------|------------|
| Flat | 1.0 | O(N*d) | O(N*d) | O(1) | Baseline, corect dar lent la N mare |
| IVF | 0.9-0.99 | O(nlist_probe * Nprobe * d) | O(N*d) | O(N) kmeans | Trebuie sa probezi k>1 clustere |
| HNSW | ~0.95-0.99 | O(log N) efectiv | O(N*M) | O(N log N) | Parametri: `M`, `efConstruction`, `efSearch` |
| PQ | 0.5-0.9 | foarte rapid | ~1/16 din flat | O(N) | Cuantizare, pierzi din recall |

Regula generala: **porneste cu flat** (numpy). Treci la HNSW/IVF cand `N > 100k`.

## Filtrare (metadata)

Doua scheme:

- **Pre-filter**: reduci spatiul de cautare la documentele care respecta filtrul, apoi cauti.
  - Pro: nu aduci zgomot.
  - Contra: daca filtrul e agresiv, sub-spatiul poate fi prea mic pentru index-ul aproximativ si recall-ul scade local.
- **Post-filter**: cauti top-K mare, apoi filtrezi.
  - Pro: simplu.
  - Contra: daca filtrul elimina multe, poate sa nu mai ramana `k` rezultate.

Noi vom implementa pre-filter in-memory.

## Distante vs similaritati

Pentru vectori L2-normalizati, `cos(a, b) = a . b`, deci dot product = cosinus. Pentru ne-normalizati, trebuie divizat cu norme. In productie **normalizam la scriere**.

Pentru L2 (distanta euclidiana) pe vectori normalizati: `||a - b||^2 = 2 - 2 a.b`. Similaritatea e `1 - 0.5 * ||a - b||^2`.

## Pitfall-uri

- **Dim mismatch**: index construit pe d=384 primeste query d=768. Arunca exceptie la scriere si la cautare.
- **Id-uri duplicate**: un `add` cu acelasi id trebuie tratat ca upsert (sau respins explicit). Nu lasati duplicate silent.
- **Numerica**: dot product pe `float16` poate pierde precizie. Foloseste `float32` pentru scoring.

## Exercitii in acest modul

Implementezi clasa `VectorStore`:

```python
class VectorStore:
    def __init__(self, dim: int): ...
    def add(self, id: str, vector: np.ndarray, metadata: dict | None = None) -> None: ...
    def search(self, query: np.ndarray, k: int, where: dict | None = None) -> list[tuple[str, float, dict]]: ...
```

Cerinte:
- Scor = cosinus (pe date normalizate implicit sau calculat explicit).
- `add` ridica `ValueError` daca `vector.shape[-1] != self.dim`.
- `where` e un dict `{camp: valoare}`; filtrul e pre-filter, egalitate stricta pe fiecare cheie.

## Debug tips

- Nu uita ca `where` poate fi `None` sau `{}` - ambele cazuri = fara filtru.
- Intoarce `[]` daca nu exista nicio intrare care respecta filtrul, nu arunca.
- Pastreaza o ordine deterministica (ex: `id` ascendent) la egalitate de scor, dar testul e construit sa nu produca scoruri egale.
