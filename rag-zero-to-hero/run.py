"""
Runner interactiv pentru RAG Zero to Hero.

Utilizare:
    python run.py            # reia de la primul modul netrecut
    python run.py --reset    # sterge tot progresul (progress/*.done)
    python run.py --status   # echivalent cu `python verify.py --status`
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "progress"
PROGRESS.mkdir(exist_ok=True)

MODULES = [
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


def next_pending() -> str | None:
    for mid, _ in MODULES:
        if not (PROGRESS / f"{mid}.done").exists():
            return mid
    return None


def reset() -> None:
    n = 0
    for p in PROGRESS.glob("*.done"):
        p.unlink()
        n += 1
    print(f"Progres resetat ({n} fisiere sterse).")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.reset:
        reset()
        return 0
    if args.status:
        return subprocess.call([sys.executable, str(ROOT / "verify.py"), "status"])

    mid = next_pending()
    if mid is None:
        print("Toate modulele sunt trecute. Felicitari.")
        return subprocess.call([sys.executable, str(ROOT / "verify.py"), "status"])

    folder = dict(MODULES)[mid]
    readme = ROOT / folder / "README.md"
    print("=" * 60)
    print(f"Urmatorul modul: {mid} - {folder}")
    print(f"Citeste:   {readme}")
    print(f"Editeaza:  {ROOT / folder / 'exercitii.py'}")
    print("Apoi ruleaza:")
    print(f"    python verify.py {mid}")
    print("=" * 60)
    sys.stdout.flush()
    return subprocess.call([sys.executable, str(ROOT / "verify.py"), mid])


if __name__ == "__main__":
    sys.exit(main())
