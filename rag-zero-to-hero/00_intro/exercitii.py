"""
Exercitii modulul 00 - Intro & setup.

Scop: sa validam ca ai mediul Python functional si sa-ti pui mana pe "stub + check".
"""
from __future__ import annotations

import sys
from platform import python_version
from typing import Dict


# -----------------------------------------------------------------
# Exercitiul 1: greet(nume) -> str
# -----------------------------------------------------------------
# Cerinta: sa intoarca un string care contine `nume` si cuvantul "RAG".
# Exemplu: greet("Ana") -> "Salut Ana, bine ai venit la cursul RAG!"
# -----------------------------------------------------------------

def greet(name: str) -> str:
    """Intoarce un mesaj de salut care contine `name` si "RAG"."""
    # TODO: inlocuieste linia urmatoare cu o implementare valida.
    return f"Hello, {name}RAG!"
    raise NotImplementedError("Implementeaza greet(name).")


# -----------------------------------------------------------------
# Exercitiul 2: check_env() -> dict
# -----------------------------------------------------------------
# Cerinta: intoarce un dict cu cel putin cheile:
#   - "python_version": str (ex: "3.11.4")
#   - "python_ok": bool  (True daca versiunea >= 3.10)
# Hint: foloseste sys.version_info.
# -----------------------------------------------------------------

def check_env() -> Dict[str, object]:
    """Intoarce {"python_version": str, "python_ok": bool}."""
    # TODO: implementeaza.
    py_ver_min = sys.version_info.minor
    py_ver_maj = sys.version_info.major
    if py_ver_maj>= 3 and py_ver_min>= 10:
        return{'python_ok': True}
    else:
        return{'python_ok': False}
    return {"python_version": sys.version, "python_ok": None}

    raise NotImplementedError("Implementeaza check_env().")


if __name__ == "__main__":
    print(greet("Ana"))
    print(check_env())
