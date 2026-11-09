"""Esporta un progetto pytonIta come progetto Python: .py, requirements.txt, script di installazione delle librerie, LEGGIMI.

Uso:  python pit2py.py --progetto cartella_progetto cartella_destinazione
"""
import ast
import glob
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pit2py                                   # noqa: E402
from pit2py_tabelle import cartelle_lib         # noqa: E402

IGNORA = {"__pycache__", ".git", ".rad", ".claude", ".idea", ".vscode", "node_modules"}
SALTA_FILE = (".form.json", ".mattonelle.json")         # sorgenti dei progettisti: servono solo a PitStudio
MANIFESTO = "progetto.rad.json"

# modulo -> pacchetto di PyPI, quando i nomi sono diversi e il pacchetto non e' installato con pitonit
PYPI = {"numpy": "numpy", "pandas": "pandas", "scipy": "scipy", "matplotlib": "matplotlib", "requests": "requests",
        "reportlab": "reportlab", "tksheet": "tksheet", "PIL": "pillow", "cv2": "opencv-python", "yaml": "pyyaml", "sklearn": "scikit-learn", "dateutil": "python-dateutil",
        "bs4": "beautifulsoup4", "serial": "pyserial", "skimage": "scikit-image", "attr": "attrs", "OpenGL": "PyOpenGL",
        "docx": "python-docx", "dotenv": "python-dotenv", "jwt": "pyjwt", "Crypto": "pycryptodome", "fitz": "pymupdf"}


def _normalizza(nome):
    return re.sub(r"[-_.]+", "-", nome).lower()


def distribuzioni_installate():
    """{modulo di primo livello: (pacchetto, versione)} letto da *.dist-info di pitonit (senza importare nulla)."""
    risultato = {}
    for lib in cartelle_lib():
        for sp in (os.path.join(lib, "site-packages"),):
            for info in glob.glob(os.path.join(sp, "*.dist-info")):
                base = os.path.basename(info)[:-len(".dist-info")]
                nome, _, versione = base.rpartition("-")
                try:
                    with open(os.path.join(info, "METADATA"), encoding="utf-8") as f:
                        for riga in f:
                            if riga.startswith("Name:"):
                                nome = riga.split(":", 1)[1].strip()
                            elif riga.startswith("Version:"):
                                versione = riga.split(":", 1)[1].strip()
                            elif not riga.strip():
                                break
                except OSError:
                    pass
                top = []
                tp = os.path.join(info, "top_level.txt")
                if os.path.exists(tp):
                    top = [x.strip() for x in open(tp, encoding="utf-8").read().split() if x.strip()]
                else:
                    rec = os.path.join(info, "RECORD")
                    if os.path.exists(rec):
                        for riga in open(rec, encoding="utf-8"):
                            p = riga.split(",")[0].split("/")[0]
                            if p and not p.endswith(".dist-info") and not p.startswith("..") and not p.startswith("_") and p not in top:
                                top.append(p[:-3] if p.endswith(".py") else p)
                if not top:
                    top = [_normalizza(nome).replace("-", "_")]
                for m in top:
                    risultato.setdefault(m, (nome, versione))
    return risultato


def moduli_importati(testo):
    """Nomi di primo livello importati in modo assoluto da un file Python."""
    trovati = set()
    try:
        albero = ast.parse(testo)
    except SyntaxError:
        return trovati
    for n in ast.walk(albero):
        if isinstance(n, ast.Import):
            trovati.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
            trovati.add(n.module.split(".")[0])
    return trovati


def trova_requisiti(file_py, moduli_progetto):
    """([(pacchetto, versione o None)], [moduli sconosciuti]) per i file .py dati."""
    esterni = set()
    for percorso in file_py:
        try:
            testo = open(percorso, encoding="utf-8").read()
        except OSError:
            continue
        esterni |= moduli_importati(testo)
    stdlib = set(sys.stdlib_module_names) | {"__future__"}
    esterni = {m for m in esterni if m not in stdlib and m not in moduli_progetto and not m.startswith("_pit")}
    installate = distribuzioni_installate()
    pacchetti, sconosciuti = {}, []
    for m in sorted(esterni):
        if m in installate:
            nome, ver = installate[m]
            pacchetti[_normalizza(nome)] = (nome, ver)
        elif m in PYPI:
            pacchetti[_normalizza(PYPI[m])] = (PYPI[m], None)
        else:
            sconosciuti.append(m)
    return sorted(pacchetti.values(), key=lambda x: x[0].lower()), sconosciuti


def _scrivi(percorso, testo, fine_riga="\n"):
    with open(percorso, "w", encoding="utf-8", newline="") as f:
        f.write(testo.replace("\n", fine_riga))


