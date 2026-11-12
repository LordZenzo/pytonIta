# Scheda dei comandi

Tutto ciò che serve in una pagina. Per i dettagli: [il linguaggio](#linguaggio) · [le lezioni](#lezioni) · [le librerie](#librerie).

## Struttura del programma

| Per fare questo | Si scrive |
|---|---|
| stampare | `stampa("ciao", x)` |
| chiedere (sempre testo) | `nome = leggi_tastiera("Nome? ")` |
| commento | `# testo` |
| variabile | `eta = 12` · `eta += 1` |
| f-testo | `f"{nome} ha {eta} anni"` |
| scelta | `se c:` · `altrimenti_se c2:` · `altrimenti:` |
| ciclo su elementi | `per x in lista:` |
| ciclo con contatore | `per i in intervallo_di(1, 11):` |
| ciclo con condizione | `mentre c:` |
| uscire / saltare | `interrompi` · `continua` |
| non fare nulla | `passa` |
| funzione | `definisci f(a, b=1):` … `ritorna valore` |
| classe | `classe Cane:` · `definisci __inizializza__(se_stesso, nome):` |
| ereditare | `classe Gatto(Animale):` |
| errori | `prova:` · `eccetto ErroreDiValore come errore:` · `infine:` |
| sollevare un errore | `solleva ErroreDiValore("messaggio")` |
| file | `con apri("a.txt", codifica="utf-8") come f:` |
| importare | `importa matematica` · `da matematica importa pi` · `importa x come y` |
| variabile globale | `globale contatore` |
| funzione senza nome | `lambda x: x * 2` |
| generatore | `produci valore` |
| cancellare | `elimina lista[0]` |

## Valori e operatori

| | |
|---|---|
| costanti | `Vero` `Falso` `Nessuno` |
| aritmetica | `+ - * / // % **` |
| confronti | `== != < > <= >=` |
| logica | `e` `o` `non` |
| appartenenza | `x in lista` · `x non in lista` |
| identità | `x è Nessuno` · `x è non Nessuno` |
| liste, tuple, insiemi, dizionari | `[1, 2]` · `(1, 2)` · `{1, 2}` · `{"a": 1}` |
| fette | `voti[0]` · `voti[-1]` · `voti[1:3]` · `voti[::-1]` |

## Funzioni predefinite più usate

| | |
|---|---|
| `lunghezza_di(x)` | quanti elementi |
| `tipo_intero(x)` `tipo_decimale(x)` `tipo_testo(x)` | converte |
| `tipo_lista(x)` `tipo_insieme(x)` `tipo_dizionario(x)` | crea |
| `intervallo_di(n)` | 0 … n−1 |
| `somma_di(x)` `massimo_di(x)` `minimo_di(x)` | totali |
| `ordinato_di(x)` | copia ordinata (`inverso=Vero`, `chiave=…`) |
| `enumera(x, inizio=1)` | posizione + elemento |
| `abbina(a, b)` | coppie |
| `arrotonda(x, 2)` `valore_assoluto(x)` | numeri |
| `tipo_di(x)` · `è_istanza(x, T)` | tipo di un valore |
| `tutti_veri(x)` · `almeno_uno_vero(x)` | tutti veri / almeno uno vero |
| `apri(nome, modalita)` | apre un file (`"r"` `"w"` `"a"`) |

## Metodi

| Tipo | Metodi |
|---|---|
| **lista** | `aggiungi` `inserisci` `rimuovi` `estrai` `ordina` `inverti` `indice` `conta` `estendi` `svuota` `copia` |
| **testo** | `maiuscolo` `minuscolo` `titolo` `elimina_spazi` `sostituisci` `separa` `unisci` `trova` `conta` `inizia_con` `finisce_con` `formatta` `è_cifra` `è_alfabetico` |
| **dizionario** | `chiavi` `valori` `elementi` `ottieni` `aggiorna` `estrai` `imposta_predefinito` |
| **insieme** | `aggiungi` `scarta` `unione` `intersezione` `differenza` |
| **file** | `leggi_tutto` `leggi_riga` `leggi_righe` `scrivi` `chiudi` |

## Errori più frequenti

`ErroreDiSintassi` · `ErroreDiIndentazione` · `ErroreDiNome` · `ErroreDiTipo` · `ErroreDiValore` · `ErroreDiIndice` · `ErroreDiChiave` · `DivisionePerZero` · `FileNonTrovato` · `ModuloNonTrovato`

## Librerie principali

`matematica` · `casuale` · `tempo` · `data_ora` · `sistema` · `sistema_operativo` · `percorso` · `formato_json` · `tabelle_csv` · `espressioni_regolari` · `collezioni` · `statistica` · `database` · `interfaccia` (finestre) · `richieste` (web) — elenco completo e pannello **Librerie** a sinistra.

## Scorciatoie di PitStudio

| | |
|---|---|
| **F5** esegui · **Maiusc+F5** ferma | **F6** debug · **F9** punto di arresto |
| **F10** passo · **F11** entra · **Maiusc+F11** esci | **Ctrl+Spazio** suggerimenti |
| **F1** guida sulla parola | **Ctrl+S** salva · **Ctrl+F** cerca |

## Esempio completo

```pit
definisci media(voti):
    ritorna somma_di(voti) / lunghezza_di(voti)

voti = [7, 8, 6]
per i, v in enumera(voti, 1):
    stampa(f"{i}) {v}")
stampa("Media:", arrotonda(media(voti), 1))
```

```output
1) 7
2) 8
3) 6
Media: 7.0
```
