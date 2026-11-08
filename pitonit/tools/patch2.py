import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

SRC = r'C:\AppPython\pitonit\src'
M = SRC + r'\Modules\main.c'

# ---- main.c ---------------------------------------------------------
sub(M, '''/* --- pymain_run_python() ---------------------------------------- */
''', '''/* --- pitonit: modalita' italiana --------------------------------- */

extern PyObject *_PyItaliano_Builtins(void);
static int pymain_italiano = 0;

static int
pymain_wcs_endswith(const wchar_t *s, const wchar_t *suffix)
{
    size_t n = wcslen(s), m = wcslen(suffix);
    return n >= m && _wcsicmp(s + n - m, suffix) == 0;
}

/* __main__ usa i builtin italiani */
static void
pymain_italianize_main(void)
{
    PyObject *mod = PyImport_AddModuleRef("__main__");
    if (mod == NULL) {
        PyErr_Clear();
        return;
    }
    PyObject *d = PyModule_GetDict(mod);
    PyObject *b = _PyItaliano_Builtins();
    if (b != NULL) {
        PyDict_SetItemString(d, "__builtins__", b);
        Py_DECREF(b);
    }
    else {
        PyErr_Clear();
    }
    Py_DECREF(mod);
}

/* --- pymain_run_python() ---------------------------------------- */
''')

sub(M, '''    PyCompilerFlags cf = _PyCompilerFlags_INIT;
    cf.cf_flags |= PyCF_IGNORE_COOKIE;
    PyObject *result = NULL;
    PyObject *string_obj = PyUnicode_FromString("<string>");''', '''    PyCompilerFlags cf = _PyCompilerFlags_INIT;
    cf.cf_flags |= PyCF_IGNORE_COOKIE;
    if (pymain_italiano) {
        cf.cf_flags |= PyCF_ITALIANO;
    }
    PyObject *result = NULL;
    PyObject *string_obj = PyUnicode_FromString("<string>");''')

sub(M, '''    /* _PyRun_AnyFile(closeit=1) calls fclose(fp) before running code */
    PyCompilerFlags cf = _PyCompilerFlags_INIT;
''', '''    /* _PyRun_AnyFile(closeit=1) calls fclose(fp) before running code */
    PyCompilerFlags cf = _PyCompilerFlags_INIT;
    if (pymain_italiano) {
        cf.cf_flags |= PyCF_ITALIANO;
    }
''')

sub(M, '''    PyCompilerFlags cf = _PyCompilerFlags_INIT;
    PyObject *result = NULL;
    PyObject *stdin_obj = PyUnicode_FromString("<stdin>");''', '''    PyCompilerFlags cf = _PyCompilerFlags_INIT;
    if (pymain_italiano) {
        cf.cf_flags |= PyCF_ITALIANO;
    }
    PyObject *result = NULL;
    PyObject *stdin_obj = PyUnicode_FromString("<stdin>");''')

sub(M, '''    pymain_header(config);

    _PyInterpreterState_SetRunningMain(interp);''', '''    pymain_header(config);

    /* pitonit: italiano per tutto tranne i file .py/.pyw (Python normale) */
    pymain_italiano = !(config->run_filename != NULL &&
                        (pymain_wcs_endswith(config->run_filename, L".py") ||
                         pymain_wcs_endswith(config->run_filename, L".pyw")));
    if (pymain_italiano) {
        pymain_italianize_main();
    }

    _PyInterpreterState_SetRunningMain(interp);''')

# ---- bltinmodule.c : exec/eval + builtin italiani ---------------------
B = SRC + r'\Python\bltinmodule.c'
sub(B, '''/*[clinic input]
exec
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
_italiano_set_builtins(PyObject *globals, int italiano)
{
    int r = PyDict_Contains(globals, &_Py_ID(__builtins__));
    if (r < 0) {
        return -1;
    }
    if (r > 0) {
        return 0;
    }
    PyObject *b = NULL;
    if (italiano) {
        b = _PyItaliano_Builtins();
        if (b == NULL) {
            return -1;
        }
    }
    else {
        b = Py_XNewRef(PyEval_GetBuiltins());
    }
    r = PyDict_SetItem(globals, &_Py_ID(__builtins__), b);
    Py_DECREF(b);
    return r;
}

/*[clinic input]
exec
''')
