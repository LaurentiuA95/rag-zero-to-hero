# Modulul 00 - Introducere in RAG

## Obiectiv

Sa intelegi **ce problema rezolva RAG** si sa ai un mediu Python functional pentru restul cursului.

## Ce este RAG?

**Retrieval-Augmented Generation** este un pattern in care un LLM raspunde folosind context extras dintr-o baza de cunostinte externa, nu doar greutatile modelului. Scopuri principale:

1. **Actualizare fara re-training** - cunostinte noi sunt indexate, nu invatate.
2. **Atribuire** - raspunsul poate cita sursele.
3. **Reducerea halucinatiilor** - modelul e ghidat sa foloseasca textul furnizat.
4. **Cost** - documentele tale raman in vector store; in prompt merg doar cele relevante.

## Arhitectura minimala

```
    (documente)
        |
        v
  [ chunking ] --> [ embeddings ] --> [ vector store ]
                                               ^
                                               |
  query  --> [ embed(query) ] ------------------+ retrieve top-k
                                               |
                                               v
                                        [ prompt + context ]
                                               |
                                               v
                                           [  LLM  ]
                                               |
                                               v
                                       raspuns + citari
```

Fiecare cutie e un modul separat in curs.

## Glosar minimal

- **Chunk**: fragment de text (propozitii, paragrafe, sliding window) cu dimensiune controlata.
- **Embedding**: vector dens `R^d` care aproximeaza semantica textului; apropierea in spatiu ≈ similaritate semantica.
- **Retriever**: componenta care, pentru un query, intoarce top-k chunks relevante (BM25, dense, hibrid).
- **Grounding**: constrangerea LLM-ului sa raspunda **doar** pe baza contextului furnizat.
- **Citare**: identificator al sursei (ex: `doc1#chunk3`) atasat raspunsului.

## Trade-offs pe scurt

| Dimensiune | Creste ... daca ... | Scade ... daca ... |
|-----------|--------------------|--------------------|
| Recall | chunks mai mari, k mai mare, hibrid | chunks prea mici, index prost |
| Precizie | re-ranker, filtre metadata | chunks amestecate, k prea mare |
| Latenta | k mare, re-ranker, LLM mare | cache, k mic, modele mici |
| Cost | context lung, LLM mare | chunks scurte, cache, model mic |
| Faithfulness | grounding strict, citari obligatorii | prompt permisiv |

## Ce vei face in acest modul

1. Verifici versiunea de Python (>= 3.10).
2. Implementezi doua functii utilitare.
3. Rulezi `python verify.py 00` - daca trece, se deblocheaza modulul 01.

## Debug tips

- Daca `pip install -r requirements.txt` esueaza pe `torch`, foloseste `pip install torch --index-url https://download.pytorch.org/whl/cpu`.
- Daca `sentence-transformers` incearca sa descarce modele si nu ai internet, ruleaza modulele 00-04 fara el; apare ca dependinta abia din modulul 01 (optional).

## Urmatorul pas

Editeaza `exercitii.py`, ruleaza `python verify.py 00`.
