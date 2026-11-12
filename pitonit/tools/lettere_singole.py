"""Elenca i nomi di una sola lettera nei file .pit di una cartella, per sistemarli a poco a poco.

Uso (con l'interprete pitonit):
    pitonit.exe lettere_singole.py [cartella] [--file nome.pit] [--lettera q] [--massimo N]

Senza opzioni stampa, per ogni file, quante volte compare ogni lettera (dal file più pieno al meno pieno) e il totale.
Con --file mostra le righe di quel file (con il testo), con --lettera solo quella lettera.
Le lettere ammesse (i, j, k, n, x, y, z, e il trattino basso) non si contano: sono quelle del controllo statico di pitonit.
«e», «o», «l», «I» sono errori gravi e non compaiono qui: li ferma il controllo.
Non cambia nessun file: serve a guardare e a decidere."""
import os
import re
import sys

import _controlla

CARTELLE_ESCLUSE = {"__pycache__", ".git", ".rad", ".claude", "node_modules", "venv", ".venv", "build", "dist", "esempi", "installazione"}
NOME_NEL_MESSAGGIO = re.compile(r"«(\w)» è un nome di una sola lettera")


def file_pit(cartella):
    for radice, cartelle, nomi in os.walk(cartella):
        cartelle[:] = sorted(d for d in cartelle if d not in CARTELLE_ESCLUSE)
        for nome in sorted(nomi):
            if nome.lower().endswith(".pit"):
                yield os.path.join(radice, nome)


def lettere_di(percorso):
    """[(riga, lettera)] dei nomi di una sola lettera di un file."""
    try:
        with open(percorso, "rb") as f:
            dati = f.read()
    except OSError:
        return [], []
    errori, avvisi, righe = _controlla.analizza(dati, percorso)
    trovate = []
    for riga, _colonna, messaggio in avvisi:
        m = NOME_NEL_MESSAGGIO.search(messaggio)
        if m:
            trovate.append((riga, m.group(1)))
    return trovate, righe


def main(argv):
    cartella = "."
    solo_file = None
    solo_lettera = None
    massimo = 40
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--file" and i + 1 < len(argv):
            solo_file = argv[i + 1]
            i += 1
        elif a == "--lettera" and i + 1 < len(argv):
            solo_lettera = argv[i + 1]
            i += 1
        elif a == "--massimo" and i + 1 < len(argv):
            massimo = int(argv[i + 1])
            i += 1
        elif not a.startswith("--"):
            cartella = a
        i += 1
    totale = 0
    per_lettera = {}
    tabella = []
    for percorso in file_pit(cartella):
        if solo_file and os.path.basename(percorso) != os.path.basename(solo_file) and solo_file not in percorso:
            continue
        trovate, righe = lettere_di(percorso)
        if solo_lettera:
            trovate = [t for t in trovate if t[1] == solo_lettera]
        if not trovate:
            continue
        totale += len(trovate)
        conteggio = {}
        for riga, lettera in trovate:
            conteggio[lettera] = conteggio.get(lettera, 0) + 1
            per_lettera[lettera] = per_lettera.get(lettera, 0) + 1
        tabella.append((len(trovate), os.path.relpath(percorso, cartella), conteggio, trovate, righe))
    tabella.sort(key=lambda t: (-t[0], t[1]))
    if solo_file:
        for quanti, relativo, conteggio, trovate, righe in tabella:
            print(f"{relativo}: {quanti} nomi di una lettera")
            visti = set()
            for riga, lettera in trovate:
                if riga in visti:
                    continue
                visti.add(riga)
                print(f"  {riga:5d} [{lettera}]  {righe[riga - 1].strip()[:110] if 0 < riga <= len(righe) else ''}")
    else:
        for quanti, relativo, conteggio, trovate, righe in tabella[:massimo]:
            dettaglio = ", ".join(f"{l}×{n}" for l, n in sorted(conteggio.items(), key=lambda kv: (-kv[1], kv[0])))
            print(f"{quanti:5d}  {relativo}   ({dettaglio})")
        if len(tabella) > massimo:
            print(f"       … e altri {len(tabella) - massimo} file (--massimo per vederli)")
    print()
    if totale == 0:
        print("Nessun nome di una sola lettera.")
    else:
        riepilogo = ", ".join(f"{l}×{n}" for l, n in sorted(per_lettera.items(), key=lambda kv: (-kv[1], kv[0])))
        print(f"Totale: {totale} in {len(tabella)} file. Per lettera: {riepilogo}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
