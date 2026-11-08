# Lezione 7 · Lavorare con i testi

**Obiettivo:** tagliare, cercare e trasformare le parole.

## Un testo è una sequenza di caratteri

Come una lista, un testo ha una lunghezza e si legge per posizione (da zero) e per fette:

```pit
parola = "pitone"
stampa(lunghezza(parola))
stampa(parola[0])
stampa(parola[-1])
stampa(parola[1:4])
stampa(parola[::-1])
```

```output
6
p
e
ito
enotip
```

`parola[::-1]` legge il testo al contrario. I testi **non si possono modificare** carattere per carattere: se ne crea uno nuovo.

## Metodi utili

```pit
frase = "  Ciao a tutti, benvenuti  "
stampa(frase.elimina_spazi())
stampa(frase.maiuscolo())
stampa(frase.minuscolo())
stampa(frase.sostituisci("tutti", "voi"))
stampa(frase.conta("t"))
stampa(frase.elimina_spazi().titolo())
```

```output
Ciao a tutti, benvenuti
  CIAO A TUTTI, BENVENUTI
  ciao a tutti, benvenuti
  Ciao a voi, benvenuti
4
Ciao A Tutti, Benvenuti
```

| Metodo | Cosa fa |
|---|---|
| `maiuscolo()`, `minuscolo()`, `titolo()` | cambia le maiuscole |
| `elimina_spazi()` | toglie gli spazi a inizio e fine |
| `sostituisci(a, b)` | sostituisce `a` con `b` |
| `trova(x)` | posizione di `x` (−1 se non c'è) |
| `inizia_con(x)`, `finisce_con(x)` | controlla l'inizio o la fine |
| `separa(sep)` | divide in una lista di parole |
| `unisci(lista)` | unisce con il testo come collante |
| `è_cifra()`, `è_alfabetico()` | controlla il contenuto |

## Dividere e unire

```pit
frase = "uno due tre quattro"
parole = frase.separa()
stampa(parole)
stampa(lunghezza(parole))
stampa("-".unisci(parole))
dati = "Anna,22,Roma".separa(",")
stampa(dati)
```

```output
['uno', 'due', 'tre', 'quattro']
4
uno-due-tre-quattro
['Anna', '22', 'Roma']
```

## Formattare con gli f-testi

Dentro le graffe puoi dire **come** mostrare il valore:

```pit
prezzo = 1234.5
percentuale = 0.256
stampa(f"Prezzo: {prezzo:.2f} euro")
stampa(f"Percentuale: {percentuale:.1%}")
stampa(f"[{'ciao':>10}]")
stampa(f"[{'ciao':<10}]")
stampa(f"[{'ciao':^10}]")
stampa(f"{7:03d}")
```

```output
Prezzo: 1234.50 euro
Percentuale: 25.6%
[      ciao]
[ciao      ]
[   ciao   ]
007
```

`.2f` = due cifre decimali; `>10` allinea a destra in 10 caratteri; `03d` = tre cifre con zeri davanti.

## Testi su più righe

```pit
poesia = """Nel mezzo del cammin
di nostra vita"""
stampa(poesia)
stampa(poesia.separa_righe())
```

```output
Nel mezzo del cammin
di nostra vita
['Nel mezzo del cammin', 'di nostra vita']
```

`\n` dentro un testo è un **a capo**, `\t` una tabulazione.

## Esercizi

1. Chiedi una parola e dì se è un **palindromo** (si legge uguale al contrario, come `radar`).
2. Conta quante vocali ci sono in `"programmazione"`.
3. Data `"mario rossi"`, stampa `"Mario Rossi"` (iniziali maiuscole).
4. Dato `"2024-05-17"` stampa giorno, mese e anno separati (suggerimento: `separa("-")`).

## Soluzioni

```pit
parola = "radar"
se parola == parola[::-1]:
    stampa(parola, "è un palindromo")
altrimenti:
    stampa(parola, "non è un palindromo")
```

```output
radar è un palindromo
```

```pit
conteggio = 0
per lettera in "programmazione":
    se lettera in "aeiou":
        conteggio += 1
stampa(conteggio)
```

```output
6
```

```pit
stampa("mario rossi".titolo())
```

```output
Mario Rossi
```

```pit
anno, mese, giorno = "2024-05-17".separa("-")
stampa("Giorno", giorno, "mese", mese, "anno", anno)
```

```output
Giorno 17 mese 05 anno 2024
```
