# Il linguaggio pytonIta

pytonIta è **Python con le parole in italiano**: stessa logica, stesse librerie, ma le parole chiave, le funzioni predefinite, i metodi dei tipi base, le eccezioni e i messaggi di errore sono in italiano.
I programmi sono file `.pit` e si eseguono con l'interprete **pitonit**. Un programma pytonIta fa esattamente ciò che farebbe il programma Python equivalente.

```pit
definisci fattoriale(n):
    se n <= 1:
        ritorna 1
    ritorna n * fattoriale(n - 1)


per i in intervallo(1, 6):
    stampa(i, "! =", fattoriale(i))
```

## Parole chiave

Nei file `.pit` valgono **solo** le parole chiave italiane (quelle inglesi diventano nomi qualsiasi). Cerca una parola nel campo di ricerca della guida, oppure premi F1 sulla parola nell'editor.

| Italiano | Inglese | Significato |
|---|---|---|
| `se` · `altrimenti_se` · `altrimenti` | `if` · `elif` · `else` | scelta tra alternative |
| `per … in …` | `for … in …` | ripete per ogni elemento |
| `mentre` | `while` | ripete finché la condizione è vera |
| `interrompi` · `continua` | `break` · `continue` | esce dal ciclo · salta al prossimo giro |
| `definisci` | `def` | crea una funzione |
| `ritorna` | `return` | restituisce un valore |
| `produci` | `yield` | produce un valore alla volta (generatore) |
| `classe` | `class` | crea una classe |
| `importa` · `da … importa` · `come` | `import` · `from … import` · `as` | usa altri moduli |
| `prova` · `eccetto` · `infine` · `solleva` | `try` · `except` · `finally` · `raise` | gestione degli errori |
| `con` | `with` | gestore di contesto (es. file aperti) |
| `e` · `o` · `non` | `and` · `or` · `not` | operatori logici |
| `è` · `è non` | `is` · `is not` | identità |
| `in` · `non in` | `in` · `not in` | appartenenza |
| `Vero` · `Falso` · `Nessuno` | `True` · `False` · `None` | costanti |
| `passa` | `pass` | non fa nulla |
| `globale` · `nonlocale` | `global` · `nonlocal` | variabili di altri ambiti |
| `lambda` | `lambda` | funzione senza nome |
| `asserisci` | `assert` | verifica una condizione |
| `elimina` | `del` | elimina un nome o un elemento |
| `asincrono` · `attendi` | `async` · `await` | programmazione asincrona |
| `confronta` · `caso` | `match` · `case` | confronto di strutture |
| `tipo` | `type` | definisce un alias di tipo |

La scelta in una riga si scrive con `X se condizione altrimenti Y` (come `X if condizione else Y`).

## Regole da ricordare

- **`Vero`, `Falso`, `Nessuno`**: scrivere `True`, `False` o `None` in un file `.pit` dà un errore che spiega cosa usare.
- **Parole riservate come nomi**: parole italiane molto naturali come `classe`, `con` (connessione), `prova`, `da`, `elimina`, `produci` sono anche parole chiave. L'interprete le sa leggere come nomi, ma **il controllo che gira prima dell'esecuzione le considera un errore grave e il programma non parte**: scegli un altro nome (`nome_classe`, `connessione`, `esperimento`, `cancella`, `aspetta`…). Fanno eccezione gli *attributi* (`oggetto.classe`) e i *metodi* (`definisci elimina(se_stesso):` dentro una classe). Le lettere `e` e `o` sono gli operatori «and» e «or»: neppure come nomi di una lettera sola si possono usare (scrivi `evento`, `errore`, `elemento`).
- **Parole chiave inglesi**: `pass`, `class`, `def`, `return`… sarebbero nomi qualunque e l'errore comparirebbe solo se la riga viene eseguita. Il controllo le blocca prima e dice come si scrivono in italiano (`pass` → `passa`).
- **Funzioni predefinite nascoste**: `testo = "ciao"` seguito da `testo(5)` non può funzionare, perché la variabile ha preso il posto della funzione `testo()`. Lo stesso vale per `lista`, `tipo`, `somma`, `massimo`, `minimo`, `mappa`, `intervallo`, `leggi`… e per i nomi inglesi (`str`, `list`…). Se la variabile viene richiamata come funzione il programma non parte. Una variabile con quel nome che non viene mai richiamata è lecita, e così `nome = lambda ...` (è una funzione scritta apposta).
- **Il controllo**: parte da solo quando lanci un file `.pit` e quando importi un modulo `.pit`. Per vedere anche gli avvisi (nomi inglesi come `print`, nomi non definiti, variabili che nascondono funzioni predefinite) usa `pitonit -m _controlla programma.pit`. Una riga con il commento `# controlla: ok` viene saltata; `# controlla: ignora-file` nelle prime cinque righe salta tutto il file; la variabile d'ambiente `PITONIT_SENZA_CONTROLLO=1` lo spegne.
- **`e` e `o` sono operatori, non nomi**: una variabile `e` (evento, errore) o `o` (oggetto) è un errore grave del controllo e il programma non parte. Scrivi `eccetto ErroreDiValore come errore:`, `lambda evento: ...`, `per elemento in lista`.
- **Il primo parametro dei metodi** si chiama per convenzione `se_stesso` (è `self`); `__inizializza__` è `__init__`, `__testo__` è `__str__`, `__lunghezza__`, `__uguale__`, `__somma__`, `__chiama__`, `__entra__`/`__esci__`, `__nome__`…
- Il **nome inglese continua a funzionare** per funzioni, metodi, moduli ed eccezioni: `print` e `stampa` sono la stessa cosa, come `ValueError` e `ErroreDiValore`. Solo le *parole chiave* e le tre costanti sono solo italiane.

