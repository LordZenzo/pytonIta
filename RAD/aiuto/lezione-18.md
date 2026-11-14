# Lezione 18 · Generatori e iteratori

**Obiettivo:** produrre i valori **uno alla volta**, solo quando servono, senza costruire liste enormi.

## Che cosa è un iteratore

Quando scrivi `per x in qualcosa`, Python chiede a `qualcosa` un valore dopo l'altro. Puoi farlo anche a mano, con `iteratore_di` e `prossimo_elemento`:

```pit
giorni = ["lun", "mar", "mer"]
it = iteratore_di(giorni)
stampa(prossimo_elemento(it))
stampa(prossimo_elemento(it))
stampa(prossimo_elemento(it))
```

```output
lun
mar
mer
```

Una quarta chiamata darebbe l'errore `FineIterazione`: il ciclo `per` lo cattura da solo e si ferma.

## La funzione generatore

Una funzione che usa `produci` al posto di `ritorna` è un **generatore**: restituisce un valore, **si ferma ricordandosi dove era**, e riparte dal punto in cui si era fermata quando serve il valore successivo.

```pit
definisci conta_fino_a(massimo):
    n = 1
    mentre n <= massimo:
        produci n
        n += 1

per numero in conta_fino_a(3):
    stampa("ho ricevuto", numero)
```

```output
ho ricevuto 1
ho ricevuto 2
ho ricevuto 3
```

Per vedere cosa succede davvero, metti una `stampa` dentro il generatore:

```pit
definisci saluti():
    stampa("preparo il primo")
    produci "ciao"
    stampa("preparo il secondo")
    produci "salve"
    stampa("finito")

g = saluti()
stampa("creato, ma non è partito")
stampa(prossimo_elemento(g))
stampa(prossimo_elemento(g))
```

```output
creato, ma non è partito
preparo il primo
ciao
preparo il secondo
salve
```

Chiamare `saluti()` **non esegue nulla**: crea soltanto il generatore. Il codice parte alla prima richiesta di un valore.

## Perché è utile

1. **Risparmia memoria.** Una lista di un milione di numeri occupa spazio; un generatore ne tiene in mente uno solo.
2. **Può essere infinito**, perché i valori si calcolano solo quando servono:

```pit
definisci pari():
    n = 0
    mentre Vero:
        produci n
        n += 2

per numero in pari():
    se numero > 8:
        interrompi
    stampa(numero)
```

```output
0
2
4
6
8
```

3. **Racconta una sequenza** senza costruirla tutta: per esempio le righe di un file enorme, o i numeri di Fibonacci.

```pit
definisci fibonacci():
    a, b = 0, 1
    mentre Vero:
        produci a
        a, b = b, a + b

prime = []
per valore in fibonacci():
    se valore > 50:
        interrompi
    prime.aggiungi(valore)
stampa(prime)
```

```output
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Espressioni generatore

Una comprehension scritta con le tonde (invece delle quadre) è un generatore: non costruisce la lista, produce i valori man mano.

```pit
totale = somma_di(n * n per n in intervallo_di(1, 1001))
stampa(totale)
```

```output
333833500
```

Funzioni come `somma_di`, `massimo_di`, `minimo_di`, `tutti_veri` e `almeno_uno_vero` accettano direttamente un generatore.

```pit
parole = ["sole", "luna", "mare"]
stampa(tutti_veri(lunghezza_di(p) == 4 per p in parole))
stampa(almeno_uno_vero(p.inizia_con("m") per p in parole))
```

```output
Vero
Vero
```

## Un generatore si consuma una volta sola

```pit
g = (n * 2 per n in [1, 2, 3])
stampa(tipo_lista(g))
stampa(tipo_lista(g))
```

```output
[2, 4, 6]
[]
```

Dopo il primo giro il generatore è «finito». Se ti serve ripassarlo, convertilo in lista oppure crealo di nuovo.

## Esercizi

1. Scrivi un generatore `multipli(base, quanti)` che produce `base`, `2*base`, … per `quanti` valori. Stampa i multipli di 7 (i primi 4).
2. Scrivi un generatore `lettere_maiuscole(testo)` che produce solo le lettere maiuscole di un testo (suggerimento: il metodo `c.isupper()` dice se una lettera è maiuscola).
3. Calcola, con un'espressione generatore, la somma dei numeri pari da 1 a 100.

## Soluzioni

```pit
definisci multipli(base, quanti):
    per k in intervallo_di(1, quanti + 1):
        produci base * k

stampa(tipo_lista(multipli(7, 4)))
```

```output
[7, 14, 21, 28]
```

```pit
definisci lettere_maiuscole(testo):
    per c in testo:
        se c.isupper():
            produci c

stampa("".join(lettere_maiuscole("Ciao Mondo da Anna")))
```

```output
CMA
```

```pit
stampa(somma_di(n per n in intervallo_di(1, 101) se n % 2 == 0))
```

```output
2550
```
