import re
p = r'C:\AppPython\pitonit\src\Parser\pegen.c'
s = open(p, encoding='latin-1', newline='').read()

# 1) "è" come sequenza di escape UTF-8 nel sorgente C
s = s.replace('{"\u00c3\u00a8", "is"}', r'{"\xc3\xa8", "is"}')

# 2) switch/while con i caratteri di escape corretti
a = s.index("    const char *q = new_token->end;")
b = s.index("    return 1;\r\n}", a)
nuovo = (
    "    const char *q = new_token->end;\r\n"
    "    while (*q == ' ' || *q == '\\t') {\r\n"
    "        q++;\r\n"
    "    }\r\n"
    "    switch (*q) {\r\n"
    "        case '\\0': case '\\n': case '\\r': case '=': case ',': case ')':\r\n"
    "        case ']': case '}': case ':': case '.': case ';': case '#': case '\\\\':\r\n"
    "            return 0;\r\n"
    "    }\r\n"
)
s = s[:a] + nuovo + s[b:]
open(p, 'w', encoding='latin-1', newline='').write(s)
print("fatto", s.count('\x00'))
