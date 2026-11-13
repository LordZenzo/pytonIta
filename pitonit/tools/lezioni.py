"""Verifica (e riempie) gli esempi delle lezioni di PitStudio.

Uso:
    python lezioni.py --verifica      controlla che ogni esempio funzioni e che i blocchi «output» coincidano
    python lezioni.py --riempi        riscrive i blocchi «output» con il risultato reale dell'esecuzione

Convenzioni dei blocchi nei file RAD/aiuto/lezione-NN.md:
    ```pit            programma completo: deve girare senza errori
    ```pit errore     programma che deve fallire (mostra un errore)
    ```pit sintassi   solo controllo della sintassi (finestre, programmi che non terminano)
    ```output         risultato del blocco pit che lo precede (verificato / riempito da questo strumento)
    ```esempio        trascrizione scritta a mano (programmi che usano leggi): non verificata
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
PITONIT = os.path.join(os.path.dirname(QUI), "installazione", "pitonit.exe")
AIUTO = os.path.join(os.path.dirname(os.path.dirname(QUI)), "RAD", "aiuto")
INGRESSO = "Anna\n12\n5\n3\n7\n2\n1\n0\n"
INGRESSI = [INGRESSO, "12\n5\n3\n7\n2\n1\n0\n", "4.5\n2\n10\n20\n", "1\n3\n2\n"]

CONTROLLO = ("import sys\nsrc = open(sys.argv[1], encoding='utf-8').read()\n"
             "compile(src, sys.argv[1], 'exec', 0x10000, True)\n")


def blocchi(righe):
    """[(lingua, inizio, fine, codice)]: indici di riga del contenuto (fine esclusa)."""
    risultato = []
    i = 0
    while i < len(righe):
        r = righe[i].strip()
        if r.startswith("```"):
            lingua = r[3:].strip()
            j = i + 1
            while j < len(righe) and not righe[j].strip().startswith("```"):
                j += 1
            risultato.append((lingua, i + 1, j, "\n".join(righe[i + 1:j])))
            i = j + 1
        else:
            i += 1
    return risultato


def esegui(codice, cartella, ingresso=INGRESSO):
    percorso = os.path.join(cartella, "prova.pit")
    with open(percorso, "w", encoding="utf-8", newline="\n") as f:
        f.write(codice + "\n")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([PITONIT, "-u", percorso], input=ingresso, capture_output=True, text=True, encoding="utf-8",
                          cwd=cartella, env=env, timeout=30)


def controlla_sintassi(codice, cartella):
    percorso = os.path.join(cartella, "sintassi.pit")
    with open(percorso, "w", encoding="utf-8", newline="\n") as f:
        f.write(codice + "\n")
    driver = os.path.join(cartella, "_controllo.py")
    with open(driver, "w", encoding="utf-8") as f:
        f.write(CONTROLLO)
    return subprocess.run([PITONIT, driver, percorso], capture_output=True, text=True, encoding="utf-8", cwd=cartella)


def lavora(percorso, riempi):
    nome = os.path.basename(percorso)
    righe = open(percorso, encoding="utf-8").read().split("\n")
    problemi = []
    modifiche = []
    cartella = tempfile.mkdtemp(prefix="lezione_")
    elenco = blocchi(righe)
    totale = 0
    for k, (lingua, inizio, fine, codice) in enumerate(elenco):
        parti = lingua.split()
        if not parti or parti[0] != "pit":
            continue
        totale += 1
        opzione = parti[1] if len(parti) > 1 else ""
        riga_blocco = inizio
        if opzione == "sintassi":
            r = controlla_sintassi(codice, cartella)
            if r.returncode != 0:
                problemi.append(f"{nome}:{riga_blocco}: sintassi non valida: {r.stderr.strip().splitlines()[-1:]}")
            continue
        if opzione == "errore":
            r = esegui(codice, cartella)
            if r.returncode == 0:
                problemi.append(f"{nome}:{riga_blocco}: doveva fallire ma è riuscito")
            continue
        usa_ingresso = "leggi(" in codice or "leggi_tastiera(" in codice
        candidati = (INGRESSI if usa_ingresso else [INGRESSO])
        r = None
        try:
            for ingresso in candidati:
                r = esegui(codice, cartella, ingresso)
                if r.returncode == 0 or (usa_ingresso and "FineDelFile" in r.stderr):
                    break
        except subprocess.TimeoutExpired:
            problemi.append(f"{nome}:{riga_blocco}: tempo scaduto")
            continue
        if r.returncode != 0 and not (usa_ingresso and "FineDelFile" in r.stderr):
            problemi.append(f"{nome}:{riga_blocco}: errore\n      " + "\n      ".join(r.stderr.strip().splitlines()[-4:]))
            continue
        # blocco output subito dopo?
        if k + 1 < len(elenco) and elenco[k + 1][0] == "output":
            _, i2, f2, atteso = elenco[k + 1]
            tra = [x for x in righe[fine + 1:i2 - 1] if x.strip()]
            if tra:
                continue
            reale = "\n".join(x.rstrip() for x in r.stdout.replace("\r\n", "\n").rstrip("\n").split("\n"))
            if riempi:
                if reale != atteso:
                    modifiche.append((i2, f2, reale))
            elif reale != atteso:
                problemi.append(f"{nome}:{i2}: output diverso\n      atteso: {atteso!r}\n      reale:  {reale!r}")
    if riempi and modifiche:
        for i2, f2, reale in sorted(modifiche, reverse=True):
            righe[i2:f2] = reale.split("\n")
        with open(percorso, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(righe))
    return totale, problemi, len(modifiche)


def main():
    riempi = "--riempi" in sys.argv
    file_ = sorted(glob.glob(os.path.join(AIUTO, "lezione-*.md")))
    tot = 0
    guai = []
    for p in file_:
        n, problemi, scritti = lavora(p, riempi)
        tot += n
        guai += problemi
        print(f"{os.path.basename(p)}: {n} esempi" + (f", {scritti} output riscritti" if riempi else ""))
    print(f"\nTotale: {tot} esempi, {len(guai)} problemi")
    for g in guai:
        print(" -", g)
    return 1 if guai else 0


if __name__ == "__main__":
    sys.exit(main())
