"""Traduce programmi pytonIta (.pit) in Python (.py) che girano con un Python normale, senza pitonit.

Uso:  python pit2py.py origine.pit destinazione.py
      python pit2py.py --progetto cartella_origine cartella_destinazione

Cosa fa, restando fedele al testo (commenti, righe e rientri non cambiano):
  * parole chiave italiane (se, per, ritorna, Vero...) -> inglese, con le stesse regole di contesto del parser di pitonit
  * funzioni, tipi ed eccezioni predefiniti (stampa, lunghezza, ErroreDiValore...) -> inglese, rispettando i nomi dell'utente
  * moduli italiani (matematica, interfaccia...) e i loro nomi -> moduli e nomi originali (import compresi)
  * metodi e attributi italiani (lista.aggiungi, finestra.impacchetta...) -> inglese; se un nome italiano puo' voler dire
    piu' cose, il programma scoglie a esecuzione con una piccola funzione _pit_attr inserita nel file
  * opzioni con nome (chiave=, testo=, comando=...), metodi speciali (__inizializza__ -> __init__), se_stesso -> self

Tutto cio' che non e' italiano resta com'e'. Il rapporto elenca i punti da guardare a mano.
"""
import keyword
import ast
import io
import os
import re
import sys
import tokenize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import py2pit                                   # noqa: E402  (analisi degli ambiti)
from pit2py_tabelle import Tabelle, KW_IT2EN, SOFT   # noqa: E402

DUNDER = {
    "__inizializza__": "__init__", "__nuovo__": "__new__", "__elimina__": "__del__", "__testo__": "__str__",
    "__rappresentazione__": "__repr__", "__lunghezza__": "__len__", "__ottieni_elemento__": "__getitem__",
    "__imposta_elemento__": "__setitem__", "__elimina_elemento__": "__delitem__", "__contiene__": "__contains__",
    "__iterazione__": "__iter__", "__prossimo__": "__next__", "__chiama__": "__call__", "__entra__": "__enter__",
    "__esci__": "__exit__", "__uguale__": "__eq__", "__diverso__": "__ne__", "__minore__": "__lt__",
    "__minore_uguale__": "__le__", "__maggiore__": "__gt__", "__maggiore_uguale__": "__ge__", "__somma__": "__add__",
    "__sottrazione__": "__sub__", "__moltiplicazione__": "__mul__", "__divisione__": "__truediv__",
    "__divisione_intera__": "__floordiv__", "__modulo__": "__mod__", "__potenza__": "__pow__",
    "__negativo__": "__neg__", "__booleano__": "__bool__", "__intero__": "__int__", "__decimale__": "__float__",
    "__nome__": "__name__", "__documentazione__": "__doc__", "__classe__": "__class__", "__dizionario__": "__dict__",
    "__tutto__": "__all__", "__ottieni_attributo__": "__getattr__", "__imposta_attributo__": "__setattr__",
}

PROTOTIPI = {"lista": [], "dizionario": {}, "insieme": set(), "testo": ""}

AIUTO_ATTR = '''

def _pit_attr(oggetto, *nomi):
    """Dove il nome italiano poteva voler dire piu' cose: usa il primo attributo che l'oggetto ha davvero."""
    for n in nomi:
        if hasattr(oggetto, n):
            return getattr(oggetto, n)
    return getattr(oggetto, nomi[-1])
'''

_TAB = []


def tabelle():
    if not _TAB:
        _TAB.append(Tabelle())
    return _TAB[0]


# ====================================================================== fase 1: parole chiave
OP_INIZIO_ESPR = {"(", "[", "{", ",", "=", "+", "-", "*", "/", "|", "&", "<", ">", "%", "==", "!=", "<=", ">=", "~", "^",
                  "<<", ">>", "**", "//", "@", "->", ":=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=",
                  "**=", "//=", "@="}
PAROLE_ESPR = {"se", "altrimenti_se", "mentre", "ritorna", "in", "non", "e", "o", "è", "produci", "attendi", "asserisci",
               "elimina", "solleva", "per", "come", "eccetto", "da", "importa", "lambda"}
FINE_OPERANDO = {"NAME", "NUMBER", "STRING", "FSTRING_END"}
SENZA_OPERANDO = {"pass", "break", "continue", "return", "raise", "yield", "lambda", "else", "try", "finally", "except", "async"}
SENZA_DUE_PUNTI = {"class", "with", "from", "del", "import", "def", "for", "if", "while", "global", "nonlocal", "assert",
                   "await", "in", "not", "is", "as"}
FINE_RIGA_VIETATA = {"class", "def", "with", "global", "nonlocal", "import", "del", "assert", "while"}
COMPOSTE = {"class", "def", "with", "try", "while", "finally", "except"}
SENZA_SEGUITO = {"class", "def", "try", "finally", "pass", "break", "continue", "global", "nonlocal"}
DI_ISTRUZIONE = {"class", "def", "with", "try", "while", "except", "finally", "return", "pass", "raise", "del", "global",
                 "nonlocal", "assert", "break", "continue", "import"}
