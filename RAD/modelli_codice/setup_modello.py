"""Programma di installazione (Setup) di un programma creato con PitStudio.

PitStudio lo impacchetta con PyInstaller insieme a due file: `setup_pacchetto.zip` (il programma) e `setup_manifesto.json`
(nome, versione, autore, file da avviare). Chi lo riceve fa doppio clic, sceglie la cartella e preme «Installa»: non serve niente altro,
e non servono i permessi di amministratore (si installa nel profilo dell'utente).

Il programma si disinstalla da «App» di Windows: l'installazione copia questo stesso file come «Disinstalla.exe» nella cartella.

Uso da riga di comando (per provarlo o per installare senza finestra):
    Setup.exe                      finestra guidata
    Setup.exe /S                   installa senza finestra (anche --silenzioso)
        --cartella=PERCORSO        dove installare (predefinito: %LOCALAPPDATA%\\Programs\\<nome>)
        --senza-collegamenti       niente collegamenti sul desktop e nel menu Start
    Disinstalla.exe --disinstalla  [--silenzioso]
"""
import json
import os
import shutil
import subprocess
import sys
import zipfile

try:
    import winreg
except ImportError:                       # non Windows: il Setup serve solo lì
    winreg = None

RADICE_REGISTRO = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
NASCONDI = 0x08000000 if os.name == "nt" else 0          # CREATE_NO_WINDOW
FILE_ELENCO = "installato.json"                           # cosa ha creato l'installazione (serve alla disinstallazione)
NOME_DISINSTALLATORE = "Disinstalla.exe"


# ---------------------------------------------------------------- dati incorporati
def risorsa(nome):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


def leggi_manifesto(percorso=None):
    with open(percorso or risorsa("setup_manifesto.json"), encoding="utf-8") as f:
        m = json.load(f)
    m.setdefault("versione", "1.0.0")
    m.setdefault("autore", "")
    m.setdefault("descrizione", "")
    m.setdefault("id", "".join(c for c in m["nome"] if c.isalnum()) or "programma")
    return m


# ---------------------------------------------------------------- cartelle di sistema
def cartella_predefinita(m):
    base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    return os.path.join(base, "Programs", m["nome"])


def cartella_desktop():
    return os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")


def cartella_menu_start():
    return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Microsoft", "Windows", "Start Menu", "Programs")


# ---------------------------------------------------------------- collegamenti
def _ps(testo):
    return "'" + testo.replace("'", "''") + "'"


def crea_collegamento(percorso_lnk, destinazione, cartella="", icona="", descrizione=""):
    """Crea un collegamento .lnk (con PowerShell: nessuna libreria in più). Ritorna True se riuscito."""
    os.makedirs(os.path.dirname(percorso_lnk), exist_ok=True)
    script = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut(%s);$s.TargetPath=%s;$s.WorkingDirectory=%s;$s.IconLocation=%s;$s.Description=%s;$s.Save()"
              % (_ps(percorso_lnk), _ps(destinazione), _ps(cartella or os.path.dirname(destinazione)), _ps(icona or destinazione), _ps(descrizione)))
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script], capture_output=True, text=True, timeout=60,
                           creationflags=NASCONDI)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and os.path.exists(percorso_lnk)


# ---------------------------------------------------------------- installazione
def _estrai(archivio, cartella, avanza=None):
    """Estrae l'archivio nella cartella, rifiutando i percorsi che escono da essa."""
    base = os.path.abspath(cartella)
    with zipfile.ZipFile(archivio) as z:
        nomi = z.namelist()
        for i, nome in enumerate(nomi):
            destinazione = os.path.abspath(os.path.join(base, nome))
            if destinazione != base and not destinazione.startswith(base + os.sep):
                raise ValueError("il pacchetto contiene un percorso non valido: " + nome)
            z.extract(nome, base)
            if avanza:
                avanza(i + 1, len(nomi))


