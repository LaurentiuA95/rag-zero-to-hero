# Modulul 08 - Production RAG

## Obiectiv

Sa iei componentele construite in 00-07 si sa le transformi intr-un sistem care merge **24/7**: cu caching, limite de cost, observabilitate, si protectie PII.

## Preocuparile principale

| Preocupare | Metrica tipica | Instrument |
|-----------|----------------|------------|
| Latenta | p50, p95, p99 ms | tracing (OpenTelemetry) |
| Cost | $ per 1000 query-uri | counter pe tokens in/out |
| Recall | Recall@k, MRR, nDCG | eval pipeline (mod. 06) |
| Faithfulness | % claims grounded | judge/heuristic |
| Securitate | leak PII, prompt injection | redact + whitelist |
| Drift | delta recall vs baseline | monitoring periodic |

## 1. Caching

Doua niveluri:

- **Retrieval cache**: `query_hash -> list[doc_id, score]`. TTL scurt (ore) daca corpus-ul se schimba.
- **LLM cache**: `(prompt_hash) -> response`. TTL lung (zile).

Structura tipica: LRU cu `capacity` fix. Policy: evict cel mai putin recent folosit. Atentie la hash-ul stabil: foloseste `hashlib.sha256` pe un string canonicalizat (JSON sortat).

### LRU: complexitate O(1)

Implementare cu `collections.OrderedDict` e O(1) pentru get/put/evict:

```python
class LRU:
    def __init__(self, capacity):
        self.c = capacity
        self.d = OrderedDict()
    def get(self, k):
        if k not in self.d: return None
        self.d.move_to_end(k)
        return self.d[k]
    def put(self, k, v):
        if k in self.d: self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.c:
            self.d.popitem(last=False)
```

## 2. Token budgeting

Contextul tau are N chunks dar contextul LLM-ului e limitat (iar pretul creste liniar). Strategia: alege greedy cele mai bine clasate chunks pana umpli bugetul.

```
pick = []
used = 0
for c in ranked_chunks:
    tcount = count_tokens(c)
    if used + tcount > budget: continue  # sau break
    pick.append(c)
    used += tcount
```

In curs aproximam token count = `len(text.split())`.

## 3. Observabilitate

Per query, log-eaza (event, latency, status):
- `retrieve_start`, `retrieve_end(n_hits, latency_ms)`
- `rerank_end(latency_ms)`
- `generate_start(prompt_tokens)`, `generate_end(output_tokens, latency_ms)`
- `final(citations, faithfulness_proxy)`

Foloseste structured logging (JSON). In productie, trimite catre un backend (OpenTelemetry, Datadog, Honeycomb).

## 4. PII redaction

Inainte de a pune date in prompt sau in log, redacteaza informatiile sensibile. Tipare simple:
- email: `\w[\w.+-]*@\w+\.\w+`
- telefon (intl): `\+?\d[\d \-().]{6,}\d`
- IBAN: `\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b`

Inlocuire: `<EMAIL>`, `<PHONE>`, `<IBAN>`. Regex-urile sunt conservator false-positive (prind "aproape" tot), dar pentru date structurate e ok.

Atentie: **regex redaction e doar prima linie**; pentru PII la scara, foloseste un tool dedicat (presidio, spaCy NER).

## 5. Securitate - threat model rapid

- **Asset**: raspunsuri corecte, fara leak de date.
- **Atacatori**: user curios, atacator care face prompt injection prin docs, atacator care scraper-eaza API-ul.
- **Surface**:
  - `Documents in corpus` - pot contine prompt injection. Mitigare: sanitizeaza, taie instructiuni.
  - `Prompt template` - poate fi exploatat cu "ignore previous instructions". Mitigare: sandwich defense, filter pe output.
  - `API` - rate limit, auth.
- **Reziduuri**: un atacator determinat cu nr mare de query-uri poate extrage fragmente. Nu pune date secrete in corpus.

## Exercitii in acest modul

1. `LRUCache(capacity)` cu `get(key)` si `put(key, value)` - semantica LRU standard.
2. `TokenBudget(max_tokens)` cu `fit(list[str]) -> list[str]` - pastreaza stringurile in ordine pana la epuizarea bugetului (tokens = `len(s.split())`); sare peste siruri care n-ar incapea si continua.
3. `redact_pii(text) -> str` - redacteaza email si telefon cu regex, inlocuieste cu `<EMAIL>` / `<PHONE>`.