NON_INIZIA_ESPR = {"from", "for", "if", "elif", "else", "in", "is", "as", "async"}


class Tk:
    """Un token come lo vede il parser di pitonit (senza a capo non logici e commenti)."""
    __slots__ = ("tipo", "s", "r", "c", "fr", "fc", "parola", "riga")

    def __init__(self, tipo, s, r, c, fr, fc, riga):
        self.tipo, self.s, self.r, self.c, self.fr, self.fc, self.riga = tipo, s, r, c, fr, fc, riga
        self.parola = None            # parola chiave inglese se classificato come tale


def _tipo(t):
    if t.parola is not None:
        return "KW"
    return t.tipo


def _prev_parola(prev, w):
    """prev e' la parola chiave italiana w (solo se e' stata classificata come parola chiave)."""
    return prev is not None and prev.parola is not None and prev.s == w


def _prev_espr_kw(prev):
    return prev.parola is not None and prev.s in PAROLE_ESPR


def _prev_inizio_espr(prev):
    if prev.tipo == "OP" and prev.s in OP_INIZIO_ESPR:
        return True
    return _prev_espr_kw(prev)


def _prev_fine_operando(prev):
    if prev.parola is None and prev.tipo in FINE_OPERANDO:
        if prev.tipo == "NAME" and keyword.iskeyword(prev.s) and prev.s not in ("True", "False", "None"):
            return False        # «in», «lambda»...: parole chiave scritte uguali in italiano; dopo di loro serve un operando (per x in e["a"]: «e» è un nome)
        return True
    if prev.tipo == "OP" and prev.s in (")", "]", "}", "..."):
        return True
    return prev.parola is not None and prev.s in ("Vero", "Falso", "Nessuno")


def _e_operatore(toks, i, t):
    """'e' e 'o' sono operatori solo tra due operandi (porta di _it_is_operator_position)."""
    if i == 0:
        return False
    prev = toks[i - 1]
    if not _prev_fine_operando(prev):
        return False
    q = t.riga[t.fc:].lstrip(" \t")
    c = q[0] if q else "\n"
    if c in "\n\r#\\":
        return True
    if c in "=,)]}:.;":
        return False
    return True


def _in_bersaglio_for(toks, i):
    profondita = 0
    for k in range(i - 1, -1, -1):
        t = toks[k]
        if t.tipo == "OP" and t.s in (")", "]", "}"):
            profondita += 1
        elif t.tipo == "OP" and t.s in ("(", "[", "{"):
            if profondita == 0:
                return False
            profondita -= 1
        elif profondita == 0:
            if t.tipo in ("NEWLINE", "INDENT", "DEDENT") or (t.tipo == "OP" and t.s in (":", "=")) or _prev_parola(t, "in"):
                return False
            if _prev_parola(t, "per"):
                return True
    return False


def _punti_dopo_da(toks, i):
    k = i - 1
    while k >= 0 and toks[k].tipo == "OP" and toks[k].s in (".", "..."):
        k -= 1
    return k >= 0 and k < i - 1 and _prev_parola(toks[k], "da")


def _parola_e_nome(toks, i, t, en):
    """Porta fedele di _it_keyword_is_name (Parser/pegen.c di pitonit): True se la parola italiana e' qui un nome."""
    if en in ("True", "False", "None", "and", "or"):
        return False
    prev = toks[i - 1] if i else None
    if prev is not None:
        if prev.tipo == "OP" and prev.s in (".", "..."):
            if en == "import" and _punti_dopo_da(toks, i):
                return False
            if prev.s == ".":
                return True
        if any(_prev_parola(prev, w) for w in ("per", "come", "globale", "nonlocale", "importa")):
            return True
        if _prev_parola(prev, "definisci") or _prev_parola(prev, "classe"):
            return True
    for k in range(i - 1, 0, -1):
        x = toks[k]
        if x.parola is None and x.tipo == "NAME" and x.s == t.s and (_prev_parola(toks[k - 1], "definisci") or _prev_parola(toks[k - 1], "classe")):
            return True
    dopo = t.riga[t.fc:]
    if en == "del" and dopo[:1] == "(":
        return True
    if prev is not None and en == "yield":
        istruzione = (prev.tipo in ("NEWLINE", "INDENT", "DEDENT") or (prev.tipo == "OP" and prev.s in (":", ";", "=", "("))
                      or _prev_parola(prev, "attendi"))
        if not istruzione:
            return True
        if prev.tipo == "OP" and prev.s in ("=", "(") and dopo[:1] == "(":
            return True
    q = dopo.lstrip(" \t")
    c = q[0] if q else "\n"
    solo_operando = en not in SENZA_OPERANDO
    if c in "=<>/%|&^!":
        return True
    if c in ",)]}":
        if solo_operando:
            return True
    elif c == ":":
        if en in SENZA_DUE_PUNTI:
            return True
    elif c == ".":
        if en not in ("from", "import") and not (q[1:2].isdigit()) and q[1:2] != ".":
            return True
    elif c in "\n\r;#":
        if en in FINE_RIGA_VIETATA:
            return True
    if prev is not None and prev.tipo == "OP" and prev.s == ":" and en in COMPOSTE:
        return True
    if c in "+-*~@" and en in SENZA_SEGUITO:
        return True
    if prev is not None and en in NON_INIZIA_ESPR and _prev_inizio_espr(prev) \
            and not (en == "from" and _prev_parola(prev, "produci")) \
            and not (en == "in" and _prev_parola(prev, "non")) \
            and not (en == "in" and prev.tipo == "OP" and prev.s == "," and _in_bersaglio_for(toks, i)) \
            and not (en == "is" and _prev_parola(prev, "non")):
        return True
    if prev is not None and en in DI_ISTRUZIONE:
        if _prev_inizio_espr(prev):
            return True
        if en != "import" and _prev_fine_operando(prev):
            return True
    return False


