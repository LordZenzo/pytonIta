"""Crea l'installazione separata di pitonit in C:\\AppPython\\pitonit\\installazione.

Conserva Lib\\site-packages e Scripts (pip e le librerie installate in pitonit).
"""
import glob
import os
import shutil
import tempfile

RADICE = r'C:\AppPython\pitonit'
SRC = os.path.join(RADICE, 'src')
BUILD = os.path.join(SRC, 'PCbuild', 'amd64')
DEST = os.path.join(RADICE, 'installazione')
TCL = os.path.join(SRC, 'externals', 'tcltk-8.6.15.0', 'amd64', 'lib')

ESCLUDI_LIB = {'test', 'tests', 'idlelib', 'turtledemo', '__pycache__',
               'lib2to3', 'site-packages'}

# conserva pip e le librerie gia' installate
parcheggio = tempfile.mkdtemp()
for sotto in (os.path.join('Lib', 'site-packages'), 'Scripts'):
    p = os.path.join(DEST, sotto)
    if os.path.isdir(p):
        shutil.move(p, os.path.join(parcheggio, sotto.replace(os.sep, '_')))
if os.path.isdir(DEST):
    try:
        shutil.rmtree(DEST)
    except OSError:
        # una shell aperta dentro installazione blocca la cartella: rimetti tutto a posto
        for nome in os.listdir(parcheggio):
            dest_ = os.path.join(DEST, 'Lib', 'site-packages') if nome == 'Lib_site-packages'                 else os.path.join(DEST, nome)
            os.makedirs(os.path.dirname(dest_), exist_ok=True)
            shutil.move(os.path.join(parcheggio, nome), dest_)
        raise SystemExit('ERRORE: installazione in uso (chiudi le shell aperte dentro). '
                         'pip e librerie sono state ripristinate.')
os.makedirs(os.path.join(DEST, 'DLLs'))
os.makedirs(os.path.join(DEST, 'Lib'))
sp = os.path.join(parcheggio, 'Lib_site-packages')
shutil.move(sp, os.path.join(DEST, 'Lib', 'site-packages')) if os.path.isdir(sp) \
    else os.makedirs(os.path.join(DEST, 'Lib', 'site-packages'))
sc = os.path.join(parcheggio, 'Scripts')
if os.path.isdir(sc):
    shutil.move(sc, os.path.join(DEST, 'Scripts'))
shutil.rmtree(parcheggio, ignore_errors=True)


def copia(src, dst):
    shutil.copy2(src, dst)


copia(os.path.join(BUILD, 'python.exe'), os.path.join(DEST, 'pitonit.exe'))
copia(os.path.join(BUILD, 'pythonw.exe'), os.path.join(DEST, 'pitonitw.exe'))
for nome in ('python313.dll', 'python3.dll', 'vcruntime140.dll', 'vcruntime140_1.dll'):
    p = os.path.join(BUILD, nome)
    if os.path.exists(p):
        copia(p, DEST)

for p in glob.glob(os.path.join(BUILD, '*.pyd')) + glob.glob(os.path.join(BUILD, '*.dll')):
    nome = os.path.basename(p)
    if nome.lower() in ('python313.dll', 'python3.dll', 'vcruntime140.dll',
                        'vcruntime140_1.dll', 'pyshellext.dll'):
        continue
    if nome.startswith('_test') or nome.startswith('xx'):
        continue
    copia(p, os.path.join(DEST, 'DLLs'))


def ignora(cartella, contenuti):
    return [c for c in contenuti if c in ESCLUDI_LIB or c.endswith('.pyc')]


for voce in os.listdir(os.path.join(SRC, 'Lib')):
    if voce in ESCLUDI_LIB:
        continue
    s = os.path.join(SRC, 'Lib', voce)
    d = os.path.join(DEST, 'Lib', voce)
    if os.path.isdir(s):
        shutil.copytree(s, d, ignore=ignora)
    else:
        copia(s, d)

# Tcl/Tk per tkinter
for cart in ('tcl8', 'tcl8.6', 'tk8.6', 'dde1.4', 'reg1.3'):
    s = os.path.join(TCL, cart)
    if os.path.isdir(s):
        shutil.copytree(s, os.path.join(DEST, 'tcl', cart))

# Ignora PYTHONHOME/PYTHONPATH/registro e il site utente di Python
for exe in ('pitonit', 'pitonitw'):
    with open(os.path.join(DEST, exe + '._pth'), 'w', encoding='utf-8') as f:
        f.write('python313.zip\n.\nLib\nDLLs\nLib\\site-packages\nimport site\n')

for p in glob.glob(os.path.join(RADICE, 'extra', '*')):
    copia(p, DEST)
shutil.copytree(os.path.join(RADICE, 'esempi'), os.path.join(DEST, 'esempi'))
print('installato in', DEST)
