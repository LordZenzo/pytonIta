# Lezione 9 · Le funzioni

**Obiettivo:** dare un nome a un pezzo di codice per riusarlo.

## Definire e chiamare

Una **funzione** è un blocco di istruzioni con un nome. Si crea con `definisci` e poi si **chiama** scrivendone il nome con le parentesi:

```pit
definisci saluta():
    stampa("Ciao!")
    stampa("Come stai?")

saluta()
saluta()
```

```output
Ciao!
Come stai?
Ciao!
Come stai?
```

Dopo `definisci saluta():` non succede niente: la funzione esegue il suo codice solo quando viene chiamata.

## Parametri

I **parametri** sono valori che la funzione riceve:

```pit
definisci saluta(nome, volte=1):
    per _ in intervallo_di(volte):
        stampa(f"Ciao, {nome}!")

saluta("Anna")
saluta("Luca", 2)
saluta(volte=3, nome="Sara")
```

```output
Ciao, Anna!
Ciao, Luca!
Ciao, Luca!
Ciao, Sara!
Ciao, Sara!
Ciao, Sara!
```

`volte=1` è un valore **predefinito**: se non lo dai, vale 1. Puoi passare i valori per posizione o per nome.

## Restituire un valore: ritorna

`ritorna` fa uscire dalla funzione e consegna un risultato a chi l'ha chiamata:

```pit
definisci area_rettangolo(base, altezza):
    ritorna base * altezza

a = area_rettangolo(4, 5)
stampa(a)
stampa(area_rettangolo(2, 3) + area_rettangolo(1, 1))
```

```output
20
7
```

Se una funzione non ha `ritorna`, restituisce `Nessuno`. **`stampa` e `ritorna` sono cose diverse**: `stampa` mostra un valore a schermo, `ritorna` lo passa al programma perché lo usi.

## Variabili locali

Le variabili create dentro una funzione **esistono solo lì dentro**:

```pit errore
definisci conta():
    contatore = 10
    ritorna contatore

conta()
stampa(contatore)    # errore: fuori dalla funzione non esiste
```

Se vuoi proprio modificare una variabile del programma dall'interno di una funzione, la dichiari con `globale`; ma di solito è meglio passare i valori come parametri e restituire il risultato.

## Funzioni che usano altre funzioni

```pit
definisci e_pari(n):
    ritorna n % 2 == 0

definisci pari_fino_a(limite):
    risultato = []
    per n in intervallo_di(limite + 1):
        se e_pari(n):
            risultato.aggiungi(n)
    ritorna risultato

stampa(pari_fino_a(10))
```

```output
[0, 2, 4, 6, 8, 10]
```

## Una funzione che chiama se stessa

La **ricorsione**: il fattoriale di n è n × il fattoriale di n−1.

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

Serve sempre un **caso base** (qui `n <= 1`) che fermi la catena, altrimenti la funzione non finisce mai.

## Perché le funzioni

- **si riusano**: scrivi una volta, chiami mille volte;
- **si leggono**: `calcola_sconto(prezzo)` spiega cosa fa meglio di cinque righe di conti;
- **si correggono in un posto solo**.

## Esercizi

1. Scrivi `quadrato(n)` che restituisce n al quadrato, e stampa il quadrato di 9.
2. Scrivi `massimo_tra(a, b, c)` che restituisce il maggiore dei tre, senza usare `massimo`.
3. Scrivi `media(lista)` che restituisce la media di una lista di numeri.
4. Scrivi `e_primo(n)` che dice se n è un numero primo; poi stampa i primi minori di 30.

## Soluzioni

```pit
definisci quadrato(n):
    ritorna n * n

stampa(quadrato(9))
```

```output
81
```

```pit
definisci massimo_tra(a, b, c):
    grande = a
    se b > grande:
        grande = b
    se c > grande:
        grande = c
    ritorna grande

stampa(massimo_tra(4, 9, 2))
```

```output
9
```

```pit
definisci media(numeri):
    ritorna somma_di(numeri) / lunghezza_di(numeri)

stampa(media([6, 8, 10]))
```

```output
8.0
```

```pit
definisci e_primo(n):
    se n < 2:
        ritorna Falso
    per d in intervallo_di(2, n):
        se n % d == 0:
            ritorna Falso
    ritorna Vero

stampa([n per n in intervallo_di(30) se e_primo(n)])
```

```output
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```
