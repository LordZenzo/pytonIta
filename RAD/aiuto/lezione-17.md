# Lezione 17 · Comprehension, lambda e ricorsione

**Obiettivo:** scrivere in poche righe i cicli che costruiscono liste, usare funzioni senza nome e risolvere un problema richiamando la stessa funzione.

## Costruire una lista in una riga

Questo ciclo crea la lista dei quadrati:

```pit
quadrati = []
per n in intervallo_di(1, 6):
    quadrati.aggiungi(n * n)
stampa(quadrati)
```

```output
[1, 4, 9, 16, 25]
```

Si può scrivere in **una riga**, con una *comprehension* (in italiano: «lista per costruzione»):

```pit
quadrati = [n * n per n in intervallo_di(1, 6)]
stampa(quadrati)
```

```output
[1, 4, 9, 16, 25]
```

Si legge da sinistra a destra: «`n * n` **per** ogni `n` **in** `intervallo_di(1, 6)`». Il risultato è identico, ma più corto e più chiaro quando il ciclo fa una cosa sola.

## Con una condizione

Aggiungendo `se` alla fine si tengono solo alcuni elementi:

```pit
numeri = [3, 8, 5, 12, 7, 10]
pari = [n per n in numeri se n % 2 == 0]
stampa(pari)

lunghi = [p per p in ["sole", "luna", "stella", "cielo"] se lunghezza_di(p) > 4]
stampa(lunghi)
```

```output
[8, 12, 10]
['stella', 'cielo']
```

Si può anche **trasformare** ogni elemento:

```pit
nomi = ["anna", "luca", "sara"]
stampa([nome.capitalizza() per nome in nomi])
```

```output
['Anna', 'Luca', 'Sara']
```

> Se la riga diventa lunga o difficile da leggere, usa un normale ciclo `per`: la comprehension serve a **semplificare**, non a stupire.

## Insiemi e dizionari

Con le graffe si costruiscono insiemi e dizionari allo stesso modo:

```pit
parole = ["ciao", "mare", "ciao", "sole", "mare"]
stampa(ordinato_di({p per p in parole}))

lunghezze = {p: lunghezza_di(p) per p in ["ciao", "mare", "stella"]}
stampa(lunghezze)
```

```output
['ciao', 'mare', 'sole']
{'ciao': 4, 'mare': 4, 'stella': 6}
```

## Funzioni senza nome: lambda

Una `lambda` è una piccola funzione scritta in una riga, senza `definisci`:

```pit
raddoppia = lambda x: x * 2
stampa(raddoppia(21))
```

```output
42
```

Il suo uso tipico è dire **come ordinare** o **cosa confrontare**:

```pit
parole = ["pera", "mela", "albicocca", "kiwi"]
stampa(ordinato_di(parole, chiave=lambda p: lunghezza_di(p)))
stampa(massimo_di(parole, chiave=lambda p: lunghezza_di(p)))
```

```output
['pera', 'mela', 'kiwi', 'albicocca']
albicocca
```

`chiave=` riceve la funzione che calcola, per ogni elemento, il valore da confrontare. Con le lambda ci sono anche `filtra` e `mappa_funzione`, ma una comprehension di solito si legge meglio.

## La ricorsione

Una funzione è **ricorsiva** quando richiama se stessa per risolvere un problema più piccolo. Il fattoriale di 4 è `4 × 3 × 2 × 1`; ma anche `4 × (fattoriale di 3)`:

```pit
definisci fattoriale(n):
    se n <= 1:
        ritorna 1
    ritorna n * fattoriale(n - 1)

stampa(fattoriale(5))
```

```output
120
```

Una funzione ricorsiva ha sempre due parti:

1. il **caso base**, dove si ferma (`se n <= 1: ritorna 1`);
2. il **passo ricorsivo**, che si avvicina al caso base (`fattoriale(n - 1)`).

Senza il caso base la funzione non finirebbe mai: Python si ferma da solo dopo circa 1000 chiamate con un errore `ErroreDiRicorsione`.

Ancora un esempio: sommare i numeri di una lista, un elemento alla volta.

```pit
definisci somma_lista(numeri):
    se non numeri:
        ritorna 0
    ritorna numeri[0] + somma_lista(numeri[1:])

stampa(somma_lista([4, 8, 15, 16]))
```

```output
43
```

Ogni problema ricorsivo si può scrivere anche con un ciclo; la ricorsione è comoda quando il problema ha una struttura «a scatole dentro scatole» (cartelle, alberi, espressioni).

## Esercizi

1. Con una comprehension, crea la lista dei cubi dei numeri da 1 a 5.
2. Dalla lista `["Anna", "Bo", "Carlo", "Di"]` tieni solo i nomi di **almeno 3 lettere**, scritti in maiuscolo.
3. Ordina `["b2", "a10", "c1"]` in base al **numero** che segue la lettera (usa `chiave=` e una lambda).
4. Scrivi una funzione ricorsiva `conto_alla_rovescia(n)` che stampa `n`, `n-1`, … fino a 1 e poi `Via!`.

## Soluzioni

```pit
stampa([n ** 3 per n in intervallo_di(1, 6)])
```

```output
[1, 8, 27, 64, 125]
```

```pit
nomi = ["Anna", "Bo", "Carlo", "Di"]
stampa([nome.maiuscolo() per nome in nomi se lunghezza_di(nome) >= 3])
```

```output
['ANNA', 'CARLO']
```

```pit
codici = ["b2", "a10", "c1"]
stampa(ordinato_di(codici, chiave=lambda c: tipo_intero(c[1:])))
```

```output
['c1', 'b2', 'a10']
```

```pit
definisci conto_alla_rovescia(n):
    se n == 0:
        stampa("Via!")
        ritorna
    stampa(n)
    conto_alla_rovescia(n - 1)

conto_alla_rovescia(3)
```

```output
3
2
1
Via!
```