def leggi_token(sorgente):
    righe = sorgente.splitlines(keepends=True)
    toks = []
    for t in tokenize.generate_tokens(io.StringIO(sorgente).readline):
        nome = tokenize.tok_name[t.type]
        if nome in ("NL", "COMMENT", "ENCODING", "ENDMARKER"):
            continue
        if nome == "OP" or nome in ("NAME", "NUMBER", "STRING", "NEWLINE", "INDENT", "DEDENT") or nome.startswith("FSTRING"):
            r = t.start[0]
            riga = righe[r - 1] if r - 1 < len(righe) else ""
            toks.append(Tk(nome, t.string, r, t.start[1], t.end[0], t.end[1], riga if t.end[0] == r else riga))
    return toks, righe


def traduci_parole_chiave(sorgente):
    """Passo 1: parole chiave italiane -> inglesi (e metodi speciali). Ritorna il nuovo testo."""
    toks, righe = leggi_token(sorgente)
    for i, t in enumerate(toks):
        if t.tipo != "NAME":
            continue
        en = KW_IT2EN.get(t.s)
        if en is None:
            continue
        if en in ("and", "or") and not _e_operatore(toks, i, t):
            continue
        if _parola_e_nome(toks, i, t, en):
            continue
        t.parola = en
    # parole chiave "morbide": confronta / caso / tipo
    morbide = {}
    inizio = []
    for i, t in enumerate(toks):
        primo = i == 0 or toks[i - 1].tipo in ("NEWLINE", "INDENT", "DEDENT")
        if t.tipo == "NAME" and t.parola is None and t.s in SOFT and primo:
            inizio.append(i)
    attive = []
    for i in inizio:
        t = toks[i]
        k = i
        while k < len(toks) and toks[k].tipo != "NEWLINE":
            k += 1
        fine_due_punti = k > i and toks[k - 1].tipo == "OP" and toks[k - 1].s == ":"
        while attive and t.c <= attive[-1]:
            attive.pop()
        if t.s == "confronta" and fine_due_punti:
            morbide[i] = "match"
            attive.append(t.c)
        elif t.s == "caso" and fine_due_punti and attive and t.c > attive[-1]:
            morbide[i] = "case"
        elif t.s == "tipo" and i + 2 < len(toks) and toks[i + 1].tipo == "NAME" and toks[i + 1].parola is None \
                and toks[i + 2].tipo == "OP" and toks[i + 2].s in ("=", "["):
            morbide[i] = "type"
    mod = {}
    for i, t in enumerate(toks):
        nuovo = None
        if t.parola is not None:
            nuovo = t.parola
        elif i in morbide:
            nuovo = morbide[i]
        elif t.tipo == "NAME" and t.s in DUNDER:
            nuovo = DUNDER[t.s]
        if nuovo and nuovo != t.s:
            mod.setdefault(t.r - 1, []).append((t.c, len(t.s), nuovo))
    return applica(righe, mod)


def applica(righe, modifiche):
    """modifiche: {indice riga: [(colonna, lunghezza, nuovo testo)]} -> testo."""
    righe = list(righe)
    for r, lista in modifiche.items():
        for c, n, nuovo in sorted(lista, key=lambda x: (x[0], x[1]), reverse=True):
            righe[r] = righe[r][:c] + nuovo + righe[r][c + n:]
    return "".join(righe)


