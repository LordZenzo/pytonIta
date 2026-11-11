# Lezione 10 · I file

**Obiettivo:** salvare e leggere dati sul disco.

## Dove vanno i file

Un nome di file senza percorso (come `appunti.txt`) viene cercato nella **cartella del progetto**: quando premi F5 il programma parte da lì. Il nuovo file compare nel pannello *Progetto* (premi ⟳ se non lo vedi).

## Scrivere un file

`apri(nome, "w")` apre il file in scrittura (`w` = *write*; se esiste lo svuota). Con `con` il file si chiude da solo al termine del blocco:

```pit
con apri("appunti.txt", "w", codifica="utf-8") come f:
    f.scrivi("Prima riga\n")
    f.scrivi("Seconda riga\n")
stampa("File scritto")
```

```output
File scritto
```

`encoding="utf-8"` garantisce che lettere accentate e simboli si salvino bene.

## Leggere un file

```pit
con apri("appunti.txt", "w", codifica="utf-8") come f:
    f.scrivi("Prima riga\nSeconda riga\nTerza riga\n")

con apri("appunti.txt", codifica="utf-8") come f:
    contenuto = f.leggi_tutto()
stampa(contenuto)
```

```output
Prima riga
Seconda riga
Terza riga
```

Per leggere **una riga alla volta** (comodo con file grandi):

```pit
con apri("appunti.txt", "w", codifica="utf-8") come f:
    f.scrivi("uno\ndue\ntre\n")

con apri("appunti.txt", codifica="utf-8") come f:
    per numero, riga in enumera(f, 1):
        stampa(numero, riga.elimina_spazi())
```

```output
1 uno
2 due
3 tre
```

## Aggiungere in fondo

La modalità `"a"` (*append*) aggiunge senza cancellare:

```pit
con apri("registro.txt", "a", codifica="utf-8") come f:
    f.scrivi("nuova voce\n")
con apri("registro.txt", codifica="utf-8") come f:
    stampa(lunghezza_di(f.leggi_righe()) >= 1)
```

```output
Vero
```

## Controllare se un file esiste

```pit
importa sistema_operativo
stampa(sistema_operativo.percorso.esiste("non_c_e.txt"))
stampa(sistema_operativo.percorso.esiste("."))
```

```output
Falso
Vero
```

## Salvare dati strutturati: JSON

Liste e dizionari si salvano comodamente in formato **JSON** (leggibile anche da altri programmi):

```pit
importa formato_json

dati = {"nome": "Anna", "voti": [8, 9, 7]}
con apri("dati.json", "w", codifica="utf-8") come f:
    formato_json.scarica(dati, f, indent=2)

con apri("dati.json", codifica="utf-8") come f:
    letti = formato_json.carica(f)
stampa(letti["voti"])
```

```output
[8, 9, 7]
```

Provare i file `.json` nel pannello Progetto: PitStudio li mostra come albero.

## Esercizi

1. Scrivi in `lista.txt` i numeri da 1 a 5, uno per riga; poi rileggili e stampane la somma.
2. Scrivi un programma che aggiunge una riga con la data a `diario.txt` ogni volta che viene eseguito (usa `importa data_ora` e `data_ora.OraData.adesso()`).
3. Salva in un file JSON un dizionario con nome ed età di tre persone e rileggilo.

## Soluzioni

```pit
con apri("lista.txt", "w", codifica="utf-8") come f:
    per n in intervallo_di(1, 6):
        f.scrivi(f"{n}\n")

totale = 0
con apri("lista.txt", codifica="utf-8") come f:
    per riga in f:
        totale += tipo_intero(riga)
stampa("Somma:", totale)
```

```output
Somma: 15
```

```pit
importa data_ora

adesso = data_ora.OraData.adesso()
con apri("diario.txt", "a", codifica="utf-8") come f:
    f.scrivi(f"Eseguito il {adesso:%d/%m/%Y alle %H:%M}\n")
stampa("Diario aggiornato")
```

```output
Diario aggiornato
```

```pit
importa formato_json

persone = {"Anna": 22, "Luca": 31, "Sara": 27}
con apri("persone.json", "w", codifica="utf-8") come f:
    formato_json.scarica(persone, f, indent=2)
con apri("persone.json", codifica="utf-8") come f:
    stampa(formato_json.carica(f))
```

```output
{'Anna': 22, 'Luca': 31, 'Sara': 27}
```
