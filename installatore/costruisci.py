"""Costruisce l'installatore di pytonIta: pacchetti compressi + Installa_pytonIta.exe (PyInstaller).

Uso:  python costruisci.py [--solo-pacchetti]
"""
import os
import shutil
import subprocess
import sys
import zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
PITONIT = os.path.join(RADICE, "pitonit", "installazione")
STRUMENTI = os.path.join(RADICE, "pitonit", "tools")
RAD = os.path.join(RADICE, "RAD")
PACCHETTI = os.path.join(QUI, "pacchetti")
SP = os.path.join("Lib", "site-packages")

# pacchetti "scientifici": componente facoltativo (numpy, pandas, scipy, matplotlib e dipendenze)
SCIENTIFICI = ["numpy", "numpy.libs", "scipy", "scipy.libs", "pandas", "pandas.libs", "matplotlib", "mpl_toolkits",
               "fontTools", "contourpy", "kiwisolver", "cycler", "pyparsing", "dateutil", "tzdata", "pylab.py"]
DIST_SCIENTIFICI = ("numpy-", "scipy-", "pandas-", "matplotlib-", "fonttools-", "contourpy-", "kiwisolver-", "cycler-",
                    "pyparsing-", "python_dateutil-", "tzdata-")
ESCLUDI_RAD = ("tests", "__pycache__", "docs")


def e_scientifico(rel):
    rel = rel.replace("\\", "/")
    pre = SP.replace("\\", "/") + "/"
    if not rel.startswith(pre):
        return False
    nome = rel[len(pre):].split("/")[0]
    return nome in SCIENTIFICI or (nome.endswith(".dist-info") and nome.startswith(DIST_SCIENTIFICI))


def file_di(base):
    for cartella, sottocartelle, nomi in os.walk(base):
        sottocartelle[:] = [d for d in sottocartelle if d != "__pycache__"]
        for n in nomi:
            if n.endswith((".pyc", ".log")) and "__pycache__" in cartella:
                continue
            percorso = os.path.join(cartella, n)
            yield percorso, os.path.relpath(percorso, base)


def scrivi(zf, percorso, nome_in_zip):
    zf.write(percorso, nome_in_zip.replace("\\", "/"))


def versione_base():
    """Legge PRINCIPALE.MODIFICHE da RAD/rad/__init__.pit (unica fonte)."""
    import re
    testo = open(os.path.join(RAD, "rad", "__init__.pit"), encoding="utf-8").read()
    return re.search(r'VERSIONE_BASE = "([\d.]+)"', testo).group(1)


def versione_completa():
    """1.1.<versione di Python di pitonit>, es. 1.1.3.13.18"""
    r = subprocess.run([os.path.join(PITONIT, "pitonit.exe"), "-c", "importa sys; stampa('.'.join(testo(x) per x in sys.version_info[:3]))"],
                       capture_output=True, text=True, encoding="utf-8")
    return versione_base() + "." + r.stdout.strip()


def scrivi_versione():
    v = versione_completa()
    with open(os.path.join(QUI, "_versione.py"), "w", encoding="utf-8") as f:
        f.write(f'VERSIONE = "{v}"' + chr(10))
    numeri = (v.split(".") + ["0"] * 4)[:4]
    righe = ['1 ICON "rad.ico"', '1 VERSIONINFO', 'FILEVERSION ' + ",".join(numeri), 'PRODUCTVERSION ' + ",".join(numeri),
             'BEGIN', ' BLOCK "StringFileInfo"', ' BEGIN', '  BLOCK "041004b0"', '  BEGIN',
             '   VALUE "ProductName", "PitStudio"', '   VALUE "FileDescription", "PitStudio - ambiente di sviluppo per pytonIta"',
             f'   VALUE "FileVersion", "{v}"', f'   VALUE "ProductVersion", "{v}"', '  END', ' END',
             ' BLOCK "VarFileInfo"', ' BEGIN', '  VALUE "Translation", 0x410, 1200', ' END', 'END']
    with open(os.path.join(QUI, "rad.rc"), "w", encoding="utf-8") as f:
        f.write(chr(10).join(righe) + chr(10))
    print("Versione:", v)
    return v


