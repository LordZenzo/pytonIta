# Lezione 11 · Gli errori

**Obiettivo:** capire i messaggi d'errore e gestire i problemi senza far fermare il programma.

## Gli errori non sono un fallimento

Tutti i programmatori sbagliano, ogni giorno. L'importante è **leggere il messaggio**: dice cosa è successo e dove. Un errore compare così nella console:

```pit errore
etichetta = "voti"
stampa(etichetta + 5)
```

```esempio
Traceback (ultima chiamata per ultima):
  File "lezioni.pit", riga 2, in <module>
    stampa(etichetta + 5)
           ~~~~~~~~~~^~~
ErroreDiTipo: si può concatenare solo testo a testo (trovato "int")

✖ terminato con codice 1 (0.1 s)
💡 Non si può unire testo e numero con «+». Converti il numero in testo, ...
```

Come si legge, **dal basso verso l'alto**:

1. l'ultima riga è il **tipo di errore** (`ErroreDiTipo`) e il motivo;
2. sopra c'è **dove**: il file e la **riga** (clicca sul nome del file nella console per saltarci nell'editor);
3. la riga con 💡 è il **suggerimento di PitStudio**: cosa controllare per correggere.

## Gli errori più comuni

| Errore | Quando succede |
|---|---|
| `ErroreDiSintassi` | il codice è scritto male: manca un `:`, una parentesi, una virgoletta |
| `ErroreDiIndentazione` | il rientro è sbagliato |
| `ErroreDiNome` | hai usato un nome che non esiste (errore di battitura, variabile non creata) |
| `ErroreDiTipo` | hai combinato tipi incompatibili (testo + numero) |
| `ErroreDiValore` | il tipo è giusto ma il valore no (`tipo_intero("abc")`) |
| `ErroreDiIndice` | hai chiesto un elemento oltre la fine di una lista |
| `ErroreDiChiave` | la chiave non c'è nel dizionario |
| `DivisionePerZero` | hai diviso per zero |
| `FileNonTrovato` | il file non esiste |

I primi due (sintassi e indentazione) vengono segnalati **mentre scrivi**: la riga si colora di rosso e il messaggio compare nella barra di stato.

## Gestire gli errori: prova / eccetto

A volte l'errore è prevedibile (l'utente scrive «ciao» dove serve un numero). Con `prova` provi a eseguire il codice; se va male, `eccetto` decide cosa fare invece di far fermare tutto:

```pit
testo_numero = "abc"
prova:
    n = tipo_intero(testo_numero)
    stampa("Hai scritto", n)
eccetto ErroreDiValore:
    stampa("Non è un numero valido")
stampa("Il programma continua")
```

```output
Non è un numero valido
Il programma continua
```

Puoi gestire errori diversi in modo diverso, e leggere il messaggio con `come`:

```pit
definisci dividi(a, b):
    prova:
        ritorna a / b
    eccetto DivisionePerZero:
        stampa("Non si divide per zero!")
        ritorna Nessuno
    eccetto ErroreDiTipo come errore:
        stampa("Tipi non validi:", errore)
        ritorna Nessuno

stampa(dividi(10, 4))
stampa(dividi(1, 0))
stampa(dividi("a", 2))
```

```output
2.5
Non si divide per zero!
Nessuno
Tipi non validi: tipi di operando non supportati per /: 'str' e 'int'
Nessuno
```

`infine` (opzionale) contiene codice che gira **sempre**, qualunque cosa accada:

```pit
prova:
    stampa("provo")
    1 / 0
eccetto DivisionePerZero:
    stampa("errore gestito")
infine:
    stampa("pulizia finale")
```

```output
provo
errore gestito
pulizia finale
```

## Un ciclo che insiste finché l'utente scrive bene

```pit
mentre Vero:
    prova:
        eta = tipo_intero(leggi_tastiera("Quanti anni hai? "))
        interrompi
    eccetto ErroreDiValore:
        stampa("Scrivi un numero intero, per favore.")
stampa("Hai", eta, "anni")
```

```esempio
Quanti anni hai? boh
Scrivi un numero intero, per favore.
Quanti anni hai? 14
Hai 14 anni
```

## Sollevare un errore

Puoi essere **tu** a fermare il programma quando qualcosa non va, con `solleva`:

```pit
definisci radice(n):
    se n < 0:
        solleva ErroreDiValore("il numero deve essere positivo")
    ritorna n ** 0.5

prova:
    stampa(radice(16))
    stampa(radice(-4))
eccetto ErroreDiValore come errore:
    stampa("Errore:", errore)
```

```output
4.0
Errore: il numero deve essere positivo
```

## Errori «pigri»

Evita `eccetto:` vuoto o `eccetto Eccezione:` per tutto: nasconderebbe anche i tuoi sbagli. Cattura **solo** gli errori che sai gestire.

## Esercizi

1. Scrivi una funzione `numero_sicuro(testo)` che restituisce il numero intero, o `Nessuno` se il testo non è valido.
2. Fai leggere un indice da 0 a 2 e stampa l'elemento corrispondente di `["a", "b", "c"]`, gestendo `ErroreDiIndice` e `ErroreDiValore`.
3. Prova a far comparire apposta quattro errori diversi e leggi ogni suggerimento 💡.

## Soluzioni

```pit
definisci numero_sicuro(t):
    prova:
        ritorna tipo_intero(t)
    eccetto ErroreDiValore:
        ritorna Nessuno

stampa(numero_sicuro("42"), numero_sicuro("zzz"))
```

```output
42 Nessuno
```

```pit
lettere = ["a", "b", "c"]
prova:
    i = tipo_intero(leggi_tastiera("Indice (0-2): "))
    stampa(lettere[i])
eccetto ErroreDiValore:
    stampa("Non è un numero")
eccetto ErroreDiIndice:
    stampa("Indice fuori dall'elenco")
```
