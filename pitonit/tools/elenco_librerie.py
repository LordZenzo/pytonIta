"""Genera ELENCO_LIBRERIE.md dai dizionari."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dizionari'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
from genera_moduli import D, DIZ

righe = ["# Librerie in italiano\n", "| Modulo italiano | Libreria originale | Nomi | Metodi/attributi |", "|---|---|---|---|"]
tot = 0
for f in sorted(os.listdir(DIZ)):
    if f.endswith('.py') and not f.startswith('_'):
        m = importlib.import_module(f[:-3])
        for k, v in m.MODULI.items():
            n = len(D(v.get('nomi', '')))
            t = sum(len(D(x)) for x in v.get('tipi', {}).values())
            auto = 0
            pf = os.path.join(r'C:\AppPython\pitonit\src\Lib', *k.split('.'))
            for cand in (pf + '.py', os.path.join(pf, '__init__.py')):
                if os.path.exists(cand):
                    import ast
                    for riga in open(cand, encoding='utf-8'):
                        if riga.startswith('_AUTO_NOMI = '):
                            auto += len(ast.literal_eval(riga.split(' = ', 1)[1]))
                        elif riga.startswith('_AUTO_TIPI = '):
                            auto += sum(len(x) for x in ast.literal_eval(riga.split(' = ', 1)[1]).values())
            righe.append(f"| `{k}` | `{v['orig']}` | {n + t} | {auto} |")
            tot += n + t + auto
righe.append(f"\nTotale alias: **{tot}**. Il nome originale resta sempre disponibile.")
open(os.path.join(os.path.dirname(DIZ), '..', 'ELENCO_LIBRERIE.md'), 'w', encoding='utf-8').write("\n".join(righe) + "\n")
print(len(righe) - 4, "moduli,", tot, "alias")
