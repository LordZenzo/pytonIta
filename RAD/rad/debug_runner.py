"""Esegue un programma pytonIta (.pit) o Python (.py) sotto il controllo del debugger di PitStudio.

Uso:  pitonit -u debug_runner.py programma.pit [--punti file.json] [--inizio] [argomenti del programma...]

Il dialogo con PitStudio passa dagli stessi canali del programma:
  - eventi in uscita (stdout):   \x01DBG{json}\x02
  - comandi in ingresso (stdin): \x01CMD <comando> [dati]\n   (solo mentre il programma è fermo)
Comandi: continua, passo (sopra), entra, esci, ferma, osserva <json lista> (osservate: uguale ma senza risposta), frame <numero nella pila>, punti <json>
  osserva: ogni voce è un'espressione oppure {"e": espressione, "ferma": true}: con «ferma», «continua» si arresta appena il valore cambia
  (watchpoint: il programma gira riga per riga sotto controllo, quindi più lentamente).
Ogni sosta porta anche «valutazione»: come si calcola, passo dopo passo, l'espressione della riga che sta per essere eseguita.
I punti di arresto sono {file: [riga | [riga, condizione, dopo_n_passaggi, messaggio], ...]}:
  condizione  = espressione (anche con parole italiane): si ferma solo se è vera;
  dopo        = si ferma solo dal passaggio numero N in poi;
  messaggio   = «punto di registrazione»: scrive il messaggio ({espressione} viene sostituita) e non si ferma.
"""
import ast
import bdb
import json
import linecache
import os
import pprint
import re
import sys

INIZIO, FINE = "\x01DBG", "\x02"
FLAG_ITALIANO = 0x10000          # PyCF_ITALIANO: parole chiave italiane
LIMITE_VALORE = 160
LIMITE_VARIABILI = 80
LIMITE_COMPLETO = 200000         # caratteri del valore «intero» mandato a richiesta (oltre si accorcia, con una nota)


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


def completo(valore, massimo=LIMITE_COMPLETO):
    """Il valore per intero, leggibile: un testo si mostra com'è (non con gli «\\n»), liste e dizionari su più righe con i rientri."""
    try:
        if isinstance(valore, str):
            testo = valore
        elif isinstance(valore, (list, tuple, dict, set, frozenset)):
            testo = pprint.pformat(valore, width=88, compact=True, sort_dicts=False)
        else:
            testo = repr(valore)
    except Exception:
        testo = "<non rappresentabile>"
    if len(testo) > massimo:
        testo = testo[:massimo] + "\n… (altri %d caratteri non mostrati)" % (len(testo) - massimo)
    return testo


_NON_ESISTE = object()                 # l'espressione osservata non si può valutare (variabile non ancora creata, ambito diverso…)


def valore_it(valore, breve_max=40):
    """Come si mostra un valore a chi impara: Vero/Falso/Nessuno, e testi lunghi accorciati."""
    if valore is _NON_ESISTE:
        return "—"
    if valore is True:
        return "Vero"
    if valore is False:
        return "Falso"
    if valore is None:
        return "Nessuno"
    try:
        if isinstance(valore, range):
            testo = "intervallo_di(%d, %d)" % (valore.start, valore.stop) if valore.step == 1 else "intervallo_di(%d, %d, %d)" % (valore.start, valore.stop, valore.step)
        elif isinstance(valore, (list, tuple)) and len(valore) <= 8:
            apri, chiudi = ("[", "]") if isinstance(valore, list) else ("(", ")" if len(valore) != 1 else ",)")
            testo = apri + ", ".join(valore_it(x, 20) for x in valore) + chiudi
        else:
            testo = repr(valore)
    except Exception:
        testo = "<non rappresentabile>"
    return testo if len(testo) <= breve_max else testo[:breve_max - 1] + "…"


# ---------------------------------------------------------------- la memoria: nomi e oggetti con i loro riferimenti
_IMMUTABILI = (int, float, complex, str, bytes, bool, type(None))
_TIPI_IT = {"list": "lista", "dict": "dizionario", "tuple": "tupla", "set": "insieme", "frozenset": "insieme_congelato"}


