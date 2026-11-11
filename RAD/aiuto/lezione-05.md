# Lezione 5 · Ripetere

**Obiettivo:** far eseguire più volte le stesse istruzioni.

## per e intervallo

`intervallo_di(n)` produce i numeri da 0 a n−1. Il ciclo `per` li prende uno alla volta:

```pit
per i in intervallo_di(5):
    stampa("giro numero", i)
```

```output
giro numero 0
giro numero 1
giro numero 2
giro numero 3
giro numero 4
```

Anche qui: i due punti e il **rientro**. Tutto ciò che è rientrato si ripete.

`intervallo_di(inizio, fine)` e `intervallo_di(inizio, fine, passo)` danno più controllo (la fine è **esclusa**):

```pit
per n in intervallo_di(1, 6):
    stampa(n, "per 3 fa", n * 3)

per d in intervallo_di(10, 0, -3):
    stampa(d)
```

```output
1 per 3 fa 3
2 per 3 fa 6
3 per 3 fa 9
4 per 3 fa 12
5 per 3 fa 15
10
7
4
1
```

## Ripetere su un testo

`per` funziona su qualunque sequenza, per esempio le lettere di una parola:

```pit
per lettera in "ciao":
    stampa(lettera.maiuscolo())
```

```output
C
I
A
O
```

## Accumulare un risultato

Un ciclo serve spesso a costruire un totale:

```pit
totale = 0
per n in intervallo_di(1, 101):
    totale += n
stampa("La somma da 1 a 100 è", totale)
```

```output
La somma da 1 a 100 è 5050
```

## mentre: ripetere finché…

`mentre` ripete **finché la condizione è vera**. Va usato quando non sai in anticipo quante volte:

```pit
n = 1
mentre n < 100:
    n = n * 2
    stampa(n)
```

```output
2
4
8
16
32
64
128
```

Attenzione al **ciclo infinito**: se la condizione non diventa mai falsa, il programma non finisce più. Premi **Maiusc+F5** per fermarlo.

## interrompi e continua

- `interrompi` esce subito dal ciclo;
- `continua` salta al giro successivo.

```pit
per n in intervallo_di(1, 20):
    se n % 2 == 0:
        continua          # salta i pari
    se n > 9:
        interrompi        # si ferma oltre il 9
    stampa(n)
```

```output
1
3
5
7
9
```

## Cicli dentro i cicli

```pit
per riga in intervallo_di(1, 4):
    per colonna in intervallo_di(1, 4):
        stampa(riga * colonna, fine="\t")
    stampa()
```

```output
1	2	3
2	4	6
3	6	9
```

`fine="\t"` dice a `stampa` di non andare a capo ma di mettere una tabulazione.

## Esercizi

1. Stampa i numeri da 1 a 10, uno per riga.
2. Stampa la tabellina del 7 (da 7×1 a 7×10).
3. Calcola il fattoriale di 6 (1·2·3·4·5·6) con un ciclo.
4. Con `mentre`, parti da 1000 e dimezza finché il valore è maggiore di 10, stampando ogni valore.
5. Disegna un triangolo di asterischi con 5 righe, usando un ciclo (suggerimento: `"*" * i`).

## Soluzioni

```pit
per n in intervallo_di(1, 11):
    stampa(n)
```

```output
1
2
3
4
5
6
7
8
9
10
```

```pit
per n in intervallo_di(1, 11):
    stampa(f"7 x {n} = {7 * n}")
```

```output
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

```pit
fattoriale = 1
per n in intervallo_di(1, 7):
    fattoriale *= n
stampa(fattoriale)
```

```output
720
```

```pit
valore = 1000
mentre valore > 10:
    valore = valore / 2
    stampa(valore)
```

```output
500.0
250.0
125.0
62.5
31.25
15.625
7.8125
```

```pit
per i in intervallo_di(1, 6):
    stampa("*" * i)
```

```output
*
**
***
****
*****
```
