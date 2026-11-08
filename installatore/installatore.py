"""Installazione guidata di pytonIta (interprete pitonit + ambiente PitStudio).

Interattivo (finestra a passi) oppure silenzioso:
    Installa_pytonIta.exe /S [/D=cartella] [/NOSCI] [/NOPITSTUDIO] [/NOASSOC] [/NOPATH] [/NOMENU] [/DESKTOP]
"""
import ctypes
import json
import os
import subprocess
import sys
import threading
import time
import traceback
import zipfile

try:
    from _versione import VERSIONE      # scritto da costruisci.py: 1.1.<versione di Python di pitonit>
except ImportError:
    VERSIONE = "1.1"
NOME = "pytonIta"
CHIAVE_DISINSTALLA = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\pytonIta"
CREA_SENZA_FINESTRA = 0x08000000


def risorsa(*parti):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parti)


def cartella_pacchetti():
    p = risorsa("pacchetti")
    return p


PACCHETTI = {
    "pitonit": ("pitonit.zip", "Interprete pitonit e librerie italiane", True),
    "rad": ("rad.zip", "PitStudio - ambiente di sviluppo", False),
    "scientifiche": ("scientifiche.zip", "Librerie scientifiche (numpy, pandas, scipy, matplotlib)", False),
}


def dimensione_pacchetto(chiave):
    percorso = os.path.join(cartella_pacchetti(), PACCHETTI[chiave][0])
    try:
        with zipfile.ZipFile(percorso) as z:
            return sum(i.file_size for i in z.infolist())
    except OSError:
        return 0


def mb(n):
    return f"{n / 1e6:.0f} MB"


# ===================================================================== operazioni di sistema
def powershell(script):
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                   creationflags=CREA_SENZA_FINESTRA, capture_output=True, timeout=60)


def crea_collegamento(percorso_lnk, destinazione, argomenti="", cartella="", icona="", descrizione=""):
    os.makedirs(os.path.dirname(percorso_lnk), exist_ok=True)

    def q(t):
        return "'" + str(t).replace("'", "''") + "'"
    script = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut(%s);$s.TargetPath=%s;$s.Arguments=%s;"
              "$s.WorkingDirectory=%s;$s.IconLocation=%s;$s.Description=%s;$s.Save()"
              % (q(percorso_lnk), q(destinazione), q(argomenti), q(cartella), q(icona or destinazione), q(descrizione)))
    powershell(script)


def cartella_menu_start():
    return os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "pytonIta")


def cartella_desktop():
    try:
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0000, None, 0, buf)   # CSIDL_DESKTOPDIRECTORY
        if buf.value:
            return buf.value
    except Exception:
        pass
    return os.path.join(os.environ["USERPROFILE"], "Desktop")


def notifica_ambiente():
    try:
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, ctypes.byref(ctypes.c_ulong()))
    except Exception:
        pass


def aggiungi_al_path(cartella):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as k:
        try:
            valore, tipo = winreg.QueryValueEx(k, "Path")
        except FileNotFoundError:
            valore, tipo = "", winreg.REG_EXPAND_SZ
        voci = [v for v in valore.split(";") if v]
        if cartella.lower() not in [v.lower().rstrip("\\") for v in voci]:
            voci.append(cartella)
            winreg.SetValueEx(k, "Path", 0, tipo or winreg.REG_EXPAND_SZ, ";".join(voci))
    notifica_ambiente()


