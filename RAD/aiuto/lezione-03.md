# Lezione 3 · Parlare con il programma

**Obiettivo:** far scrivere dei dati all'utente e usarli.

## leggi: chiedere un valore

`leggi_tastiera("domanda")` mostra la domanda, aspetta che l'utente scriva qualcosa e prema Invio, poi **restituisce quel testo**. Nella console di PitStudio scrivi la risposta nella riga in basso e premi Invio.

```pit
nome = leggi_tastiera("Come ti chiami? ")
stampa("Ciao,", nome)
```

```esempio
Come ti chiami? Anna
Ciao, Anna
```

## Attenzione: leggi restituisce sempre testo

Anche se l'utente scrive `12`, ottieni il **testo** `"12"`, non il numero. Per fare calcoli va convertito con `tipo_intero(...)` o `tipo_decimale(...)`:

```pit
anni = tipo_intero(leggi_tastiera("Quanti anni hai? "))
stampa("Fra dieci anni ne avrai", anni + 10)
```

```esempio
Quanti anni hai? 12
Fra dieci anni ne avrai 22
```

Se invece scrivessi `anni = leggi_tastiera(...)` e poi `anni + 10`, otterresti un errore: non si può sommare un testo a un numero (la console te lo spiega).

## Un piccolo programma completo

```pit
stampa("Calcolatrice dell'area del rettangolo")
base = tipo_decimale(leggi_tastiera("Base: "))
altezza = tipo_decimale(leggi_tastiera("Altezza: "))
area = base * altezza
stampa(f"L'area è {area}")
```

```esempio
Calcolatrice dell'area del rettangolo
Base: 4.5
Altezza: 2
L'area è 9.0
```

## Se l'utente sbaglia

Se scrive lettere dove serve un numero, `tipo_intero("abc")` dà un errore. Nella [lezione 11](#lezione-11) vedrai come gestirlo con garbo; per ora è normale che si fermi.

## Esercizi

1. Chiedi nome e cognome e stampa `Benvenuto, Nome Cognome!`.
2. Chiedi due numeri interi e stampa la loro somma e la loro media.
3. Chiedi il prezzo di un oggetto e lo sconto in percentuale; stampa il prezzo finale.
4. Chiedi quanti minuti dura un film e stampa quante ore e minuti sono (usa `//` e `%`).

## Soluzioni

```pit
nome = leggi_tastiera("Nome: ")
cognome = leggi_tastiera("Cognome: ")
stampa(f"Benvenuto, {nome} {cognome}!")
```

```pit
a = tipo_intero(leggi_tastiera("Primo numero: "))
b = tipo_intero(leggi_tastiera("Secondo numero: "))
stampa("Somma:", a + b)
stampa("Media:", (a + b) / 2)
```

```pit
prezzo = tipo_decimale(leggi_tastiera("Prezzo: "))
sconto = tipo_decimale(leggi_tastiera("Sconto %: "))
stampa("Prezzo finale:", prezzo - prezzo * sconto / 100)
```

```pit
minuti = tipo_intero(leggi_tastiera("Durata in minuti: "))
stampa(f"{minuti // 60} ore e {minuti % 60} minuti")
```
