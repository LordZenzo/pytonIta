"""Verifica completa prima di ogni release (da lanciare con l'interprete installato):

    installazione\\pitonit.exe tools\\verifica_tutto.py [--rapida]

Passi:
  1. controllo statico (_controlla) su tutti i file .pit di PitStudio, esempi, installatore, strumenti;
  2. andata e ritorno .pit -> Python (pit2py) di tutti i file di PitStudio: devono compilare;
  3. verifica dei moduli italiani (verifica_moduli.pit);
  4. tutti i test di PitStudio (tests/prova_*.pit): codice di uscita 0 e nessuna riga ERRORE:/PROVE FALLITE/Traceback.
Con --rapida si saltano i test di PitStudio (passo 4).
Il test prova_crea_exe costruisce davvero degli eseguibili (serve internet e qualche minuto): con --senza-exe lo si salta.
Codice di uscita: 0 se tutto passa.
"""
import glob
import json
import os
import subprocess
import sys
import threading
import time

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # ...\pitonit
APP = os.path.dirname(RADICE)                                            # ...\AppPython
RAD = os.path.join(APP, "RAD")
PIT = os.path.join(RADICE, "installazione", "pitonit.exe")
sys.path.insert(0, os.path.join(RADICE, "src", "Lib"))
sys.path.insert(0, os.path.join(RADICE, "tools"))

problemi = []
DURATE = os.path.join(RADICE, "tools", "verifica_durate.json")        # quanto è durato ogni pezzo l'ultima volta: dà i pesi alla barra


