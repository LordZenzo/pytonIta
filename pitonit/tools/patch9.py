import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

M = r'C:\AppPython\pitonit\src\Modules\main.c'
sub(M, '''    if (pymain_italiano) {
        cf.cf_flags |= PyCF_ITALIANO;
    }
    PyObject *result = NULL;
    PyObject *string_obj = PyUnicode_FromString("<string>");''', '''    if (pymain_italiano) {
        cf.cf_flags |= PyCF_ITALIANO;
        /* -c: se il testo non e' italiano valido ma e' Python valido (come il
           codice inglese che pip, subprocess e multiprocessing passano a -c),
           lo si esegue come Python normale. */
        PyObject *prova = Py_CompileStringExFlags(PyBytes_AsString(bytes),
                                                  "<string>", Py_file_input,
                                                  &cf, -1);
        if (prova != NULL) {
            Py_DECREF(prova);
        }
        else {
            PyObject *exc = PyErr_GetRaisedException();
            PyCompilerFlags cf_en = _PyCompilerFlags_INIT;
            cf_en.cf_flags |= PyCF_IGNORE_COOKIE;
            PyObject *prova_en = Py_CompileStringExFlags(PyBytes_AsString(bytes),
                                                         "<string>", Py_file_input,
                                                         &cf_en, -1);
            if (prova_en != NULL) {
                Py_DECREF(prova_en);
                Py_DECREF(exc);
                cf.cf_flags &= ~PyCF_ITALIANO;
            }
            else {
                PyErr_Clear();
                PyErr_SetRaisedException(exc);
                PyErr_Clear();    /* l'errore verra' ripresentato da _PyRun_SimpleString */
            }
        }
    }
    PyObject *result = NULL;
    PyObject *string_obj = PyUnicode_FromString("<string>");''')
print("ok")