LEGGIMI = """{nome} - programma Python

Questo programma e' stato scritto con pytonIta (PitStudio) ed e' stato convertito in Python normale:
non serve pytonIta per usarlo.

Come avviarlo
  1. Serve Python {versione_python} o piu' recente (https://www.python.org/downloads/).
{passo_librerie}  {n}. Avvia:   python {principale}

Note
  * Nel testo stampato, Vero/Falso/Nessuno diventano True/False/None e i messaggi d'errore sono quelli di Python (in inglese).
  * I commenti e i nomi che hai scelto restano come li hai scritti.
{note_librerie}  * Dettagli della conversione: CONVERSIONE.md
"""


def converti_progetto(origine, destinazione, nome_progetto=None):
    """Converte il progetto in `origine` nella cartella `destinazione` (da creare o vuota).
    Ritorna un dizionario: destinazione, file_python, altri_file, pacchetti [(nome, versione)], sconosciuti, errori [(file, testo)], note, principale."""
    origine = os.path.abspath(origine)
    destinazione = os.path.abspath(destinazione)
    if os.path.exists(destinazione) and os.listdir(destinazione):
        raise FileExistsError("La cartella di destinazione non e' vuota: " + destinazione)
    manifesto = {}
    mp = os.path.join(origine, MANIFESTO)
    if os.path.exists(mp):
        try:
            manifesto = json.load(open(mp, encoding="utf-8"))
        except ValueError:
            manifesto = {}
    nome_progetto = nome_progetto or manifesto.get("nome") or os.path.basename(origine)
    elenco_pit, altri = [], []
    for radice, cartelle, files in os.walk(origine):
        cartelle[:] = sorted(c for c in cartelle if c not in IGNORA)
        for f in sorted(files):
            p = os.path.join(radice, f)
            rel = os.path.relpath(p, origine)
            if f == MANIFESTO or f.endswith(SALTA_FILE):
                continue
            (elenco_pit if f.endswith(".pit") else altri).append(rel)
    # prima passata: i nomi che il programma definisce (per non scambiarli per alias di libreria)
    progetto = pit2py.Progetto()
    t2 = {}
    errori = []
    for rel in elenco_pit:
        try:
            t2[rel] = pit2py.traduci_parole_chiave(open(os.path.join(origine, rel), encoding="utf-8").read())
            progetto.aggiungi(ast.parse(t2[rel]))
        except ((SyntaxError,) + tokenizer_errori()) as e:
            errori.append((rel, f"errore di sintassi: {e}"))
    rapporto, convertiti = [], []
    os.makedirs(destinazione, exist_ok=True)
    for rel in elenco_pit:
        if rel not in t2:
            continue
        try:
            conv = pit2py.Convertitore(progetto)
            out = conv.converti(t2[rel], rel)
        except Exception as e:                      # un file che non si converte non ferma gli altri
            errori.append((rel, f"{type(e).__name__}: {e}"))
            continue
        dest = os.path.join(destinazione, rel[:-4] + ".py")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        _scrivi(dest, out)
        convertiti.append(rel[:-4] + ".py")
        for r, cat, testo in conv.rapporto:
            rapporto.append((rel, r, cat, testo))
    for rel in altri:
        dest = os.path.join(destinazione, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(origine, rel), dest)
    tutti_py = [os.path.join(destinazione, r) for r in convertiti] + [os.path.join(destinazione, r) for r in altri if r.endswith(".py")]
    moduli_progetto = {os.path.splitext(os.path.basename(p))[0] for p in tutti_py} | {
        c for c in os.listdir(destinazione) if os.path.isdir(os.path.join(destinazione, c))}
    pacchetti, sconosciuti = trova_requisiti(tutti_py, moduli_progetto)
    principale = manifesto.get("principale") or "principale.pit"
    principale = (principale[:-4] + ".py") if principale.endswith(".pit") else principale
    if not os.path.exists(os.path.join(destinazione, principale)):
        candidati = [r for r in convertiti if os.path.basename(r) in ("principale.py", "main.py")] or convertiti[:1]
        principale = candidati[0] if candidati else principale
    # ---- file di accompagnamento
    if pacchetti:
        righe = [f"{n}=={v}" if v else n for n, v in pacchetti]
        testo = ("# Librerie esterne usate dal programma (versioni con cui e' stato provato).\n"
                 "# Se una versione non esiste piu' per il tuo Python, togli il \"==...\" e pip sceglie la piu' recente.\n"
                 + "\n".join(righe) + "\n")
        for s in sconosciuti:
            testo += f"# {s}   <- non riconosciuta: cerca su PyPI il pacchetto che la contiene\n"
        _scrivi(os.path.join(destinazione, "requirements.txt"), testo)
        _scrivi(os.path.join(destinazione, "installa_librerie.bat"),
                "@echo off\r\nchcp 65001 >nul\r\necho Installo le librerie necessarie...\r\n"
                "where py >nul 2>nul && (py -m pip install -r \"%~dp0requirements.txt\") || (python -m pip install -r \"%~dp0requirements.txt\")\r\n"
                "if errorlevel 1 (\r\n  echo.\r\n  echo Non sono riuscito a installare le librerie. Controlla che Python e internet funzionino.\r\n) else (\r\n  echo.\r\n  echo Fatto.\r\n)\r\npause\r\n", fine_riga="\n")
        _scrivi(os.path.join(destinazione, "installa_librerie.sh"),
                "#!/bin/sh\ncd \"$(dirname \"$0\")\"\necho \"Installo le librerie necessarie...\"\n"
                "(python3 -m pip install -r requirements.txt) || (python -m pip install -r requirements.txt) || {\n"
                "  echo \"Non sono riuscito a installare le librerie: controlla Python e internet.\"; exit 1; }\necho Fatto.\n")
    passo = "  2. Installa le librerie: doppio clic su installa_librerie.bat (Windows) oppure  sh installa_librerie.sh  (Linux, Mac).\n" if pacchetti else ""
    note = ("  * Le librerie sono elencate in requirements.txt con le versioni usate per provare il programma.\n" if pacchetti else "")
    if any("tkinter" in moduli_importati(open(p, encoding="utf-8").read()) for p in tutti_py if os.path.exists(p)):
        note += "  * Il programma usa tkinter: su Linux potrebbe servire installarlo (pacchetto python3-tk).\n"
    _scrivi(os.path.join(destinazione, "LEGGIMI.txt"), LEGGIMI.format(
        nome=nome_progetto, versione_python=f"{sys.version_info.major}.{sys.version_info.minor}",
        passo_librerie=passo, n=3 if pacchetti else 2, principale=principale, note_librerie=note))
    # ---- rapporto
    quante = {}
    for _, _, cat, _ in rapporto:
        quante[cat] = quante.get(cat, 0) + 1
    md = [f"# Conversione di «{nome_progetto}» in Python", "",
          f"- File convertiti: {len(convertiti)}", f"- Altri file copiati: {len(altri)}", f"- Errori: {len(errori)}", ""]
    if pacchetti:
        md += ["## Librerie esterne", ""] + [f"- {n}{'==' + v if v else ''}" for n, v in pacchetti] + [""]
    if sconosciuti:
        md += ["Moduli esterni non riconosciuti (aggiungili a requirements.txt a mano): " + ", ".join(sconosciuti), ""]
    if errori:
        md += ["## File non convertiti", ""] + [f"- {r}: {e}" for r, e in errori] + [""]
    if quante:
        md += ["## Punti da guardare", "", "Dove un nome italiano poteva voler dire piu' cose, il programma sceglie mentre gira (funzione `_pit_attr`).", ""]
        md += [f"- {c}: {n}" for c, n in sorted(quante.items())] + [""]
        md += ["<details><summary>Elenco</summary>", ""] + [f"- {r}:{riga} {cat}: {t}" for r, riga, cat, t in rapporto[:400]] + ["", "</details>"]
    _scrivi(os.path.join(destinazione, "CONVERSIONE.md"), "\n".join(md) + "\n")
    return {"destinazione": destinazione, "file_python": len(convertiti), "altri_file": len(altri), "pacchetti": pacchetti,
            "sconosciuti": sconosciuti, "errori": errori, "note": quante, "principale": principale}


def esporta(origine, destinazione, nome_progetto=None):
    """Come converti_progetto ma stampa il riassunto. Ritorna 0 se tutto e' andato bene."""
    try:
        r = converti_progetto(origine, destinazione, nome_progetto)
    except FileExistsError as e:
        print(e)
        return 2
    print(f"Progetto convertito in {r['destinazione']}")
    print(f"  file Python: {r['file_python']}  altri file: {r['altri_file']}  librerie esterne: {len(r['pacchetti'])}  errori: {len(r['errori'])}")
    for f, e in r["errori"]:
        print("  ERRORE", f, e)
    return 0 if not r["errori"] else 1


def tokenizer_errori():
    import tokenize
    return (tokenize.TokenError, IndentationError)


if __name__ == "__main__":
    sys.exit(esporta(sys.argv[1], sys.argv[2]))
