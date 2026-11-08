"""Hook di Claude Code per i progetti PitStudio.

Lo esegue Claude Code (tramite pitonit.exe) a ogni evento configurato in .claude/settings.local.json del progetto;
l'evento arriva come JSON su stdin. Fa tre cose, tutte locali:

  UserPromptSubmit   fotografa i file del progetto: serve al pulsante «Annulla» di PitStudio;
  PostToolUse        dopo ogni scrittura di un .pit/.py ne controlla la sintassi e, se è sbagliata, lo dice a Claude (exit 2);
  Stop               chiude la richiesta: se qualcosa è cambiato nasce un gruppo annullabile.

Non parla con la rete e non legge né conserva alcuna credenziale. Qualunque problema interno finisce in silenzio (exit 0):
un hook non deve mai bloccare il lavoro.
"""
import json
import os
import sys
import time

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(QUI))          # cartella che contiene il pacchetto rad


def radice_progetto(cartella):
    """Risale da cartella fino a trovare progetto.rad.json (la radice di un progetto PitStudio)."""
    c = os.path.abspath(cartella)
    while True:
        if os.path.exists(os.path.join(c, "progetto.rad.json")):
            return c
        padre = os.path.dirname(c)
        if padre == c:
            return None
        c = padre


def leggi_evento():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return {}


def registro(radice):
    from rad.registro_ai import RegistroAI
    return RegistroAI(os.path.join(radice, ".rad", "ai_registro.jsonl"))


def al_prompt(ev, radice):
    from rad.progetto import Progetto
    from rad.storia import Storia
    storia = Storia(Progetto(radice))
    id_richiesta = (ev.get("prompt_id") or ev.get("session_id") or "cc")[:6] + time.strftime("%H%M%S")
    descrizione = " ".join((ev.get("prompt") or "").split())[:120]
    storia.inizia_persistente(id_richiesta, "Claude Code: " + descrizione)
    registro(radice).scrivi("richiesta", richiesta=id_richiesta, motore="claude_code", domanda=descrizione[:80])


def dopo_scrittura(ev, radice):
    dati = ev.get("tool_input") or {}
    percorso = dati.get("file_path") or dati.get("path")
    if not percorso or not percorso.lower().endswith((".pit", ".py", ".pyw")):
        return 0
    percorso = os.path.abspath(percorso)
    try:
        with open(percorso, "rb") as f:
            contenuto = f.read().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    from rad import esecuzione
    errore = esecuzione.controlla_sintassi(contenuto, percorso)
    rel = os.path.relpath(percorso, radice)
    linguaggio = "py" if percorso.lower().endswith((".py", ".pyw")) else "pit"
    if errore is None:
        registro(radice).scrivi("scrittura", motore="claude_code", file=rel, linguaggio=linguaggio, esito="valido")
        return 0
    riga, colonna, messaggio = errore
    registro(radice).scrivi("scrittura", motore="claude_code", file=rel, linguaggio=linguaggio, esito="sintassi", errore=str(messaggio)[:200])
    sys.stderr.write(f"PitStudio: il file {rel} ha un errore di sintassi alla riga {riga}, colonna {colonna}: {messaggio}\n"
                     "Correggilo prima di continuare (i file .pit usano le parole chiave italiane: se, per, definisci, ritorna, Vero/Falso/Nessuno).\n")
    return 2


def alla_fine(ev, radice):
    from rad.progetto import Progetto
    from rad.storia import Storia
    gruppo = Storia(Progetto(radice)).concludi_persistente()
    if gruppo:
        registro(radice).scrivi("modifiche", motore="claude_code", richiesta=gruppo["id"], file=len(gruppo["modifiche"]))


def principale():
    for flusso in (sys.stdout, sys.stderr, sys.stdin):
        try:
            flusso.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ev = leggi_evento()
    radice = radice_progetto(ev.get("cwd") or os.getcwd())
    if not radice:
        return 0
    nome = ev.get("hook_event_name")
    try:
        if nome == "UserPromptSubmit":
            al_prompt(ev, radice)
        elif nome == "PostToolUse":
            return dopo_scrittura(ev, radice)
        elif nome == "Stop":
            alla_fine(ev, radice)
    except Exception as errore:          # un hook non deve mai fermare Claude Code
        try:
            registro(radice).scrivi("errore_hook", evento=str(nome), errore=repr(errore)[:200])
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(principale())