def _dimensione_kb(cartella):
    totale = 0
    for radice, _, files in os.walk(cartella):
        for f in files:
            try:
                totale += os.path.getsize(os.path.join(radice, f))
            except OSError:
                pass
    return totale // 1024


def registra_disinstallazione(m, cartella, disinstallatore):
    """La voce di «App» di Windows (solo per l'utente corrente)."""
    if winreg is None:
        return
    exe = os.path.join(cartella, m["exe"])
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RADICE_REGISTRO + "\\" + m["id"]) as k:
        for nome, valore in (("DisplayName", m["nome"]), ("DisplayVersion", m["versione"]), ("Publisher", m["autore"]),
                             ("InstallLocation", cartella), ("DisplayIcon", exe),
                             ("UninstallString", '"%s" --disinstalla' % disinstallatore),
                             ("QuietUninstallString", '"%s" --disinstalla --silenzioso' % disinstallatore)):
            winreg.SetValueEx(k, nome, 0, winreg.REG_SZ, valore)
        winreg.SetValueEx(k, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(k, "NoRepair", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(k, "EstimatedSize", 0, winreg.REG_DWORD, int(_dimensione_kb(cartella)))


def installa(m, cartella, pacchetto=None, desktop=True, menu=True, avanza=None, disinstallatore_da=None):
    """Copia il programma in `cartella`, crea i collegamenti e la voce di disinstallazione. Ritorna l'elenco di ciò che ha creato.
    `disinstallatore_da`: il file da copiare come Disinstalla.exe (di norma questo stesso Setup)."""
    cartella = os.path.abspath(cartella)
    os.makedirs(cartella, exist_ok=True)
    _estrai(pacchetto or risorsa("setup_pacchetto.zip"), cartella, avanza)
    exe = os.path.join(cartella, m["exe"])
    if not os.path.exists(exe):
        raise FileNotFoundError("nel pacchetto manca " + m["exe"])
    creati = {"cartella": cartella, "collegamenti": [], "id": m["id"]}
    sorgente = disinstallatore_da if disinstallatore_da is not None else (sys.executable if getattr(sys, "frozen", False) else None)
    disinstallatore = os.path.join(cartella, NOME_DISINSTALLATORE)
    if sorgente and os.path.exists(sorgente):
        shutil.copy2(sorgente, disinstallatore)
    if desktop:
        lnk = os.path.join(cartella_desktop(), m["nome"] + ".lnk")
        if crea_collegamento(lnk, exe, cartella, exe, m["descrizione"]):
            creati["collegamenti"].append(lnk)
    if menu:
        lnk = os.path.join(cartella_menu_start(), m["nome"], m["nome"] + ".lnk")
        if crea_collegamento(lnk, exe, cartella, exe, m["descrizione"]):
            creati["collegamenti"].append(lnk)
        if os.path.exists(disinstallatore):
            lnk2 = os.path.join(cartella_menu_start(), m["nome"], "Disinstalla " + m["nome"] + ".lnk")
            if crea_collegamento(lnk2, disinstallatore, cartella, exe, "Disinstalla " + m["nome"]):
                creati["collegamenti"].append(lnk2)
                # il comando di disinstallazione ha bisogno dell'argomento: si scrive nel collegamento
                _argomenti_collegamento(lnk2, "--disinstalla")
    registra_disinstallazione(m, cartella, disinstallatore)
    with open(os.path.join(cartella, FILE_ELENCO), "w", encoding="utf-8") as f:
        json.dump(creati, f, ensure_ascii=False, indent=1)
    return creati


def _argomenti_collegamento(lnk, argomenti):
    script = "$s=(New-Object -ComObject WScript.Shell).CreateShortcut(%s);$s.Arguments=%s;$s.Save()" % (_ps(lnk), _ps(argomenti))
    try:
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script], capture_output=True, timeout=60, creationflags=NASCONDI)
    except (OSError, subprocess.SubprocessError):
        pass


