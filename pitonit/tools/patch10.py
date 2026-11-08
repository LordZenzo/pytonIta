import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

sub(r'C:\AppPython\pitonit\src\Parser\pegen.c', '''    PyObject *id = _PyPegen_new_identifier(p, s);
    if (id == NULL) {
        p->error_indicator = 1;''', '''    if ((p->flags & PyPARSE_ITALIANO) &&
        (strcmp(s, "None") == 0 || strcmp(s, "True") == 0 ||
         strcmp(s, "False") == 0)) {
        RAISE_SYNTAX_ERROR_KNOWN_LOCATION(
            t, "nel codice italiano usa Vero, Falso e Nessuno (non True, False, None)");
        return NULL;
    }
    PyObject *id = _PyPegen_new_identifier(p, s);
    if (id == NULL) {
        p->error_indicator = 1;''')
print("ok")
