import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

B = r'C:\AppPython\pitonit\src\Python\bltinmodule.c'

sub(B, '''static PyMethodDef builtin_methods[] = {
    {"__build_class__", _PyCFunction_CAST(builtin___build_class__),
     METH_FASTCALL | METH_KEYWORDS, build_class_doc},
''', '''/* pitonit: _aggiungi_alias(tipo, nome_inglese, nome_italiano)
   Aggiunge al dizionario del tipo un secondo nome per un attributo gia'
   esistente (es. list.append -> list.aggiungi). Restituisce True se fatto. */
static PyObject *
builtin__aggiungi_alias(PyObject *module, PyObject *args)
{
    PyObject *tipo, *en, *it;
    if (!PyArg_ParseTuple(args, "OUU", &tipo, &en, &it)) {
        return NULL;
    }
    if (!PyType_Check(tipo)) {
        PyErr_SetString(PyExc_TypeError, "serve un tipo");
        return NULL;
    }
    PyObject *dict = PyType_GetDict((PyTypeObject *)tipo);
    if (dict == NULL) {
        Py_RETURN_FALSE;
    }
    PyObject *valore = PyDict_GetItemWithError(dict, en);
    if (valore == NULL) {
        Py_DECREF(dict);
        if (PyErr_Occurred()) {
            return NULL;
        }
        Py_RETURN_FALSE;
    }
    PyObject *nome = Py_NewRef(it);
    PyUnicode_InternInPlace(&nome);
    int r = PyDict_SetItem(dict, nome, valore);
    Py_DECREF(nome);
    Py_DECREF(dict);
    if (r < 0) {
        return NULL;
    }
    PyType_Modified((PyTypeObject *)tipo);
    Py_RETURN_TRUE;
}

static PyMethodDef builtin_methods[] = {
    {"__build_class__", _PyCFunction_CAST(builtin___build_class__),
     METH_FASTCALL | METH_KEYWORDS, build_class_doc},
    {"_aggiungi_alias", builtin__aggiungi_alias, METH_VARARGS,
     "pitonit: aggiunge un nome italiano a un attributo di un tipo."},
''')
print("ok")
