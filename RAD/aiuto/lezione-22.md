# Lezione 22 · Moduli e pacchetti

**Obiettivo:** dividere un programma grande in **più file** e usare le librerie scritte da altri.

## Un modulo è un file

Finora hai scritto programmi in un file solo. Quando il programma cresce, conviene mettere le funzioni che vanno insieme in un file a parte: un **modulo**. Ogni file `.pit` è già un modulo.

Immagina due file nella stessa cartella. Il primo, `geometria.pit`, contiene le funzioni:

```pit sintassi
"""Piccole funzioni di geometria."""
PI_GRECO = 3.14159

definisci area_cerchio(raggio):
    ritorna PI_GRECO * raggio ** 2

definisci area_rettangolo(base, altezza):
    ritorna base * altezza
```

Il secondo, `principale.pit`, le usa:

```pit sintassi
importa geometria

stampa(geometria.area_cerchio(2))
stampa(geometria.area_rettangolo(3, 4))
```

Lanciando `principale.pit` compare:

```esempio
12.56636
12
```

- `importa geometria` carica il file `geometria.pit` (senza l'estensione);
- poi si usa `nome_modulo.cosa`: `geometria.area_cerchio(2)`.

> Il nome del file diventa il nome del modulo: scegli nomi **senza spazi e senza accenti**, con lettere minuscole e il trattino basso (`gestione_clienti.pit`). Non chiamare un tuo file come una libreria che ti serve (un file `casuale.pit` nasconderebbe il modulo `casuale`).

## Tre modi di importare

```pit sintassi
importa geometria                         # si scrive geometria.area_cerchio(...)
da geometria importa area_rettangolo      # si scrive solo area_rettangolo(...)
importa geometria come geo                # nome più corto: geo.area_cerchio(...)
```

- usare `importa modulo` rende chiaro **da dove** arriva ogni funzione: è la scelta più sicura;
- `da modulo importa nome` accorcia, ma due moduli con la stessa funzione si «pestano i piedi»;
- evita `da modulo importa *`: non si capisce più cosa arriva da dove.

## Il codice che parte solo se lanci il file

Dentro un modulo si può mettere del codice di prova. Se però lo lasci scoperto, parte anche quando **un altro file** importa il modulo. Per evitarlo si usa questa formula:

```pit
definisci saluta(nome):
    ritorna f"Ciao, {nome}!"

se __nome__ == "__main__":
    stampa("prova del modulo:")
    stampa(saluta("Anna"))
```

```output
prova del modulo:
Ciao, Anna!
```

`__nome__` vale `"__main__"` soltanto quando il file è quello lanciato direttamente. Se lo importi da altrove, vale il nome del modulo e il blocco `se` viene saltato. È una convenzione che troverai in quasi tutti i programmi.

## Un pacchetto è una cartella

Quando i moduli sono molti li metti in una **cartella**: il **pacchetto**. Dentro ci va un file `__init__.pit` (può essere vuoto): dice a Python che quella cartella è un pacchetto.

```esempio
mio_progetto/
    principale.pit
    utili/
        __init__.pit
        testi.pit
        numeri.pit
```

```pit sintassi
da utili.testi importa titolo
da utili importa numeri
```

Il punto separa la cartella dal file: `utili.testi` è il file `utili/testi.pit`.

## Le librerie che ci sono già

Non devi scrivere tutto: pytonIta include oltre cento librerie con nomi italiani, per esempio:

```pit
importa casuale
importa matematica

casuale.imposta_seme(42)
stampa(casuale.intero_casuale(1, 6) in [1, 2, 3, 4, 5, 6])
stampa(matematica.radice_quadrata(81))
stampa(matematica.pigreco)
```

```output
Vero
9.0
3.141592653589793
```

Ogni libreria ha il suo elenco di funzioni nella guida (pagina [Le librerie in italiano](#librerie)), e nell'editor basta scrivere `casuale.` e premere **Ctrl+Spazio** per vedere i nomi disponibili.

## Le librerie degli altri

Il mondo Python ha migliaia di librerie in più (grafici, giochi, intelligenza artificiale…). Si scaricano con `pip`, il programma di installazione dei pacchetti. In PitStudio non serve il terminale: il pannello **Pip** (la linguetta a sinistra) cerca, installa e toglie i pacchetti, **per il progetto** o per tutti. Dopo l'installazione basta `importa nome_libreria`.

Se una libreria esterna manca, vedrai un errore chiaro:

```pit errore
importa libreria_che_non_esiste
```

```output
Traceback (ultima chiamata per ultima):
  File "prova.pit", riga 1, in <module>
ErroreDiImportazione: No module named 'libreria_che_non_esiste'
```

Il pannello **Librerie**, invece, serve per le librerie incluse con pytonIta (le «scientifiche» come numpy e matplotlib, o le librerie italiane online): le trovi spiegate nella [pagina Librerie](#librerie).

## Esercizi

1. Crea un file `saluti.pit` con le funzioni `buongiorno(nome)` e `buonasera(nome)`, poi un file `principale.pit` che le usa entrambe.
2. Nel modulo `saluti`, aggiungi un blocco `se __nome__ == "__main__":` con una prova veloce. Verifica che **non** parta quando importi il modulo.
3. Sposta `saluti.pit` dentro una cartella `cortesie/` (con `__init__.pit`) e cambia l'`importa` di conseguenza.

## Soluzioni

```pit sintassi
# saluti.pit
definisci buongiorno(nome):
    ritorna f"Buongiorno, {nome}!"

definisci buonasera(nome):
    ritorna f"Buonasera, {nome}!"

se __nome__ == "__main__":
    stampa(buongiorno("prova"))
```

```pit sintassi
# principale.pit
importa saluti

stampa(saluti.buongiorno("Anna"))
stampa(saluti.buonasera("Luca"))
```

Lanciando `principale.pit` compaiono **due** righe (la prova nel modulo non parte):

```esempio
Buongiorno, Anna!
Buonasera, Luca!
```

Con la cartella `cortesie/` (e il file vuoto `cortesie/__init__.pit`) l'import diventa:

```pit sintassi
da cortesie importa saluti
# oppure
da cortesie.saluti importa buongiorno
```
