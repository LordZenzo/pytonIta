"""Esegue un programma pytonIta (.pit) o Python (.py) sotto il controllo del debugger di PitStudio.

Uso:  pitonit -u debug_runner.py programma.pit [--punti file.json] [--inizio] [argomenti del programma...]

Il dialogo con PitStudio passa dagli stessi canali del programma:
  - eventi in uscita (stdout):   \x01DBG{json}\x02
  - comandi in ingresso (stdin): \x01CMD <comando> [dati]\n   (solo mentre il programma è fermo)
Comandi: continua, passo (sopra), entra, esci, ferma, osserva <json lista di espressioni>, frame <numero nella pila>, punti <json>
I punti di arresto sono {file: [riga | [riga, condizione, dopo_n_passaggi, messaggio], ...]}:
  condizione  = espressione (anche con parole italiane): si ferma solo se è vera;
  dopo        = si ferma solo dal passaggio numero N in poi;
  messaggio   = «punto di registrazione»: scrive il messaggio ({espressione} viene sostituita) e non si ferma.
"""
import bdb
import json
import os
import re
import sys

INIZIO, FINE = "\x01DBG", "\x02"
FLAG_ITALIANO = 0x10000          # PyCF_ITALIANO: parole chiave italiane
LIMITE_VALORE = 160
LIMITE_VARIABILI = 80


def emetti(**dati):
    sys.stdout.flush()
    sys.__stdout__.write(INIZIO + json.dumps(dati, ensure_ascii=False) + FINE)
    sys.__stdout__.flush()


def breve(valore):
    try:
        t = repr(valore)
    except Exception:
        t = "<non rappresentabile>"
    return t if len(t) <= LIMITE_VALORE else t[:LIMITE_VALORE] + "…"


def tipo_di(valore):
    return type(valore).__name__


