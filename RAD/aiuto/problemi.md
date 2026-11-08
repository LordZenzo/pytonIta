# Problemi e domande frequenti

## Il programma non parte

| Sintomo | Cosa fare |
|---|---|
| «sintassi non valida» su una riga con `if`, `for`, `def`… | stai usando parole inglesi: in un `.pit` servono `se`, `per`, `definisci`… (vedi [Il linguaggio](#linguaggio)) |
| «nel codice italiano usa Vero, Falso e Nessuno» | hai scritto `True`, `False` o `None` |
| «sintassi non valida» su un nome che sembra normale | forse è una **parola riservata** usata dove è ambigua (le parole come `classe`, `con`, `da`, `prova` sono accettate come nomi nella maggior parte dei casi, ma non a inizio istruzione). Rinominala: `cancella`, `aspetta`, `tipo_`… |
| `ModuloNonTrovato` | il modulo non esiste in pitonit: controlla il nome (usa i suggerimenti dopo `importa`). Per installare una libreria: `pitonit -m pip install nome` dalla cartella `pitonit\installazione` |
| `ErroreDiNome: il nome 'x' non è definito` | errore di battitura, o la variabile non è stata ancora creata |
| La console dice «Un programma è già in esecuzione» | premi **Ferma** (Maiusc+F5) e riprova |
| Il programma non mostra l'output finché non finisce | stai usando un'altra copia di pitonit senza `-u`; lascia l'interprete predefinito |

## L'assistente AI

| Sintomo | Cosa fare |
|---|---|
| «Manca la chiave API» | *Strumenti → Impostazioni → Assistente AI* e incolla la chiave |
| «Errore 401» | la chiave non è valida o è scaduta |
| «Errore 404 / modello non trovato» | il nome del modello è sbagliato: scegli uno dal menu della chat |
| «Errore 429» o «sovraccarico» | troppe richieste: aspetta qualche secondo e riprova |
| «Connessione non riuscita» | controlla la rete, il proxy o l'indirizzo dell'API nelle impostazioni |
| L'assistente non trova un file | i percorsi sono relativi al progetto: apri il progetto giusto |
| Non vuoi che scriva da solo | lascia attive le **conferme** nelle impostazioni |

## Aspetto

- **Le icone sono quadratini o simboli strani**: PitStudio usa il carattere *Segoe Fluent Icons* (Windows 11) o *Segoe MDL2 Assets* (Windows 10). Se mancano, ripiega su simboli semplici.
- **Il testo è troppo piccolo o troppo grande**: **Ctrl +/−**, oppure la dimensione del carattere nelle impostazioni.
- **Voglio ripartire da zero**: chiudi PitStudio e cancella `C:\Users\<tu>\.rad\config.json` (le impostazioni) — i progetti non vengono toccati.
- **Gli errori interni di PitStudio** (non dei tuoi programmi) finiscono in `C:\Users\<tu>\.rad\errori.log`.

## Domande frequenti

**Posso usare le librerie di Python?** Sì. pitonit è un Python completo: tutte le librerie installate funzionano, con i loro nomi originali o con quelli italiani.

**Un `.py` si può eseguire con pitonit?** Sì: i file `.py` restano Python normale (parole inglesi). Solo i `.pit` usano le parole chiave italiane.

**Si possono mescolare i due linguaggi?** Un modulo `.py` si può importare da un `.pit` e viceversa. Dentro lo stesso file vale una sola lingua per le parole chiave.

**Dove sono i file di PitStudio?** I programmi sono nella cartella del progetto. Le impostazioni e il registro sono in `C:\Users\<tu>\.rad`. La chat e le schede aperte di ogni progetto sono in `<progetto>\.rad`.

**Posso aprire un progetto di PitStudio in un altro editor?** Certo: sono file di testo normali (i `.pit` sono UTF-8).

**Come converto un vecchio programma Python?** In *Python → pytonIta* c'è lo strumento `py2pit.py` nella cartella `pitonit\tools`. Poi, se vuoi vederlo a mattonelle, [convertilo](#conversione).

## Informazioni

- **Versione**: vedi *Aiuto → Informazioni su PitStudio*.
- **Interprete**: pitonit, basato su CPython 3.13, con parole chiave italiane riconosciute direttamente dal parser (nessuna traduzione intermedia).
- **Cartelle**: `PitStudio` (l'applicazione) e `pitonit` (l'interprete e le librerie, con il codice sorgente delle modifiche).
