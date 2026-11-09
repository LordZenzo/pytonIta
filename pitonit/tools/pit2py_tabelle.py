"""Tabelle italiano -> inglese per pit2py, ricavate (senza eseguirli) dai file di pitonit:

  _italiano.py            parole chiave, funzioni, eccezioni, metodi dei tipi base, opzioni (chiave=, inverso=...)
  _mappa_moduli.py        modulo originale -> modulo italiano
  <modulo italiano>.py    nomi (analizza = _ott(_orig, 'parse')), classi (alias_tipo), opzioni (_OPZ), ponti

Tutto viene letto con ast: nessun modulo viene importato.
"""
import ast
import glob
import os

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
KW_IT2EN = {v: k for k, v in KEYWORDS.items() if v != k}
SOFT = {"confronta": "match", "caso": "case", "tipo": "type"}


def cartelle_lib():
    """Le cartelle Lib di pitonit: sviluppo (installazione\\Lib) o installato (pitonit\\Lib)."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidati = [os.path.join(base, "installazione", "Lib"), os.path.join(base, "Lib"),
                 os.path.join(os.path.dirname(base), "Lib")]
    return [c for c in candidati if os.path.exists(os.path.join(c, "_mappa_moduli.py"))]


def _leggi(percorso):
    with open(percorso, encoding="utf-8") as f:
        return ast.parse(f.read())


def _dict_testi(nodo):
    """{str: str} se il nodo e' un dizionario letterale di soli testi (altrimenti None)."""
    try:
        v = ast.literal_eval(nodo)
    except Exception:
        return None
    if isinstance(v, dict) and all(isinstance(k, str) and isinstance(x, str) for k, x in v.items()):
        return v
    return None


