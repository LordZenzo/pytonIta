"""Esegue un programma pytonIta (.pit) o Python (.py) sotto il controllo del debugger di PitStudio.

Uso:  pitonit -u debug_runner.py programma.pit [--punti file.json] [--inizio] [argomenti del programma...]

Il dialogo con PitStudio passa dagli stessi canali del programma:
  - eventi in uscita (stdout):   \x01DBG{json}\x02
  - comandi in ingresso (stdin): \x01CMD <comando> [dati]\n   (solo mentre il programma è fermo)
Comandi: continua, passo (sopra), entra, esci, ferma, osserva <json lista di espressioni>
"""
import bdb
import json
import os
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
        self.primo = True
        self.cartella_stdlib = os.path.normcase(os.path.dirname(os.__file__))
        self.questo = os.path.normcase(os.path.abspath(__file__))
        for file, righe in punti.items():
            for riga in righe:
                self.set_break(os.path.abspath(file), int(riga))

    # --- quali frame interessano: solo il codice dell'utente
    def _utente(self, frame):
        nome = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        if frame.f_code.co_filename.startswith("<") or nome == self.questo:
            return False
        return not nome.startswith(self.cartella_stdlib)

    def stop_here(self, frame):
        return super().stop_here(frame) and self._utente(frame)

    def break_here(self, frame):
        return self._utente(frame) and super().break_here(frame)

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

    def fermo(self, frame):
        self.fermo_frame = frame
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
                self.invia_stato(frame)          # aggiorna i valori delle espressioni osservate
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
        self.clear_all_breaks()
        for file, righe in punti.items():
            for riga in righe:
                self.set_break(os.path.abspath(file), int(riga))

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

    def invia_stato(self, frame):
        pila = []
        f = frame
        while f is not None:
            if self._utente(f):
                pila.append({"file": os.path.abspath(f.f_code.co_filename), "riga": f.f_lineno, "funzione": f.f_code.co_name})
            f = f.f_back
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
        emetti(evento="fermo", file=os.path.abspath(frame.f_code.co_filename), riga=frame.f_lineno,
               funzione=frame.f_code.co_name, pila=pila, variabili=variabili, osservate=osservate)


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