class Debugger(bdb.Bdb):
    def __init__(self, programma, punti, inizio):
        super().__init__()
        self.programma = os.path.abspath(programma)
        self.inizio = inizio
        self.osservate = []
        self.fermo_frame = None
        self.scelto = None               # il frame della pila di cui si vedono variabili ed espressioni
        self.speciali = {}               # (file, riga) -> {"se": ..., "dopo": ..., "messaggio": ...}
        self.passaggi = {}               # (file, riga) -> quante volte si è passati (con la condizione vera)
        self.avviso = ""
        self.primo = True
        self.cartella_stdlib = os.path.normcase(os.path.dirname(os.__file__))
        self.questo = os.path.normcase(os.path.abspath(__file__))
        self.imposta_punti(punti)

    def imposta_punti(self, punti):
        self.clear_all_breaks()
        self.speciali = {}
        for file, righe in punti.items():
            file = os.path.abspath(file)
            for voce in righe:
                if isinstance(voce, (list, tuple)):
                    riga = int(voce[0])
                    se = (voce[1] if len(voce) > 1 else "") or ""
                    dopo = int(voce[2]) if len(voce) > 2 and voce[2] else 0
                    messaggio = (voce[3] if len(voce) > 3 else "") or ""
                    if se.strip() or dopo or messaggio.strip():
                        chiave = (file, riga)
                        self.speciali[chiave] = {"se": se.strip(), "dopo": dopo, "messaggio": messaggio.strip()}
                        self.passaggi.setdefault(chiave, 0)
                else:
                    riga = int(voce)
                self.set_break(file, riga)

    def valuta(self, espressione, frame):
        codice = compile(espressione, "<espressione>", "eval", FLAG_ITALIANO, True)
        return eval(codice, frame.f_globals, frame.f_locals)

    def messaggio_formattato(self, modello, frame):
        def sostituisci(m):
            try:
                return str(self.valuta(m.group(1), frame))
            except Exception as errore:
                return "<" + type(errore).__name__ + ">"
        return re.sub(r"\{([^{}]+)\}", sostituisci, modello)

    # --- quali frame interessano: solo il codice dell'utente
    def _utente(self, frame):
        nome = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        if frame.f_code.co_filename.startswith("<") or nome == self.questo:
            return False
        return not nome.startswith(self.cartella_stdlib)

    def stop_here(self, frame):
        return super().stop_here(frame) and self._utente(frame)

    def break_here(self, frame):
        if not (self._utente(frame) and super().break_here(frame)):
            return False
        chiave = (os.path.abspath(frame.f_code.co_filename), frame.f_lineno)
        extra = self.speciali.get(chiave)
        if not extra:
            return True
        if extra["se"]:
            try:
                if not self.valuta(extra["se"], frame):
                    return False
            except Exception as errore:
                self.avviso = "Condizione della riga %d non valutabile (%s): mi fermo comunque." % (chiave[1], type(errore).__name__)
                return True
        self.passaggi[chiave] = self.passaggi.get(chiave, 0) + 1
        if extra["dopo"] and self.passaggi[chiave] < extra["dopo"]:
            return False
        if extra["messaggio"]:
            sys.stdout.write("🔶 riga %d: %s\n" % (chiave[1], self.messaggio_formattato(extra["messaggio"], frame)))
            sys.stdout.flush()
            return False
        return True

    # --- eventi del debugger
    def user_line(self, frame):
        if self.primo:
            self.primo = False
            if not self.inizio:
                self.set_continue()          # partenza libera: ci si ferma solo sui punti di arresto
                if not self.break_here(frame):
                    return
        self.fermo(frame)

    def user_call(self, frame, argument_list):
        pass

    def user_exception(self, frame, exc_info):
        pass

    def pila_utente(self, frame):
        pila = []
        f = frame
        while f is not None:
            if self._utente(f):
                pila.append(f)
            f = f.f_back
        return pila

    def fermo(self, frame):
        self.fermo_frame = frame
        self.scelto = frame
        self.invia_stato(frame)
        while True:
            comando = self.leggi_comando()
            if comando is None or comando[0] == "ferma":
                self.set_quit()
                raise SystemExit(0)
            nome, dati = comando
            if nome == "osserva":
                try:
                    self.osservate = list(json.loads(dati))
                except ValueError:
                    self.osservate = []
                self.invia_stato(self.scelto or frame, "frame")          # aggiorna i valori delle espressioni osservate
                continue
            if nome == "frame":
                try:
                    pila = self.pila_utente(frame)
                    self.scelto = pila[int(dati)]
                except (ValueError, IndexError):
                    self.scelto = frame
                self.invia_stato(self.scelto, "frame")
                continue
            if nome == "punti":
                self.aggiorna_punti(dati)
                continue
            if nome == "continua":
                self.set_continue()
            elif nome == "passo":
                self.set_next(frame)
            elif nome == "entra":
                self.set_step()
            elif nome == "esci":
                self.set_return(frame)
            else:
                continue
            return

    def aggiorna_punti(self, dati):
        try:
            punti = json.loads(dati)
        except ValueError:
            return
        self.imposta_punti(punti)

    def leggi_comando(self):
        while True:
            riga = sys.stdin.readline()
            if riga == "":
                return None
            riga = riga.rstrip("\r\n")
            if riga.startswith("\x01CMD "):
                resto = riga[5:].strip()
                nome, _, dati = resto.partition(" ")
                return nome, dati

    def invia_stato(self, frame, evento="fermo"):
        pila = [{"file": os.path.abspath(f.f_code.co_filename), "riga": f.f_lineno, "funzione": f.f_code.co_name}
                for f in self.pila_utente(self.fermo_frame or frame)]
        locali = frame.f_locals
        globali = frame.f_globals
        variabili = []
        if frame.f_code.co_name == "<module>":
            fonte = {k: v for k, v in globali.items() if not k.startswith("__")}
        else:
            fonte = dict(locali)
        for nome, valore in list(fonte.items())[:LIMITE_VARIABILI]:
            if nome.startswith("__") or type(valore).__name__ in ("module",):
                continue
            variabili.append({"nome": nome, "valore": breve(valore), "tipo": tipo_di(valore)})
        osservate = []
        for espressione in self.osservate:
            try:
                codice = compile(espressione, "<osserva>", "eval", FLAG_ITALIANO, True)
                osservate.append({"espressione": espressione, "valore": breve(eval(codice, globali, locali))})
            except Exception as errore:
                osservate.append({"espressione": espressione, "valore": "⚠ " + type(errore).__name__})
        avviso, self.avviso = self.avviso, ""
        emetti(evento=evento, file=os.path.abspath(frame.f_code.co_filename), riga=frame.f_lineno,
               funzione=frame.f_code.co_name, pila=pila, variabili=variabili, osservate=osservate, avviso=avviso)


def main(argv):
    if not argv:
        print("uso: debug_runner.py programma [--punti file.json] [--inizio] [argomenti]", file=sys.stderr)
        return 2
    programma = argv[0]
    resto = argv[1:]
    punti = {}
    inizio = False
    args_programma = []
    i = 0
    while i < len(resto):
        if resto[i] == "--punti" and i + 1 < len(resto):
            try:
                with open(resto[i + 1], encoding="utf-8") as f:
                    punti = json.load(f)
            except (OSError, ValueError):
                punti = {}
            i += 2
        elif resto[i] == "--inizio":
            inizio = True
            i += 1
        else:
            args_programma.append(resto[i])
            i += 1
    programma = os.path.abspath(programma)
    with open(programma, encoding="utf-8") as f:
        sorgente = f.read()
    flag = FLAG_ITALIANO if programma.lower().endswith(".pit") else 0
    codice = compile(sorgente, programma, "exec", flag, True)
    sys.argv = [programma] + args_programma
    sys.path.insert(0, os.path.dirname(programma))
    ambiente = {"__name__": "__main__", "__file__": programma}
    d = Debugger(programma, punti, inizio)
    emetti(evento="avviato", file=programma)
    try:
        d.reset()
        d.set_step()
        sys.settrace(d.trace_dispatch)
        exec(codice, ambiente)
        sys.settrace(None)
    except SystemExit as e:
        emetti(evento="fine", codice=e.code if isinstance(e.code, int) else 0)
        return e.code if isinstance(e.code, int) else 0
    except BaseException:
        sys.settrace(None)
        import traceback
        traceback.print_exc()
        emetti(evento="fine", codice=1)
        return 1
    emetti(evento="fine", codice=0)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