# ---------------------------------------------------------------- disinstallazione
def _rimuovi_dopo_l_uscita(cartella):
    """Un programma non può cancellare il proprio file mentre gira: un piccolo script (in %TEMP%) riprova a togliere la cartella finché ci riesce."""
    import tempfile
    script = os.path.join(tempfile.gettempdir(), "togli_" + os.path.basename(cartella).replace(" ", "_") + ".bat")
    righe = ["@echo off",
             "for /l %%i in (1,1,30) do (",
             '  rmdir /s /q "' + cartella + '" >nul 2>&1',
             '  if not exist "' + cartella + '" goto fine',
             "  ping -n 2 127.0.0.1 >nul",
             ")",
             ":fine",
             'del "%~f0"']
    with open(script, "w", encoding="mbcs", errors="replace", newline="") as f:
        f.write("\r\n".join(righe) + "\r\n")
    subprocess.Popen(["cmd", "/c", script], creationflags=NASCONDI | 0x00000008, close_fds=True)


def disinstalla(cartella, differita=True):
    """Toglie collegamenti, voce di «App» e cartella. Il programma in esecuzione (Disinstalla.exe) non può cancellare se stesso:
    con `differita` la cartella viene tolta da un comando che parte subito dopo l'uscita. Ritorna l'elenco di ciò che è stato tolto."""
    cartella = os.path.abspath(cartella)
    tolti = []
    elenco = {}
    prova = os.path.join(cartella, FILE_ELENCO)
    if os.path.exists(prova):
        try:
            with open(prova, encoding="utf-8") as f:
                elenco = json.load(f)
        except (OSError, ValueError):
            elenco = {}
    for lnk in elenco.get("collegamenti", []):
        try:
            os.remove(lnk)
            tolti.append(lnk)
            cartella_lnk = os.path.dirname(lnk)
            if os.path.normcase(os.path.dirname(cartella_lnk)) == os.path.normcase(cartella_menu_start()) and not os.listdir(cartella_lnk):
                os.rmdir(cartella_lnk)           # la cartella del programma nel menu Start, se è rimasta vuota
        except OSError:
            pass
    if winreg is not None and elenco.get("id"):
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, RADICE_REGISTRO + "\\" + elenco["id"])
            tolti.append("registro")
        except OSError:
            pass
    if os.path.isdir(cartella):
        if differita:
            _rimuovi_dopo_l_uscita(cartella)
        else:
            shutil.rmtree(cartella, ignore_errors=True)
        tolti.append(cartella)
    return tolti


