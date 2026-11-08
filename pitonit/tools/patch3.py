import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

B = r'C:\AppPython\pitonit\src\Python\bltinmodule.c'

sub(B, '''/*[clinic input]
eval as builtin_eval
''', '''/* ---- pitonit: dizionario dei builtin italiani ------------------------ */

static PyObject *_italiano_builtins = NULL;

PyObject *
_PyItaliano_Builtins(void)
{
    if (_italiano_builtins == NULL) {
        PyObject *mod = PyImport_ImportModule("_italiano");
        if (mod == NULL) {
            return NULL;
        }
        PyObject *b = PyObject_GetAttrString(mod, "builtins_italiani");
        Py_DECREF(mod);
        if (b == NULL) {
            return NULL;
        }
        _italiano_builtins = b;
    }
    return Py_NewRef(_italiano_builtins);
}

/* inserisce __builtins__ in globals: italiani se il codice e' italiano */
static int
_italiano_set_builtins(PyObject *globals, PyObject *source)
{
    int r = PyDict_Contains(globals, &_Py_ID(__builtins__));
    if (r != 0) {
        return r < 0 ? -1 : 0;
    }
    int italiano;
    if (PyCode_Check(source)) {
        italiano = (((PyCodeObject *)source)->co_flags & PyCF_ITALIANO) != 0;
    }
    else {
        PyCompilerFlags cf = _PyCompilerFlags_INIT;
        PyEval_MergeCompilerFlags(&cf);
        italiano = (cf.cf_flags & PyCF_ITALIANO) != 0;
    }
    PyObject *b;
    if (italiano) {
        b = _PyItaliano_Builtins();
        if (b == NULL) {
            return -1;
        }
    }
    else {
        b = Py_NewRef(PyEval_GetBuiltins());
    }
    r = PyDict_SetItem(globals, &_Py_ID(__builtins__), b);
    Py_DECREF(b);
    return r;
}

/*[clinic input]
eval as builtin_eval
''')

sub(B, '''    int r = PyDict_Contains(globals, &_Py_ID(__builtins__));
    if (r == 0) {
        r = PyDict_SetItem(globals, &_Py_ID(__builtins__), PyEval_GetBuiltins());
    }
    if (r < 0) {
        goto error;
    }

    if (PyCode_Check(source)) {
        if (PySys_Audit("exec", "O", source) < 0) {''', '''    int r = _italiano_set_builtins(globals, source);
    if (r < 0) {
        goto error;
    }

    if (PyCode_Check(source)) {
        if (PySys_Audit("exec", "O", source) < 0) {''')

sub(B, '''    int r = PyDict_Contains(globals, &_Py_ID(__builtins__));
    if (r == 0) {
        r = PyDict_SetItem(globals, &_Py_ID(__builtins__), PyEval_GetBuiltins());
    }
    if (r < 0) {
        goto error;
    }

    if (closure == Py_None) {''', '''    int r = _italiano_set_builtins(globals, source);
    if (r < 0) {
        goto error;
    }

    if (closure == Py_None) {''')
print("ok")
