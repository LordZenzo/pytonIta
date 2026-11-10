"""Costruisce la zona delle librerie del repository: copia in librerie/moduli/ i moduli italiani del runtime
e scrive librerie/indice.json (nome, versione, categoria, descrizione, file con impronta SHA-256).

Uso (con un Python qualsiasi):
    python librerie/costruisci_indice.py [cartella_Lib_del_runtime]

La versione di una libreria sale (1.0 -> 1.1 ...) da sola quando i suoi file cambiano rispetto all'indice precedente.
"""
import ast
import hashlib
import json
import os
import re
import shutil
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
LIB_PREDEFINITA = os.path.join(RADICE, "pitonit", "installazione", "Lib")
MODULI = os.path.join(QUI, "moduli")
INDICE = os.path.join(QUI, "indice.json")
FORMATO = 1


def sha(percorso):
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def catalogo():
    """CATALOGO di RAD/rad/librerie.pit: modulo -> (categoria, descrizione)."""
    testo = open(os.path.join(RADICE, "RAD", "rad", "librerie.pit"), encoding="utf-8").read()
    m = re.search(r"^CATALOGO = (\{.*?^\})", testo, re.S | re.M)
    return ast.literal_eval(m.group(1))


def nomi_italiani(lib):
    sys.path.insert(0, lib)
    import _mappa_moduli
    sys.path.pop(0)
    return sorted({v.split(".")[0] for v in _mappa_moduli.MAPPA.values()}), _mappa_moduli.MAPPA


def file_di(lib, nome):
    """I file .py di una libreria (percorsi relativi, con /)."""
    semplice = os.path.join(lib, nome + ".py")
    if os.path.isfile(semplice):
        return [nome + ".py"]
    cartella = os.path.join(lib, nome)
    trovati = []
    for dirpath, dirnomi, filenomi in os.walk(cartella):
        dirnomi[:] = [d for d in dirnomi if d != "__pycache__"]
        for f in filenomi:
            if f.endswith(".py"):
                trovati.append(os.path.relpath(os.path.join(dirpath, f), lib).replace(os.sep, "/"))
    return sorted(trovati)


def main():
    lib = sys.argv[1] if len(sys.argv) > 1 else LIB_PREDEFINITA
    nomi, mappa = nomi_italiani(lib)
    cat = catalogo()
    vecchio = {}
    if os.path.isfile(INDICE):
        for voce in json.load(open(INDICE, encoding="utf-8")).get("librerie", []):
            vecchio[voce["nome"]] = voce
    originali = {}
    for orig, it in mappa.items():
        originali.setdefault(it.split(".")[0], orig.split(".")[0])
    voci = []
    mancanti = []
    for nome in nomi:
        elenco = file_di(lib, nome)
        if not elenco:
            mancanti.append(nome)
            continue
        file_ = []
        for rel in elenco:
            dest = os.path.join(MODULI, *rel.split("/"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(os.path.join(lib, *rel.split("/")), dest)
            file_.append({"percorso": rel, "sha256": sha(dest)})
        categoria, descrizione = cat.get(nome, ("Altre", "Libreria italiana di %s." % originali.get(nome, nome)))
        versione = "1.0"
        prima = vecchio.get(nome)
        if prima:
            versione = prima["versione"]
            if [(f["percorso"], f["sha256"]) for f in prima["file"]] != [(f["percorso"], f["sha256"]) for f in file_]:
                maggiore, minore = versione.split(".")
                versione = "%s.%d" % (maggiore, int(minore) + 1)
        voci.append({"nome": nome, "versione": versione, "categoria": categoria, "descrizione": descrizione,
                     "originale": originali.get(nome, nome), "file": file_})
    json.dump({"formato": FORMATO, "librerie": voci}, open(INDICE, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)
    print("librerie:", len(voci), "file:", sum(len(v["file"]) for v in voci), "mancanti:", mancanti)


main()
