# Modulul 05 - Generation

## Obiectiv

Sa construiesti un prompt corect pentru RAG si sa transformi contextul retrieved intr-un raspuns cu **citari explicite**, fara halucinatie.

## Anatomia unui prompt RAG

Un prompt de calitate are patru zone distincte:

1. **System / instructiune**: regulile jocului. "Raspunde doar folosind contextul. Daca nu stii, spune ca nu stii. Citeaza sursa prin id."
2. **Context**: bucatile retrieved, fiecare cu `id` si text. **Intotdeauna** pune id-ul langa text, altfel modelul nu are de unde cita.
3. **Intrebare**: intrebarea utilizatorului.
4. **Format de iesire**: JSON strict sau markdown cu sectiuni ("Raspuns" + "Surse"). JSON e mai parsabil.

Exemplu minimal:

```
Esti asistent. Raspunde doar pe baza contextului de mai jos.
Daca raspunsul nu e in context, spune "Nu stiu".
Citeaza sursele prin id-ul lor.

Context:
[doc1] Soarele este o stea.
[doc2] Luna orbiteaza Pamantul.

Intrebare: Ce e Soarele?

Raspuns (format JSON): {"text": ..., "citations": ["doc1", ...]}.
```

## Grounding: de ce e greu

LLM-urile au knowledge prior puternic. Daca intrebi ceva din prior (ex: "Cine a scris Luceafarul?") modelul poate raspunde **fara sa foloseasca contextul**, ignorandu-l. Solutii:

- **Instructiune stricta**: "Raspunde doar pe baza contextului; altfel spune 'Nu stiu'."
- **Verificare post-hoc**: la rescrie, intreaba modelul "marcheaza in citat orice afirmatie care nu are acoperire in context".
- **Contrastiv**: adauga un context "capcana" care contine informatie falsa si verifica ca modelul o urmeaza strict (pentru a detecta leakage din prior).

## Citari

Politica minima: **fiecare afirmatie** trebuie atribuita unui id din context. La generare:
- Format `[doc_id]` imediat dupa afirmatie, sau
- Lista `"citations": [...]` in iesirea structurata.

Pe partea de evaluare (modulul 06), faithfulness = `|claims acoperiti| / |claims total|`.

## MockLLM

In curs folosim un `MockLLM` determinist. Scop: exercitiile sa ruleze fara API keys si fara nedeterminism. In productie, inlocuiesti cu orice client (OpenAI, Anthropic, local vLLM, etc.).

`MockLLM.complete(prompt)` trebuie sa:
- Extraga din prompt contextele sub forma `[id] text` (parse simplu).
- Aleaga contextul care are **overlap lexical maxim** cu intrebarea (dupa tokenizare lower-case).
- Intoarca un string sub forma `<propozitie preluata din context> [id]`.

Aceasta e o implementare extractiva; nu "genereaza" fraze noi, dar modeleaza comportamentul corect "grounded" si imi permite sa testez `answer_with_context`.

## Parametri LLM utili pentru RAG

- **Temperature**: 0.0-0.3 pentru raspunsuri factuale.
- **Max tokens**: limiteaza in functie de buget.
- **Stop tokens**: `"\n\n"` pentru a evita divagatii.
- **Seed**: pentru reproducibilitate (daca API-ul suporta).

## Exercitii in acest modul

1. `build_rag_prompt(question, contexts) -> str`
   - `contexts`: list[dict] cu cheile `"id"`, `"text"`.
   - Prompt-ul trebuie sa contina: instructiunea, fiecare context marcat cu `[id]`, intrebarea, si un format de raspuns.

2. `MockLLM` cu metoda `.complete(prompt: str) -> str`
   - Parseaza prompt-ul (extrage contexte + intrebare), alege contextul cu overlap maxim, intoarce string-ul.

3. `answer_with_context(question, contexts, llm) -> dict`
   - Construieste prompt-ul, apeleaza `llm.complete(...)`, parseaza iesirea intr-un dict `{"text": ..., "citations": [...]}`.

## Debug tips

- In prompt, pune id-urile in paranteze patrate: `[doc1]`. Parsing-ul devine trivial.
- MockLLM poate folosi regex `re.findall(r"\[(\w+)\]\s*([^\[]+)", prompt)` pentru a extrage contexte.
- Asigura-te ca intrebarea e clar delimitata in prompt (ex: `Intrebare: ...`).
