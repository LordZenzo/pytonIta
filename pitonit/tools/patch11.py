import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

sub(r'C:\AppPython\pitonit\src\Python\symtable.c', '''            _PyUnicode_EqualToASCIIString(e->v.Name.id, "super")) {''',
    '''            (_PyUnicode_EqualToASCIIString(e->v.Name.id, "super") ||
             _PyUnicode_EqualToASCIIString(e->v.Name.id, "genitore"))) {''')
print("ok")
