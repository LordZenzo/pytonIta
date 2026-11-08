# Lezione 8 · I dizionari

**Obiettivo:** associare un valore a un nome, come in una rubrica.

## Che cos'è un dizionario

Una lista trova gli elementi per **posizione**; un **dizionario** li trova per **chiave**. Si scrive con le graffe, ogni voce è `chiave: valore`:

```pit
rubrica = {"Anna": "333 1234567", "Luca": "347 7654321"}
stampa(rubrica["Anna"])
rubrica["Sara"] = "320 1112223"       # aggiunge una voce
rubrica["Luca"] = "000 0000000"       # cambia una voce
stampa(rubrica)
stampa(lunghezza(rubrica))
```

```output
333 1234567
{'Anna': '333 1234567', 'Luca': '000 0000000', 'Sara': '320 1112223'}
3
```

## Chiavi che mancano

Se chiedi una chiave che non esiste ottieni un errore (`ErroreDiChiave`). Per evitarlo:

```pit
rubrica = {"Anna": "333 1234567"}
stampa("Anna" in rubrica)
stampa("Piero" in rubrica)
stampa(rubrica.ottieni("Piero"))
stampa(rubrica.ottieni("Piero", "sconosciuto"))
```

```output
Vero
Falso
Nessuno
sconosciuto
```

`ottieni(chiave, predefinito)` restituisce il valore, oppure il predefinito (o `Nessuno`) se la chiave non c'è.

## Scorrere un dizionario

```pit
voti = {"italiano": 8, "storia": 7, "inglese": 9}
per materia in voti:
    stampa(materia)

per materia, voto in voti.elementi():
    stampa(f"{materia}: {voto}")

stampa(lista(voti.chiavi()))
stampa(somma(voti.valori()) / lunghezza(voti))
```

```output
italiano
storia
inglese
italiano: 8
storia: 7
inglese: 9
['italiano', 'storia', 'inglese']
8.0
```

| Metodo | Cosa restituisce |
|---|---|
| `chiavi()` | le chiavi |
| `valori()` | i valori |
| `elementi()` | le coppie (chiave, valore) |
| `ottieni(k, d)` | valore o predefinito |
| `estrai(k)` | toglie la voce e la restituisce |
| `aggiorna(altro)` | aggiunge le voci di un altro dizionario |

## Esempio: contare le parole

```pit
frase = "la casa è la mia casa"
conteggi = {}
per parola in frase.separa():
    conteggi[parola] = conteggi.ottieni(parola, 0) + 1
stampa(conteggi)
```

```output
{'la': 2, 'casa': 2, 'è': 1, 'mia': 1}
```

## Dizionari dentro le liste

Molti dati reali sono liste di dizionari:

```pit
studenti = [
    {"nome": "Anna", "voto": 8},
    {"nome": "Luca", "voto": 6},
    {"nome": "Sara", "voto": 9},
]
per s in studenti:
    stampa(f"{s['nome']:<6} {s['voto']}")
migliore = massimo(studenti, chiave=lambda s: s["voto"])
stampa("Il migliore è", migliore["nome"])
```

```output
Anna   8
Luca   6
Sara   9
Il migliore è Sara
```

## Gli insiemi

Un **insieme** è come una lista senza ordine e **senza doppioni**:

```pit
colori = {"rosso", "verde", "rosso", "blu"}
stampa(lunghezza(colori))
stampa(lista(insieme([1, 2, 2, 3, 3, 3])))
```

```output
3
[1, 2, 3]
```

## Esercizi

1. Crea un dizionario con tre città e le loro regioni; stampa la regione di una città scelta.
2. Conta quante volte compare ciascuna lettera nella parola `"banana"`.
3. Data la lista di prezzi `{"pane": 1.2, "latte": 1.5, "uova": 2.8}` stampa il totale e il prodotto più caro.

## Soluzioni

```pit
regioni = {"Torino": "Piemonte", "Napoli": "Campania", "Bari": "Puglia"}
stampa(regioni["Napoli"])
```

```output
Campania
```

```pit
lettere = {}
per l in "banana":
    lettere[l] = lettere.ottieni(l, 0) + 1
stampa(lettere)
```

```output
{'b': 1, 'a': 3, 'n': 2}
```

```pit
prezzi = {"pane": 1.2, "latte": 1.5, "uova": 2.8}
stampa("Totale:", somma(prezzi.valori()))
caro = massimo(prezzi, chiave=prezzi.ottieni)
stampa("Il più caro:", caro)
```

```output
Totale: 5.5
Il più caro: uova
```