# ====================================================================== fase 2: nomi, moduli, metodi
class Progetto:
    """Nomi definiti dall'utente in tutto il progetto: servono a non scambiarli per alias di libreria."""

    def __init__(self):
        self.definiti = set()       # def, class, attributi assegnati, nomi assegnati in classi e a livello di modulo
        self.classi = set()         # nomi delle classi definite dall'utente
        self.parametri = set()      # nomi di parametri delle funzioni dell'utente
        self.moduli_utente = set()  # moduli (file) del progetto

    def aggiungi(self, albero):
        for n in ast.walk(albero):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.definiti.add(n.name)
                if isinstance(n, ast.ClassDef):
                    self.classi.add(n.name)
                else:
                    self.parametri.update(py2pit._args_nomi(n.args))
            elif isinstance(n, ast.Lambda):
                self.parametri.update(py2pit._args_nomi(n.args))
            elif isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del)):
                self.definiti.add(n.attr)
        for n in albero.body:
            if isinstance(n, (ast.Assign, ast.AnnAssign)):
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                    for x in ast.walk(t):
                        if isinstance(x, ast.Name):
                            self.definiti.add(x.id)
        for n in ast.walk(albero):
            if isinstance(n, ast.ClassDef):
                for b in n.body:
                    if isinstance(b, (ast.Assign, ast.AnnAssign)):
                        for t in (b.targets if isinstance(b, ast.Assign) else [b.target]):
                            for x in ast.walk(t):
                                if isinstance(x, ast.Name):
                                    self.definiti.add(x.id)


class RisolutoreIt(py2pit.Risolutore):
    """Trova i riferimenti a funzioni/eccezioni predefinite col nome italiano."""

    def visit_Name(self, n):
        if n.id in tabelle().builtin and self._builtin(n.id):
            self.riferimenti.add((n.lineno, n.col_offset))


def _colonne(righe):
    def a_colonna(riga, byte):
        return len(righe[riga - 1].encode()[:byte].decode())
    return a_colonna


