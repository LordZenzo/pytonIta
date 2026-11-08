import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

sub(r'C:\AppPython\pitonit\src\Python\preconfig.c', '''    if (config->utf8_mode < 0) {
        config->utf8_mode = 0;
    }
    return _PyStatus_OK();
}''', '''    if (config->utf8_mode < 0) {
        /* pitonit: UTF-8 per impostazione predefinita (accenti, simboli, emoji).
           Si disattiva con -X utf8=0 o PYTHONUTF8=0. */
        config->utf8_mode = 1;
    }
    return _PyStatus_OK();
}''')
print("ok")
