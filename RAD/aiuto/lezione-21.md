# Lezione 21 · Provare il proprio codice

**Obiettivo:** scrivere piccoli programmi che **controllano da soli** se le tue funzioni fanno quello che devono, così puoi cambiarle senza paura.

## Perché si scrivono i test

Hai scritto una funzione e l'hai provata un paio di volte a mano: funziona. Una settimana dopo la modifichi per aggiungere una cosa e, senza accorgertene, ne rompi un'altra. Un **test** è un controllo scritto una volta e rifatto in un secondo, ogni volta che vuoi.

## `asserisci`: la prova più semplice

`asserisci` verifica una condizione: se è vera non succede nulla, se è falsa il programma si ferma con un errore.

```pit
definisci media(voti):
    ritorna somma_di(voti) / lunghezza_di(voti)

asserisci media([6, 8]) == 7
asserisci media([10]) == 10
stampa("tutto bene")
```

```output
tutto bene
```

Se un controllo fallisce, l'errore ti dice quale e, se vuoi, perché:

```pit errore
definisci doppio(n):
    ritorna n + 2

asserisci doppio(5) == 10, "il doppio di 5 deve essere 10"
```

```output
Traceback (ultima chiamata per ultima):
  File "prova.pit", riga 4, in <module>
ErroreDiAsserzione: il doppio di 5 deve essere 10
```

(La funzione sommava 2 invece di moltiplicare: il test ha trovato lo sbaglio.)

## Che cosa provare

Non basta il caso comodo. Prova anche:

- un caso **normale** (`media([6, 8])`);
- un caso **limite**: un solo elemento, zero, il numero più grande ammesso;
- un caso **sbagliato** che deve dare un errore preciso.

```pit
definisci sconto(prezzo, percentuale):
    se percentuale < 0 o percentuale > 100:
        solleva ErroreDiValore("la percentuale deve stare tra 0 e 100")
    ritorna prezzo - prezzo * percentuale / 100

asserisci sconto(200, 10) == 180
asserisci sconto(50, 0) == 50
asserisci sconto(80, 100) == 0

prova:
    sconto(100, 150)
    stampa("ERRORE: doveva fallire")
eccetto ErroreDiValore:
    stampa("il caso sbagliato viene rifiutato")
```

```output
il caso sbagliato viene rifiutato
```

## Il modulo `test_unitari`

Quando i controlli sono tanti conviene organizzarli. Il modulo `test_unitari` (in inglese `unittest`) raggruppa i test in una **classe**: ogni metodo il cui nome inizia con `test_` è una prova, e alla fine ottieni un riassunto.

```pit
importa io
importa test_unitari

definisci sconto(prezzo, percentuale):
    se percentuale < 0 o percentuale > 100:
        solleva ErroreDiValore("percentuale fuori da 0-100")
    ritorna prezzo - prezzo * percentuale / 100

classe ProvaSconto(test_unitari.CasoDiTest):
    definisci test_sconto_normale(se_stesso):
        se_stesso.asserisci_uguale(sconto(200, 10), 180)

    definisci test_nessuno_sconto(se_stesso):
        se_stesso.asserisci_uguale(sconto(50, 0), 50)

    definisci test_percentuale_sbagliata(se_stesso):
        con se_stesso.asserisci_solleva(ErroreDiValore):
            sconto(100, 150)

caricatore = test_unitari.CaricatoreTest()
gruppo = caricatore.carica_test_da_caso(ProvaSconto)
esecutore = test_unitari.EsecutoreTestTestuale(stream=io.StringIO(), verbosity=0)
esito = esecutore.esegui(gruppo)
stampa("prove eseguite:", esito.testsRun)
stampa("fallite:", lunghezza_di(esito.failures) + lunghezza_di(esito.errors))
```

```output
prove eseguite: 3
fallite: 0
```

I controlli più comuni:

| Metodo | Verifica che… |
|---|---|
| `asserisci_uguale(a, b)` | `a == b` |
| `asserisci_diverso(a, b)` | `a != b` |
| `asserisci_vero(x)` / `asserisci_falso(x)` | `x` sia vero / falso |
| `asserisci_in(a, raccolta)` | `a` sia nella raccolta |
| `asserisci_quasi_uguale(a, b)` | numeri decimali quasi uguali (per gli arrotondamenti) |
| `asserisci_solleva(Errore)` | il blocco `con` sollevi quell'errore |

Di solito si scrive `test_unitari.principale()` alla fine del file: lanciandolo, esegue tutti i test e stampa un riassunto con le righe che falliscono.

## Con PitStudio: il pannello Test

Non devi lanciare i test uno per uno. Il pannello **Test** (la linguetta «Test» a sinistra) trova da solo i file che si chiamano `test_…` o `prova_…`, oppure quelli nella cartella `tests`, li esegue tutti e mostra con una spunta quali sono riusciti. Un test riesce se finisce **senza errori**: per questo `asserisci` basta. Vedi la [guida ai test del progetto](#test-progetto).

Abitudine consigliata: **quando trovi un errore, scrivi prima un test che lo mostra**, poi correggi il codice finché il test passa. Quell'errore non potrà più tornare senza che te ne accorga.

## Esercizi

1. Scrivi una funzione `e_bisestile(anno)` e controllala con `asserisci` su quattro anni: 2000 (sì), 1900 (no), 2024 (sì), 2023 (no).
2. Scrivi `massimo_di_tre(a, b, c)` e provala anche con due numeri uguali e con numeri negativi.
3. Scrivi una classe di test `ProvaTesto` con due metodi che controllano `"Ciao".maiuscolo()` e `"  a  ".elimina_spazi()` usando `asserisci_uguale`.

## Soluzioni

```pit
definisci e_bisestile(anno):
    ritorna (anno % 4 == 0 e anno % 100 != 0) o anno % 400 == 0

asserisci e_bisestile(2000)
asserisci non e_bisestile(1900)
asserisci e_bisestile(2024)
asserisci non e_bisestile(2023)
stampa("anni controllati")
```

```output
anni controllati
```

```pit
definisci massimo_di_tre(a, b, c):
    ritorna massimo_di(a, b, c)

asserisci massimo_di_tre(1, 5, 3) == 5
asserisci massimo_di_tre(4, 4, 2) == 4
asserisci massimo_di_tre(-5, -2, -9) == -2
stampa("ok")
```

```output
ok
```

```pit
importa io
importa test_unitari

classe ProvaTesto(test_unitari.CasoDiTest):
    definisci test_maiuscolo(se_stesso):
        se_stesso.asserisci_uguale("Ciao".maiuscolo(), "CIAO")

    definisci test_spazi(se_stesso):
        se_stesso.asserisci_uguale("  a  ".elimina_spazi(), "a")

gruppo = test_unitari.CaricatoreTest().carica_test_da_caso(ProvaTesto)
esito = test_unitari.EsecutoreTestTestuale(stream=io.StringIO(), verbosity=0).esegui(gruppo)
stampa(esito.testsRun, "prove, riuscite:", esito.wasSuccessful())
```

```output
2 prove, riuscite: Vero
```
