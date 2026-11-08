# Il progettista di finestre

Il progettista ti fa costruire una finestra con il mouse. Non devi scrivere il codice dell'aspetto: PitStudio lo genera, e tu scrivi solo quello che succede quando l'utente fa qualcosa.

![Il progettista](immagini/progettista.png)

## Creare una finestra

*File → Nuova finestra (progettista)…* (o il pulsante nella barra). Scegli un nome (lettere, cifre e `_`, senza parole riservate). Si apre la scheda con tre colonne:

1. **Componenti** (palette): l'elenco di ciò che puoi inserire.
2. **La finestra**: l'area di disegno con la griglia.
3. **Proprietà**: le impostazioni del componente scelto (o della finestra, se non hai scelto niente).

## Inserire e muovere i componenti

- Scegli un componente nella palette e **clicca sulla finestra** per inserirlo (o fai doppio clic nella palette).
- **Trascina** un componente per spostarlo; usa le **otto maniglie** blu per ridimensionarlo. Con la griglia attiva si allinea a passi di 8 punti.
- **Maiusc+clic** aggiunge alla selezione; **Ctrl+A** seleziona tutto. Le **frecce** spostano di un punto (con Maiusc di dieci).
- **Ctrl+C / Ctrl+V**, **Ctrl+D** copiano e duplicano; **Canc** elimina; **Ctrl+Z / Ctrl+Y** annullano e ripetono.
- Il menu **Allinea** dispone più componenti: a sinistra, a destra, in alto, in basso, centrati, stessa larghezza o altezza, distribuiti in modo uniforme.

## I componenti

| Componente | Per cosa serve |
|---|---|
| **Pulsante** | un pulsante con evento *clic* |
| **Etichetta** | testo fisso, con allineamento |
| **CampoTesto** | una riga di testo (anche nascosta, per le password); evento *Invio* |
| **AreaTesto** | testo su più righe |
| **Elenco** | un elenco di voci; evento *selezione* |
| **CasellaSelezione** | una casella da spuntare |
| **PulsanteOpzione** | scelta tra più opzioni dello stesso *gruppo* |
| **Cursore** | un cursore con minimo, massimo e valore; evento *cambio* |
| **CasellaCombinata** | un menu a tendina |
| **BarraProgresso** | una barra di avanzamento |
| **Albero** | una tabella con colonne (anche gerarchica) |
| **Tela** | un'area dove disegnare |
| **Riquadro** | un contenitore decorativo con bordo |
| **Immagine** | un'immagine presa dal progetto |
| **Separatore** | una linea |

## Le proprietà e gli eventi

Cambiando una proprietà (testo, colori, carattere, stato normale/disabilitato…) il componente si aggiorna subito. Il campo **Nome** è il nome con cui lo userai nel codice
(`se_stesso.pulsante1`).

Un campo **Evento** contiene il nome di una funzione. Scrivilo (o premi **⏎**: PitStudio propone `al_clic_pulsante1`) e PitStudio:
1. salva il disegno e rigenera la finestra;
2. aggiunge la funzione vuota nel file della logica;
3. ti porta alla funzione, pronta da riempire. Anche un **doppio clic** sul componente apre il suo gestore.

## I tre file di una finestra

| File | Contenuto | Si modifica? |
|---|---|---|
| `nome.form.json` | il disegno (componenti, posizioni, proprietà) | dal progettista |
| `nome_ui.pit` | il codice che costruisce la finestra | **no**: viene riscritto a ogni salvataggio |
| `nome.pit` | la tua logica: una classe che eredita la finestra e contiene i gestori | **sì**, è tuo |

Quando aggiungi un evento PitStudio aggiunge in `nome.pit` solo la funzione che manca e non tocca il resto. Per provare la finestra: **Prova** nella barra del progettista.

## Esempio

```pit
classe Saluto(SalutoUI):
    definisci __inizializza__(se_stesso, radice):
        se_stesso.costruisci_ui(radice)

    definisci al_clic_saluta(se_stesso, evento=Nessuno):
        nome = se_stesso.campoTesto1.ottieni()
        se_stesso.etichetta1.configura(testo=f"Ciao, {nome}!")
```

> **Nota:** la finestra usa posizioni assolute (in punti): è semplice e prevedibile. Se ti serve una finestra ridimensionabile con componenti che si adattano, scrivi il codice con `impacchetta`/`griglia` nel file della logica.
