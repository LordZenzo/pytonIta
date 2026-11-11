# I trabocchetti più comuni

Pochi errori fanno perdere tempo ai principianti: quasi sempre dipendono dai nomi. PitStudio li cerca **prima** di far partire il programma. Gli errori gravi sottolineati in **rosso** nell'editor (e scritti nella barra di stato) bloccano l'esecuzione; gli avvisi in **arancione** non la bloccano. Passa il mouse sulla parola per leggere il motivo.

## 1. Una parola chiave usata come nome

Le parole del linguaggio (`classe`, `con`, `da`, `prova`, `elimina`, `produci`, `attendi`…) non si possono usare come nomi di variabili, di funzioni o di parametri.

| Non scrivere | Scrivi |
|---|---|
| `classe = "3A"` | `nome_classe = "3A"` |
| `con = sqlite3.connect(...)` | `connessione = sqlite3.connect(...)` |
| `definisci f(da, a):` | `definisci f(inizio, fine):` |
| `prova = [1, 2, 3]` | `esperimento = [1, 2, 3]` |

I **metodi** di una classe (`definisci elimina(se_stesso):`) e gli **attributi** (`oggetto.classe`) sono permessi: vivono dentro l'oggetto e non si confondono con le parole del linguaggio.

## 2. Parole inglesi al posto di quelle italiane

`pass`, `break`, `class`, `def`, `return`, `None`, `True`… sembrerebbero nomi qualunque e l'errore comparirebbe solo se la riga viene eseguita. Il controllo le blocca prima e dice come si scrivono: `pass` → `passa`, `None` → `Nessuno`, `True` → `Vero`.

## 3. `e` e `o` come nomi

`e` e `o` sono gli operatori «and» e «or». Una lettera sola non è un nome chiaro: al loro posto usa un nome intero.

| Non scrivere | Scrivi |
|---|---|
| `eccetto ErroreDiValore come e:` | `eccetto ErroreDiValore come errore:` |
| `definisci clic(e):` | `definisci clic(evento):` |
| `per e in elenco:` | `per elemento in elenco:` |

## 4. Una funzione predefinita nascosta da una variabile

Se una variabile ha lo stesso nome di una funzione del linguaggio e poi la richiami come funzione, il programma non può funzionare. Per questo i nomi italiani delle funzioni predefinite hanno un trattino basso: sono difficili da usare per caso.

| Funzione | Nome |
|---|---|
| tipi | `tipo_testo`, `tipo_lista`, `tipo_intero`, `tipo_decimale`, `tipo_dizionario`, `tipo_insieme`, `tipo_tupla`, `tipo_byte`, `oggetto_base` |
| misure | `lunghezza_di`, `somma_di`, `massimo_di`, `minimo_di`, `valore_assoluto`, `potenza_di`, `intervallo_di` |
| elenchi | `ordinato_di`, `inverso_di`, `mappa_funzione`, `tutti_veri`, `almeno_uno_vero`, `prossimo_elemento`, `iteratore_di`, `crea_fetta` |
| altro | `tipo_di`, `leggi_tastiera`, `carattere_da_codice`, `classe_base` (era `genitore`), `valuta_espressione`, `mostra_aiuto`, `variabili_di`, `nomi_locali`, `nomi_globali`, `impronta_di`, `identità_di`, `attributo_calcolato` |

I nomi come `testo`, `lista`, `lunghezza`, `somma`, `tipo` sono **liberi**: usali pure per le tue variabili. Valgono anche i nomi inglesi (`str`, `list`, `max`…): una variabile che si chiama `max` e poi viene richiamata (`max(3, 4)`) è un errore grave.

Una variabile che contiene una funzione scritta apposta (`quadrato = lambda x: x * x`) è permessa.

## Se proprio serve

- `# controlla: ok` alla fine di una riga la salta.
- `# controlla: ignora-file` nelle prime cinque righe di un file lo salta tutto.
- `PITONIT_SENZA_CONTROLLO=1` (variabile d'ambiente) spegne il controllo.
- Strumenti → Impostazioni → Editor → «Sottolinea gli errori gravi mentre scrivi» toglie solo le sottolineature, non il blocco.
- `pitonit -m _controlla programma.pit` stampa tutti gli errori e anche gli avvisi (nomi inglesi come `print`, nomi non definiti, variabili che nascondono funzioni predefinite).