class Convertitore:
    def __init__(self, progetto):
        self.p = progetto
        self.t = tabelle()
        self.rapporto = []          # (riga, categoria, testo)
        self.usa_aiuto = False

    def nota(self, riga, cat, testo):
        self.rapporto.append((riga, cat, testo))

    # ------------------------------------------------------------ moduli e nomi importati
    def _importazioni(self, albero):
        """name -> percorso del modulo italiano per i nomi che sono (solo) moduli importati."""
        t = self.t
        legami = {}
        altri = set()
        for n in ast.walk(albero):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                altri.add(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                altri.add(n.name)
                if not isinstance(n, ast.ClassDef):
                    altri.update(py2pit._args_nomi(n.args))
            elif isinstance(n, ast.Lambda):
                altri.update(py2pit._args_nomi(n.args))
        for n in ast.walk(albero):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in t.moduli or a.name.split(".")[0] in {m.split(".")[0] for m in t.moduli}:
                        if a.asname:
                            legami.setdefault(a.asname, set()).add(a.name)
                        else:
                            legami.setdefault(a.name.split(".")[0], set()).add(a.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
                if n.module in t.moduli:
                    en_mod = t.moduli[n.module]
                    for a in n.names:
                        if a.name == "*":
                            continue
                        if (n.module + "." + a.name) in t.moduli:
                            legami.setdefault(a.asname or a.name, set()).add(n.module + "." + a.name)
                            continue
                        completo = t.nomi.get(n.module, {}).get(a.name)
                        if completo and (en_mod + "." + completo) in {v for v in t.moduli.values()}:
                            legami.setdefault(a.asname or a.name, set()).add(
                                next(k for k, v in t.moduli.items() if v == en_mod + "." + completo))
        return {k: next(iter(v)) for k, v in legami.items() if len(v) == 1}

    def converti(self, testo2, nome_file=""):
        """Passo 2 su un testo con parole chiave gia' inglesi. Ritorna il testo Python."""
        t = self.t
        try:
            albero = ast.parse(testo2)
        except SyntaxError as e:
            raise SyntaxError(f"{nome_file}: {e.msg} (riga {e.lineno}) dopo la traduzione delle parole chiave") from e
        righe = testo2.splitlines(keepends=True)
        col = _colonne(righe)
        mod = {}

        def sost(riga, c, n, nuovo):
            mod.setdefault(riga - 1, []).append((c, n, nuovo))

        def inserisci(riga, c, nuovo):
            mod.setdefault(riga - 1, []).append((c, 0, nuovo))

        moduli_nome = self._importazioni(albero)
        self.radici_file = set()
        for n in ast.walk(albero):
            if isinstance(n, ast.Import):
                for a in n.names:
                    for k in range(len(a.name.split(".")), 0, -1):
                        pre = ".".join(a.name.split(".")[:k])
                        if pre in t.moduli:
                            self.radici_file.add(t.moduli[pre].split(".")[0])
                            break
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level and n.module in t.moduli:
                self.radici_file.add(t.moduli[n.module].split(".")[0])
        # nomi legati a un modulo italiano e mai riassegnati in altro modo
        altri = set()
        for n in ast.walk(albero):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                altri.add(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                altri.add(n.name)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                altri.update(py2pit._args_nomi(n.args))
        moduli_nome = {k: v for k, v in moduli_nome.items() if k not in altri}

        # ---- 1. funzioni, tipi ed eccezioni predefinite
        ris = RisolutoreIt(albero)
        conflitto = {n.id for n in ast.walk(albero) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)} | altri
        usa_builtins = False
        for (r, cb) in sorted(ris.riferimenti):
            c = col(r, cb)
            it = None
            m = re.match(r"[^\W\d]\w*", righe[r - 1][c:])
            if m:
                it = m.group(0)
            if it and it in t.builtin:
                en = t.builtin[it]
                if en in conflitto and en != it:
                    sost(r, c, len(it), "_pit_builtins." + en)
                    usa_builtins = True
                    self.nota(r, "conflitto", f"«{en}» e' anche un nome del programma: uso builtins.{en}")
                else:
                    sost(r, c, len(it), en)

        # ---- 2. importazioni
        mod_it = t.moduli
        for n in ast.walk(albero):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in mod_it:
                        en = mod_it[a.name]
                        self._sost_testo(righe, col, sost, n, a.name, en)
                    elif a.name.split(".")[0] in {m.split(".")[0] for m in mod_it}:
                        pezzi = a.name.split(".")
                        # prefisso italiano piu' lungo
                        for k in range(len(pezzi), 0, -1):
                            pre = ".".join(pezzi[:k])
                            if pre in mod_it:
                                self._sost_testo(righe, col, sost, n, pre, mod_it[pre])
                                break
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level and n.module in mod_it:
                en_mod = mod_it[n.module]
                self._sost_testo(righe, col, sost, n, n.module, en_mod)
                for a in n.names:
                    if a.name == "*":
                        continue
                    completo = t.nomi.get(n.module, {}).get(a.name)
                    sub_it = n.module + "." + a.name
                    if completo is None and sub_it in mod_it:      # da interfaccia importa tema  ->  da tkinter importa ttk as tema
                        sub_en = mod_it[sub_it]
                        completo = sub_en[len(en_mod) + 1:] if sub_en.startswith(en_mod + ".") else sub_en
                    if completo is None:
                        continue            # nome gia' inglese (o sconosciuto): resta
                    nuovo = completo
                    sotto = (en_mod + "." + completo) in set(mod_it.values())
                    if "." in completo and not sotto:
                        self.nota(n.lineno, "importazione", f"«{a.name}» e' «{completo}»: controlla l'importazione")
                    self._sost_nome_import(righe, col, sost, n, a, nuovo)
        for n in ast.walk(albero):
            if isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                nome_f = n.func.id if isinstance(n.func, ast.Name) else ""
                if nome_f in ("exec", "eval", "compile", "esegui", "valuta", "compila") and nome_f in set(self.t.builtin) | {"exec", "eval", "compile"}:
                    self.nota(n.lineno, "codice in una stringa", "il codice dentro la stringa non viene tradotto: controllalo a mano")
        # ---- 3. accessi a moduli e attributi
        self._attributi(albero, righe, col, sost, inserisci, moduli_nome, mod_it)
        # ---- 4. opzioni con nome
        self._opzioni(albero, righe, col, sost, moduli_nome)
        # ---- 5. se_stesso -> self
        if not any(isinstance(x, ast.Name) and x.id == "self" for x in ast.walk(albero)):
            for x in ast.walk(albero):
                if isinstance(x, ast.Name) and x.id == "se_stesso":
                    sost(x.lineno, col(x.lineno, x.col_offset), len("se_stesso"), "self")
                elif isinstance(x, ast.arg) and x.arg == "se_stesso":
                    sost(x.lineno, col(x.lineno, x.col_offset), len("se_stesso"), "self")
        risultato = applica(righe, mod)
        if usa_builtins:
            risultato = self._dopo_docstring(risultato, "import builtins as _pit_builtins\n")
        if self.usa_aiuto:
            risultato = self._dopo_docstring(risultato, AIUTO_ATTR.lstrip("\n") + "\n")
        ast.parse(risultato)
        return risultato

    def _dopo_docstring(self, testo, inserto):
        """Mette inserto dopo la docstring e gli 'from __future__' iniziali."""
        albero = ast.parse(testo)
        riga = 0
        for i, n in enumerate(albero.body):
            if i == 0 and isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant) and isinstance(n.value.value, str):
                riga = n.end_lineno
            elif isinstance(n, ast.ImportFrom) and n.module == "__future__":
                riga = n.end_lineno
            else:
                break
        righe = testo.splitlines(keepends=True)
        righe.insert(riga, ("\n" if riga else "") + inserto + ("\n" if not inserto.endswith("\n\n") else ""))
        return "".join(righe)

    # ---- sostituzioni nel testo di import
    def _sost_testo(self, righe, col, sost, nodo, vecchio, nuovo):
        """Sostituisce il nome del modulo (vecchio) nella riga dell'import."""
        r = nodo.lineno
        for k in range(r, nodo.end_lineno + 1):
            riga = righe[k - 1]
            m = re.search(r"(?<![\w.])" + re.escape(vecchio) + r"(?![\w])", riga[(col(r, nodo.col_offset) if k == r else 0):])
            if m:
                inizio = m.start() + (col(r, nodo.col_offset) if k == r else 0)
                sost(k, inizio, len(vecchio), nuovo)
                return

    def _sost_nome_import(self, righe, col, sost, nodo, alias, completo):
        """Dentro 'da modulo importa nome': nome italiano -> nome originale (con 'come' per non cambiare il resto del codice)."""
        for k in range(nodo.lineno, nodo.end_lineno + 1):
            riga = righe[k - 1]
            m = re.search(r"(?<![\w.])" + re.escape(alias.name) + r"(?![\w])", riga[(col(nodo.lineno, nodo.col_offset) + 7) if k == nodo.lineno else 0:])
            if m:
                inizio = m.start() + ((col(nodo.lineno, nodo.col_offset) + 7) if k == nodo.lineno else 0)
                resto = riga[inizio + len(alias.name):]
                gia_come = re.match(r"\s+as\s+\w+", resto) is not None
                if "." in completo:
                    sost(k, inizio, len(alias.name), completo.split(".")[-1] if gia_come else completo.split(".")[-1] + " as " + alias.name)
                else:
                    sost(k, inizio, len(alias.name), completo if gia_come else completo + " as " + alias.name)
                return

    # ------------------------------------------------------------ attributi
    def _catena(self, nodo, moduli_nome):
        """Se nodo e' Name/Attribute che descrive un modulo italiano, ritorna il suo percorso italiano."""
        if isinstance(nodo, ast.Name):
            return moduli_nome.get(nodo.id)
        if isinstance(nodo, ast.Attribute):
            base = self._catena(nodo.value, moduli_nome)
            if base and (base + "." + nodo.attr) in self.t.moduli:
                return base + "." + nodo.attr
        return None

    def _attributi(self, albero, righe, col, sost, inserisci, moduli_nome, mod_it):
        t = self.t
        # classi con le loro prime variabili (self)
        self_di = {}
        for f in ast.walk(albero):
            if isinstance(f, ast.ClassDef):
                for m in f.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.args.args:
                        for x in ast.walk(m):
                            self_di[id(x)] = m.args.args[0].arg
                        # ponti: metodi che la libreria richiama per nome (solo se la classe deriva da quella libreria)
                        if f.bases and m.name in t.ponti and self._deriva_da(f, {c for c, _ in t.ponti[m.name]}):
                            en = next(e for c, e in t.ponti[m.name] if c in self._basi(f))
                            r0 = m.lineno
                            inizio = righe[r0 - 1].index(m.name, col(r0, m.col_offset))
                            sost(r0, inizio, len(m.name), en)
                            self.nota(m.lineno, "metodo", f"«{m.name}» -> «{en}» (la libreria lo richiama per nome)")
        tipi_nome = self._tipi_nomi(albero)
        trattati = set()
        for n in ast.walk(albero):
            if not isinstance(n, ast.Attribute):
                continue
            r, fine_c = n.end_lineno, col(n.end_lineno, n.end_col_offset)
            inizio_attr = fine_c - len(n.attr)
            if righe[r - 1][inizio_attr:fine_c] != n.attr:
                continue
            percorso = self._catena(n.value, moduli_nome)
            # (a) il modulo stesso: nome del modulo italiano -> originale
            if percorso and isinstance(n.value, ast.Name) and id(n.value) not in trattati:
                trattati.add(id(n.value))
                if n.value.id in moduli_nome and n.value.id in self._import_semplici(albero):
                    base = moduli_nome[n.value.id]
                    sost(n.value.lineno, col(n.value.lineno, n.value.col_offset), len(n.value.id), mod_it[base])
            # (b) attributo di un modulo italiano
            if percorso is not None and (percorso + "." + n.attr) in t.moduli:
                sotto = t.moduli[percorso + "." + n.attr]
                padre = t.moduli[percorso]
                nuovo = sotto[len(padre) + 1:] if sotto.startswith(padre + ".") else sotto
                sost(r, inizio_attr, len(n.attr), nuovo)
                continue
            if percorso is not None:
                nomi = t.nomi.get(percorso, {})
                if n.attr in nomi and nomi[n.attr] != n.attr:
                    sost(r, inizio_attr, len(n.attr), nomi[n.attr])
                continue
            if isinstance(n.value, ast.Name) and n.value.id in moduli_nome:
                continue
            # (c) metodo o attributo italiano di un oggetto
            cand = t.attr.get(n.attr)
            if not cand or n.attr in DUNDER:
                continue
            inglesi = [e for e, _ in sorted(cand.items(), key=lambda kv: -kv[1]) if e != n.attr]
            if not inglesi:
                continue
            inglesi = self._filtra(n.attr, inglesi)
            proprio = n.attr in self.p.definiti
            tipo = tipi_nome.get(self._chiave(n.value))
            if tipo == "utente" and proprio:
                continue                      # oggetto di una classe del programma: il metodo e' suo
            if tipo in PROTOTIPI:
                ammessi = [e for e in inglesi if hasattr(PROTOTIPI[tipo], e)]
                if len(ammessi) == 1:         # lista, dizionario, insieme o testo: il nome inglese e' certo
                    sost(r, inizio_attr, len(n.attr), ammessi[0])
                    continue
                if ammessi:
                    inglesi = ammessi
                    proprio = False
            ricevitore_self = isinstance(n.value, ast.Name) and self_di.get(id(n)) == n.value.id
            if proprio and ricevitore_self:
                continue
            memorizza = isinstance(n.ctx, (ast.Store, ast.Del))
            if proprio and memorizza:
                continue
            if len(inglesi) == 1 and not proprio:
                sost(r, inizio_attr, len(n.attr), inglesi[0])
                continue
            if memorizza:
                sost(r, inizio_attr, len(n.attr), inglesi[0])
                self.nota(r, "ambiguo", f"«.{n.attr}» assegnato: scelto «{inglesi[0]}» tra {inglesi}")
                continue
            # scelta a esecuzione
            if self._tra_parentesi(righe, col, n):
                sost(r, inizio_attr, len(n.attr), inglesi[0])
                self.nota(r, "ambiguo", f"«.{n.attr}»: scelto «{inglesi[0]}» tra {inglesi}")
                continue
            punto = righe[r - 1].rfind(".", 0, inizio_attr)
            if punto < 0:
                sost(r, inizio_attr, len(n.attr), inglesi[0])
                self.nota(r, "ambiguo", f"«.{n.attr}»: scelto «{inglesi[0]}» tra {inglesi}")
                continue
            nomi_cand = ([n.attr] if proprio else []) + inglesi
            inserisci(n.value.lineno, col(n.value.lineno, n.value.col_offset), "_pit_attr(")
            sost(r, punto, fine_c - punto, ", " + ", ".join(repr(x) for x in nomi_cand) + ")")
            self.usa_aiuto = True
            self.nota(r, "scelta a esecuzione", f"«.{n.attr}» -> {nomi_cand}")

    def _filtra(self, it, inglesi):
        """Tiene i nomi inglesi che una libreria importata dal file (o i tipi base) definisce davvero."""
        buoni = [e for e in inglesi if (self.t.radici.get((it, e), {""}) & (self.radici_file | {""}))]
        return buoni or inglesi

    def _chiave(self, nodo):
        if isinstance(nodo, ast.Name):
            return nodo.id
        if isinstance(nodo, ast.Attribute):
            b = self._chiave(nodo.value)
            return b + "." + nodo.attr if b else None
        return None

    def _tipi_nomi(self, albero):
        """{nome o self.nome: 'lista'|'dizionario'|'insieme'|'testo'|'utente'} quando ogni assegnazione del file dice lo stesso."""
        visti = {}

        def tipo_di(v):
            if isinstance(v, (ast.List, ast.ListComp)):
                return "lista"
            if isinstance(v, (ast.Dict, ast.DictComp)):
                return "dizionario"
            if isinstance(v, (ast.Set, ast.SetComp)):
                return "insieme"
            if isinstance(v, ast.JoinedStr) or (isinstance(v, ast.Constant) and isinstance(v.value, str)):
                return "testo"
            if isinstance(v, ast.Call) and isinstance(v.func, ast.Name):
                f = v.func.id
                if f in self.p.classi:
                    return "utente"
                return {"lista": "lista", "list": "lista", "dizionario": "dizionario", "dict": "dizionario",
                        "insieme": "insieme", "set": "insieme", "testo": "testo", "str": "testo"}.get(f)
            return None

        for n in ast.walk(albero):
            bersagli = []
            if isinstance(n, ast.Assign):
                bersagli = [(t, n.value) for t in n.targets]
            elif isinstance(n, ast.AnnAssign) and n.value is not None:
                bersagli = [(n.target, n.value)]
            for t, v in bersagli:
                k = self._chiave(t)
                if k:
                    visti.setdefault(k, set()).add(tipo_di(v))
        return {k: next(iter(v)) for k, v in visti.items() if len(v) == 1 and None not in v}

    def _basi(self, classe):
        """Nomi (originali) delle classi base: l'ultimo pezzo di ogni base, tradotto se e' un alias italiano."""
        t = self.t
        nomi = set()
        for b in classe.bases:
            term = b.id if isinstance(b, ast.Name) else b.attr if isinstance(b, ast.Attribute) else None
            if not term:
                continue
            nomi.add(term)
            for tab in t.nomi.values():
                if term in tab:
                    nomi.add(tab[term].split(".")[-1])
        return nomi

    def _deriva_da(self, classe, nomi_ponte):
        return bool(self._basi(classe) & nomi_ponte)

    def _import_semplici(self, albero):
        """Nomi legati da 'importa modulo' senza 'come': e' il nome italiano del modulo che va cambiato nel codice."""
        if getattr(self, "_cache_is", (None,))[0] is not albero:
            self._cache_is = (albero, {a.name.split(".")[0] for n in ast.walk(albero) if isinstance(n, ast.Import) for a in n.names if not a.asname})
        return self._cache_is[1]

    def _importato_con_alias(self, albero, nome):
        for n in ast.walk(albero):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.asname == nome:
                        return True
        return False

    def _tra_parentesi(self, righe, col, n):
        """Il valore a sinistra del punto e' racchiuso tra parentesi: (x).attr"""
        v = n.value
        r, fc = v.end_lineno, col(v.end_lineno, v.end_col_offset)
        resto = righe[r - 1][fc:].lstrip()
        if resto.startswith(")"):
            dopo = resto[1:].lstrip()
            return dopo.startswith(".")
        return False

    # ------------------------------------------------------------ opzioni con nome
    def _opzioni(self, albero, righe, col, sost, moduli_nome):
        t = self.t
        funzioni_utente = set(self.p.definiti)
        for n in ast.walk(albero):
            if not isinstance(n, ast.Call) or not n.keywords:
                continue
            f = n.func
            nome_f = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if nome_f in funzioni_utente or nome_f in ("dizionario", "dict", "formatta", "format"):
                continue
            for k in n.keywords:
                if not k.arg:
                    continue
                nome_en = k.arg
                if k.arg in t.opzioni and k.arg not in self.p.parametri:
                    cand = [e for e, _ in sorted(t.opzioni[k.arg].items(), key=lambda kv: -kv[1]) if e != k.arg]
                    cand = self._filtra(k.arg, cand) if cand else cand
                    cand.sort(key=lambda e: len(self.t.radici.get((k.arg, e), ())))      # a pari merito, il nome piu' specifico (dpi e non resolution)
                    if cand:
                        if len(cand) > 1:
                            self.nota(k.value.lineno, "ambiguo", f"opzione «{k.arg}=»: scelta «{cand[0]}» tra {cand}")
                        r = k.lineno
                        sost(r, col(r, k.col_offset), len(k.arg), cand[0])
                        nome_en = cand[0]
                # valori testuali italiani di certe opzioni: fill="entrambi" -> fill="both"
                v = k.value
                if nome_en in t.valori and isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value in t.valori[nome_en]                         and v.lineno == v.end_lineno:
                    c0, c1 = col(v.lineno, v.col_offset), col(v.end_lineno, v.end_col_offset)
                    letterale = righe[v.lineno - 1][c0:c1]
                    if len(letterale) >= 2 and letterale[0] in "\"'" and letterale[-1] == letterale[0] and letterale[1:-1] == v.value:
                        sost(v.lineno, c0 + 1, len(v.value), t.valori[nome_en][v.value])


def converti_testo(sorgente, progetto=None, nome_file=""):
    """Un file .pit (testo) -> (testo Python, rapporto)."""
    progetto = progetto or Progetto()
    t2 = traduci_parole_chiave(sorgente)
    try:
        progetto.aggiungi(ast.parse(t2))
    except SyntaxError:
        pass
    c = Convertitore(progetto)
    out = c.converti(t2, nome_file)
    return out, c.rapporto


def main(argv):
    a = [x for x in argv if not x.startswith("--")]
    if "--progetto" in argv:
        from pit2py_progetto import esporta
        return esporta(a[0], a[1])
    if len(a) < 2:
        print(__doc__)
        return 2
    sorgente = open(a[0], encoding="utf-8").read()
    out, rapp = converti_testo(sorgente, nome_file=a[0])
    with open(a[1], "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"{a[0]} -> {a[1]}  ({len(out.splitlines())} righe, {len(rapp)} note)")
    for r, cat, testo in rapp[:20]:
        print(f"   riga {r}: {cat}: {testo}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