def registra_estensione(cartella, con_rad):
    import winreg

    def imposta(percorso, valore, nome=""):
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, percorso) as k:
            winreg.SetValueEx(k, nome, 0, winreg.REG_SZ, valore)
    pit = os.path.join(cartella, "pitonit", "pitonit.exe")
    pitw = os.path.join(cartella, "pitonit", "pitonitw.exe")
    base = r"Software\Classes\Pitonit.Programma"
    imposta(r"Software\Classes\.pit", "Pitonit.Programma")
    imposta(base, "Programma pytonIta")
    imposta(base + r"\DefaultIcon", os.path.join(cartella, "pitonit.ico"))
    imposta(base + r"\shell\open", "Esegui con pitonit")
    imposta(base + r"\shell\open\command", '"%s" "%%1" %%*' % pit)
    if con_rad:
        rad = os.path.join(cartella, "PitStudio.exe")
        imposta(base + r"\shell\modifica", "Modifica con PitStudio")
        imposta(base + r"\shell\modifica\command", '"%s" "%%1"' % rad)
    try:
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, None, None)
    except Exception:
        pass
    return pit, pitw


def registra_disinstallazione(cartella, dimensione_kb, con_rad):
    import winreg
    uninst = '"%s" "%s"' % (os.path.join(cartella, "pitonit", "pitonitw.exe"), os.path.join(cartella, "disinstalla.pit"))
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, CHIAVE_DISINSTALLA) as k:
        for nome, valore in (("DisplayName", "pytonIta (pitonit + PitStudio)" if con_rad else "pytonIta (pitonit)"),
                             ("DisplayVersion", VERSIONE), ("Publisher", "pytonIta"),
                             ("InstallLocation", cartella),
                             ("DisplayIcon", os.path.join(cartella, "PitStudio.exe") if con_rad else os.path.join(cartella, "pitonit", "pitonit.exe")),
                             ("UninstallString", uninst)):
            winreg.SetValueEx(k, nome, 0, winreg.REG_SZ, valore)
        winreg.SetValueEx(k, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(k, "NoRepair", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(k, "EstimatedSize", 0, winreg.REG_DWORD, int(dimensione_kb))


SCRIPT_DISINSTALLA = r'''"""Disinstalla pytonIta (scritto in pytonIta, eseguito da pitonitw)."""
importa os, sys, subprocess, winreg, ctypes
importa tkinter come tk
da tkinter importa messagebox

CARTELLA = os.path.dirname(os.path.abspath(__file__))
SENZA_FINESTRA = 0x08000000


definisci rimuovi_chiave(percorso):
    subprocess.run(["reg", "delete", "HKCU\\" + percorso, "/f"], creationflags=SENZA_FINESTRA, capture_output=Vero)


definisci togli_dal_path():
    prova:
        con winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) come k:
            valore, tipo = winreg.QueryValueEx(k, "Path")
            nostra = os.path.join(CARTELLA, "pitonit").lower()
            voci = [v per v in valore.split(";") se v e v.lower().rstrip("\\") != nostra]
            winreg.SetValueEx(k, "Path", 0, tipo, ";".join(voci))
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, ctypes.byref(ctypes.c_ulong()))
    eccetto Exception:
        passa


definisci principale():
    radice = tk.Tk()
    radice.withdraw()
    se non messagebox.askyesno("Disinstalla pytonIta",
                               "Vuoi rimuovere pytonIta (interprete pitonit e PitStudio) da:\n\n" + CARTELLA +
                               "\n\nI tuoi programmi e progetti fuori da questa cartella non vengono toccati.",
                               parent=radice):
        ritorna
    togli_dal_path()
    rimuovi_chiave(r"Software\Classes\.pit")
    rimuovi_chiave(r"Software\Classes\Pitonit.Programma")
    rimuovi_chiave(r"Software\Microsoft\Windows\CurrentVersion\Uninstall\pytonIta")
    menu = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "pytonIta")
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop", "PitStudio.lnk")
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", menu], creationflags=SENZA_FINESTRA, capture_output=Vero)
    # il collegamento sul desktop si toglie solo se punta a questa installazione (potrebbe essercene uno dell'utente con lo stesso nome)
    prova:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "(New-Object -ComObject WScript.Shell).CreateShortcut('" + desktop + "').TargetPath"],
                           capture_output=Vero, text=Vero, creationflags=SENZA_FINESTRA, timeout=30)
        destinazione = r.stdout.strip().lower()
        se destinazione e destinazione.startswith(CARTELLA.lower()):
            os.remove(desktop)
    eccetto (OSError, subprocess.SubprocessError):
        passa
    # la cartella contiene questo stesso programma: la cancella un processo separato, dopo che siamo usciti
    subprocess.Popen('cmd /c ping -n 3 127.0.0.1 >nul & rmdir /s /q "' + CARTELLA + '"',
                     creationflags=SENZA_FINESTRA | 0x00000008, close_fds=Vero)
    messagebox.showinfo("Disinstalla pytonIta", "pytonIta è stato rimosso.", parent=radice)


principale()
'''


# ===================================================================== installazione vera e propria
class Opzioni:
    def __init__(self):
        self.cartella = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", "pytonIta")
        self.rad = True
        self.scientifiche = True
        self.associa = True
        self.path = True
        self.menu = True
        self.desktop = False


FILE_DA_CONTROLLARE = ("PitStudio.exe", os.path.join("pitonit", "pitonit.exe"), os.path.join("pitonit", "pitonitw.exe"),
                       os.path.join("pitonit", "python313.dll"), os.path.join("pitonit", "DLLs", "_tkinter.pyd"))


def in_uso(cartella):
    """File di una installazione esistente che non si possono sostituire perché il programma è aperto."""
    bloccati = []
    for rel in FILE_DA_CONTROLLARE:
        percorso = os.path.join(cartella, rel)
        if os.path.exists(percorso):
            try:
                with open(percorso, "ab"):
                    pass
            except OSError:
                bloccati.append(rel)
    return bloccati


def versione_installata(cartella):
    """Versione di pytonIta già installata in cartella (o None)."""
    try:
        with open(os.path.join(cartella, "installazione.json"), encoding="utf-8") as f:
            return json.load(f).get("versione")
    except (OSError, ValueError):
        return None


class ProgrammaInUso(Exception):
    pass


def installa(op, avanza, scrivi):
    """Esegue l'installazione. avanza(frazione, testo) e scrivi(riga) aggiornano l'interfaccia."""
    cartella = os.path.abspath(op.cartella)
    bloccati = in_uso(cartella)
    if bloccati:
        raise ProgrammaInUso("pytonIta è in esecuzione: chiudi PitStudio e i programmi pitonit aperti, poi riprova. (File in uso: "
                             + ", ".join(bloccati) + ")")
    precedente = versione_installata(cartella)
    if precedente:
        scrivi(f"Aggiorno l'installazione esistente (versione {precedente}) alla {VERSIONE}")
    scelti = ["pitonit"] + (["rad"] if op.rad else []) + (["scientifiche"] if op.scientifiche else [])
    totale = 0
    infos = {}
    for chiave in scelti:
        percorso = os.path.join(cartella_pacchetti(), PACCHETTI[chiave][0])
        z = zipfile.ZipFile(percorso)
        infos[chiave] = z
        totale += sum(i.file_size for i in z.infolist())
    os.makedirs(cartella, exist_ok=True)
    fatto = 0
    ultimo = 0.0
    for chiave in scelti:
        scrivi(f"Copio: {PACCHETTI[chiave][1]}")
        z = infos[chiave]
        for info in z.infolist():
            z.extract(info, cartella)
            fatto += info.file_size
            adesso = time.time()
            if adesso - ultimo > 0.08:
                avanza(fatto / max(1, totale) * 0.9, info.filename)
                ultimo = adesso
        z.close()
    avanza(0.92, "Configurazione…")
    shutil_copia(risorsa("pitonit.ico"), os.path.join(cartella, "pitonit.ico"))
    shutil_copia(risorsa("rad.ico"), os.path.join(cartella, "rad.ico"))
    with open(os.path.join(cartella, "disinstalla.pit"), "w", encoding="utf-8", newline="\n") as f:
        f.write(SCRIPT_DISINSTALLA)
    pit = os.path.join(cartella, "pitonit", "pitonit.exe")
    pitw = os.path.join(cartella, "pitonit", "pitonitw.exe")
    rad = os.path.join(cartella, "PitStudio.exe")
    if op.associa:
        scrivi("Associo i file .pit a pitonit")
        registra_estensione(cartella, op.rad)
    if op.path:
        scrivi("Aggiungo pitonit al PATH dell'utente")
        aggiungi_al_path(os.path.join(cartella, "pitonit"))
    if op.menu:
        scrivi("Creo i collegamenti nel menu Start")
        m = cartella_menu_start()
        if op.rad:
            crea_collegamento(os.path.join(m, "PitStudio.lnk"), rad, cartella=cartella,
                              icona=rad, descrizione="PitStudio - ambiente di sviluppo per pytonIta")
        crea_collegamento(os.path.join(m, "Console pitonit.lnk"), "cmd.exe",
                          argomenti='/k "%s" -i' % pit, cartella=os.path.expanduser("~"), icona=os.path.join(cartella, "pitonit.ico"),
                          descrizione="Interprete interattivo pitonit")
        crea_collegamento(os.path.join(m, "Disinstalla pytonIta.lnk"), pitw, argomenti='"%s"' % os.path.join(cartella, "disinstalla.pit"),
                          cartella=cartella, icona=os.path.join(cartella, "pitonit.ico"))
        if op.rad:
            crea_collegamento(os.path.join(m, "Guida di PitStudio.lnk"), os.path.join(cartella, "PitStudio", "aiuto", "html", "index.html"))
    if op.desktop and op.rad:
        scrivi("Creo il collegamento sul desktop")
        crea_collegamento(os.path.join(cartella_desktop(), "PitStudio.lnk"), rad, cartella=cartella, icona=rad)
    kb = totale / 1024
    registra_disinstallazione(cartella, kb, op.rad)
    with open(os.path.join(cartella, "installazione.json"), "w", encoding="utf-8") as f:
        json.dump({"versione": VERSIONE, "componenti": scelti, "associa": op.associa, "path": op.path}, f, indent=2)
    avanza(0.97, "Verifica…")
    scrivi("Verifico l'installazione")
    r = subprocess.run([pit, "-c", "stampa('pitonit funziona:', 6 * 7)"], capture_output=True, text=True,
                       encoding="utf-8", creationflags=CREA_SENZA_FINESTRA, timeout=120)
    if r.returncode != 0 or "42" not in r.stdout:
        raise RuntimeError("pitonit non parte dopo l'installazione:\n" + (r.stderr or r.stdout))
    scrivi(r.stdout.strip())
    avanza(1.0, "Fatto")
    return cartella


def shutil_copia(a, b):
    import shutil
    shutil.copyfile(a, b)


# ===================================================================== finestra a passi
def avvia_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    BLU = "#2563eb"
    SCURO = "#0f172a"
    op = Opzioni()
    radice = tk.Tk()
    radice.title(f"Installazione di {NOME} {VERSIONE}")
    radice.geometry("760x520")
    radice.resizable(False, False)
    try:
        radice.iconbitmap(risorsa("rad.ico"))
    except Exception:
        pass
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    stile = ttk.Style(radice)
    try:
        stile.theme_use("vista")
    except Exception:
        pass
    stile.configure("Titolo.TLabel", font=("Segoe UI Semibold", 16))
    stile.configure("Sotto.TLabel", font=("Segoe UI", 10), foreground="#555555")
    stile.configure("TCheckbutton", font=("Segoe UI", 10))
    stile.configure("TLabel", font=("Segoe UI", 10))

    banda = tk.Frame(radice, bg=SCURO, width=210)
    banda.pack(side="left", fill="y")
    banda.pack_propagate(False)
    tk.Label(banda, text="pytonIta", bg=SCURO, fg="white", font=("Segoe UI Semibold", 22)).pack(pady=(40, 0))
    tk.Label(banda, text="Python in italiano\n+ ambiente PitStudio", bg=SCURO, fg="#93c5fd", font=("Segoe UI", 11), justify="center").pack(pady=(4, 30))
    voci_banda = []
    for t in ("Benvenuto", "Componenti", "Opzioni", "Installazione", "Fine"):
        et = tk.Label(banda, text="   " + t, bg=SCURO, fg="#64748b", anchor="w", font=("Segoe UI", 11))
        et.pack(fill="x", padx=20, pady=5)
        voci_banda.append(et)
    tk.Label(banda, text=f"versione {VERSIONE}", bg=SCURO, fg="#475569", font=("Segoe UI", 9)).pack(side="bottom", pady=14)

    destra = tk.Frame(radice)
    destra.pack(side="left", fill="both", expand=True)
    contenuto = ttk.Frame(destra, padding=(26, 24, 26, 8))
    contenuto.pack(fill="both", expand=True)
    sep = ttk.Separator(destra)
    sep.pack(fill="x")
    barra = ttk.Frame(destra, padding=(26, 12))
    barra.pack(fill="x")
    b_annulla = ttk.Button(barra, text="Annulla", command=lambda: chiudi())
    b_annulla.pack(side="left")
    b_avanti = ttk.Button(barra, text="Avanti  ›")
    b_avanti.pack(side="right")
    b_indietro = ttk.Button(barra, text="‹  Indietro")
    b_indietro.pack(side="right", padx=8)

    stato = {"pagina": 0, "installando": False, "finito": False, "cartella": ""}
    v_cartella = tk.StringVar(value=op.cartella)
    v = {k: tk.BooleanVar(value=getattr(op, k)) for k in ("rad", "scientifiche", "associa", "path", "menu", "desktop")}
    v_lancia = tk.BooleanVar(value=True)
    v_guida = tk.BooleanVar(value=False)
    dim = {k: dimensione_pacchetto(k) for k in PACCHETTI}
    widget_prog = {}

    def svuota():
        for w in contenuto.winfo_children():
            w.destroy()

    def titolo(testo, sotto=""):
        ttk.Label(contenuto, text=testo, style="Titolo.TLabel").pack(anchor="w")
        if sotto:
            ttk.Label(contenuto, text=sotto, style="Sotto.TLabel", wraplength=480, justify="left").pack(anchor="w", pady=(2, 14))

    def spazio_necessario():
        n = dim["pitonit"]
        if v["rad"].get():
            n += dim["rad"]
        if v["scientifiche"].get():
            n += dim["scientifiche"]
        return n

    def pagina_benvenuto():
        titolo("Benvenuto", "Questa procedura installa pytonIta sul tuo computer.")
        testo = ("• pitonit: un interprete Python vero, con parole chiave, funzioni e librerie in italiano.\n"
                 "  I programmi sono file .pit; quelli .py continuano a funzionare come Python normale.\n\n"
                 "• PitStudio: l'ambiente di sviluppo (editor con suggerimenti, progettista di finestre,\n"
                 "  programmazione a mattonelle, assistente AI, guida integrata).\n\n"
                 "Non servono i permessi di amministratore e non c'è conflitto con un eventuale Python già installato.\n\n"
                 "Premi Avanti per continuare.")
        ttk.Label(contenuto, text=testo, justify="left", wraplength=500).pack(anchor="w")

    def sfoglia():
        c = filedialog.askdirectory(parent=radice, initialdir=os.path.dirname(v_cartella.get()) or None, title="Cartella di installazione")
        if c:
            v_cartella.set(os.path.normpath(os.path.join(c, NOME)) if os.listdir(c) else os.path.normpath(c))

    def pagina_componenti():
        titolo("Cartella e componenti", "Scegli dove installare e cosa installare.")
        riga = ttk.Frame(contenuto)
        riga.pack(fill="x")
        ttk.Entry(riga, textvariable=v_cartella).pack(side="left", fill="x", expand=True)
        ttk.Button(riga, text="Sfoglia…", command=sfoglia).pack(side="left", padx=(8, 0))
        ttk.Separator(contenuto).pack(fill="x", pady=14)
        c1 = ttk.Checkbutton(contenuto, text=f"pitonit — interprete e librerie in italiano  ({mb(dim['pitonit'])})  [necessario]")
        c1.state(["selected", "disabled"])
        c1.pack(anchor="w", pady=3)
        ttk.Checkbutton(contenuto, text=f"PitStudio — ambiente di sviluppo  ({mb(dim['rad'])})", variable=v["rad"], command=aggiorna_spazio).pack(anchor="w", pady=3)
        ttk.Checkbutton(contenuto, text=f"Librerie scientifiche: numpy, pandas, scipy, matplotlib  ({mb(dim['scientifiche'])})",
                        variable=v["scientifiche"], command=aggiorna_spazio).pack(anchor="w", pady=3)
        ttk.Label(contenuto, text="Le librerie scientifiche sono facoltative: senza di esse i moduli italiani\n«numerico», «tabelle», «scienza» e «grafici» non sono utilizzabili.",
                  style="Sotto.TLabel").pack(anchor="w", pady=(6, 0))
        widget_prog["spazio"] = ttk.Label(contenuto, text="")
        widget_prog["spazio"].pack(anchor="w", pady=(18, 0))
        aggiorna_spazio()

    def aggiorna_spazio():
        e = widget_prog.get("spazio")
        if e is not None and e.winfo_exists():
            try:
                import shutil
                p = v_cartella.get()
                while p and not os.path.exists(p):
                    nuovo = os.path.dirname(p)
                    if nuovo == p:
                        break
                    p = nuovo
                libero = shutil.disk_usage(p or "C:\\").free
                e.configure(text=f"Spazio necessario: circa {mb(spazio_necessario())}   —   disponibile: {libero / 1e9:.1f} GB")
            except Exception:
                e.configure(text=f"Spazio necessario: circa {mb(spazio_necessario())}")

    def pagina_opzioni():
        titolo("Opzioni", "Come integrare pytonIta in Windows.")
        ttk.Checkbutton(contenuto, text="Associa i file .pit a pitonit (doppio clic per eseguirli; «Modifica con PitStudio» nel menu)", variable=v["associa"]).pack(anchor="w", pady=4)
        ttk.Checkbutton(contenuto, text="Aggiungi pitonit al PATH (per scrivere «pitonit» in qualsiasi terminale)", variable=v["path"]).pack(anchor="w", pady=4)
        ttk.Checkbutton(contenuto, text="Crea i collegamenti nel menu Start", variable=v["menu"]).pack(anchor="w", pady=4)
        c = ttk.Checkbutton(contenuto, text="Crea un collegamento a PitStudio sul desktop", variable=v["desktop"])
        c.pack(anchor="w", pady=4)
        if not v["rad"].get():
            v["desktop"].set(False)
            c.state(["disabled"])
        ttk.Separator(contenuto).pack(fill="x", pady=16)
        riepilogo = (f"Cartella: {v_cartella.get()}\nComponenti: pitonit" + (" + PitStudio" if v["rad"].get() else "") +
                     (" + librerie scientifiche" if v["scientifiche"].get() else "") + f"\nSpazio: circa {mb(spazio_necessario())}")
        ttk.Label(contenuto, text=riepilogo, style="Sotto.TLabel", justify="left").pack(anchor="w")
        ttk.Label(contenuto, text="\nPremi Installa per cominciare.").pack(anchor="w")

    def pagina_installazione():
        titolo("Installazione in corso", "Attendi qualche istante…")
        widget_prog["testo"] = ttk.Label(contenuto, text="Preparazione…", style="Sotto.TLabel")
        widget_prog["testo"].pack(anchor="w", pady=(0, 6))
        widget_prog["barra"] = ttk.Progressbar(contenuto, maximum=100, length=480)
        widget_prog["barra"].pack(fill="x")
        riquadro = tk.Text(contenuto, height=11, wrap="word", font=("Consolas", 9), relief="flat", bg="#f4f6f8", state="disabled")
        riquadro.pack(fill="both", expand=True, pady=(14, 0))
        widget_prog["log"] = riquadro

    def log(riga):
        def f():
            r = widget_prog.get("log")
            if r is not None and r.winfo_exists():
                r.configure(state="normal")
                r.insert("end", riga + "\n")
                r.see("end")
                r.configure(state="disabled")
        radice.after(0, f)

    def avanza(frazione, testo):
        def f():
            b = widget_prog.get("barra")
            if b is not None and b.winfo_exists():
                b["value"] = frazione * 100
                widget_prog["testo"].configure(text=testo if len(testo) < 70 else "…" + testo[-66:])
        radice.after(0, f)

    def pagina_fine(errore=None):
        svuota()
        if errore:
            titolo("Installazione non riuscita", "Qualcosa è andato storto.")
            r = tk.Text(contenuto, height=14, wrap="word", font=("Consolas", 9), relief="flat", bg="#fff4f4")
            r.insert("1.0", errore)
            r.configure(state="disabled")
            r.pack(fill="both", expand=True)
            return
        titolo("Installazione completata", f"pytonIta è installato in\n{stato['cartella']}")
        if v["rad"].get():
            ttk.Checkbutton(contenuto, text="Avvia PitStudio adesso", variable=v_lancia).pack(anchor="w", pady=4)
            ttk.Checkbutton(contenuto, text="Apri la guida di PitStudio nel browser", variable=v_guida).pack(anchor="w", pady=4)
        testo = ("\nPer provare l'interprete apri «Console pitonit» dal menu Start, oppure scrivi\n    pitonit programma.pit\n"
                 "in un terminale (se hai scelto il PATH, dopo averlo riaperto).\n\n"
                 "Per disinstallare: Impostazioni di Windows → App, oppure il collegamento «Disinstalla pytonIta».")
        ttk.Label(contenuto, text=testo, justify="left", wraplength=500).pack(anchor="w", pady=(14, 0))

    def mostra(n):
        stato["pagina"] = n
        svuota()
        for i, et in enumerate(voci_banda):
            et.configure(fg="white" if i == n else ("#94a3b8" if i < n else "#64748b"),
                         font=("Segoe UI Semibold", 11) if i == n else ("Segoe UI", 11))
        b_indietro.state(["!disabled"] if 0 < n < 3 else ["disabled"])
        b_avanti.state(["!disabled"])
        b_annulla.state(["!disabled"])
        if n == 0:
            pagina_benvenuto()
            b_avanti.configure(text="Avanti  ›")
        elif n == 1:
            pagina_componenti()
            b_avanti.configure(text="Avanti  ›")
        elif n == 2:
            pagina_opzioni()
            b_avanti.configure(text="Installa")
        elif n == 3:
            pagina_installazione()
            b_avanti.state(["disabled"])
            b_indietro.state(["disabled"])
            b_annulla.state(["disabled"])
            b_avanti.configure(text="Avanti  ›")
            avvia_installazione()
        elif n == 4:
            b_annulla.state(["disabled"])
            b_indietro.state(["disabled"])
            b_avanti.configure(text="Fine")

    def avvia_installazione():
        for k in v:
            setattr(op, k, v[k].get())
        op.cartella = v_cartella.get().strip()
        stato["installando"] = True

        def lavoro():
            try:
                stato["cartella"] = installa(op, avanza, log)
                esito = None
            except ProgrammaInUso as errore:
                esito = str(errore)
            except Exception:
                esito = traceback.format_exc()
            stato["installando"] = False

            def chiudi_pagina():
                mostra(4)
                pagina_fine(esito)
                if esito:
                    b_avanti.configure(text="Chiudi")
                    stato["finito"] = True
                else:
                    stato["finito"] = True
            radice.after(0, chiudi_pagina)
        threading.Thread(target=lavoro, daemon=True).start()

    def avanti():
        n = stato["pagina"]
        if n == 1:
            c = v_cartella.get().strip()
            if not c or not os.path.isabs(c):
                messagebox.showwarning(NOME, "Indica una cartella di installazione valida (percorso completo).", parent=radice)
                return
            if os.path.exists(c) and os.listdir(c) and not os.path.exists(os.path.join(c, "installazione.json")):
                if not messagebox.askyesno(NOME, f"La cartella\n{c}\nnon è vuota e non contiene una installazione di pytonIta.\nInstallare comunque qui?", parent=radice):
                    return
        if n == 2:      # sta per partire l'installazione: niente programmi aperti dentro la cartella
            c = v_cartella.get().strip()
            while in_uso(os.path.abspath(c)):
                if not messagebox.askretrycancel(NOME, "PitStudio (o un programma pitonit) è aperto in questa cartella.\n"
                                                 "Chiudilo e premi Riprova per continuare.", parent=radice):
                    return
        if n == 4:
            if not (stato["finito"] and stato["cartella"]):
                radice.destroy()
                return
            rad = os.path.join(stato["cartella"], "PitStudio.exe")
            if v["rad"].get() and v_lancia.get() and os.path.exists(rad):
                subprocess.Popen([rad], cwd=os.path.dirname(rad), creationflags=CREA_SENZA_FINESTRA)
            if v["rad"].get() and v_guida.get():
                guida = os.path.join(stato["cartella"], "PitStudio", "aiuto", "html", "index.html")
                if os.path.exists(guida):
                    os.startfile(guida)
            radice.destroy()
            return
        mostra(n + 1)

    def indietro():
        if 0 < stato["pagina"] < 3:
            mostra(stato["pagina"] - 1)

    def chiudi():
        if stato["installando"]:
            return
        if stato["pagina"] < 4 and not messagebox.askyesno(NOME, "Vuoi davvero interrompere l'installazione?", parent=radice):
            return
        radice.destroy()

    b_avanti.configure(command=avanti)
    b_indietro.configure(command=indietro)
    radice.protocol("WM_DELETE_WINDOW", chiudi)
    mostra(0)
    radice.mainloop()
    return radice


def avvia_silenzioso(argv):
    op = Opzioni()
    for a in argv:
        u = a.upper()
        if u.startswith("/D="):
            op.cartella = a[3:].strip('"')
        elif u == "/NOSCI":
            op.scientifiche = False
        elif u in ("/NORAD", "/NOPITSTUDIO"):
            op.rad = False
        elif u == "/NOASSOC":
            op.associa = False
        elif u == "/NOPATH":
            op.path = False
        elif u == "/NOMENU":
            op.menu = False
        elif u == "/DESKTOP":
            op.desktop = True
    cartella = installa(op, lambda f, t: None, lambda r: print(r, flush=True))
    print("Installato in", cartella)


if __name__ == "__main__":
    args = sys.argv[1:]
    if any(a.upper() == "/S" for a in args):
        if sys.stdout is None:      # exe senza console: il rapporto va in un file accanto all'installatore
            sys.stdout = sys.stderr = open(os.path.join(os.environ.get("TEMP", "."), "installa_pytonIta.log"), "w", encoding="utf-8")
        try:
            avvia_silenzioso(args)
        except Exception:
            traceback.print_exc()
            sys.exit(1)
    else:
        avvia_gui()
