# Lezione 2 · Variabili e tipi

**Obiettivo:** memorizzare dei valori e dare loro un nome.

## Che cos'è una variabile

Una **variabile** è una scatola con un nome in cui si conserva un valore. Si crea con il segno `=` (assegnazione): a sinistra il nome, a destra il valore.

```pit
eta = 12
nome = "Marco"
stampa(nome, "ha", eta, "anni")
```

```output
Marco ha 12 anni
```

Il valore si può cambiare quando vuoi, anche usando il valore precedente:

```pit
punti = 10
punti = punti + 5
stampa(punti)
punti += 3        # abbreviazione di: punti = punti + 3
stampa(punti)
```

```output
15
18
```

## I nomi delle variabili

- possono contenere lettere, numeri e `_`, ma **non iniziare con un numero**;
- maiuscole e minuscole sono diverse: `Nome` e `nome` non sono la stessa variabile;
- scegli nomi che spiegano: `prezzo_totale` è meglio di `x`;
- le **parole chiave** di pytonIta (`se`, `per`, `mentre`, `classe`…) hanno un significato speciale: meglio non usarle come nomi. Alcune molto naturali (`classe`, `con`, `prova`, `da`) funzionano comunque come nomi di variabile, ma una scelta più descrittiva (`classe_3a`, `connessione`, `esempio`) rende il programma più chiaro.

## I tipi di valore

Ogni valore ha un **tipo**:

| Tipo | Esempi | Nome del tipo |
|---|---|---|
| numero intero | `7`, `-30`, `0` | `int` (si converte con `tipo_intero(...)`) |
| numero decimale | `3.14`, `-0.5` | `float` (si converte con `tipo_decimale(...)`) |
| testo | `"ciao"`, `'a'` | `str` (si converte con `tipo_testo(...)`) |
| vero/falso | `Vero`, `Falso` | `bool` |
| niente | `Nessuno` | `NoneType` |

Per i decimali si usa il **punto**, non la virgola. Con `tipo_di(...)` chiedi al programma di che tipo è un valore (il computer usa i nomi inglesi dei tipi: `int`, `float`, `str`, `bool`):

```pit
stampa(tipo_di(7))
stampa(tipo_di(3.14))
stampa(tipo_di("ciao"))
stampa(tipo_di(Vero))
```

```output
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

## Unire testi e numeri

Il testo si può unire con `+`, ma **non si può sommare un testo a un numero**: prima il numero va trasformato in testo.

```pit
anni = 12
stampa("Ho " + tipo_testo(anni) + " anni")
```

```output
Ho 12 anni
```

Più comodo è il **f-testo**: un testo che inizia con `f` e contiene variabili o calcoli tra graffe `{}`.

```pit
nome = "Sara"
voto = 8.5
stampa(f"{nome} ha preso {voto}")
stampa(f"Il doppio è {voto * 2}")
```

```output
Sara ha preso 8.5
Il doppio è 17.0
```

## Convertire

```pit
stampa(tipo_intero("42") + 1)
stampa(tipo_decimale("2.5") * 2)
stampa(tipo_intero(3.9))
stampa(arrotonda(3.14159, 2))
```

```output
43
5.0
3
3.14
```

Attenzione: `tipo_intero(3.9)` taglia i decimali (non arrotonda).

## Esercizi

1. Metti in variabili la base (8) e l'altezza (5) di un rettangolo e stampa area e perimetro.
2. Con un f-testo stampa: `Marco ha 12 anni e fra 3 anni ne avrà 15`, usando le variabili `nome` ed `eta`.
3. Quanti secondi ci sono in una settimana? Usa variabili con nomi chiari.
4. Prova `stampa("5" + 5)` e leggi il messaggio d'errore con il suggerimento.

## Soluzioni

```pit
base = 8
altezza = 5
stampa("Area:", base * altezza)
stampa("Perimetro:", 2 * (base + altezza))
```

```output
Area: 40
Perimetro: 26
```

```pit
nome = "Marco"
eta = 12
stampa(f"{nome} ha {eta} anni e fra 3 anni ne avrà {eta + 3}")
```

```output
Marco ha 12 anni e fra 3 anni ne avrà 15
```

```pit
secondi_al_giorno = 24 * 60 * 60
stampa(secondi_al_giorno * 7)
```

```output
604800
```

```pit errore
stampa("5" + 5)
```
