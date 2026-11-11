# Lezione 4 · Prendere decisioni

**Obiettivo:** far fare al programma cose diverse a seconda dei casi.

## se

```pit
eta = 16
se eta >= 18:
    stampa("Sei maggiorenne")
```

```output

```

Questa volta niente viene stampato, perché 16 non è ≥ 18. Osserva due cose importanti:

- la riga con `se` finisce con i **due punti** `:`;
- le istruzioni da eseguire vanno **rientrate** (4 spazi a destra): il rientro dice quali righe appartengono al `se`. L'editor lo fa da solo quando premi Invio dopo i due punti.

## altrimenti

```pit
eta = 16
se eta >= 18:
    stampa("Sei maggiorenne")
altrimenti:
    stampa("Sei minorenne")
stampa("Fine")
```

```output
Sei minorenne
Fine
```

L'ultima riga non è rientrata: viene eseguita sempre.

## altrimenti_se: più casi

```pit
voto = 7
se voto >= 9:
    stampa("Ottimo")
altrimenti_se voto >= 6:
    stampa("Sufficiente")
altrimenti:
    stampa("Insufficiente")
```

```output
Sufficiente
```

Il computer controlla le condizioni **in ordine** e si ferma alla prima vera.

## I confronti

| Scrivi | Significa |
|---|---|
| `a == b` | uguale (due uguali!) |
| `a != b` | diverso |
| `a < b`, `a > b` | minore, maggiore |
| `a <= b`, `a >= b` | minore o uguale, maggiore o uguale |

Attenzione: **un solo `=` assegna, due `==` confrontano**. Scrivere `se x = 1:` è un errore comune, e la console te lo ricorda.

## Combinare condizioni: e, o, non

```pit
eta = 25
ha_patente = Vero
se eta >= 18 e ha_patente:
    stampa("Puoi guidare")

giorno = "sabato"
se giorno == "sabato" o giorno == "domenica":
    stampa("È weekend")

se non ha_patente:
    stampa("Niente auto")
altrimenti:
    stampa("Hai la patente")
```

```output
Puoi guidare
È weekend
Hai la patente
```

- `a e b`: vera se **entrambe** sono vere;
- `a o b`: vera se **almeno una** è vera;
- `non a`: l'opposto.

Con `in` controlli se un valore è dentro un testo o una lista: `se "a" in "casa":`.

## Esercizi

1. Dato un numero `n`, stampa se è pari o dispari (suggerimento: `n % 2`).
2. Chiedi due numeri e stampa il maggiore (senza usare `massimo`).
3. Chiedi la temperatura: sotto 10 «Fa freddo», da 10 a 25 «Si sta bene», oltre «Fa caldo».
4. Un anno è bisestile se è divisibile per 4 ma non per 100, oppure se è divisibile per 400. Scrivi il programma per un anno scelto.

## Soluzioni

```pit
n = 7
se n % 2 == 0:
    stampa("pari")
altrimenti:
    stampa("dispari")
```

```output
dispari
```

```pit
a = tipo_intero(leggi_tastiera("A: "))
b = tipo_intero(leggi_tastiera("B: "))
se a > b:
    stampa("Il maggiore è", a)
altrimenti:
    stampa("Il maggiore è", b)
```

```pit
t = tipo_decimale(leggi_tastiera("Temperatura: "))
se t < 10:
    stampa("Fa freddo")
altrimenti_se t <= 25:
    stampa("Si sta bene")
altrimenti:
    stampa("Fa caldo")
```

```pit
anno = 2024
se (anno % 4 == 0 e anno % 100 != 0) o anno % 400 == 0:
    stampa(anno, "è bisestile")
altrimenti:
    stampa(anno, "non è bisestile")
```

```output
2024 è bisestile
```