## Opzioni con nome in italiano

Le funzioni più comuni accettano le opzioni **anche in italiano** (quelle inglesi continuano a funzionare):

| Funzione | Opzioni |
|---|---|
| `stampa(...)` | `separatore=`, `fine=`, `svuota=` |
| `ordinato(x)` e `lista.ordina()` | `chiave=`, `inverso=` |
| `massimo(x)` / `minimo(x)` | `chiave=`, `predefinito=` |
| `somma(x)` | `inizio=` |
| `arrotonda(x)` | `cifre=` |
| `enumera(x)` | `inizio=` |
| `abbina(a, b)` | `rigoroso=` |
| `apri(nome)` | `modalita=`, `codifica=`, `errori=`, `a_capo=` |
| `testo.separa()` | `separatore=`, `max_divisioni=` |
| `testo.codifica()`, `byte.decodifica()` | `codifica=`, `errori=` |

```pit
stampa("a", "b", separatore="-")
stampa(ordinato([3, 1, 2], inverso=Vero))
```

```output
a-b
[3, 2, 1]
```

## Funzioni predefinite

{{funzioni_predefinite}}

## Metodi dei tipi base

| Tipo | Metodi |
|---|---|
| **lista** | `aggiungi`, `estendi`, `inserisci`, `rimuovi`, `estrai`, `ordina`, `inverti`, `conta`, `indice`, `svuota`, `copia` |
| **dizionario** | `chiavi`, `valori`, `elementi`, `ottieni`, `aggiorna`, `imposta_predefinito`, `estrai_ultimo` |
| **insieme** | `aggiungi`, `scarta`, `unione`, `intersezione`, `differenza`, `è_sottoinsieme` |
| **testo** | `separa`, `unisci`, `maiuscolo`, `minuscolo`, `titolo`, `capitalizza`, `elimina_spazi`, `sostituisci`, `formatta`, `inizia_con`, `finisce_con`, `trova`, `è_cifra`, `è_alfabetico`… |
| **file** | `leggi_tutto`, `leggi_riga`, `leggi_righe`, `scrivi`, `scrivi_righe`, `chiudi`, `posiziona` |

## Eccezioni

{{eccezioni}}

## Un esempio completo

```pit
importa formato_json
da percorso importa Percorso


classe Rubrica:
    definisci __inizializza__(se_stesso, file):
        se_stesso.file = Percorso(file)
        se_stesso.contatti = {}
        se se_stesso.file.esiste():
            se_stesso.contatti = formato_json.carica_testo(se_stesso.file.leggi_testo())

    definisci aggiungi(se_stesso, nome, telefono):
        se_stesso.contatti[nome] = telefono
        se_stesso.file.scrivi_testo(formato_json.scarica_testo(se_stesso.contatti, rientro=2))

    definisci __testo__(se_stesso):
        ritorna "\n".join(f"{n}: {t}" per n, t in sorted(se_stesso.contatti.elementi()))


rubrica = Rubrica("rubrica.json")
prova:
    nome = leggi("Nome? ")
    rubrica.aggiungi(nome, leggi("Telefono? "))
eccetto InterruzioneDaTastiera:
    stampa("Annullato")
stampa(rubrica)
```
