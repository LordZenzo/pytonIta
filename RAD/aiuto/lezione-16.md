# Lezione 16 · Tuple e insiemi

**Obiettivo:** conoscere altre due raccolte: la **tupla** (una lista che non cambia) e l'**insieme** (valori senza ripetizioni).

## La tupla

Una tupla assomiglia a una lista, ma si scrive con le parentesi tonde e **non si può modificare** dopo averla creata:

```pit
punto = (3, 5)
stampa(punto)
stampa(punto[0], punto[1])
stampa(lunghezza_di(punto))
```

```output
(3, 5)
3 5
2
```

Provare a cambiare un elemento dà un errore:

```pit errore
punto = (3, 5)
punto[0] = 9
```

```output
Traceback (ultima chiamata per ultima):
  File "prova.pit", riga 2, in <module>
ErroreDiTipo: 'tuple' object does not support item assignment
```

Si usa una tupla quando i valori **stanno insieme e non devono cambiare**: le coordinate di un punto, un giorno e un mese, il nome e il cognome.

Una tupla con un solo elemento vuole la virgola finale: `(7,)`. Senza virgola sono solo parentesi attorno a un numero.

## Spacchettare

Si può distribuire una tupla in più variabili in un colpo solo. È anche il modo per scambiare due valori:

```pit
punto = (3, 5)
x, y = punto
stampa("x =", x, "y =", y)

a = 1
b = 2
a, b = b, a
stampa(a, b)
```

```output
x = 3 y = 5
2 1
```

Le funzioni che «restituiscono più valori» in realtà restituiscono una tupla:

```pit
definisci minimo_e_massimo(numeri):
    ritorna minimo_di(numeri), massimo_di(numeri)

piccolo, grande = minimo_e_massimo([4, 9, 2, 7])
stampa(piccolo, grande)
```

```output
2 9
```

## L'insieme

Un **insieme** contiene valori **senza ripetizioni** e senza un ordine preciso. Si scrive con le graffe, oppure con `tipo_insieme(...)`:

```pit
colori = {"rosso", "verde", "rosso", "blu", "verde"}
stampa(lunghezza_di(colori))
stampa("blu" in colori)
stampa("giallo" in colori)
```

```output
3
Vero
Falso
```

Il trucco più usato: **togliere i doppioni** da una lista.

```pit
voti = [7, 8, 7, 9, 8, 7]
diversi = tipo_insieme(voti)
stampa(ordinato_di(diversi))
```

```output
[7, 8, 9]
```

Si aggiunge e si toglie con `aggiungi` e `rimuovi`:

```pit
nomi = {"Anna", "Luca"}
nomi.aggiungi("Sara")
nomi.aggiungi("Anna")
nomi.rimuovi("Luca")
stampa(ordinato_di(nomi))
```

```output
['Anna', 'Sara']
```

> Un insieme **vuoto** si crea con `tipo_insieme()`, non con `{}`: le graffe vuote sono un dizionario.

## Unione, intersezione, differenza

Gli insiemi si combinano come in matematica:

```pit
classe_a = {"Anna", "Luca", "Sara"}
classe_b = {"Luca", "Marco", "Sara", "Elisa"}
stampa(ordinato_di(classe_a.unione(classe_b)))
stampa(ordinato_di(classe_a.intersezione(classe_b)))
stampa(ordinato_di(classe_a.differenza(classe_b)))
```

```output
['Anna', 'Elisa', 'Luca', 'Marco', 'Sara']
['Luca', 'Sara']
['Anna']
```

- `unione`: tutti, una volta sola;
- `intersezione`: solo quelli presenti in **entrambi**;
- `differenza`: quelli del primo che **non** sono nel secondo.

## Quale raccolta scegliere?

| Raccolta | Ordine | Si modifica | Doppioni | Quando |
|---|---|---|---|---|
| lista `[ ]` | sì | sì | sì | elenco che cresce e cambia |
| tupla `( )` | sì | **no** | sì | valori che stanno insieme |
| insieme `{ }` | **no** | sì | **no** | appartenenza, togliere i doppioni |
| dizionario `{ : }` | sì | sì | chiavi uniche | coppie chiave → valore |

## Esercizi

1. Data la lista `[3, 1, 3, 2, 1, 5]`, stampa quanti valori **diversi** contiene.
2. Scrivi una funzione `prodotto_e_somma(a, b)` che restituisce due valori, e spacchettali in due variabili.
3. Date due liste di invitati, stampa (in ordine) i nomi che compaiono in **entrambe**.

## Soluzioni

```pit
numeri = [3, 1, 3, 2, 1, 5]
stampa(lunghezza_di(tipo_insieme(numeri)))
```

```output
4
```

```pit
definisci prodotto_e_somma(a, b):
    ritorna a * b, a + b

p, s = prodotto_e_somma(3, 4)
stampa(p, s)
```

```output
12 7
```

```pit
venerdi = ["Anna", "Luca", "Sara"]
sabato = ["Sara", "Marco", "Anna"]
stampa(ordinato_di(tipo_insieme(venerdi).intersezione(tipo_insieme(sabato))))
```

```output
['Anna', 'Sara']
```
