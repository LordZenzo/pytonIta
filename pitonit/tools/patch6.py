import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

SRC = r'C:\AppPython\pitonit\src'

sub(SRC + r'\Modules\main.c', '''    fprintf(stderr, "Python %s on %s\\n", Py_GetVersion(), Py_GetPlatform());
    if (config->site_import) {
        fprintf(stderr, "%s\\n", COPYRIGHT);
    }''', '''    fprintf(stderr, "Pitonit %s (Python in italiano, basato su CPython) su %s\\n",
            Py_GetVersion(), Py_GetPlatform());
    if (config->site_import) {
        fprintf(stderr, "Digita \\"aiuto\\", \\"diritti_d_autore\\", "
                        "\\"riconoscimenti\\" o \\"licenza\\" per maggiori informazioni.\\n");
    }''')

sub(SRC + r'\Python\initconfig.c', '''        printf("Python %s\\n",
                (print_version >= 2) ? Py_GetVersion() : PY_VERSION);''', '''        printf("Pitonit %s\\n",
                (print_version >= 2) ? Py_GetVersion() : PY_VERSION);''')

sub(SRC + r'\Lib\code.py', '''cprt = 'Type "help", "copyright", "credits" or "license" for more information.\'''',
    '''cprt = 'Digita "aiuto", "diritti_d_autore", "riconoscimenti" o "licenza" per maggiori informazioni.\'''')

sub(SRC + r'\Lib\_italiano.py', '''def _stampa_italiana(*args, sep=" ", end="\\n", file=None, flush=False):
    """print() che mostra in italiano il messaggio delle eccezioni."""
    args = [traduci_errore(str(a)) if isinstance(a, BaseException) else a
            for a in args]
    _b.print(*args, sep=sep, end=end, file=file, flush=flush)
''', '''_COSTANTI = {True: "Vero", False: "Falso", None: "Nessuno"}


def rappresenta(x):
    """repr() che scrive Vero/Falso/Nessuno (anche dentro liste, tuple, ...)."""
    t = type(x)
    if x is True or x is False or x is None:
        return _COSTANTI[x]
    if t is list:
        return "[" + ", ".join(rappresenta(i) for i in x) + "]"
    if t is tuple:
        if len(x) == 1:
            return "(" + rappresenta(x[0]) + ",)"
        return "(" + ", ".join(rappresenta(i) for i in x) + ")"
    if t is dict:
        return "{" + ", ".join(rappresenta(k) + ": " + rappresenta(v)
                               for k, v in x.items()) + "}"
    if t is set and x:
        return "{" + ", ".join(rappresenta(i) for i in x) + "}"
    return repr(x)


def _come_testo(a):
    if isinstance(a, BaseException):
        return traduci_errore(str(a))
    if a is True or a is False or a is None or type(a) in (list, tuple, dict, set):
        return rappresenta(a)
    return a


def _stampa_italiana(*args, sep=" ", end="\\n", file=None, flush=False):
    """print() che scrive in italiano costanti ed errori."""
    _b.print(*[_come_testo(a) for a in args], sep=sep, end=end, file=file,
             flush=flush)


def _mostra_risultato(valore):
    """sys.displayhook della console interattiva."""
    if valore is None:
        return
    builtins_italiani["_"] = valore
    _b._ = valore
    sys.stdout.write(rappresenta(valore) + "\\n")
''')

sub(SRC + r'\Lib\_italiano.py', '''    builtins_italiani["stampa"] = _stampa_italiana
''', '''    builtins_italiani["stampa"] = _stampa_italiana
    if sys.displayhook is sys.__displayhook__:
        sys.displayhook = _mostra_risultato
''')
print("ok")
