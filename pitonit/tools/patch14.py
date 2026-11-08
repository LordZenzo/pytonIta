p = r'C:\AppPython\pitonit\tools\genera_moduli.py'
s = open(p, encoding='utf-8').read()

old = "        righe.append('_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)')\n"
new = old + "    righe.append('from _italiano import importa_basi as _basi')\n    righe.append('_basi(_orig)')\n"
assert old in s
s = s.replace(old, new)
# l'import delle basi vale anche per i moduli senza traduzione automatica
s = s.replace("    righe.append('from _italiano import importa_basi as _basi')\n    righe.append('_basi(_orig)')\n",
              "    righe.append('')\n    righe.append('from _italiano import importa_basi as _basi')\n    righe.append('_basi(_orig)')\n")

old2 = "    with open(os.path.join(os.path.dirname(DIZ), 'non_tradotti.txt'), 'w', encoding='utf-8') as f:"
new2 = '''    mappa = {s['orig']: k for k, s in tutti.items()}
    with open(os.path.join(LIB, '_mappa_moduli.py'), 'w', encoding='utf-8', newline='\\n') as f:
        f.write('"""Generato da tools/genera_moduli.py: modulo originale -> modulo italiano."""\\n')
        f.write(f'MAPPA = {mappa!r}\\n')
''' + old2
assert old2 in s
s = s.replace(old2, new2, 1)
open(p, 'w', encoding='utf-8').write(s)

q = r'C:\AppPython\pitonit\src\Lib\_italiano.py'
t = open(q, encoding='utf-8', newline='').read()
t += '''

def importa_basi(modulo):
    """Importa i moduli italiani delle classi base definite in altri moduli, cosi'
    i loro alias (es. Message.ottieni_tipo_contenuto) valgono anche per le sottoclassi."""
    import importlib
    import sys
    try:
        from _mappa_moduli import MAPPA
    except ImportError:
        return
    for nome in dir(modulo):
        c = getattr(modulo, nome, None)
        if not isinstance(c, type):
            continue
        for b in c.__mro__[1:]:
            m = getattr(b, "__module__", None)
            if m and m != modulo.__name__ and m in MAPPA and MAPPA[m] not in sys.modules:
                try:
                    importlib.import_module(MAPPA[m])
                except Exception:
                    pass
'''
open(q, 'w', encoding='utf-8', newline='').write(t)
print("ok")
