"""Cosa usano davvero i programmi dell'utente e cosa manca ancora in italiano.

Uso: python analisi_uso.py [--json uscita.json]
"""
import ast
import importlib
import inspect
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dizionari'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genera_moduli import D, DIZ  # noqa

RADICE = r'C:\AppPython'
ESCLUDI = {'pitonit', 'pytonita', 'ModFile2_pit', '__pycache__', '.git', 'node_modules'}


def file_utente():
    for cart, dirs, files in os.walk(RADICE):
        dirs[:] = [d for d in dirs if d not in ESCLUDI]
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(cart, f)


def nomi_usati():
    usati = {}
    for p in file_utente():
        try:
            albero = ast.parse(open(p, encoding='utf-8').read())
        except Exception:
            continue
        for n in ast.walk(albero):
            nome = None
            if isinstance(n, ast.Attribute):
                nome = n.attr
            elif isinstance(n, ast.keyword) and n.arg:
                nome = n.arg
            elif isinstance(n, ast.ImportFrom):
                for a in n.names:
                    usati.setdefault(a.name, set()).add(os.path.basename(p))
            if nome:
                usati.setdefault(nome, set()).add(os.path.basename(p))
    return usati


def carica_specs():
    tutti = {}
    for f in sorted(os.listdir(DIZ)):
        if f.endswith('.py') and not f.startswith('_'):
            m = importlib.import_module(f[:-3])
            tutti.update(m.MODULI)
    return tutti


def pubblici(oggetto):
    return {n for n in dir(oggetto) if not n.startswith('_')}


GENERICI = set()
for _t in (str, list, dict, set, bytes, int, float, tuple, object, frozenset, bytearray):
    GENERICI |= set(dir(_t))
GENERICI |= {'args', 'time', 'path', 'name', 'type', 'value', 'values', 'error', 'x', 'y', 'width', 'height', 'text', 'font', 'command'}


def main():
    usati = {k: v for k, v in nomi_usati().items() if k not in GENERICI}
    specs = carica_specs()
    mancanti = {}
    for it, s in specs.items():
        try:
            mod = importlib.import_module(s['orig'])
        except Exception:
            continue
        coperti = set(D(s.get('nomi', '')).values())
        classi = {}
        for c, mappa in s.get('tipi', {}).items():
            coperti |= {v.lstrip('@') for v in D(mappa).values()}
        opz = set(D(s.get('opz', '')).values()) if s.get('opz') else set()
        # nomi gia' tradotti in automatico (letti dal modulo generato)
        pf = os.path.join(r'C:\AppPython\pitonit\src\Lib', *it.split('.'))
        for cand in (pf + '.py', os.path.join(pf, '__init__.py')):
            if os.path.exists(cand):
                for riga in open(cand, encoding='utf-8'):
                    if riga.startswith('_AUTO_NOMI = '):
                        coperti |= set(ast.literal_eval(riga.split(' = ', 1)[1]).values())
                    elif riga.startswith('_AUTO_TIPI = '):
                        for mp in ast.literal_eval(riga.split(' = ', 1)[1]).values():
                            coperti |= set(mp.values())
        candidati = set(pubblici(mod))
        for nome in list(candidati):
            ogg = getattr(mod, nome, None)
            if inspect.isclass(ogg):
                candidati |= {n for n in pubblici(ogg)}
        gap = sorted(n for n in candidati if n in usati and n not in coperti and n not in opz
                     and not n.isupper() or (n in usati and n.isupper() and n not in coperti))
        gap = [n for n in gap if n in usati]
        if gap:
            mancanti[it] = gap
    return mancanti, usati


if __name__ == '__main__':
    mancanti, usati = main()
    for it, gap in mancanti.items():
        print(f"{it}: {len(gap)}")
        print("   ", " ".join(gap))
    if '--json' in sys.argv:
        json.dump(mancanti, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
