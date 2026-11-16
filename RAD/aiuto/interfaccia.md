# L'interfaccia

![Le aree della finestra di PitStudio](immagini/interfaccia.png)

## Le aree

| Area | A cosa serve |
|---|---|
| **Barra degli strumenti** (in alto) | Apri/Nuovo progetto, Salva, **Esegui** e Ferma, nuova finestra, nuovo programma a mattonelle, Cerca; a destra Assistente, Guida, Impostazioni. Passa il mouse su un pulsante per vedere il suggerimento e la scorciatoia |
| **Progetto** (a sinistra) | L'albero dei file della cartella del progetto. Doppio clic apre un file; clic destro per nuovo file, rinomina, elimina, converti… |
| **Schede** (al centro) | Ogni file aperto ha la sua scheda: editor di codice, visualizzatore di immagini/JSON/tabelle, progettista di finestre, editor a mattonelle. La **✕** chiude la scheda; un pallino ● indica modifiche non salvate |
| **Console** (sotto le schede) | L'output dei programmi, gli errori con link alla riga e la riga per scrivere all'input del programma |
| **Assistente** (a destra) | La chat con l'AI |
| **Barra di stato** (in basso) | Messaggi, posizione del cursore, versione dell'interprete e stato dell'assistente |

## Cambiare la disposizione

- Trascina i separatori tra le aree per cambiarne le dimensioni.
- Da *Visualizza* puoi nascondere il pannello Progetto, la Console e l'Assistente: utile quando serve spazio per il progettista o per le mattonelle.
- PitStudio ricorda la disposizione, le schede aperte e l'ultimo progetto: alla riapertura ritrovi tutto com'era.
- **Ctrl +** e **Ctrl −** cambiano la dimensione del testo; il tema chiaro/scuro si cambia da *Visualizza → Tema chiaro / scuro*.

## Una finestra con le schede, o una finestra per scheda

Di solito i file aperti stanno tutti nella finestra principale, in schede. Se preferisci, ogni scheda (un file, il disegno di una finestra, un database) può stare **in una finestra separata**: comoda con più monitor o per confrontare due file a fianco.

- **Visualizza → Ogni scheda in una finestra separata** (o *Impostazioni → Finestre*) sceglie come si aprono i file da ora in poi; se ci sono già schede aperte, PitStudio chiede se spostarle.
- **Stacca in una finestra**: dal tasto destro sulla linguetta, o *Visualizza → Stacca la scheda corrente in una finestra*. **Riporta la scheda corrente nella finestra principale** e **Riporta tutte le schede nella finestra principale** fanno il percorso inverso. Se la scheda ha modifiche non salvate, PitStudio chiede cosa fare (e se annulli non sposta niente).
- Ogni finestra ha la barra dei menu di PitStudio e le stesse scorciatoie (Ctrl+S salva il file di quella finestra); il titolo mostra il nome del file e il pallino ● delle modifiche. Chiudere la finestra chiude la scheda.
- La posizione e la dimensione di ogni file si ricordano; alla riapertura ritrovi le finestre dove le avevi lasciate. Le schede miste (alcune nella principale, altre in finestre) vanno benissimo.
- Il pannello Progetto, la Console e l'Assistente restano nella finestra principale. Le schede di tipo «database» (MySQL, PostgreSQL) non si possono spostare dopo l'apertura: chiudile e riaprile.

## Menu

- **File**: progetti, nuovi file, finestre e programmi a mattonelle, conversione, salva, esci.
- **Modifica**: annulla/ripeti, trova e sostituisci, vai a riga, commenta, duplica riga, suggerimenti.
- **Progetto**: cerca nel progetto, aggiungi risorse, file principale, proprietà.
- **Esegui**: esegui il file principale o quello corrente, ferma, controlla la sintassi.
- **Visualizza**: pannelli, tema, zoom. **Strumenti**: impostazioni, chiedi all'AI di spiegare/correggere, manuale pytonIta. **Aiuto**: questa guida.