# ---------------------------------------------------------------- finestra
def finestra_installazione(m):
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    radice = tk.Tk()
    radice.title("Installazione di " + m["nome"])
    radice.resizable(False, False)
    larghezza, altezza = 560, 330
    radice.geometry("%dx%d+%d+%d" % (larghezza, altezza, (radice.winfo_screenwidth() - larghezza) // 2, (radice.winfo_screenheight() - altezza) // 3))
    tk.Label(radice, text=m["nome"] + "  " + m["versione"], font=("Segoe UI", 16, "bold"), anchor="w").pack(fill="x", padx=20, pady=(18, 0))
    testo = m["descrizione"] or "Questo programma verrà installato sul tuo computer."
    if m["autore"]:
        testo += "\n" + m["autore"]
    tk.Label(radice, text=testo, anchor="w", justify="left", wraplength=510, fg="#555555").pack(fill="x", padx=20, pady=(2, 10))
    riga = tk.Frame(radice)
    riga.pack(fill="x", padx=20)
    tk.Label(riga, text="Installa in:").pack(side="left")
    var_cartella = tk.StringVar(value=cartella_predefinita(m))
    tk.Entry(riga, textvariable=var_cartella).pack(side="left", fill="x", expand=True, padx=6)
    tk.Button(riga, text="Sfoglia…", command=lambda: var_cartella.set(filedialog.askdirectory(initialdir=os.path.dirname(var_cartella.get())) or var_cartella.get())).pack(side="left")
    var_desktop = tk.BooleanVar(value=True)
    var_menu = tk.BooleanVar(value=True)
    tk.Checkbutton(radice, text="Crea un collegamento sul desktop", variable=var_desktop, anchor="w").pack(fill="x", padx=20, pady=(10, 0))
    tk.Checkbutton(radice, text="Crea un collegamento nel menu Start", variable=var_menu, anchor="w").pack(fill="x", padx=20)
    stato = tk.Label(radice, text="", anchor="w", fg="#555555")
    stato.pack(fill="x", padx=20, pady=(10, 0))
    barra = ttk.Progressbar(radice, maximum=100)
    barra.pack(fill="x", padx=20, pady=4)
    var_avvia = tk.BooleanVar(value=True)
    casella_avvia = tk.Checkbutton(radice, text="Avvia " + m["nome"] + " alla fine", variable=var_avvia, anchor="w")
    fondo = tk.Frame(radice)
    fondo.pack(side="bottom", fill="x", padx=20, pady=14)
    pulsante_chiudi = tk.Button(fondo, text="Annulla", width=12, command=radice.destroy)
    pulsante_chiudi.pack(side="right", padx=(8, 0))
    pulsante = tk.Button(fondo, text="Installa", width=12, default="active")
    pulsante.pack(side="right")
    esito = {}

    def avanza(i, n):
        barra["value"] = 100 * i / max(1, n)
        radice.update_idletasks()

    def installa_ora():
        pulsante.config(state="disabled")
        pulsante_chiudi.config(state="disabled")
        stato.config(text="Copio i file…")
        radice.update_idletasks()
        try:
            esito["creati"] = installa(m, var_cartella.get(), None, var_desktop.get(), var_menu.get(), avanza)
        except Exception as e:                                   # noqa: BLE001 - qualunque problema va detto all'utente
            messagebox.showerror("Installazione non riuscita", str(e))
            radice.destroy()
            return
        barra["value"] = 100
        stato.config(text="Installazione completata.")
        casella_avvia.pack(fill="x", padx=20)
        pulsante.config(text="Fine", state="normal", command=fine)
        pulsante_chiudi.pack_forget()

    def fine():
        cartella = esito["creati"]["cartella"]
        radice.destroy()
        if var_avvia.get():
            subprocess.Popen([os.path.join(cartella, m["exe"])], cwd=cartella, close_fds=True)

    pulsante.config(command=installa_ora)
    radice.mainloop()


def finestra_disinstallazione(m, cartella):
    import tkinter as tk
    from tkinter import messagebox

    radice = tk.Tk()
    radice.withdraw()
    if messagebox.askyesno("Disinstalla " + m["nome"], "Vuoi togliere %s dal computer?\n\nI documenti che hai creato con il programma non vengono toccati." % m["nome"]):
        disinstalla(cartella)
        messagebox.showinfo("Disinstalla " + m["nome"], m["nome"] + " è stato rimosso.")
    radice.destroy()


# ---------------------------------------------------------------- avvio
def main(argv):
    silenzioso = any(a in ("/S", "/s", "--silenzioso") for a in argv)
    cartella = None
    for a in argv:
        if a.startswith("--cartella="):
            cartella = a.split("=", 1)[1]
    try:
        m = leggi_manifesto()
    except (OSError, ValueError, KeyError):
        m = None
    if "--disinstalla" in argv:
        if cartella is None:
            cartella = os.path.dirname(os.path.abspath(sys.executable))
        if silenzioso:
            disinstalla(cartella)
        else:
            finestra_disinstallazione(m or {"nome": os.path.basename(cartella)}, cartella)
        return 0
    if m is None:
        print("Pacchetto di installazione non valido.", file=sys.stderr)
        return 2
    if silenzioso:
        senza = "--senza-collegamenti" in argv
        installa(m, cartella or cartella_predefinita(m), None, not senza, not senza)
        return 0
    finestra_installazione(m)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
