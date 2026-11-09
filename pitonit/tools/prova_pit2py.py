"""Controllo di pit2py.

  1. Le parole chiave tradotte danno lo stesso albero sintattico che pitonit legge dai .pit del progetto.
  2. Andata e ritorno Python -> pytonIta (py2pit) -> Python (pit2py) su moduli della libreria standard.

Uso:  python prova_pit2py.py
"""
import ast
import glob
import os
import sys
import sysconfig

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
sys.path.insert(0, QUI)
import pit2py   # noqa: E402
import py2pit   # noqa: E402


def parte1():
    files = (glob.glob(os.path.join(RADICE, "RAD", "rad", "*.pit")) + glob.glob(os.path.join(RADICE, "RAD", "tests", "*.pit"))
             + glob.glob(os.path.join(RADICE, "pitonit", "esempi", "**", "*.pit"), recursive=True))
    tmp = os.path.join(RADICE, "_tmp_kw.py")
    uguali, diversi = 0, []
    for f in files:
        src = open(f, encoding="utf-8").read()
        try:
            open(tmp, "w", encoding="utf-8", newline="\n").write(pit2py.traduci_parole_chiave(src))
            if py2pit.tipi_python(tmp) == py2pit.tipi_pitonit(f):
                uguali += 1
            else:
                diversi.append(f)
        except Exception as e:
            diversi.append(f"{f}: {type(e).__name__} {str(e)[:80]}")
    if os.path.exists(tmp):
        os.remove(tmp)
    print(f"parte 1: {len(files)} file .pit, parole chiave identiche a pitonit su {uguali}")
    for d in diversi[:10]:
        print("   DIVERSO", d)
    return not diversi


def parte2():
    lib = sysconfig.get_paths()["stdlib"]
    n, ok, ko = 0, 0, []
    for f in sorted(glob.glob(os.path.join(lib, "*.py"))):
        try:
            src = open(f, encoding="utf-8").read()
            orig = ast.parse(src)
        except Exception:
            continue
        n += 1
        try:
            t2 = pit2py.traduci_parole_chiave(py2pit.traduci(src, []))
            if [type(x).__name__ for x in ast.walk(ast.parse(t2))] == [type(x).__name__ for x in ast.walk(orig)]:
                ok += 1
            else:
                ko.append(os.path.basename(f))
        except Exception as e:
            ko.append(f"{os.path.basename(f)}: {type(e).__name__} {str(e)[:80]}")
    print(f"parte 2: {n} moduli della libreria standard, andata e ritorno identico su {ok}")
    for k in ko[:10]:
        print("   DIVERSO", k)
    return not ko


if __name__ == "__main__":
    sys.exit(0 if (parte1() & parte2()) else 1)
