p = r'C:\AppPython\pitonit\src\Lib\_italiano.py'
s = open(p, encoding='utf-8', newline='').read()

old = '''        try:
            setattr(k, it, vars(k)[en])
        except TypeError:                      # tipi scritti in C
            if not _b._aggiungi_alias(k, en, it):
                raise
'''
new = '''        try:
            setattr(k, it, _delega(vars(k)[en], en, it))
        except TypeError:                      # tipi scritti in C
            if not _b._aggiungi_alias(k, en, it):
                raise
'''
assert old in s
s = s.replace(old, new)

helper = '''

def _delega(v, en, it):
    """Alias che rispetta le sottoclassi: richiama sempre il nome inglese
    (cosi' se una sottoclasse ridefinisce `submit`, `invia` usa la sua versione)."""
    import types
    if isinstance(v, types.FunctionType):
        def alias(self, *a, **k):
            return getattr(self, en)(*a, **k)
        alias.__name__ = it
        alias.__qualname__ = it
        alias.__doc__ = v.__doc__
        return alias
    if isinstance(v, property):
        return property(
            lambda self: getattr(self, en),
            (lambda self, val: setattr(self, en, val)) if v.fset else None,
            (lambda self: delattr(self, en)) if v.fdel else None,
            v.__doc__)
    if isinstance(v, classmethod) and isinstance(v.__func__, types.FunctionType):
        def alias(cls, *a, **k):
            return getattr(cls, en)(*a, **k)
        alias.__name__ = it
        return classmethod(alias)
    return v

'''
marker = '\ndef traduci_kw('
assert marker in s
s = s.replace(marker, helper + marker, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)

q = r'C:\AppPython\pitonit\tools\dizionari\p1_altre.py'
t = open(q, encoding='utf-8').read()
t = t.replace("('ottieni', 'invia', 'metti', 'elimina', 'testa', 'modifica', 'richiesta')",
              "('ottieni', 'invia', 'metti', 'cancella', 'testa', 'modifica', 'richiesta')")
open(q, 'w', encoding='utf-8').write(t)
print("ok")
