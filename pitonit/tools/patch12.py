p = r'C:\AppPython\pitonit\tools\genera_moduli.py'
s = open(p, encoding='utf-8').read()
old = '''    if s.get('extra'):
        righe.append(s['extra'].rstrip())
    return "\\n".join(righe) + "\\n"
'''
new = '''    if s.get('extra'):
        righe.append(s['extra'].rstrip())
    if s.get('auto', True):
        curati_it = set(nomi)
        for m in s.get('tipi', {}).values():
            curati_it |= set(D(m))
        curati_en = set(nomi.values())
        an, at = auto_alias(s, curati_it, curati_en)
        righe.append('')
        righe.append("# --- traduzione automatica del resto dell'API (glossario) ---")
        righe.append(f'_AUTO_NOMI = {an!r}')
        righe.append(f'_AUTO_TIPI = {at!r}')
        righe.append('from _italiano import applica_auto as _auto')
        righe.append('_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)')
    return "\\n".join(righe) + "\\n"
'''
assert old in s
s = s.replace(old, new)

# rapporto delle parole sconosciute
old2 = "    with open(os.path.join(os.path.dirname(DIZ), 'moduli_generati.txt'), 'w', encoding='utf-8') as f:"
new2 = '''    with open(os.path.join(os.path.dirname(DIZ), 'non_tradotti.txt'), 'w', encoding='utf-8') as f:
        for w, n in sorted(IGNOTE.items(), key=lambda x: -x[1]):
            f.write(f"{n}\\t{w}\\n")
    with open(os.path.join(os.path.dirname(DIZ), 'moduli_generati.txt'), 'w', encoding='utf-8') as f:'''
assert old2 in s
s = s.replace(old2, new2)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