def costruisci_memoria(variabili, massimo_oggetti=30, massimo_elementi=10, profondita=3):
    """I nomi (variabili) e gli oggetti a cui puntano, per il disegno della memoria. Valori semplici (numeri, testi, Vero…) restano dentro il nome;
    liste, dizionari, insiemi, tuple e istanze diventano oggetti con i loro elementi, uno solo anche se più nomi vi puntano.
    -> {"nomi": [{nome, valore, ref}], "oggetti": {id: {tipo, testo, elementi: [{chiave, valore, ref}], troncato}}}"""
    import inspect
    oggetti = {}

    def elemento(chiave, x, livello, etichetta):
        if isinstance(x, _IMMUTABILI):
            return {"chiave": chiave, "valore": valore_it(x, 24), "ref": None}
        return {"chiave": chiave, "valore": None, "ref": registra(x, livello, etichetta)}

    coda = []                  # oggetti registrati e ancora da riempire, in ordine di distanza dai nomi

    def registra(v, livello, etichetta=""):
        ref = str(id(v))
        if ref in oggetti:
            return ref
        if len(oggetti) >= massimo_oggetti:
            return None
        tipo = type(v).__name__
        # «etichetta»: a chi appartiene (il nome della variabile, oppure il percorso: a[2], c['x'], persona.indirizzo)
        voce = {"tipo": _TIPI_IT.get(tipo, tipo), "testo": valore_it(v, 30), "elementi": [], "troncato": False, "etichetta": etichetta}
        oggetti[ref] = voce
        coda.append((voce, v, livello))
        return ref

    def riempi(voce, v, livello):
        if livello >= profondita:
            voce["troncato"] = True
            return
        try:
            if isinstance(v, (list, tuple)):
                for k, x in enumerate(v[:massimo_elementi]):
                    voce["elementi"].append(elemento(k, x, livello + 1, f"{voce['etichetta']}[{k}]"))
                voce["troncato"] = len(v) > massimo_elementi
            elif isinstance(v, (set, frozenset)):
                for x in list(v)[:massimo_elementi]:
                    voce["elementi"].append(elemento(None, x, livello + 1, f"{voce['etichetta']}[…]"))
                voce["troncato"] = len(v) > massimo_elementi
            elif isinstance(v, dict):
                for chiave, x in list(v.items())[:massimo_elementi]:
                    voce["elementi"].append(elemento(valore_it(chiave, 16), x, livello + 1, f"{voce['etichetta']}[{valore_it(chiave, 16)}]"))
                voce["troncato"] = len(v) > massimo_elementi
            else:
                for nome, x in list(vars(v).items())[:massimo_elementi]:
                    if not nome.startswith("_"):            # attributi privati (_x, __x) non si disegnano
                        voce["elementi"].append(elemento(nome, x, livello + 1, f"{voce['etichetta']}.{nome}"))
        except Exception:
            pass

    nomi = []
    for nome, v in variabili.items():
        if inspect.isroutine(v) or inspect.isclass(v) or inspect.ismodule(v):
            continue
        if isinstance(v, _IMMUTABILI):
            nomi.append({"nome": nome, "valore": valore_it(v, 24), "ref": None})
        else:
            riferimento = registra(v, 1, nome)
            nomi.append({"nome": nome, "valore": None, "ref": riferimento})
            if riferimento is not None:
                oggetti[riferimento].setdefault("nomi", []).append(nome)
    while coda:                # prima gli oggetti dei nomi (livello 1), poi i loro elementi (livello 2)...: ognuno si riempie al livello più vicino
        voce, v, livello = coda.pop(0)
        riempi(voce, v, livello)
    for voce in oggetti.values():                    # un oggetto a cui puntano più nomi li porta tutti: «a, b»
        if voce.get("nomi"):
            voce["etichetta"] = ", ".join(voce["nomi"])
        voce.pop("nomi", None)
    return {"nomi": nomi, "oggetti": oggetti}


# ---------------------------------------------------------------- spiegazione passo-passo della riga
_BUILTIN_SICURI = {len, sum, min, max, abs, round, sorted, str, int, float, bool, repr, ord, chr, list, tuple, set, range, divmod, pow}


def _figli_espressione(nodo):
    """I sotto-espressioni da ridurre (di una chiamata non si riduce il nome della funzione)."""
    figli = []
    for c in ast.iter_child_nodes(nodo):
        if not isinstance(c, ast.expr):
            continue
        if isinstance(nodo, ast.Call) and c is nodo.func:
            continue
        figli.append(c)
    return figli


def _foglia(nodo):
    """Nomi, costanti e catene di attributi (a.b.c) si valutano d'un colpo, senza mostrarne le parti."""
    if isinstance(nodo, (ast.Name, ast.Constant)):
        return True
    if isinstance(nodo, ast.Attribute):
        return _foglia(nodo.value)
    return False


