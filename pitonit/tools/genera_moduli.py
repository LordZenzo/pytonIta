"""Genera in Lib/ i moduli italiani che avvolgono le librerie.

I dati stanno in tools/dizionari/*.py (ognuno definisce MODULI).
Ogni modulo italiano ri-esporta l'originale e aggiunge gli alias:
  nomi   : "italiano=inglese ..."   attributi del modulo (anche a.b.c)
  tipi   : {"Classe": "it=en ..."}  metodi/attributi delle classi
  opz    : "it=en ..."              opzioni (argomenti con nome) tradotte
  val    : {"opzione_en": "it=en"}  valori testuali tradotti per quelle opzioni
  kw     : [(["Classe",..], ["metodo",..])]  dove accettare le opzioni italiane
  extra  : codice Python aggiunto in fondo
L'originale resta sempre disponibile.
"""
import importlib
import inspect
import keyword
import os
import sys

LIB = r'C:\AppPython\pitonit\src\Lib'
DIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dizionari')
sys.path.insert(0, DIZ)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossario

IT_KW = set("Falso Nessuno Vero e come asserisci asincrono attendi interrompi classe continua definisci elimina altrimenti_se altrimenti eccetto infine per da globale se importa in è lambda nonlocale non o passa solleva ritorna prova mentre con produci".split())
IGNOTE = {}      # parola sconosciuta -> quante volte


def D(testo):
    """'a=b c=d' -> {'a': 'b', 'c': 'd'}"""
    out = {}
    for parte in testo.split():
        it, _, en = parte.partition('=')
        if not en:
            raise ValueError(f"manca '=' in {parte!r}")
        if it in IT_KW:
            raise ValueError(f"{it!r} e' una parola chiave italiana: non puo' essere un alias")
        if it in out and out[it] != en:
            raise ValueError(f"alias duplicato {it!r}: {out[it]!r} / {en!r}")
        out[it] = en
    return out


def auto_alias(s, curati_it, curati_en):
    """Traduzione automatica dell'API pubblica del modulo (nomi, classi, metodi)."""
    try:
        mod = importlib.import_module(s['orig'])
    except Exception:
        return {}, {}
    radice = s['orig'].split('.')[0]
    nomi, tipi = {}, {}
    usati = set(curati_it)

    def prova(en):
        if en.startswith('_') or en in curati_en:
            return None
        it, ignote = glossario.traduci_nome(en)
        if ignote:
            for w in ignote:
                IGNOTE[w] = IGNOTE.get(w, 0) + 1
            return None
        if not it or keyword.iskeyword(it) or it in IT_KW or not it.isidentifier():
            return None
        if en.isupper():
            it = it.upper()           # costanti: restano maiuscole
        if it == en:
            return None
        return it

    nomi_mod = getattr(mod, '__all__', None) or [n for n in dir(mod) if not n.startswith('_')]
    for en in sorted(nomi_mod):
        ogg = getattr(mod, en, None)
        if ogg is None or inspect.ismodule(ogg):
            continue
        if inspect.isclass(ogg) and not en.isupper():
            continue                  # le classi hanno traduzioni scelte a mano
        it = prova(en)
        if it and it not in usati:
            nomi[it] = en
            usati.add(it)
    for cn in sorted(n for n in dir(mod) if not n.startswith('_')):
        cl = getattr(mod, cn, None)
        if not inspect.isclass(cl) or str(getattr(cl, '__module__', '')).split('.')[0] != radice:
            continue
        mappa = {}
        propri = set(vars(cl))
        presenti = {m for k in cl.__mro__ for m in vars(k)}
        for en in sorted(propri):
            it = prova(en)
            if it and it not in presenti and it not in mappa:
                mappa[it] = en
        if mappa:
            tipi[cn] = mappa
    return nomi, tipi


def genera(nome, s):
    righe = [
        f'"""Modulo italiano per `{s["orig"]}` (generato da tools/genera_moduli.py).',
        '',
        "Contiene tutti i nomi originali piu' gli alias italiani.",
        '"""',
        f'import {s["orig"]} as _orig',
        f'from {s["orig"]} import *',
        'from _italiano import alias_tipo, kw_tipo, ottieni as _ott',
        '',
        '',
        'def __getattr__(nome):',
        '    return getattr(_orig, nome)',
        '',
    ]
    nomi = D(s.get('nomi', ''))
    for it, en in nomi.items():
        righe.append(f'{it} = _ott(_orig, {en!r})')
    if s.get('kw') or s.get('opz'):
        righe.append(f'_OPZ = {D(s["opz"])!r}')
        val = {k: D(v) for k, v in s.get('val', {}).items()}
        righe.append(f'_VAL = {val!r}')
        for classi, metodi in s.get('kw', []):
            for c in classi:
                righe.append(f'kw_tipo(_ott(_orig, {c!r}), {metodi!r}, _OPZ, _VAL)')
    for classe, mappa in s.get('tipi', {}).items():
        righe.append(f'alias_tipo(_ott(_orig, {classe!r}), {D(mappa)!r})')
    if s.get('extra'):
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
    righe.append('')
    righe.append('from _italiano import importa_basi as _basi')
    righe.append('_basi(_orig)')
    return "\n".join(righe) + "\n"


def percorso(nome, e_pacchetto):
    p = os.path.join(LIB, *nome.split('.'))
    if e_pacchetto:
        os.makedirs(p, exist_ok=True)
        return os.path.join(p, '__init__.py')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p + '.py'


def main():
    tutti = {}
    for f in sorted(os.listdir(DIZ)):
        if f.endswith('.py') and not f.startswith('_'):
            m = importlib.import_module(f[:-3])
            for k, v in m.MODULI.items():
                if k in tutti:
                    raise SystemExit(f'modulo duplicato: {k}')
                tutti[k] = v
    pacchetti = {k.rsplit('.', 1)[0] for k in tutti if '.' in k}
    for nome, s in tutti.items():
        # un modulo con sottomoduli e' un pacchetto: elimina il vecchio file .py
        if nome in pacchetti:
            vecchio = os.path.join(LIB, *nome.split('.')) + '.py'
            if os.path.exists(vecchio):
                os.remove(vecchio)
        with open(percorso(nome, nome in pacchetti), 'w', encoding='utf-8', newline='\n') as f:
            f.write(genera(nome, s))
    mappa = {s['orig']: k for k, s in tutti.items()}
    with open(os.path.join(LIB, '_mappa_moduli.py'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('"""Generato da tools/genera_moduli.py: modulo originale -> modulo italiano."""\n')
        f.write(f'MAPPA = {mappa!r}\n')
    with open(os.path.join(os.path.dirname(DIZ), 'non_tradotti.txt'), 'w', encoding='utf-8') as f:
        for w, n in sorted(IGNOTE.items(), key=lambda x: -x[1]):
            f.write(f"{n}\t{w}\n")
    with open(os.path.join(os.path.dirname(DIZ), 'moduli_generati.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(sorted(tutti)) + "\n")
    print(f'{len(tutti)} moduli generati')


if __name__ == '__main__':
    main()