def costruisci_pacchetti():
    os.makedirs(PACCHETTI, exist_ok=True)
    core = os.path.join(PACCHETTI, "pitonit.zip")
    sci = os.path.join(PACCHETTI, "scientifiche.zip")
    rad = os.path.join(PACCHETTI, "rad.zip")
    n_core = n_sci = 0
    with zipfile.ZipFile(core, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zc, \
            zipfile.ZipFile(sci, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zs:
        for percorso, rel in file_di(PITONIT):
            if rel in ("registra_pit.cmd", "annulla_registrazione_pit.cmd"):
                continue
            if e_scientifico(rel):
                scrivi(zs, percorso, "pitonit/" + rel)
                n_sci += 1
            else:
                scrivi(zc, percorso, "pitonit/" + rel)
                n_core += 1
        for nome in ("py2pit.py", "tipi_ast.pit", "pit2py.py", "pit2py_tabelle.py", "pit2py_progetto.py"):
            scrivi(zc, os.path.join(STRUMENTI, nome), "pitonit/tools/" + nome)
        scrivi(zc, os.path.join(RADICE, "pitonit", "src", "LICENSE"), "pitonit/LICENSE_CPython.txt")
        scrivi(zc, os.path.join(RADICE, "LICENSE"), "pitonit/LICENSE_pytonIta.txt")
        for nome in ("README.md", "ELENCO_LIBRERIE.md"):
            scrivi(zc, os.path.join(RADICE, "pitonit", nome), "pitonit/" + nome)
    n_rad = 0
    with zipfile.ZipFile(rad, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zr:
        for percorso, rel in file_di(RAD):
            if rel.split(os.sep)[0] in ESCLUDI_RAD or rel in ("correggi23.py", "PitStudio.exe", "PitStudio.cmd"):
                continue
            scrivi(zr, percorso, "PitStudio/" + rel)
            n_rad += 1
        scrivi(zr, os.path.join(QUI, "PitStudio.exe"), "PitStudio.exe")     # l'exe sta nella radice, accanto a pitonit        # le immagini della guida sono utili: docs è esclusa, aiuto\immagini è già inclusa
    for z, n in ((core, n_core), (sci, n_sci), (rad, n_rad)):
        print(f"{os.path.basename(z):22} {n:6} file  {os.path.getsize(z) / 1e6:7.1f} MB")


def costruisci_exe():
    for cartella in ("build", "dist"):
        shutil.rmtree(os.path.join(QUI, cartella), ignore_errors=True)
    comando = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--windowed",
               "--name", "Installa_pytonIta", "--icon", os.path.join(QUI, "rad.ico"),
               "--add-data", PACCHETTI + os.pathsep + "pacchetti",
               "--add-data", os.path.join(QUI, "rad.ico") + os.pathsep + ".",
               "--add-data", os.path.join(QUI, "pitonit.ico") + os.pathsep + ".",
               "--distpath", os.path.join(QUI, "dist"), "--workpath", os.path.join(QUI, "build"),
               "--specpath", os.path.join(QUI, "build"),
               os.path.join(QUI, "installatore.py")]
    subprocess.check_call(comando, cwd=QUI)
    print("Creato:", os.path.join(QUI, "dist", "Installa_pytonIta.exe"))


if __name__ == "__main__":
    scrivi_versione()
    subprocess.check_call([os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "cmd.exe"), "/c",
                           os.path.join(QUI, "build_exe.cmd")], cwd=QUI)
    try:
        shutil.copy(os.path.join(QUI, "PitStudio.exe"), os.path.join(RAD, "PitStudio.exe"))
    except PermissionError:
        print("Nota: RAD\PitStudio.exe è in uso (PitStudio aperto): la copia di sviluppo non è stata aggiornata; il pacchetto usa quella appena compilata.")
    costruisci_pacchetti()
    if "--solo-pacchetti" not in sys.argv:
        costruisci_exe()
