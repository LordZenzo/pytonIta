"""Traduce un programma Python (.py) in pitonit (.pit), token per token.

Uso:  python py2pit.py origine.py destinazione.pit [altro.py altro.pit ...]
      python py2pit.py --senza-verifica ...

Cosa cambia:  parole chiave (anche match/case/type), True/False/None e i nomi
dei builtin (print, len, ValueError...). Per i builtin si usa l'analisi degli
ambiti: un nome definito dal programma (es. una variabile "id") non viene toccato.
Cosa NON cambia:  commenti, stringhe, nomi di metodi/attributi di librerie.
Gli identificatori dell'utente che coincidono con parole italiane riservate
(testo, tipo, da, con...) diventano "nome_" in modo uguale in tutti i file.

Alla fine il risultato viene VERIFICATO: compilato con pitonit e confrontato
con l'originale (stessa struttura dell'albero sintattico).
"""
import ast
import io
import keyword
import os
import subprocess
import sys
import tokenize

SRC_ITALIANO = r'C:\AppPython\pitonit\src\Lib\_italiano.py'
PITONIT = next((p for p in (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pitonit.exe'), os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'installazione', 'pitonit.exe')) if os.path.exists(p)), 'pitonit.exe')
AST_PIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tipi_ast.pit')

KEYWORDS = {
    "False": "Falso", "None": "Nessuno", "True": "Vero", "and": "e",
    "as": "come", "assert": "asserisci", "async": "asincrono",
    "await": "attendi", "break": "interrompi", "class": "classe",
    "continue": "continua", "def": "definisci", "del": "elimina",
    "elif": "altrimenti_se", "else": "altrimenti", "except": "eccetto",
    "finally": "infine", "for": "per", "from": "da", "global": "globale",
    "if": "se", "import": "importa", "in": "in", "is": "è",
    "lambda": "lambda", "nonlocal": "nonlocale", "not": "non", "or": "o",
    "pass": "passa", "raise": "solleva", "return": "ritorna",
    "try": "prova", "while": "mentre", "with": "con", "yield": "produci",
}
SOFT = {"match": "confronta", "case": "caso", "type": "tipo"}
# parole italiane riservate che un identificatore utente non puo' usare
RISERVATE = ({v for k, v in KEYWORDS.items() if v != k and v not in ("e", "o")}
             | {"confronta", "caso"})


def lib_in_uso():
    """La cartella Lib dell'interprete in uso. Nell'interprete incorporato di PitStudio.exe os.__file__ non esiste: si chiede a sysconfig."""
    try:
        import sysconfig
        percorso = sysconfig.get_path("stdlib")
        if percorso:
            return percorso
    except Exception:
        pass
    return os.path.dirname(getattr(os, "__file__", "") or sys.executable)


def _percorsi_italiano():
    """Dove cercare _italiano.py: accanto all'interprete (installazione) o nei sorgenti di sviluppo."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../pitonit
    return [os.path.join(base, 'Lib', '_italiano.py'),
            os.path.join(base, 'installazione', 'Lib', '_italiano.py'),
            os.path.join(lib_in_uso(), '_italiano.py'),      # la Lib dell'interprete in uso (Linux e macOS)
            SRC_ITALIANO]


def carica_builtin():
    """Tabella inglese -> italiano dei builtin: la legge da _italiano.py senza importarlo."""
    testo = None
    for p in _percorsi_italiano():
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                testo = f.read()
            break
    if testo is None:
        raise FileNotFoundError("_italiano.py non trovato: " + "; ".join(_percorsi_italiano()))
    albero = ast.parse(testo)
    tab = {}
    for nodo in albero.body:
        if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name) and nodo.targets[0].id in ("FUNZIONI", "ECCEZIONI"):
            tab.update(ast.literal_eval(nodo.value))
    return tab


BUILTIN = carica_builtin()            # inglese -> italiano
TARGET = set(BUILTIN.values())        # nomi italiani dei builtin


# ---------------------------------------------------------------- ambiti
class Ambito:
    def __init__(self, tipo, padre=None):
        self.tipo = tipo              # modulo | funzione | classe | comp
        self.padre = padre
        self.locali = set()
        self.globali = set()
        self.nonlocali = set()


COMP = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
FUNZ = (ast.FunctionDef, ast.AsyncFunctionDef)


def _args_nomi(args):
    out = [x.arg for x in args.posonlyargs + args.args + args.kwonlyargs]
    if args.vararg:
        out.append(args.vararg.arg)
    if args.kwarg:
        out.append(args.kwarg.arg)
    return out


def _args_esterni(args):
    """Parti degli argomenti valutate nell'ambito esterno."""
    out = list(args.defaults) + [d for d in args.kw_defaults if d]
    for x in args.posonlyargs + args.args + args.kwonlyargs + \
            [y for y in (args.vararg, args.kwarg) if y]:
        if x.annotation:
            out.append(x.annotation)
    return out


def _parti(n):
    """(parti nell'ambito esterno, parti nell'ambito interno)."""
    if isinstance(n, FUNZ):
        est = n.decorator_list + _args_esterni(n.args) + ([n.returns] if n.returns else [])
        return est, n.body
    if isinstance(n, ast.Lambda):
        return _args_esterni(n.args), [n.body]
    if isinstance(n, ast.ClassDef):
        return n.decorator_list + n.bases + [k.value for k in n.keywords], n.body
    if isinstance(n, ast.DictComp):
        inn = [n.key, n.value]
    else:
        inn = [n.elt]
    gen = n.generators
    interno = []
    for i, g in enumerate(gen):
        if i:
            interno.append(g.iter)
        interno.append(g.target)
        interno.extend(g.ifs)
    return [gen[0].iter], inn + interno


def _lega(n, a):
    """Registra i nomi che il nodo n (solo lui) lega nell'ambito a."""
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        a.locali.add(n.name)
    elif isinstance(n, ast.Global):
        a.globali.update(n.names)
    elif isinstance(n, ast.Nonlocal):
        a.nonlocali.update(n.names)
    elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
        t = a
        while t.tipo == "comp" and not _in_comp_target(n):
            t = t.padre          # walrus: lega nell'ambito che contiene la comprehension
        t.locali.add(n.id)
    elif isinstance(n, ast.alias):
        a.locali.add((n.asname or n.name).split(".")[0])
    elif isinstance(n, ast.ExceptHandler) and n.name:
        a.locali.add(n.name)
    elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name:
        a.locali.add(n.name)
    elif isinstance(n, ast.MatchMapping) and n.rest:
        a.locali.add(n.rest)


_TARGET_COMP = set()


def _in_comp_target(n):
    return id(n) in _TARGET_COMP


class Risolutore(ast.NodeVisitor):
    """Trova i Name che si riferiscono a un builtin (non a un nome dell'utente)."""

    def __init__(self, albero):
        _TARGET_COMP.clear()
        for n in ast.walk(albero):
            if isinstance(n, COMP):
                for g in n.generators:
                    for x in ast.walk(g.target):
                        _TARGET_COMP.add(id(x))
        self.ambiti = {}
        self.modulo = Ambito("modulo")
        self._costruisci(albero, self.modulo)
        for a in self.ambiti.values():
            if a.tipo == "funzione":
                self.modulo.locali.update(a.locali & a.globali)
                a.locali -= a.globali | a.nonlocali
        self.pila = [self.modulo]
        self.riferimenti = set()
        for b in albero.body:
            self.visit(b)

    def _costruisci(self, n, corr):
        for f in ast.iter_child_nodes(n):
            self._nodo(f, corr)

    def _nodo(self, n, corr):
        _lega(n, corr)
        if isinstance(n, FUNZ + (ast.Lambda, ast.ClassDef) + COMP):
            tipo = ("funzione" if isinstance(n, FUNZ + (ast.Lambda,))
                    else "classe" if isinstance(n, ast.ClassDef) else "comp")
            a = Ambito(tipo, corr)
            if tipo == "funzione":
                a.locali.update(_args_nomi(n.args))
            self.ambiti[id(n)] = a
            esterno, interno = _parti(n)
            for f in esterno:
                self._nodo(f, corr)
            for f in interno:
                self._nodo(f, a)
        else:
            for f in ast.iter_child_nodes(n):
                self._nodo(f, corr)

    # --- risoluzione
    def _builtin(self, nome):
        for i, a in enumerate(reversed(self.pila)):
            if a.tipo == "classe" and i > 0:
                continue
            if nome in a.globali:
                return nome not in self.modulo.locali
            if nome in a.locali:
                return False
        return True

    def visit_Name(self, n):
        if n.id in BUILTIN and self._builtin(n.id):
            self.riferimenti.add((n.lineno, n.col_offset))

    def _scope(self, n):
        esterno, interno = _parti(n)
        for f in esterno:
            self.visit(f)
        self.pila.append(self.ambiti[id(n)])
        for f in interno:
            self.visit(f)
        self.pila.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = visit_Lambda = _scope
    visit_ClassDef = visit_ListComp = visit_SetComp = visit_DictComp = _scope
    visit_GeneratorExp = _scope


# ---------------------------------------------------------------- traduzione
def traduci(sorgente, rapporto):
    albero = ast.parse(sorgente)
    righe_orig = sorgente.splitlines(keepends=True)

    # posizioni delle parole chiave "morbide": match / case / type
    soft = set()
    for n in ast.walk(albero):
        if isinstance(n, ast.Match):
            soft.add((n.lineno, n.col_offset, "match"))
            for c in n.cases:
                soft.add((c.pattern.lineno, c.pattern.col_offset, "case"))
        elif isinstance(n, getattr(ast, "TypeAlias", ())):
            soft.add((n.lineno, n.col_offset, "type"))

    ris = Risolutore(albero)

    def a_colonna(riga, byte):
        return len(righe_orig[riga - 1].encode()[:byte].decode())

    rif = {(r, a_colonna(r, c)) for r, c in ris.riferimenti}
    soft_pos = {}
    for r, c, kw in soft:
        soft_pos.setdefault(r, []).append((a_colonna(r, c), kw))

    posizioni_pattern = sorted((r, a_colonna(r, c)) for r, cs in soft_pos.items() for c, kw in cs if kw == "case")

    toks = [t for t in tokenize.generate_tokens(io.StringIO(sorgente).readline)
            if t.type not in (tokenize.NL, tokenize.COMMENT)]
    righe = list(righe_orig)
    sost = []
    for i, t in enumerate(toks):
        if t.type != tokenize.NAME:
            continue
        s = t.string
        prec = toks[i - 1].string if i else ""
        dopo_punto = prec == "."
        if dopo_punto and s == "import":          # "from . import x": il punto non e' un attributo
            k = i - 1
            while k >= 0 and toks[k].string in (".", "..."):
                k -= 1
            if k >= 0 and toks[k].string == "from":
                dopo_punto = False
        nuovo = None
        if keyword.iskeyword(s) and not dopo_punto:
            nuovo = KEYWORDS[s]
        elif s in ("match", "case", "type") and not dopo_punto:
            r, c = t.start
            for col, kw in soft_pos.get(r, []):
                # match/type: stessa posizione; case: subito prima del pattern
                if kw == s and ((kw != "case" and col == c) or
                                (kw == "case" and c < col and
                                 toks[i - 1].type in (tokenize.NEWLINE, tokenize.INDENT,
                                                      tokenize.DEDENT))):
                    nuovo = SOFT[s]
                    break
            if nuovo is None and s == "case" and toks[i - 1].type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                # pattern tra parentesi su piu' righe: la sua posizione e' piu' avanti, ma sempre nella stessa istruzione
                prossimo = next((q for q in posizioni_pattern if q > t.start), None)
                if prossimo is not None:
                    k = i + 1
                    while k < len(toks) and toks[k].start < prossimo and toks[k].type != tokenize.NEWLINE:
                        k += 1
                    if k < len(toks) and toks[k].start >= prossimo:
                        nuovo = SOFT["case"]
            if nuovo is None and s == "type":
                # "type" come builtin (type(x)) e' gestito sotto
                if t.start in rif:
                    nuovo = BUILTIN["type"]
        elif s in RISERVATE or s in TARGET:
            nuovo = s + "_"
            rapporto.append((t.start[0], s, nuovo, "attributo" if dopo_punto else "nome"))
        elif s in BUILTIN and not dopo_punto and t.start in rif:
            nuovo = BUILTIN[s]
        if nuovo and nuovo != s:
            sost.append((t.start[0] - 1, t.start[1], len(s), nuovo))
    for r, c, n, nuovo in sorted(sost, reverse=True):
        righe[r] = righe[r][:c] + nuovo + righe[r][c + n:]
    return "".join(righe)


def tipi_python(path):
    albero = ast.parse(open(path, encoding='utf-8').read())
    return " ".join(type(n).__name__ for n in ast.walk(albero))


def tipi_pitonit(path):
    r = subprocess.run([PITONIT, AST_PIT, path], capture_output=True,
                       text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit("ERRORE di compilazione in pitonit:\n" + r.stderr)
    return r.stdout.strip()


def main(argv):
    verifica = "--senza-verifica" not in argv
    a = [x for x in argv if not x.startswith("--")]
    ok = True
    for k in range(0, len(a), 2):
        rapp = []
        src = open(a[k], encoding='utf-8').read()
        out = traduci(src, rapp)
        with open(a[k + 1], 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print(f"{a[k]} -> {a[k+1]}  ({len(src.splitlines())} righe)")
        visti = {}
        for riga, vecchio, nuovo, tipo in rapp:
            visti[vecchio] = visti.get(vecchio, 0) + 1
        for v, n in visti.items():
            print(f"   rinominato {v} -> {v}_  ({n} volte)")
        if verifica:
            if tipi_python(a[k]) == tipi_pitonit(a[k + 1]):
                print("   verifica: struttura identica all'originale  OK")
            else:
                print("   verifica: STRUTTURA DIVERSA")
                ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
