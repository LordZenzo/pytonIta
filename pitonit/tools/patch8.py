p = r'C:\AppPython\pitonit\tools\py2pit.py'
s = open(p, encoding='utf-8').read()
a = s.index("# ---------------------------------------------------------------- ambiti")
b = s.index("# ---------------------------------------------------------------- traduzione")
nuovo = '''# ---------------------------------------------------------------- ambiti
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
    for x in args.posonlyargs + args.args + args.kwonlyargs + \\
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


'''
open(p, 'w', encoding='utf-8').write(s[:a] + nuovo + s[b:])
print("ok")