class Tabelle:
    def __init__(self):
        self.builtin = {}          # italiano -> inglese (funzioni, tipi, eccezioni)
        self.moduli = {}           # modulo italiano -> modulo originale
        self.nomi = {}             # modulo italiano -> {italiano: percorso originale}
        self.attr = {}             # italiano -> {inglese: quante volte} (metodi/attributi di tipi e classi)
        self.opzioni = {}          # italiano -> {inglese: quante volte} (opzioni con nome: chiave=, testo=...)
        self.valori = {}           # opzione inglese -> {valore italiano: valore inglese} (fill="entrambi")
        self.radici = {}           # (italiano, inglese) -> insiemi di moduli originali di primo livello che lo definiscono ('' = tipi base)
        self.ponti = {}            # italiano -> inglese (metodi che la libreria richiama per nome)
        self.cartella = None
        self._carica()

    # ---------------------------------------------------------------- _italiano.py
    def _carica(self):
        cartelle = cartelle_lib()
        if not cartelle:
            raise FileNotFoundError("Lib di pitonit non trovata (serve _mappa_moduli.py)")
        lib = cartelle[0]
        self.cartella = lib
        alb = _leggi(os.path.join(lib, "_italiano.py"))
        for n in alb.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
                nome = n.targets[0].id
                d = _dict_testi(n.value)
                if nome in ("FUNZIONI", "ECCEZIONI") and d:
                    for en, it in d.items():
                        self.builtin[it] = en
                elif nome == "METODI" and d:
                    for en, it in d.items():
                        self._aggiungi(self.attr, it, en)
                elif nome == "_KW_FUNZIONI":
                    for _, mappa in ast.literal_eval(n.value).items():
                        for it, en in mappa.items():
                            self._aggiungi(self.opzioni, it, en)
        # _KW_METODI contiene nomi di tipo (list, str): si legge a mano
        for n in alb.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_KW_METODI":
                for e in n.value.elts:
                    _, it, en, mappa = e.elts
                    self._aggiungi(self.attr, it.value, en.value)
                    for k, v in ast.literal_eval(mappa).items():
                        self._aggiungi(self.opzioni, k, v)
        # le classi enumera/abbina sono funzioni predefinite con opzioni
        self.builtin.setdefault("enumera", "enumerate")
        self.builtin.setdefault("abbina", "zip")
        for it, en in (("separatore", "sep"), ("fine", "end"), ("svuota", "flush")):      # stampa(...)
            self._aggiungi(self.opzioni, it, en)
        self._aggiungi(self.opzioni, "inizio", "start")
        self._aggiungi(self.opzioni, "rigoroso", "strict")
        # ---------------------------------------------------------------- moduli italiani
        ns = {}
        exec(compile(open(os.path.join(lib, "_mappa_moduli.py"), encoding="utf-8").read(), "mappa", "exec"), ns)
        mappa = ns["MAPPA"]
        self.moduli = {it: en for en, it in mappa.items()}
        radici = [lib] + [d for d in (os.path.join(lib, "site-packages"),) if os.path.isdir(d)]
        for it, en in self.moduli.items():
            percorso = None
            for r in radici:
                p = os.path.join(r, *it.split("."))
                for cand in (p + ".py", os.path.join(p, "__init__.py")):
                    if os.path.exists(cand):
                        percorso = cand
                        break
                if percorso:
                    break
            if percorso:
                self._modulo(it, percorso)

    def _aggiungi(self, tab, chiave, valore, radice=""):
        d = tab.setdefault(chiave, {})
        d[valore] = d.get(valore, 0) + 1
        self.radici.setdefault((chiave, valore), set()).add(radice)

    def _modulo(self, it, percorso):
        alb = _leggi(percorso)
        radice = self.moduli[it].split(".")[0]
        nomi = self.nomi.setdefault(it, {})
        dizionari = {}
        for n in alb.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Dict):
                d = _dict_testi(n.value)
                if d is not None:
                    dizionari[n.targets[0].id] = d
        for n in alb.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
                nome, v = n.targets[0].id, n.value
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "_ott" and len(v.args) == 2 \
                        and isinstance(v.args[1], ast.Constant):
                    nomi[nome] = v.args[1].value
                elif nome == "_AUTO_NOMI" and nome in dizionari:
                    for k, x in dizionari[nome].items():
                        nomi.setdefault(k, x)
                elif nome == "_AUTO_TIPI" and isinstance(n.value, ast.Dict):
                    try:
                        for _, mappa in ast.literal_eval(n.value).items():
                            for k, x in mappa.items():
                                self._aggiungi(self.attr, k, x, radice)
                    except Exception:
                        pass
            elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name):
                f, a = n.value.func.id, n.value.args
                if f == "alias_tipo" and len(a) == 2:
                    d = _dict_testi(a[1])
                    for k, x in (d or {}).items():
                        self._aggiungi(self.attr, k, x.lstrip("@"), radice)
                elif f == "kw_tipo" and len(a) >= 3 and isinstance(a[2], ast.Name):
                    for k, x in dizionari.get(a[2].id, {}).items():
                        self._aggiungi(self.opzioni, k, x, radice)
                elif f == "_ponte" and len(a) == 2:
                    d = _dict_testi(a[1])
                    classe = a[0].attr if isinstance(a[0], ast.Attribute) else (a[0].args[1].value if isinstance(a[0], ast.Call) and len(a[0].args) == 2 else "")
                    classe = classe.split(".")[-1]
                    for en, k in (d or {}).items():
                        self.ponti.setdefault(k, set()).add((classe, en))
                        self._aggiungi(self.attr, k, en, radice)
        for n in alb.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id.startswith("_VAL"):
                try:
                    for opz, mappa in ast.literal_eval(n.value).items():
                        if isinstance(mappa, dict):
                            self.valori.setdefault(opz, {}).update({k: v for k, v in mappa.items() if isinstance(k, str) and isinstance(v, str)})
                except Exception:
                    pass
        for nome, d in dizionari.items():          # _OPZ e simili usati da _tr(...) nei cicli
            if nome.startswith("_O") and not nome.startswith("_AUTO"):
                for k, x in d.items():
                    self._aggiungi(self.opzioni, k, x, radice)


if __name__ == "__main__":
    t = Tabelle()
    print("builtin", len(t.builtin), "| moduli", len(t.moduli), "| con nomi", len(t.nomi),
          "| nomi", sum(len(v) for v in t.nomi.values()), "| attributi", len(t.attr), "| opzioni", len(t.opzioni), "| ponti", len(t.ponti))
    amb = {k: v for k, v in t.attr.items() if len(v) > 1}
    print("attributi con piu' di un nome inglese:", len(amb))
    for k, v in sorted(amb.items(), key=lambda kv: -sum(kv[1].values()))[:25]:
        print("  ", k, v)
    ambo = {k: v for k, v in t.opzioni.items() if len(v) > 1}
    print("opzioni ambigue:", len(ambo), list(ambo.items())[:8])