def _altezza(nodo):
    if _foglia(nodo):
        return 0
    if isinstance(nodo, ast.JoinedStr):
        return 1
    figli = _figli_espressione(nodo)
    return 1 + max((_altezza(c) for c in figli), default=0)


def _sicuro(nodo, frame):
    """Vero se valutare il nodo non può avere effetti: niente chiamate di funzioni dell'utente."""
    t = type(nodo)
    if t is ast.Name:
        return isinstance(nodo.ctx, ast.Load)
    if t is ast.Constant:
        return True
    if t is ast.Attribute:
        return _sicuro(nodo.value, frame)
    if t is ast.Call:
        if not isinstance(nodo.func, ast.Name):
            return False
        try:
            oggetto = eval(nodo.func.id, frame.f_globals, frame.f_locals)
        except Exception:
            return False
        if not any(oggetto is b for b in _BUILTIN_SICURI):
            return False
        return all(_sicuro(a, frame) for a in nodo.args) and all(_sicuro(k.value, frame) for k in nodo.keywords) and not any(isinstance(a, ast.Starred) for a in nodo.args)
    if t is ast.JoinedStr:
        return all(isinstance(v, ast.Constant) or (isinstance(v, ast.FormattedValue) and _sicuro(v.value, frame)) for v in nodo.values)
    if t in (ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp, ast.Subscript, ast.Slice, ast.Tuple, ast.List, ast.Set, ast.Dict):
        return all(_sicuro(c, frame) for c in ast.iter_child_nodes(nodo) if isinstance(c, ast.expr))
    return False


def _riduzioni(nodo, k, frame, uscita):
    """I nodi da sostituire con il loro valore al giro k: i più grandi, sicuri, di altezza <= k."""
    if isinstance(nodo, ast.Constant):
        return
    if _sicuro(nodo, frame) and _altezza(nodo) <= k:
        uscita.append(nodo)
        return
    for c in _figli_espressione(nodo):
        _riduzioni(c, k, frame, uscita)


def _espressione_della_riga(istruzione):
    """L'espressione che la riga calcola: valore di un'assegnazione, condizione di se/mentre, sequenza di per, ritorna…"""
    for tipo, campo in ((ast.Assign, "value"), (ast.AugAssign, "value"), (ast.AnnAssign, "value"), (ast.Expr, "value"), (ast.Return, "value"),
                        (ast.If, "test"), (ast.While, "test"), (ast.For, "iter"), (ast.Assert, "test")):
        if isinstance(istruzione, tipo):
            return getattr(istruzione, campo, None)
    return None


def passi_valutazione(albero, righe, riga, frame, massimo=8):
    """['a + b * 2', '3 + 8', '11']: l'espressione della riga e come si riduce, un giro alla volta. Lista vuota se non c'è niente da spiegare."""
    istruzione = None
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.stmt) and getattr(nodo, "lineno", None) == riga:
            istruzione = nodo
            break
    if istruzione is None:
        return []
    radice = _espressione_della_riga(istruzione)
    if radice is None or radice.lineno != radice.end_lineno or radice.lineno != riga or _foglia(radice) and isinstance(radice, ast.Constant):
        return []
    linea = righe[riga - 1].rstrip("\r\n").encode("utf-8")
    inizio, fine = radice.col_offset, radice.end_col_offset
    base = linea[inizio:fine]
    passi = [base.decode("utf-8", "replace")]
    valori = {}
    for k in range(0, _altezza(radice) + 1):
        scelti = []
        _riduzioni(radice, k, frame, scelti)
        if not scelti:
            continue
        sostituzioni = []
        for n in scelti:
            if n.lineno != n.end_lineno:
                return passi if len(passi) > 1 else []
            if id(n) not in valori:
                try:
                    espressione = ast.Expression(body=n)
                    ast.fix_missing_locations(espressione)
                    valori[id(n)] = valore_it(eval(compile(espressione, "<valutazione>", "eval"), frame.f_globals, frame.f_locals))
                except Exception:
                    return passi if len(passi) > 1 else []
            sostituzioni.append((n.col_offset - inizio, n.end_col_offset - inizio, valori[id(n)]))
        testo = base
        for a, b, v in sorted(sostituzioni, reverse=True):
            testo = testo[:a] + v.encode("utf-8") + testo[b:]
        t = testo.decode("utf-8", "replace")
        if t != passi[-1]:
            passi.append(t)
        if scelti and scelti[0] is radice:
            break
        if len(passi) >= massimo:
            break
    return passi if len(passi) > 1 else []


