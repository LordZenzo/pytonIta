"""Verifica completa prima di ogni release (da lanciare con l'interprete installato):

    installazione\\pitonit.exe tools\\verifica_tutto.py [--rapida]

Passi:
  1. controllo statico (_controlla) su tutti i file .pit di PitStudio, esempi, installatore, strumenti;
  2. andata e ritorno .pit -> Python (pit2py) di tutti i file di PitStudio: devono compilare;
  3. verifica dei moduli italiani (verifica_moduli.pit);
  4. tutti i test di PitStudio (tests/prova_*.pit): codice di uscita 0 e nessuna riga ERRORE:/PROVE FALLITE/Traceback.
Con --rapida si saltano i test di PitStudio (passo 4).
Codice di uscita: 0 se tutto passa.
"""
import glob
import os
import subprocess
import sys
import time

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # ...\pitonit
APP = os.path.dirname(RADICE)                                            # ...\AppPython
RAD = os.path.join(APP, "RAD")
PIT = os.path.join(RADICE, "installazione", "pitonit.exe")
sys.path.insert(0, os.path.join(RADICE, "src", "Lib"))
sys.path.insert(0, os.path.join(RADICE, "tools"))

problemi = []


def titolo(t):
    print(f"\n=== {t}", flush=True)


def tutti_pit(*cartelle):
    out = []
    for c in cartelle:
        for base, _, nomi in os.walk(c):
            if ".git" in base or "__pycache__" in base:
                continue
            out += [os.path.join(base, n) for n in nomi if n.endswith(".pit")]
    return out


# 1 ---------------------------------------------------------------- controllo statico
titolo("1. controllo statico")
import _controlla                                               # noqa: E402

file_pit = tutti_pit(RAD, os.path.join(RADICE, "esempi"), os.path.join(RADICE, "tools"),
                     os.path.join(APP, "installatore"))
gravi = 0
for p in file_pit:
    try:
        with open(p, "rb") as f:
            errori, _, _ = _controlla.analizza(f.read(), p)
    except Exception as e:                                      # noqa: BLE001
        problemi.append(f"controllo non riuscito su {p}: {e}")
        continue
    for riga, _, msg in errori:
        gravi += 1
        print(f"  {p}:{riga}: {msg}")
print(f"  {len(file_pit)} file, {gravi} errori gravi")
if gravi:
    problemi.append(f"{gravi} errori gravi dal controllo statico")

# 2 ---------------------------------------------------------------- andata e ritorno
titolo("2. pit2py su PitStudio")
import pit2py                                                   # noqa: E402

ko = 0
tot = 0
for p in tutti_pit(RAD):
    if os.sep + "campioni" + os.sep in p:
        continue
    tot += 1
    try:
        with open(p, encoding="utf-8") as f:
            py = pit2py.converti_testo(f.read(), None, os.path.basename(p))
        py = py[0] if isinstance(py, tuple) else py
        compile(py, p, "exec")
    except Exception as e:                                      # noqa: BLE001
        ko += 1
        print(f"  KO {p}: {type(e).__name__}: {str(e)[:120]}")
print(f"  {tot} file, {ko} falliti")
if ko:
    problemi.append(f"{ko} file non si convertono in Python valido")

# 3 ---------------------------------------------------------------- moduli italiani
titolo("3. moduli italiani")
verifica = os.path.join(RADICE, "tools", "verifica_moduli.pit")
if os.path.exists(verifica):
    r = subprocess.run([PIT, "-u", verifica, os.path.join(RADICE, "tools", "moduli_generati.txt")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ultime = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  codice {r.returncode}: {ultime[:150]}")
    if r.returncode != 0:
        problemi.append("verifica_moduli.pit non passa")
else:
    print("  (verifica_moduli.pit non trovato)")

# 3b --------------------------------------------------------------- esempi delle lezioni
titolo("3b. esempi delle lezioni")
if "--rapida" not in sys.argv:
    r = subprocess.run([sys.executable if sys.executable.lower().endswith("python.exe") else "python", os.path.join(RADICE, "tools", "lezioni.py"), "--verifica"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ultime = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  codice {r.returncode}: {ultime[:150]}")
    if r.returncode != 0 or " 0 problemi" not in ultime:
        problemi.append("lezioni.py --verifica segnala problemi")

# 4 ---------------------------------------------------------------- test di PitStudio
if "--rapida" not in sys.argv:
    titolo("4. test di PitStudio")
    inizio = time.time()
    falliti = []
    test = sorted(glob.glob(os.path.join(RAD, "tests", "prova_*.pit")))
    for t in test:
        try:
            r = subprocess.run([PIT, "-u", t], capture_output=True, text=True, encoding="utf-8",
                               errors="replace", cwd=RAD, timeout=170)
            uscita = r.stdout + r.stderr
            codice = r.returncode
        except subprocess.TimeoutExpired:
            uscita, codice = "", -1
        cattivo = codice != 0 or any(l.startswith(("ERRORE:", "PROVE FALLITE: [", "Traceback", "Errori gravi"))
                                     for l in uscita.splitlines())
        if cattivo:
            falliti.append(os.path.basename(t))
            print(f"  FALLITO {os.path.basename(t)} (codice {codice})")
            print("    " + "\n    ".join(uscita.strip().splitlines()[-4:]))
    subprocess.run(["git", "checkout", "--", "docs"], cwd=RAD, capture_output=True)
    print(f"  {len(test)} test in {time.time() - inizio:.0f} s, {len(falliti)} falliti")
    if falliti:
        problemi.append("test falliti: " + ", ".join(falliti))

titolo("RISULTATO")
if problemi:
    for p in problemi:
        print("  -", p)
    sys.exit(1)
print("  tutto ok")
