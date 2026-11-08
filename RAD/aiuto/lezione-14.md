# Lezione 14 · Le librerie

**Obiettivo:** usare codice già scritto da altri.

## importa

Python (e quindi pytonIta) ha migliaia di **librerie**: raccolte di funzioni pronte per i calcoli, le date, i file, la grafica, il web… Per usarne una la **importi**:

```pit
importa matematica

stampa(matematica.radice_quadrata(144))
stampa(matematica.pi)
stampa(matematica.pavimento(7.8))
stampa(matematica.mcd(12, 18))
```

```output
12.0
3.141592653589793
7
6
```

Dopo `importa matematica`, tutto ciò che contiene si usa scrivendo `matematica.` davanti.

## Altri modi di importare

```pit
da matematica importa radice_quadrata, pi
importa casuale come caso

stampa(radice_quadrata(81))
stampa(caso.scelta(["x"]))
```

```output
9.0
x
```

- `da modulo importa nome` porta solo quel nome, che usi **senza** il prefisso;
- `importa modulo come altro` lo usa con un nome più corto.

## Il pannello Librerie di PitStudio

Non devi ricordare i nomi: accanto alla scheda *Progetto* c'è la scheda **Librerie**. Mostra tutte le librerie divise per categoria (Calcolo, Data e ora, Testo, Dati e file, Rete…), ognuna con una breve descrizione.

- **Spunta** la casella per «attivare» la libreria nel progetto: comparirà sempre tra i suggerimenti e i suoi nomi si completeranno anche prima di scrivere `importa`.
- **Doppio clic** su una libreria: PitStudio inserisce `importa nome` in cima al file aperto.
- Il campo in alto filtra per nome o descrizione (prova a scrivere `file` o `date`).
- Scrivendo `matematica.` nell'editor compare l'elenco di tutto ciò che contiene.

## Alcune librerie utili

### casuale: numeri e scelte a caso

```pit
importa casuale

casuale.imposta_seme(1)               # per avere sempre lo stesso risultato
stampa(casuale.intero_casuale(1, 6))  # un dado
stampa(casuale.scelta(["rosso", "verde", "blu"]))
carte = [1, 2, 3, 4, 5]
casuale.mescola(carte)
stampa(carte)
```

```output
2
blu
[4, 2, 5, 3, 1]
```

### data_ora: date e orari

```pit
importa data_ora

natale = data_ora.Data(2030, 12, 25)
compleanno = data_ora.Data(2000, 5, 17)
giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
stampa("Natale 2030 cade di", giorni[natale.giorno_settimana()])
stampa((natale - compleanno).giorni)
stampa(f"{natale:%d/%m/%Y}")
```

```output
Natale 2030 cade di mercoledì
11179
25/12/2030
```

### tempo: pause e cronometro

`tempo.aspetta(secondi)` mette in pausa il programma; `tempo.adesso()` dà l'orologio in secondi (per misurare quanto dura qualcosa).

```pit
importa tempo

inizio = tempo.adesso()
tempo.aspetta(0.2)
stampa(tempo.adesso() - inizio >= 0.2)
```

```output
Vero
```

### statistica

```pit
importa statistica

voti = [6, 7, 7, 8, 10]
stampa(statistica.media(voti))
stampa(statistica.mediana(voti))
stampa(statistica.moda(voti))
```

```output
7.6
7
7
```

### percorso: file e cartelle come oggetti

```pit
da percorso importa Percorso

p = Percorso("esempio.txt")
p.scrivi_testo("ciao\n", encoding="utf-8")
stampa(p.esiste())
stampa(p.leggi_testo(encoding="utf-8").elimina_spazi())
```

```output
Vero
ciao
```

## Librerie non incluse

Le librerie che non sono nel pannello (le «esterne») si installano con `pip`: da un terminale, `pitonit -m pip install nome`. Poi `importa nome` come le altre.

## Il mix italiano/inglese

I nomi originali di Python continuano a funzionare: `importa math` e `importa matematica` sono la stessa libreria. Puoi leggere tutorial inglesi e usare il loro codice: le parole chiave cambiano (`if` → `se`), le librerie restano uguali.

## Esercizi

1. Con `casuale`, simula il lancio di due dadi e stampa la somma.
2. Con `data_ora`, calcola quanti giorni mancano a una data a tua scelta (usa `data_ora.Data.oggi()`).
3. Spunta nel pannello Librerie `formato_json`, poi in un nuovo file scrivi `formato_json.` e guarda i suggerimenti.

## Soluzioni

```pit
importa casuale

dado1 = casuale.intero_casuale(1, 6)
dado2 = casuale.intero_casuale(1, 6)
stampa(dado1, "+", dado2, "=", dado1 + dado2)
```

```pit
importa data_ora

oggi = data_ora.Data.oggi()
capodanno = data_ora.Data(oggi.anno + 1, 1, 1)
stampa("Giorni a capodanno:", (capodanno - oggi).giorni)
```
