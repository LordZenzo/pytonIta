import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

SRC = r'C:\AppPython\pitonit\src'

# ---- identificatori speciali (__inizializza__ -> __init__) -------------
sub(SRC + r'\Parser\pegen.c', '''_PyPegen_new_identifier(Parser *p, const char *n)
{
    PyObject *id = PyUnicode_DecodeUTF8(n, strlen(n), NULL);''', '''_PyPegen_new_identifier(Parser *p, const char *n)
{
    if ((p->flags & PyPARSE_ITALIANO) && n[0] == '_' && n[1] == '_') {
        for (int i = 0; it_dunders[i][0] != NULL; i++) {
            if (strcmp(it_dunders[i][0], n) == 0) {
                n = it_dunders[i][1];
                break;
            }
        }
    }
    PyObject *id = PyUnicode_DecodeUTF8(n, strlen(n), NULL);''')

sub(SRC + r'\Parser\pegen.c', '''static const char *const it_soft_keywords[][2] = {''', '''/* metodi speciali: __inizializza__ -> __init__ ecc. */
static const char *const it_dunders[][2] = {
    {"__inizializza__", "__init__"}, {"__nuovo__", "__new__"},
    {"__elimina__", "__del__"}, {"__testo__", "__str__"},
    {"__rappresentazione__", "__repr__"}, {"__lunghezza__", "__len__"},
    {"__ottieni_elemento__", "__getitem__"},
    {"__imposta_elemento__", "__setitem__"},
    {"__elimina_elemento__", "__delitem__"},
    {"__contiene__", "__contains__"}, {"__iterazione__", "__iter__"},
    {"__prossimo__", "__next__"}, {"__chiama__", "__call__"},
    {"__entra__", "__enter__"}, {"__esci__", "__exit__"},
    {"__uguale__", "__eq__"}, {"__diverso__", "__ne__"},
    {"__minore__", "__lt__"}, {"__minore_uguale__", "__le__"},
    {"__maggiore__", "__gt__"}, {"__maggiore_uguale__", "__ge__"},
    {"__somma__", "__add__"}, {"__sottrazione__", "__sub__"},
    {"__moltiplicazione__", "__mul__"}, {"__divisione__", "__truediv__"},
    {"__divisione_intera__", "__floordiv__"}, {"__modulo__", "__mod__"},
    {"__potenza__", "__pow__"}, {"__negativo__", "__neg__"},
    {"__booleano__", "__bool__"}, {"__intero__", "__int__"},
    {"__decimale__", "__float__"}, {"__nome__", "__name__"},
    {"__documentazione__", "__doc__"}, {"__classe__", "__class__"},
    {"__dizionario__", "__dict__"}, {"__tutto__", "__all__"},
    {"__ottieni_attributo__", "__getattr__"},
    {"__imposta_attributo__", "__setattr__"},
    {NULL, NULL}
};

static const char *const it_soft_keywords[][2] = {''')

# ---- importlib: .pit e flag italiano ------------------------------------
IB = SRC + r'\Lib\importlib\_bootstrap_external.py'
sub(IB, "SOURCE_SUFFIXES = ['.py']", "SOURCE_SUFFIXES = ['.py', '.pit']")
sub(IB, '''        return _bootstrap._call_with_frames_removed(compile, data, path, 'exec',
                                        dont_inherit=True, optimize=_optimize)''', '''        # pitonit: i file .pit usano le parole chiave italiane (PyCF_ITALIANO)
        flags = 0x10000 if str(path).endswith('.pit') else 0
        return _bootstrap._call_with_frames_removed(compile, data, path, 'exec',
                                        flags=flags, dont_inherit=True,
                                        optimize=_optimize)''')

# ---- codeop: la console interattiva e' italiana -------------------------
CO = SRC + r'\Lib\codeop.py'
sub(CO, "        self.flags = PyCF_DONT_IMPLY_DEDENT | PyCF_ALLOW_INCOMPLETE_INPUT\n",
        "        # pitonit: 0x10000 = PyCF_ITALIANO (parole chiave italiane)\n"
        "        self.flags = PyCF_DONT_IMPLY_DEDENT | PyCF_ALLOW_INCOMPLETE_INPUT | 0x10000\n")
print("ok")
