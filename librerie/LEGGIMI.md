# Librerie di pytonIta

Questa cartella è la «zona librerie» del repository: i moduli italiani con un indice che PitStudio legge per installarli e aggiornarli
(pannello **Librerie → ⟳ Novità**, vedi `RAD/aiuto/aggiornamenti.md`).

```
librerie/
  indice.json              elenco: nome, versione, categoria, descrizione, file con impronta SHA-256
  moduli/                  i file (.py): moduli singoli (matematica.py) o pacchetti (interfaccia/__init__.py, …)
  costruisci_indice.py     copia i moduli dal runtime e riscrive indice.json
```

I file di `moduli/` sono una **copia** dei moduli italiani del runtime (`pitonit/installazione/Lib`, generati da `pitonit/tools/genera_moduli.py`).
Per aggiornarla dopo una modifica:

```
python librerie/costruisci_indice.py
```

La versione di una libreria sale da sola (1.0 → 1.1) quando i suoi file cambiano. Poi `git add librerie` e commit: PitStudio vede la novità
quando legge `https://raw.githubusercontent.com/LordZenzo/pytonIta/main/librerie/indice.json`.

## Regole

- Solo file `.py`, con percorsi relativi e senza `..`: PitStudio scarta quelli che non lo rispettano.
- Un pacchetto va scritto con **tutti** i suoi file nell'indice: viene installato intero.
- Il nome di una libreria è un nome Python valido (`[a-z_]`), uguale al modulo o alla cartella.
- Il campo `formato` di `indice.json` è 1: se un giorno cambia la struttura, le versioni vecchie di PitStudio lo rifiutano senza rompersi.
- Aggiungere una libreria nuova: metti il file in `moduli/`, aggiungi una riga al `CATALOGO` di `RAD/rad/librerie.pit` (categoria e descrizione)
  e rilancia lo script.

Per provare senza pubblicare, punta PitStudio a una cartella locale: variabile d'ambiente `PITSTUDIO_LIBRERIE_ORIGINE=file:///C:/percorso/librerie/`.
