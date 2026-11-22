"""Avvio dei programmi costruiti da PitStudio («Crea l'eseguibile»): se il programma ha un errore, lo registra in un file e avvisa invece di chiudersi in silenzio.

Questo file viene messo accanto al programma al momento della costruzione e diventa il punto di partenza dell'eseguibile: carica il
programma vero (il modulo scritto in _avvio_pit.json) e gli sta intorno. Non cambia il comportamento del programma:
  - un errore non gestito, anche dentro un filo (thread) o dentro un pulsante di una finestra tkinter, viene scritto in errori.log
    (in %LOCALAPPDATA%\\<programma>\\ su Windows, in ~/.local/state/<programma>/ altrove) con data, versione e traceback;
  - nei programmi senza finestra nera compare un avviso con il percorso del registro (altrimenti l'errore sparirebbe nel nulla);
  - nei programmi da console l'errore si vede come sempre e in più resta nel registro.
Il registro si tronca da solo oltre 1 MB. Variabili d'ambiente: PITSTUDIO_SENZA_AVVISI=1 non mostra mai finestre (utile nei test).
"""
import importlib
import importlib.util
import json
import os
import platform
import runpy
import sys
import threading
import time
import traceback

_TK = "tk" + "inter"
DIMENSIONE_MASSIMA = 1024 * 1024
_ultimo_avviso = [0.0]


class _Vuoto:
    """Al posto di stdout/stderr nei programmi senza console (PyInstaller li lascia a None): scrive nel nulla invece di dare errore."""

    def write(self, testo):
        return len(testo)

    def flush(self):
        pass

    def isatty(self):
        return False


def _manifesto():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(os.path.join(base, "_avvio_pit.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"nome": "programma", "id": "programma", "versione": "", "modulo": "principale"}


def cartella_registro(identificativo):
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, identificativo)


def percorso_registro(manifesto=None):
    manifesto = manifesto or _manifesto()
    return os.path.join(cartella_registro(manifesto.get("id") or "programma"), "errori.log")


def scrivi_errore(tipo, valore, tb, contesto="", manifesto=None):
    """Aggiunge l'errore al registro. Ritorna il percorso del file, o None se non si riesce a scrivere (non deve mai dare un altro errore)."""
    manifesto = manifesto or _manifesto()
    percorso = percorso_registro(manifesto)
    try:
        os.makedirs(os.path.dirname(percorso), exist_ok=True)
        if os.path.exists(percorso) and os.path.getsize(percorso) > DIMENSIONE_MASSIMA:
            with open(percorso, "rb") as f:
                f.seek(-DIMENSIONE_MASSIMA // 4, os.SEEK_END)
                coda = f.read()
            with open(percorso, "wb") as f:
                f.write(b"[registro troncato]\n" + coda)
        testo = "".join(traceback.format_exception(tipo, valore, tb))
        intestazione = (f"=== {time.strftime('%Y-%m-%d %H:%M:%S')}  {manifesto.get('nome', '')} {manifesto.get('versione', '')}"
                        f"  (Python {platform.python_version()}, {platform.system()} {platform.release()})"
                        + (f"  [{contesto}]" if contesto else "") + " ===\n")
        with open(percorso, "a", encoding="utf-8") as f:
            f.write(intestazione + testo + "\n")
        return percorso
    except Exception:
        return None


def _senza_console():
    return sys.__stderr__ is None or sys.__stdout__ is None


def _avvisa(manifesto, percorso, fatale):
    """Una finestra con il percorso del registro: solo per i programmi senza console, e mai troppo spesso."""
    if os.environ.get("PITSTUDIO_SENZA_AVVISI") == "1" or not _senza_console():
        return
    if not fatale and time.time() - _ultimo_avviso[0] < 10:
        return
    _ultimo_avviso[0] = time.time()
    try:
        tkinter = importlib.import_module(_TK)               # import «dinamico»: così PyInstaller non include tkinter in un programma che non lo usa
        messagebox = importlib.import_module(_TK + ".messagebox")
        radice = tkinter.Tk()
        radice.withdraw()
        nome = manifesto.get("nome") or "Il programma"
        if percorso:
            testo = f"{nome} ha avuto un problema" + (" e deve chiudersi." if fatale else " (ma può continuare).") + \
                    f"\n\nI dettagli sono stati salvati in:\n{percorso}\n\nVuoi aprire la cartella con il registro?"
            if messagebox.askyesno(nome, testo, icon="error", parent=radice):
                _apri(os.path.dirname(percorso))
        else:
            messagebox.showerror(nome, f"{nome} ha avuto un problema" + (" e deve chiudersi." if fatale else "."), parent=radice)
        radice.destroy()
    except Exception:
        pass


def _apri(cartella):
    try:
        if os.name == "nt":
            os.startfile(cartella)
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", cartella])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", cartella])
    except Exception:
        pass


def _gestisci(tipo, valore, tb, contesto="", fatale=True, manifesto=None):
    manifesto = manifesto or _manifesto()
    percorso = scrivi_errore(tipo, valore, tb, contesto, manifesto)
    try:
        traceback.print_exception(tipo, valore, tb)          # nei programmi da console l'errore si vede come sempre
    except Exception:
        pass
    _avvisa(manifesto, percorso, fatale)


def installa(manifesto=None):
    """Prepara l'ambiente: flussi di uscita al sicuro, e i tre posti dove un errore sfuggirebbe (programma, fili, pulsanti di tkinter)."""
    manifesto = manifesto or _manifesto()
    if sys.stdout is None:
        sys.stdout = _Vuoto()
    if sys.stderr is None:
        sys.stderr = _Vuoto()
    sys.excepthook = lambda tipo, valore, tb: _gestisci(tipo, valore, tb, "", True, manifesto)
    threading.excepthook = lambda a: _gestisci(a.exc_type, a.exc_value, a.exc_traceback, "filo " + (a.thread.name if a.thread else "?"), False, manifesto)
    try:
        tkinter = importlib.import_module(_TK) if importlib.util.find_spec(_TK) else None
        if tkinter is None:
            return

        def segnala(self, tipo, valore, tb):
            _gestisci(tipo, valore, tb, "finestra", False, manifesto)
        tkinter.Tk.report_callback_exception = segnala          # la radice è quella che riceve gli errori dei pulsanti
        tkinter.Misc.report_callback_exception = segnala
    except ImportError:
        pass


def main():
    manifesto = _manifesto()
    installa(manifesto)
    try:
        runpy.run_module(manifesto.get("modulo", "principale"), run_name="__main__", alter_sys=True)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(130)
    except BaseException:
        tipo, valore, tb = sys.exc_info()
        _gestisci(tipo, valore, tb.tb_next or tb, "", True, manifesto)
        sys.exit(1)


if __name__ == "__main__":
    main()
