# Esportare il progetto come Python

Un programma scritto in pytonIta gira con l'interprete **pitonit**. Se lo vuoi dare a chi **non ha pytonIta**, PitStudio ne crea una **copia in Python normale** (`.py`) che funziona con qualunque Python 3.

L'originale non viene toccato.

## Come si fa

- *File → Esporta il progetto come Python…* (oppure *Progetto → Esporta il progetto come Python…*).
- Scegli la cartella in cui creare il risultato: viene creata `NomeProgetto_python` (se esiste già, `NomeProgetto_python_2`, ...).
- Alla fine PitStudio ti dice quanti file ha convertito e quali librerie servono, e puoi aprire subito la cartella.

## Cosa trovi nella cartella

| File | A cosa serve |
|---|---|
| i `.py` | il tuo codice, con parole chiave e nomi in inglese; commenti, righe e rientri restano come li avevi scritti |
| `requirements.txt` | le librerie esterne usate (per esempio `numpy`, `pandas`), con le versioni con cui il programma è stato provato |
| `installa_librerie.bat` | doppio clic su Windows: installa le librerie con `pip` |
| `installa_librerie.sh` | lo stesso per Linux e Mac |
| `LEGGIMI.txt` | come avviare il programma, scritto per chi lo riceve |
| `CONVERSIONE.md` | il rapporto: file convertiti e punti da guardare |

Chi riceve la cartella fa due cose: installa le librerie (se servono) e scrive `python principale.py`.

## Cosa viene tradotto

- le parole chiave (`se`, `per`, `ritorna`, `Vero`…);
- le funzioni e le eccezioni predefinite (`stampa`, `lunghezza`, `ErroreDiValore`…);
- i moduli italiani e i loro nomi (`matematica.radice_quadrata` diventa `math.sqrt`, `interfaccia` diventa `tkinter`…), anche negli `importa`;
- i metodi (`lista.aggiungi`, `testo.maiuscolo`, `finestra.impacchetta`…) e le opzioni con nome (`chiave=`, `testo=`, `fine=`…);
- i metodi speciali (`__inizializza__` diventa `__init__`) e `se_stesso` diventa `self`.

I nomi che hai scelto tu (variabili, funzioni, classi, metodi) non vengono toccati: se una tua classe ha un metodo che si chiama `aggiungi`, resta `aggiungi`.

## Cose da sapere

- **Nomi ambigui.** Un nome italiano può voler dire cose diverse (`aggiungi` è `append` per una lista e `add` per un insieme). Dove PitStudio capisce il tipo (`x = []`, `c = MiaClasse()`) traduce direttamente; dove non può, il programma sceglie mentre gira con una piccola funzione `_pit_attr` che trova da sola il nome giusto. Il rapporto li conta.
- **Codice dentro le stringhe.** Se il programma costruisce codice pytonIta come testo (per `esegui`/`valuta`), quel testo non viene tradotto: il rapporto lo segnala.
- **Testi stampati.** `Vero`, `Falso` e `Nessuno` diventano `True`, `False` e `None`, e i messaggi d'errore di Python sono in inglese.
- **Librerie.** Le versioni nel `requirements.txt` sono quelle di oggi: se una non esiste più per il Python di chi riceve, basta togliere il `==…` e `pip` sceglie la più recente. Serve internet.
- **tkinter.** Sui sistemi Linux può servire installare il pacchetto `python3-tk`.
