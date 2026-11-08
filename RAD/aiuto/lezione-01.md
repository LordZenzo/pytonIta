# Lezione 1 · Il primo programma

**Obiettivo:** far scrivere qualcosa al computer.

## Stampare un messaggio

Un programma è una lista di istruzioni, eseguite una dopo l'altra, dall'alto verso il basso. La prima istruzione che impari è `stampa`: mostra qualcosa sullo schermo.

```pit
stampa("Ciao, mondo!")
```

```output
Ciao, mondo!
```

Il testo va tra **virgolette** (doppie `"` oppure singole `'`). Le parentesi tonde contengono ciò che vuoi stampare.

Puoi dare più istruzioni, una per riga:

```pit
stampa("Mi chiamo pytonIta")
stampa("Parlo italiano")
stampa("e ti insegno a programmare")
```

```output
Mi chiamo pytonIta
Parlo italiano
e ti insegno a programmare
```

## Stampare numeri e calcoli

I numeri non vogliono virgolette. Il computer sa fare i conti:

```pit
stampa(2 + 3)
stampa(10 - 4)
stampa(6 * 7)
stampa(15 / 4)
stampa(15 // 4)
stampa(15 % 4)
stampa(2 ** 10)
```

```output
5
6
42
3.75
3
3
1024
```

| Simbolo | Significa |
|---|---|
| `+` `-` | somma, differenza |
| `*` | moltiplicazione |
| `/` | divisione (con la virgola) |
| `//` | divisione intera (senza resto) |
| `%` | il **resto** della divisione |
| `**` | elevamento a potenza |

Si può stampare più di una cosa nella stessa riga, separandole con la virgola:

```pit
stampa("Il doppio di 21 è", 21 * 2)
```

```output
Il doppio di 21 è 42
```

## I commenti

Tutto ciò che segue un `#` è un **commento**: il computer lo ignora, serve a te (e a chi legge) per spiegare il codice.

```pit
# Questo è un commento: non viene eseguito
stampa("Fine")  # anche qui, a fine riga
```

```output
Fine
```

## Il primo errore

Sbagliare è normale. Se scordi una virgoletta, il programma non parte e la console ti dice dov'è il problema:

```pit errore
stampa("Ciao)
```

Troverai un messaggio come *«stringa non terminata»* e un suggerimento 💡 che ti spiega cosa controllare: la riga è segnata anche in rosso nell'editor. Correggi e premi di nuovo **F5**.

## Esercizi

1. Stampa il tuo nome e la tua città su due righe.
2. Quanto fa `365 * 24`? (le ore di un anno): fallo calcolare al programma.
3. Disegna con `stampa` un piccolo triangolo fatto di asterischi `*` (almeno 3 righe).
4. Cosa stampa `stampa(7 // 2, 7 % 2)`? Indovina, poi prova.

## Soluzioni

```pit
stampa("Giulia")
stampa("Bologna")
```

```pit
stampa(365 * 24)
```

```output
8760
```

```pit
stampa("*")
stampa("**")
stampa("***")
```

```output
*
**
***
```

```pit
stampa(7 // 2, 7 % 2)
```

```output
3 1
```
