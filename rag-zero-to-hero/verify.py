"""
Auto-grader pentru RAG Zero to Hero.

Utilizare:
    python verify.py 01          # verifica doar modulul 01
    python verify.py all         # verifica toate modulele in ordine
    python verify.py --status    # afiseaza progresul curent

Conventii:
- Fiecare modul are un folder `NN_*` si un fisier `exercitii.py`.
- Testele sunt deterministe (seed=42 unde se aplica).
- Un modul e considerat "trecut" cand toate assert-urile din check-ul lui trec;
  atunci se scrie `progress/NN.done`.
- Modulul NN+1 e deblocat doar daca `progress/NN.done` exista.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import math
import os
import sys
import traceback
from pathlib import Path
from typing import Callable, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "progress"
PROGRESS.mkdir(exist_ok=True)

MODULES: List[Tuple[str, str]] = [
    ("00", "00_intro"),
    ("01", "01_embeddings"),
    ("02", "02_chunking"),
    ("03", "03_vector_stores"),
    ("04", "04_retrieval"),
    ("05", "05_generation"),
    ("06", "06_evaluation"),
    ("07", "07_advanced_retrieval"),
    ("08", "08_production_rag"),
    ("09", "09_proiect_final"),
]

# ---------- utilitare import ----------

def _load(module_id: str, folder: str):
    """Incarca {folder}/exercitii.py ca modul python izolat."""
    path = ROOT / folder / "exercitii.py"
    if not path.exists():
        raise FileNotFoundError(f"Lipseste fisierul: {path}")
    spec = importlib.util.spec_from_file_location(f"rag_{module_id}", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _require(module, name: str):
    if not hasattr(module, name):
        raise AssertionError(f"Lipseste functia/obiectul `{name}` in exercitii.py")
    return getattr(module, name)


def _close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


# ====================================================================
# CHECKS - cate unul per modul. Intoarce None la success, arunca la fail.
# ====================================================================

def check_00(m):
    greet = _require(m, "greet")
    out = greet("RAG")
    assert isinstance(out, str) and "RAG" in out, "greet('RAG') trebuie sa contina 'RAG'"
    env = _require(m, "check_env")()
    assert isinstance(env, dict) and env.get("python_ok") is True, (
        "check_env() trebuie sa verifice Python >= 3.10 si sa intoarca python_ok=True"
    )


def check_01(m):
    import numpy as np

    cosine = _require(m, "cosine_similarity")
    normalize = _require(m, "l2_normalize")
    top_k = _require(m, "top_k_similar")

    a = np.array([1.0, 0.0, 0.0])
    b = np.array([1.0, 0.0, 0.0])
    c = np.array([0.0, 1.0, 0.0])
    assert _close(float(cosine(a, b)), 1.0), "cosine(a,a) trebuie 1.0"
    assert _close(float(cosine(a, c)), 0.0), "cosine(ortogonali) trebuie 0.0"
    assert _close(float(cosine(a, -a)), -1.0), "cosine(opus) trebuie -1.0"

    v = np.array([3.0, 4.0])
    n = normalize(v)
    assert _close(float(np.linalg.norm(n)), 1.0), "l2_normalize trebuie sa intoarca norma 1"

    query = np.array([1.0, 0.0])
    db = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [-1.0, 0.0]])
    idxs, scores = top_k(query, db, k=2)
    assert list(idxs) == [0, 1], f"top_k indici gresiti: {idxs}"
    assert scores[0] >= scores[1], "top_k trebuie sortat descrescator"


def check_02(m):
    fixed = _require(m, "chunk_fixed")
    sliding = _require(m, "chunk_sliding")
    recursive = _require(m, "chunk_recursive")

    text = "abcdefghij"  # 10 chars
    chunks = fixed(text, size=3)
    assert chunks == ["abc", "def", "ghi", "j"], f"chunk_fixed gresit: {chunks}"

    chunks = sliding(text, size=4, overlap=2)
    # ferestre: [0:4]=abcd, [2:6]=cdef, [4:8]=efgh, [6:10]=ghij
    assert chunks == ["abcd", "cdef", "efgh", "ghij"], f"sliding gresit: {chunks}"

    doc = "Paragraf unu.\n\nParagraf doi are doua propozitii. Asta e a doua.\n\nFinal."
    rc = recursive(doc, max_chars=40, separators=["\n\n", ". ", " "])
    assert all(len(c) <= 40 for c in rc), f"recursive: chunk > 40: {rc}"
    joined = "".join(rc).replace(" ", "")
    assert joined.replace(".", "").replace("\n", "") != "", "recursive nu a produs nimic"
    assert len(rc) >= 2, "recursive trebuie sa sparga documentul"


def check_03(m):
    import numpy as np

    Store = _require(m, "VectorStore")
    s = Store(dim=3)
    s.add("a", np.array([1.0, 0.0, 0.0]), {"lang": "ro"})
    s.add("b", np.array([0.0, 1.0, 0.0]), {"lang": "en"})
    s.add("c", np.array([1.0, 1.0, 0.0]), {"lang": "ro"})

    hits = s.search(np.array([1.0, 0.0, 0.0]), k=2)
    assert hits[0][0] == "a", f"primul hit trebuie sa fie 'a', am primit {hits[0][0]}"

    hits_ro = s.search(np.array([1.0, 0.0, 0.0]), k=3, where={"lang": "ro"})
    ids = [h[0] for h in hits_ro]
    assert set(ids) == {"a", "c"}, f"filtrarea pe metadata gresita: {ids}"

    # dim check
    try:
        s.add("bad", np.array([1.0, 0.0]))
        raise AssertionError("trebuia sa ridice exceptie pentru dim gresit")
    except ValueError:
        pass


def check_04(m):
    docs = [
        "Pisica neagra sta pe acoperis.",
        "Cainele maro alearga in parc.",
        "Pisicile dorm mult.",
        "Parcul este verde si mare.",
    ]
    bm25 = _require(m, "bm25_retrieve")
    rrf = _require(m, "reciprocal_rank_fusion")

    idxs = bm25(docs, "pisica", k=2)
    assert 0 in idxs, f"BM25 ar trebui sa gaseasca doc 0 pentru 'pisica'; idxs={idxs}"

    r1 = [2, 0, 3, 1]
    r2 = [0, 2, 1, 3]
    fused = rrf([r1, r2], k=4)
    assert fused[0] in (0, 2), f"RRF: primul rezultat asteptat 0 sau 2, primit {fused[0]}"
    assert set(fused) == {0, 1, 2, 3}, "RRF trebuie sa includa toate documentele"


def check_05(m):
    build = _require(m, "build_rag_prompt")
    MockLLM = _require(m, "MockLLM")
    answer = _require(m, "answer_with_context")

    ctx = [
        {"id": "doc1", "text": "Soarele este o stea."},
        {"id": "doc2", "text": "Luna orbiteaza Pamantul."},
    ]
    p = build(question="Ce e Soarele?", contexts=ctx)
    assert "Soarele" in p and "doc1" in p, "prompt-ul trebuie sa includa intrebarea si id-urile contextelor"
    assert "Raspunde" in p or "raspunde" in p.lower(), "prompt-ul trebuie sa instruieze LLM sa raspunda"

    llm = MockLLM()
    out = answer("Ce e Soarele?", ctx, llm=llm)
    assert "text" in out and "citations" in out, "answer_with_context trebuie sa intoarca {text, citations}"
    assert any(c == "doc1" for c in out["citations"]), "trebuia citat doc1"


def check_06(m):
    recall_at_k = _require(m, "recall_at_k")
    mrr = _require(m, "mean_reciprocal_rank")
    ndcg = _require(m, "ndcg_at_k")
    faithful = _require(m, "faithfulness_score")

    assert _close(recall_at_k([[1, 2, 3]], [{1}], k=3), 1.0)
    assert _close(recall_at_k([[4, 5, 6]], [{1}], k=3), 0.0)
    assert _close(recall_at_k([[1, 2, 3], [9, 8, 7]], [{1}, {8}], k=3), 1.0)

    # MRR: primul relevant la pozitia 2 -> 1/2
    assert _close(mrr([[9, 1, 2]], [{1}]), 0.5)
    assert _close(mrr([[9, 8, 7]], [{1}]), 0.0)

    # nDCG la k=3 cu un singur relevant pe pozitia 1 => ideal = 1/log2(2) = 1.0
    val = ndcg([[1, 2, 3]], [{1}], k=3)
    assert _close(val, 1.0, tol=1e-6), f"nDCG asteptat 1.0, primit {val}"

    # faithfulness: afirmatii atribuite doar textelor
    ctxs = ["Pisica neagra sta pe acoperis."]
    f = faithful(claims=["Pisica neagra sta pe acoperis."], contexts=ctxs)
    assert _close(f, 1.0), f"faithfulness asteptat 1.0, primit {f}"
    f2 = faithful(claims=["Cainele alearga in parc."], contexts=ctxs)
    assert f2 == 0.0, f"faithfulness asteptat 0.0, primit {f2}"


def check_07(m):
    rerank = _require(m, "cross_encoder_rerank")
    multi = _require(m, "multi_query_expand")
    hyde = _require(m, "hyde_pseudo_doc")

    # rerank-ul folosit in test este un mock: scor = -|len(q)-len(doc)| (deterministic)
    q = "pisica"
    docs = [(0, "lungime mult prea mare ca sa fie relevanta"),
            (1, "pisoi"),
            (2, "pisica")]
    out = rerank(q, docs, k=2)
    assert out[0][0] == 2, f"rerank: top1 asteptat id=2, primit {out[0][0]}"

    qs = multi("Ce e RAG?", n=3)
    assert isinstance(qs, list) and len(qs) >= 3, "multi_query trebuie sa intoarca >=3 variante"
    assert any("RAG" in x for x in qs), "variantele trebuie sa pastreze topicul"

    pseudo = hyde("Ce e RAG?")
    assert isinstance(pseudo, str) and len(pseudo.split()) >= 10, "HyDE: pseudo-doc prea scurt"


def check_08(m):
    Cache = _require(m, "LRUCache")
    TokenBudget = _require(m, "TokenBudget")
    redact = _require(m, "redact_pii")

    c = Cache(capacity=2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)  # evict "b" (a fost accesat recent)
    assert c.get("b") is None, "LRU: b ar fi trebuit evacuat"
    assert c.get("a") == 1 and c.get("c") == 3

    tb = TokenBudget(max_tokens=20)
    kept = tb.fit(["aaaa bbbb", "cccc dddd", "eeee ffff", "gggg hhhh"])  # cuvinte ~ tokens
    # verificam ca nu depaseste bugetul
    total = sum(len(s.split()) for s in kept)
    assert total <= 20, f"TokenBudget a depasit bugetul: {total}"

    red = redact("Emailul meu este laur@example.com si telefon +40 711 222 333.")
    assert "laur@example.com" not in red, "emailul nu a fost redactat"
    assert "711" not in red, "telefonul nu a fost redactat"


def check_09(m):
    Pipeline = _require(m, "RAGPipeline")
    corpus = _require(m, "sample_corpus")()
    pipe = Pipeline.from_corpus(corpus)

    ans = pipe.answer("Cine a scris Luceafarul?")
    assert "text" in ans and "citations" in ans
    assert len(ans["citations"]) >= 1, "pipeline-ul trebuie sa intoarca cel putin o citare"

    # smoke test: raspuns diferit la intrebari diferite
    ans2 = pipe.answer("Ce este fotosinteza?")
    assert ans["text"] != ans2["text"], "pipeline-ul produce acelasi raspuns pentru intrebari diferite"


CHECKS: Dict[str, Callable] = {
    "00": check_00,
    "01": check_01,
    "02": check_02,
    "03": check_03,
    "04": check_04,
    "05": check_05,
    "06": check_06,
    "07": check_07,
    "08": check_08,
    "09": check_09,
}


# ---------- driver ----------

def is_unlocked(module_id: str) -> bool:
    if module_id == "00":
        return True
    prev_idx = [mid for mid, _ in MODULES].index(module_id) - 1
    prev_id = MODULES[prev_idx][0]
    return (PROGRESS / f"{prev_id}.done").exists()


def run_check(module_id: str) -> bool:
    folder = dict(MODULES)[module_id]
    print(f"\n=== Modulul {module_id} ({folder}) ===")
    if not is_unlocked(module_id):
        print(f"BLOCAT. Termina intai modulele anterioare.")
        return False
    try:
        mod = _load(module_id, folder)
        CHECKS[module_id](mod)
    except NotImplementedError as e:
        print(f"FAIL: functie neimplementata: {e}")
        return False
    except AssertionError as e:
        print(f"FAIL: {e}")
        return False
    except Exception:
        print("FAIL: exceptie neasteptata")
        traceback.print_exc()
        return False

    (PROGRESS / f"{module_id}.done").write_text("ok\n")
    print(f"PASS -> progress/{module_id}.done")
    return True


def status() -> None:
    print("Progres RAG Zero to Hero:")
    for mid, folder in MODULES:
        done = (PROGRESS / f"{mid}.done").exists()
        mark = "[x]" if done else ("[ ]" if is_unlocked(mid) else "[-]")
        print(f"  {mark} {mid} {folder}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default="status",
                    help="id modul (ex: 01), 'all' sau 'status'")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status or args.target == "status":
        status()
        return 0

    if args.target == "all":
        for mid, _ in MODULES:
            if not run_check(mid):
                print("\nOpreste-te aici si rezolva modulul curent.")
                status()
                return 1
        status()
        return 0

    if args.target not in CHECKS:
        print(f"Modul necunoscut: {args.target}")
        return 2

    ok = run_check(args.target)
    status()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