class Avanzamento:
    """Barra di avanzamento vera: ogni pezzo del lavoro (controllo statico, conversione, moduli, esempi e ognuno dei test) pesa quanto è durato
    l'ultima volta (la prima volta, un peso di riserva), e la percentuale è il peso del lavoro finito su quello totale. Il tempo che resta
    si stima con la velocità di questa esecuzione. In un terminale la barra si aggiorna ogni secondo sulla stessa riga; se l'uscita va su un file
    (o a Claude) ogni cambio di passo scrive una riga a sé."""
    RISERVA = {"p1": 12.0, "p2": 20.0, "p3": 25.0, "p3b": 40.0, "test": 3.0}

    def __init__(se, rapida, nomi_test):
        try:
            with open(DURATE, encoding="utf-8") as f:
                se.storico = json.load(f)
        except (OSError, ValueError):
            se.storico = {}
        se.nuovo = {"test": {}}
        se.peso = {}
        for k in ("p1", "p2", "p3") + (() if rapida else ("p3b",)):
            se.peso[k] = float(se.storico.get(k) or se.RISERVA[k])
        durate = sorted(se.storico.get("test", {}).values())
        medio = durate[len(durate) // 2] if durate else se.RISERVA["test"]
        if not rapida:
            for n in nomi_test:
                se.peso["t:" + n] = float(se.storico.get("test", {}).get(n) or medio)
        se.totale = sum(se.peso.values())
        se.fatto = 0.0                  # peso del lavoro già finito
        se.corrente = ("", 0.0)         # (chiave del pezzo in corso, quando è partito)
        se.inizio = time.time()
        se.testo = ""
        se.tty = sys.stdout.isatty()
        se.attivo = True
        se.ultima_riga = 0
        if se.tty:
            threading.Thread(target=se._ticchetta, daemon=True).start()

    def percentuale(se):
        chiave, partito = se.corrente
        dentro = 0.0
        if chiave:
            dentro = min(0.95 * se.peso.get(chiave, 0.0), time.time() - partito)
        return max(0.0, min(100.0, 100.0 * (se.fatto + dentro) / se.totale)) if se.totale else 100.0

    def restano(se):
        pronto = se.percentuale() / 100.0 * se.totale
        trascorso = time.time() - se.inizio
        if pronto < 1:
            return None
        ritmo = min(3.0, max(0.3, trascorso / pronto))        # velocità di oggi rispetto a quella dell'ultima volta
        return (se.totale - pronto) * ritmo

    @staticmethod
    def _tempo(sec):
        sec = int(sec)
        return f"{sec // 60}:{sec % 60:02d}"

    def riga(se):
        perc = se.percentuale()
        pieni = int(round(perc / 100.0 * 24))
        resto = se.restano()
        stima = f"restano ~{se._tempo(resto)}" if resto is not None else "stima in corso"
        return f"[{'#' * pieni}{'-' * (24 - pieni)}] {perc:5.1f}%  {se._tempo(time.time() - se.inizio)} trascorsi, {stima}  {se.testo}"

    def _ticchetta(se):
        while se.attivo:
            se.disegna()
            time.sleep(1.0)

    def disegna(se):
        if se.tty and se.attivo:
            riga = se.riga()[:119]
            sys.stdout.write("\r" + riga.ljust(se.ultima_riga))
            sys.stdout.flush()
            se.ultima_riga = len(riga)

    def scrivi(se, testo):
        """Una riga normale: in un terminale cancella la barra, scrive e la ridisegna."""
        if se.tty:
            sys.stdout.write("\r" + " " * se.ultima_riga + "\r")
        print(testo, flush=True)
        se.disegna()

    def inizia(se, chiave, cosa):
        se.corrente = (chiave, time.time())
        se.avvio_passo = time.time()
        se.testo = cosa
        if not se.tty:
            print(f"[{se.percentuale():5.1f}%] {cosa}", flush=True)

    def finisce(se, chiave):
        durata = time.time() - se.avvio_passo
        se.fatto += se.peso.get(chiave, 0.0)
        se.corrente = ("", 0.0)
        if chiave.startswith("t:"):
            se.nuovo["test"][chiave[2:]] = round(durata, 1)
        else:
            se.nuovo[chiave] = round(durata, 1)

    def passo_file(se, chiave, fatti, totali):
        """Dentro un passo fatto di tanti file la barra avanza con i file elaborati, non col tempo."""
        se.corrente = (chiave, time.time() - (fatti / max(1, totali)) * 0.95 * se.peso.get(chiave, 1.0) / 0.95)

    def chiudi(se):
        se.attivo = False
        if se.tty:
            sys.stdout.write("\r" + " " * se.ultima_riga + "\r")
        unito = dict(se.storico)
        unito.update({k: v for k, v in se.nuovo.items() if k != "test"})
        unito["test"] = dict(se.storico.get("test", {}))
        unito["test"].update(se.nuovo["test"])
        try:
            with open(DURATE, "w", encoding="utf-8") as f:
                json.dump(unito, f, indent=1)
        except OSError:
            pass


def titolo(t):
    if "av" in globals():
        av.scrivi(f"\n=== {t}")
    else:
        print(f"\n=== {t}", flush=True)


def tutti_pit(*cartelle):
    out = []
    for c in cartelle:
        for base, _, nomi in os.walk(c):
            if ".git" in base or "__pycache__" in base:
                continue
            out += [os.path.join(base, n) for n in nomi if n.endswith(".pit")]
    return out


RAPIDA = "--rapida" in sys.argv
test = sorted(glob.glob(os.path.join(RAD, "tests", "prova_*.pit")))
av = Avanzamento(RAPIDA, [os.path.basename(t) for t in test])

# 1 ---------------------------------------------------------------- controllo statico
titolo("1. controllo statico")
av.inizia("p1", "controllo statico")
import _controlla                                               # noqa: E402

file_pit = tutti_pit(RAD, os.path.join(RADICE, "esempi"), os.path.join(RADICE, "tools"),
                     os.path.join(APP, "installatore"))
gravi = 0
for numero, p in enumerate(file_pit):
    av.passo_file("p1", numero, len(file_pit))
    try:
        with open(p, "rb") as f:
            errori, _, _ = _controlla.analizza(f.read(), p)
    except Exception as e:                                      # noqa: BLE001
        problemi.append(f"controllo non riuscito su {p}: {e}")
        continue
    for riga, _, msg in errori:
        gravi += 1
        av.scrivi(f"  {p}:{riga}: {msg}")
av.finisce("p1")
av.scrivi(f"  {len(file_pit)} file, {gravi} errori gravi")
if gravi:
    problemi.append(f"{gravi} errori gravi dal controllo statico")

# 2 ---------------------------------------------------------------- andata e ritorno
titolo("2. pit2py su PitStudio")
import pit2py                                                   # noqa: E402

ko = 0
tot = 0
av.inizia("p2", "conversione in Python")
da_convertire = [p for p in tutti_pit(RAD) if os.sep + "campioni" + os.sep not in p]
for numero, p in enumerate(da_convertire):
    av.passo_file("p2", numero, len(da_convertire))
    tot += 1
    try:
        with open(p, encoding="utf-8") as f:
            py = pit2py.converti_testo(f.read(), None, os.path.basename(p))
        py = py[0] if isinstance(py, tuple) else py
        compile(py, p, "exec")
    except Exception as e:                                      # noqa: BLE001
        ko += 1
        av.scrivi(f"  KO {p}: {type(e).__name__}: {str(e)[:120]}")
av.finisce("p2")
av.scrivi(f"  {tot} file, {ko} falliti")
if ko:
    problemi.append(f"{ko} file non si convertono in Python valido")

# 3 ---------------------------------------------------------------- moduli italiani
titolo("3. moduli italiani")
verifica = os.path.join(RADICE, "tools", "verifica_moduli.pit")
av.inizia("p3", "moduli italiani (un passo solo: la barra avanza col tempo previsto)")
if os.path.exists(verifica):
    r = subprocess.run([PIT, "-u", verifica, os.path.join(RADICE, "tools", "moduli_generati.txt")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ultime = (r.stdout.strip().splitlines() or [""])[-1]
    av.scrivi(f"  codice {r.returncode}: {ultime[:150]}")
    if r.returncode != 0:
        problemi.append("verifica_moduli.pit non passa")
else:
    av.scrivi("  (verifica_moduli.pit non trovato)")
av.finisce("p3")

# 3b --------------------------------------------------------------- esempi delle lezioni
titolo("3b. esempi delle lezioni")
if not RAPIDA:
    av.inizia("p3b", "esempi delle lezioni (un passo solo: la barra avanza col tempo previsto)")
    r = subprocess.run([sys.executable if sys.executable.lower().endswith("python.exe") else "python", os.path.join(RADICE, "tools", "lezioni.py"), "--verifica"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ultime = (r.stdout.strip().splitlines() or [""])[-1]
    av.scrivi(f"  codice {r.returncode}: {ultime[:150]}")
    av.finisce("p3b")
    if r.returncode != 0 or " 0 problemi" not in ultime:
        problemi.append("lezioni.py --verifica segnala problemi")

# 4 ---------------------------------------------------------------- test di PitStudio
if not RAPIDA:
    titolo("4. test di PitStudio")
    inizio = time.time()
    falliti = []
    for numero, t in enumerate(test, 1):
        av.inizia("t:" + os.path.basename(t), f"test {numero}/{len(test)}: {os.path.basename(t)}")
        try:
            # la costruzione vera di un eseguibile (scarica PyInstaller, impacchetta, avvia il programma costruito) fa parte della verifica di rilascio
            costruzione = os.path.basename(t) == "prova_crea_exe.pit" and "--senza-exe" not in sys.argv
            r = subprocess.run([PIT, "-u", t], capture_output=True, text=True, encoding="utf-8",
                               errors="replace", cwd=RAD, timeout=900 if costruzione else 170,
                               env=dict(os.environ, RAD_PROVA_EXE="1") if costruzione else None)
            uscita = r.stdout + r.stderr
            codice = r.returncode
        except subprocess.TimeoutExpired:
            uscita, codice = "", -1
        cattivo = codice != 0 or any(l.startswith(("ERRORE:", "PROVE FALLITE: [", "Traceback", "Errori gravi"))
                                     for l in uscita.splitlines())
        av.finisce("t:" + os.path.basename(t))
        if cattivo:
            falliti.append(os.path.basename(t))
            av.scrivi(f"  FALLITO {os.path.basename(t)} (codice {codice})")
            av.scrivi("    " + "\n    ".join(uscita.strip().splitlines()[-4:]))
    subprocess.run(["git", "checkout", "--", "docs"], cwd=RAD, capture_output=True)
    av.scrivi(f"  {len(test)} test in {time.time() - inizio:.0f} s, {len(falliti)} falliti")
    if falliti:
        problemi.append("test falliti: " + ", ".join(falliti))

av.chiudi()
titolo("RISULTATO")
if problemi:
    for p in problemi:
        print("  -", p)
    sys.exit(1)
print("  tutto ok")