class Debugger(bdb.Bdb):
    def __init__(self, programma, punti, inizio):
        super().__init__()
        self.programma = os.path.abspath(programma)
        self.inizio = inizio
        self.osservate = []
        self.fermo_frame = None
        self.scelto = None               # il frame della pila di cui si vedono variabili ed espressioni
        self.da_fermare = []             # espressioni con «ferma quando cambia»
        self.watch = {}                  # espressione -> {"frame", "firma", "testo"}
        self.modo_watch = False          # in corso un «continua» sotto controllo dei watchpoint
        self.ultima_riga = None
        self.prec_codice = None          # per evidenziare ciò che è cambiato dall'ultima sosta
        self.prec_variabili = {}
        self.prec_osservate = {}
        self.alberi = {}                 # file -> (data di modifica, albero)
        self.speciali = {}               # (file, riga) -> {"se": ..., "dopo": ..., "messaggio": ...}
        self.passaggi = {}               # (file, riga) -> quante volte si è passati (con la condizione vera)
        self.avviso = ""
        self.primo = True
        try:
            import sysconfig
            stdlib = sysconfig.get_path("stdlib") or os.path.dirname(os.__file__)
        except Exception:
            stdlib = os.path.dirname(getattr(os, "__file__", "") or sys.executable)
        self.cartella_stdlib = os.path.normcase(stdlib)
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

    # --- watchpoint
    def _firma(self, valore):
        if valore is _NON_ESISTE:
            return None
        try:
            return repr(valore)[:2000]
        except Exception:
            return "<non rappresentabile>"

    def _valore_osservato(self, espressione, frame):
        try:
            return self.valuta(espressione, frame)
        except Exception:
            return _NON_ESISTE

    def attiva_watch(self, frame):
        self.watch = {}
        for e in self.da_fermare:
            v = self._valore_osservato(e, frame)
            self.watch[e] = {"frame": frame, "firma": self._firma(v), "testo": valore_it(v)}
        self.modo_watch = bool(self.watch)

    def _in_pila(self, frame, cercato):
        f = frame
        while f is not None:
            if f is cercato:
                return True
            f = f.f_back
        return False

    def _radice(self, frame):
        pila = self.pila_utente(frame)
        return pila[-1] if pila else frame

    def controlla_watch(self, frame):
        """Confronta i valori osservati con quelli di prima; ritorna i messaggi per quelli cambiati."""
        messaggi = []
        for e, w in self.watch.items():
            f = w["frame"]
            if not self._in_pila(frame, f):
                f = self._radice(frame)             # la funzione è finita: si continua a guardare nell'ambito più esterno
                v = self._valore_osservato(e, f)
                w.update(frame=f, firma=self._firma(v), testo=valore_it(v))
                continue
            v = self._valore_osservato(e, f)
            firma = self._firma(v)
            if firma != w["firma"]:
                prima, dopo = w["testo"], valore_it(v)
                if w["firma"] is None:
                    messaggi.append("%s è stata creata: %s" % (e, dopo))
                elif firma is None:
                    messaggi.append("%s non esiste più" % e)
                else:
                    messaggi.append("%s è cambiata: %s → %s" % (e, prima, dopo))
                w.update(firma=firma, testo=dopo)
        return messaggi

    # --- eventi del debugger
    def user_line(self, frame):
        if self.modo_watch:
            riga_prima = self.ultima_riga
            messaggi = self.controlla_watch(frame)
            if messaggi:
                self.modo_watch = False
                dopo = " (dopo la riga %d)" % riga_prima if riga_prima else ""
                self.avviso = "👁 " + "; ".join(messaggi) + dopo
                sys.stdout.write(self.avviso + "\n")
                sys.stdout.flush()
                self.fermo(frame)
                return
            if self.break_here(frame):
                self.modo_watch = False
                self.fermo(frame)
                return
            self.ultima_riga = frame.f_lineno
            return
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
                self.imposta_osservate(dati)
                self.invia_stato(self.scelto or frame, "frame")          # aggiorna i valori delle espressioni osservate
                continue
            if nome == "osservate":                       # come «osserva», ma senza rispondere (si manda subito prima di riprendere)
                self.imposta_osservate(dati)
                continue
            if nome == "valore":                          # il valore intero di una variabile o di un'espressione, per la finestra «Valore»
                self.invia_valore(self.scelto or frame, dati)
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
            self.modo_watch = False
            if nome == "continua":
                self.attiva_watch(self.scelto or frame)
                if self.modo_watch:
                    self.ultima_riga = frame.f_lineno
                    self.set_step()                  # con i watchpoint si guarda ogni riga
                else:
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

    def invia_valore(self, frame, dati):
        """Risponde con il valore intero dell'espressione (calcolata nella riga della pila scelta), o con l'errore."""
        try:
            espressione = str(json.loads(dati).get("e", "")).strip()
        except ValueError:
            espressione = ""
        try:
            codice = compile(espressione, "<valore>", "eval", FLAG_ITALIANO, True)
            valore = eval(codice, frame.f_globals, frame.f_locals)
            try:
                lunghezza = len(valore)
            except Exception:
                lunghezza = None
            emetti(evento="valore", espressione=espressione, tipo=tipo_di(valore), lunghezza=lunghezza, testo=completo(valore))
        except Exception as errore:
            emetti(evento="valore", espressione=espressione, errore=type(errore).__name__ + ": " + str(errore))

    def imposta_osservate(self, dati):
        """Le espressioni osservate: stringhe, oppure {"e": espressione, "ferma": vero/falso}."""
        self.osservate = []
        self.da_fermare = []
        try:
            voci = list(json.loads(dati))
        except ValueError:
            voci = []
        for voce in voci:
            if isinstance(voce, dict):
                e = str(voce.get("e", "")).strip()
                ferma = bool(voce.get("ferma"))
            else:
                e, ferma = str(voce).strip(), False
            if e and e not in self.osservate:
                self.osservate.append(e)
                if ferma:
                    self.da_fermare.append(e)

    def valutazione(self, frame):
        """Come si calcola, passo dopo passo, l'espressione della riga in cui il programma è fermo (vuota se non serve)."""
        try:
            file = os.path.abspath(frame.f_code.co_filename)
            if file.startswith("<") or not os.path.exists(file):
                return []
            data = os.path.getmtime(file)
            voce = self.alberi.get(file)
            if voce is None or voce[0] != data:
                with open(file, encoding="utf-8") as f:
                    sorgente = f.read()
                flag = FLAG_ITALIANO if file.lower().endswith(".pit") else 0
                albero = compile(sorgente, file, "exec", flag | ast.PyCF_ONLY_AST, True)
                voce = (data, albero, sorgente.split("\n"))
                self.alberi[file] = voce
            return passi_valutazione(voce[1], voce[2], frame.f_lineno, frame)
        except Exception:
            return []

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
        confronta = frame.f_code is self.prec_codice          # le «novità» si vedono solo restando nella stessa funzione
        for nome, valore in list(fonte.items())[:LIMITE_VARIABILI]:
            if nome.startswith("__") or type(valore).__name__ in ("module",):
                continue
            testo = breve(valore)
            variabili.append({"nome": nome, "valore": testo, "tipo": tipo_di(valore), "cambiata": confronta and self.prec_variabili.get(nome) != testo})
        osservate = []
        for espressione in self.osservate:
            try:
                codice = compile(espressione, "<osserva>", "eval", FLAG_ITALIANO, True)
                testo = breve(eval(codice, globali, locali))
            except Exception as errore:
                testo = "⚠ " + type(errore).__name__
            osservate.append({"espressione": espressione, "valore": testo, "cambiata": confronta and espressione in self.prec_osservate and self.prec_osservate[espressione] != testo,
                              "ferma": espressione in self.da_fermare})
        if evento == "fermo":
            self.prec_codice = frame.f_code
            self.prec_variabili = {v["nome"]: v["valore"] for v in variabili}
            self.prec_osservate = {o["espressione"]: o["valore"] for o in osservate}
        avviso, self.avviso = self.avviso, ""
        try:
            memoria = costruisci_memoria({k: v for k, v in fonte.items() if not k.startswith("__")}) if evento in ("fermo", "frame") else None
        except Exception:
            memoria = None
        emetti(evento=evento, memoria=memoria, file=os.path.abspath(frame.f_code.co_filename), riga=frame.f_lineno,
               funzione=frame.f_code.co_name, pila=pila, variabili=variabili, osservate=osservate, avviso=avviso,
               valutazione=self.valutazione(frame) if evento == "fermo" or evento == "frame" else [])


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
