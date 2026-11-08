p = r'C:\AppPython\pitonit\src\Include\cpython\compile.h'
s = open(p, newline='').read()
bad = "CO_FUTURE_ANNOTATIONS | " + chr(92) + "n" + "                   PyCF_ITALIANO)"
good = "CO_FUTURE_ANNOTATIONS | " + chr(92) + "\n" + "                   PyCF_ITALIANO)"
assert bad in s
s = s.replace(bad, good)
open(p, 'w', newline='').write(s)
print("ok")
