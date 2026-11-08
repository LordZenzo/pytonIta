# Lezione 6 · Le liste

**Obiettivo:** tenere insieme molti valori in un'unica variabile.

## Creare una lista

Una **lista** si scrive tra parentesi quadre, con i valori separati da virgole:

```pit
frutta = ["mela", "pera", "banana"]
numeri = [4, 8, 15, 16, 23, 42]
stampa(frutta)
stampa(lunghezza(numeri))
```

```output
['mela', 'pera', 'banana']
6
```

`lunghezza(lista)` dice quanti elementi ci sono.

## Leggere un elemento

Gli elementi si contano **da zero**: il primo è il numero 0. Con numeri negativi si parte dal fondo.

```pit
frutta = ["mela", "pera", "banana"]
stampa(frutta[0])
stampa(frutta[2])
stampa(frutta[-1])
stampa(frutta[0:2])
```

```output
mela
banana
banana
['mela', 'pera']
```

`frutta[0:2]` è una **fetta**: dall'elemento 0 fino al 2 escluso.

## Modificare

```pit
spesa = ["pane", "latte"]
spesa.aggiungi("uova")
spesa.inserisci(0, "caffè")
spesa.rimuovi("latte")
spesa[1] = "focaccia"
stampa(spesa)
ultimo = spesa.estrai()
stampa(ultimo, "->", spesa)
```

```output
['caffè', 'focaccia', 'uova']
uova -> ['caffè', 'focaccia']
```

| Metodo | Cosa fa |
|---|---|
| `aggiungi(x)` | aggiunge in fondo |
| `inserisci(posizione, x)` | inserisce in un punto |
| `rimuovi(x)` | toglie il valore `x` |
| `estrai()` | toglie e restituisce l'ultimo |
| `ordina()` | ordina la lista |
| `inverti()` | la rovescia |

## Scorrere una lista

```pit
voti = [7, 9, 6, 8]
totale = 0
per voto in voti:
    totale += voto
stampa("Somma:", totale)
stampa("Media:", somma(voti) / lunghezza(voti))
stampa("Massimo:", massimo(voti), "Minimo:", minimo(voti))
```

```output
Somma: 30
Media: 7.5
Massimo: 9 Minimo: 6
```

`somma`, `massimo` e `minimo` lavorano direttamente sulle liste. Per avere anche la posizione si usa `enumera`:

```pit
nomi = ["Anna", "Luca", "Sara"]
per posizione, nome in enumera(nomi, 1):
    stampa(f"{posizione}. {nome}")
```

```output
1. Anna
2. Luca
3. Sara
```

## Ordinare e cercare

```pit
numeri = [5, 2, 9, 1]
stampa(ordinato(numeri))
stampa(ordinato(numeri, inverso=Vero))
stampa(9 in numeri)
stampa(numeri.indice(9))
numeri.ordina()
stampa(numeri)
```

```output
[1, 2, 5, 9]
[9, 5, 2, 1]
Vero
2
[1, 2, 5, 9]
```

`ordinato(...)` crea una **nuova** lista; `lista.ordina()` cambia quella esistente.

## Liste costruite al volo

```pit
quadrati = [n * n per n in intervallo(1, 6)]
pari = [n per n in intervallo(20) se n % 2 == 0]
stampa(quadrati)
stampa(pari)
```

```output
[1, 4, 9, 16, 25]
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

Si chiama *comprensione di lista*: «n·n per ogni n…». Se non ti è chiara ora, torna a guardarla più tardi.

## Esercizi

1. Crea la lista dei tuoi 5 film preferiti e stampala numerata.
2. Dati i numeri `[3, 8, 1, 9, 4]` stampa il maggiore **senza** usare `massimo` (usa un ciclo).
3. Elimina da `[1, 2, 2, 3, 3, 3]` i doppioni, ottenendo `[1, 2, 3]` (suggerimento: controlla con `in`).
4. Crea la lista dei multipli di 5 da 5 a 50 con `intervallo`.

## Soluzioni

```pit
film = ["Alien", "Up", "Coco", "Heat", "Fargo"]
per n, titolo in enumera(film, 1):
    stampa(f"{n}) {titolo}")
```

```output
1) Alien
2) Up
3) Coco
4) Heat
5) Fargo
```

```pit
numeri = [3, 8, 1, 9, 4]
grande = numeri[0]
per n in numeri:
    se n > grande:
        grande = n
stampa(grande)
```

```output
9
```

```pit
con_doppioni = [1, 2, 2, 3, 3, 3]
unici = []
per n in con_doppioni:
    se n non in unici:
        unici.aggiungi(n)
stampa(unici)
```

```output
[1, 2, 3]
```

```pit
stampa(lista(intervallo(5, 55, 5)))
```

```output
[5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
```
