# Menu: barra, contestuale e moderno

PitStudio offre tre componenti per i menu. Hanno in comune **come si descrivono le voci** (un albero con più valori per voce, scritto in JSON) e un unico modulo, `menu_moderno.pit`, che PitStudio mette nel progetto.

| Componente | Cosa è | Dove si vede |
|---|---|---|
| **BarraMenu** | la barra dei menu vera del sistema (File, Modifica…) | in cima alla finestra |
| **MenuContestuale** | il menu del tasto destro (o Maiusc+F10) | sopra un componente o sulla finestra |
| **MenuModerno** | un menu disegnato nella finestra: laterale o in orizzontale, con il pulsante **hamburger** | dove lo metti tu, anche dentro un Riquadro |

## Le voci: un albero con più valori

Nelle proprietà del componente premi **Modifica…**: si apre l'editor ad albero. Si aggiungono voci, sotto-voci (**a qualsiasi profondità**), separatori; si spostano (▲ ▼), si portano un livello fuori (◀) o dentro (▶), si duplicano e si eliminano. A destra i valori della voce scelta:

| Valore | Significato |
|---|---|
| **Testo** | quello che si legge nel menu |
| **Nome** | un nome per ritrovare la voce dal programma; se manca vale il testo |
| **Gestore** | il metodo chiamato alla scelta (`nuovo_clic`); PitStudio lo crea nel file della logica. `@Seconda` apre un'altra finestra del progetto. Senza gestore la voce resta spenta |
| **Scorciatoia** | `Ctrl+S`, `Ctrl+Maiusc+P`, `F5`…: funziona anche a menu chiuso |
| **Icona** | si sceglie dalla **galleria** (pulsante *Galleria…*, vedi sotto), oppure si scrive un carattere (`⌂`, `★`, `📁`) o il percorso di un file `.png` o `.gif` |
| **Tipo** | *voce*, *spunta* (si può spuntare) o *opzione* (una sola per gruppo) |
| **Gruppo** | le opzioni con lo stesso gruppo si escludono a vicenda |
| **Spuntata all'inizio**, **Attiva** | stato iniziale |

La scheda **JSON** mostra la stessa definizione e si può scrivere a mano:

```json
[
  {"testo": "File", "voci": [
    {"testo": "Nuovo", "gestore": "nuovo_clic", "scorciatoia": "Ctrl+N", "icona": "＋"},
    {"testo": "Recenti", "voci": [{"testo": "Relazione.txt", "gestore": "apri_recente"}]},
    {"testo": "-"},
    {"testo": "Altra finestra", "gestore": "@Seconda"}
  ]},
  {"testo": "Vista", "voci": [
    {"testo": "Barra di stato", "tipo": "spunta", "spuntata": true, "nome": "stato"},
    {"testo": "Piccolo", "tipo": "opzione", "gruppo": "zoom", "spuntata": true},
    {"testo": "Grande", "tipo": "opzione", "gruppo": "zoom"}
  ]}
]
```

I progetti vecchi, con il menu scritto a rientri (`File` / `  Nuovo = nuovo_clic`), si aprono senza cambiare nulla; al primo «Applica» diventano JSON.

## La galleria di icone

PitStudio ha una sua **galleria di oltre 140 icone** disegnate apposta (file, modifica, frecce, interfaccia, comunicazione, media, sviluppo e dati, oggetti). Con **Galleria…** accanto al valore *Icona* si apre una finestra con la ricerca (per nome o parola chiave: «cestino» trova *elimina*), il filtro per categoria e lo **stile**: *Monocromatico* (nero o chiaro, adatto al tema) oppure *A colori* (ogni icona col suo colore, buono su qualunque fondo); un clic sceglie, il doppio clic conferma. L'icona viene copiata nella cartella `risorse/icone` del progetto, nello stile monocromatico in due versioni, `salva.png` (scura) e `salva_chiaro.png`, e il **menu moderno** usa da solo quella adatta al tema; quella a colori è un file solo, `salva_colore.png`. La stessa galleria si apre anche dal componente **Immagine** (pulsante ☺ accanto al file).

Nei tuoi programmi: `da rad importa galleria_icone` dà `galleria_icone.scegli_icona(finestra, colori)` (la finestra di scelta), `elenco_icone()` e `file_icona("salva")`. I file stanno nella cartella `icone` di PitStudio e sono liberamente usabili.

## Dal programma

I tre componenti hanno gli stessi comandi, per nome (o per testo) della voce:

```pit sintassi
se_stesso.barraMenu1.imposta_spunta("stato", Vero)     # spunta o sceglie un'opzione (toglie le altre del gruppo)
se_stesso.barraMenu1.spuntata("stato")                 # Vero o Falso
se_stesso.barraMenu1.attiva("salva", Falso)            # spegne una voce
se_stesso.barraMenu1.imposta_testo("nuovo", "Nuovo file")
se_stesso.barraMenu1.collega("salva", se_stesso.salva) # un'altra funzione al posto del gestore
se_stesso.barraMenu1.esegui("nuovo")                   # come se la voce fosse stata scelta
```

## Il menu moderno

Un **MenuModerno** si disegna dove vuoi e cambia aspetto da solo:

- **Verticale**: ogni voce con sotto-voci si apre *sul posto*, a fisarmonica, a qualsiasi profondità. Se le voci sono più dell'altezza si scorre con la rotella o con le frecce.
- **Rientro delle sotto-voci**: la proprietà *Rientro delle sotto-voci* (18 pixel per livello, a piacere) sposta a destra le voci di ogni livello nel menu verticale esteso.
- **Orizzontale**: una barra di voci; il clic apre il sotto-menu sotto la voce, i livelli successivi si aprono di lato.
- **Hamburger** (☰): riduce il menu verticale a sole **icone** (i sotto-menu si aprono a cascata di lato) o lo chiude; il menu orizzontale chiuso mostra solo l'hamburger e, al clic, l'elenco di tutte le voci. *Stato iniziale* sceglie *esteso*, *compatto* o *chiuso*.
- **Si riduce da solo**: con *Si riduce da solo se la finestra è più stretta di…* il menu passa a icone quando la finestra si restringe e torna esteso quando c'è di nuovo spazio.
- **Ricerca dei comandi**: con la casella *Campo di ricerca* un campo in cima filtra le voci mentre scrivi (Ctrl+K lo seleziona).
- **Tastiera**: frecce, Invio, Esc.
- Il tema (chiaro, scuro, verde, viola) è quello della finestra (*Aspetto*).

Altri comandi del menu moderno: `alterna()` (come l'hamburger), `apri()`, `chiudi()`, `imposta_stato("compatto")`, `espandi("Documenti")`, `seleziona("Home")` (evidenzia la «pagina attuale»), `cerca("testo")` e `al_stato`, una funzione chiamata quando cambia stato (per adattare il resto della finestra).

Per tenerlo in un lato della finestra usa **Si aggancia ai bordi** (per esempio ◀ ▲ ▼ per una barra laterale che si allunga con la finestra), oppure mettilo dentro un **Riquadro**.

> **Da sapere.** Nel progettista il menu moderno si vede come anteprima e non risponde ai clic; si prova con **▶ Prova**. L'icona come file immagine accetta i formati che tkinter legge da solo (`.png`, `.gif`), con il percorso completo o relativo alla cartella da cui parte il programma.

## Menu contestuale

Metti un **MenuContestuale**, scegli in *Si apre col tasto destro su* il componente (vuoto = tutta la finestra) e scrivi le voci. Nel programma: `se_stesso.menuContestuale1.mostra_in(x, y)` lo apre dove vuoi.

## Senza PitStudio

Il file `menu_moderno.pit` è un normale modulo: si usa anche in programmi scritti a mano, con `menu_moderno.barra(radice, definizione, se_stesso)`, `menu_moderno.contestuale(widget, definizione, se_stesso)` e `menu_moderno.MenuModerno(genitore, definizione, se_stesso, …)`, dove la definizione è il testo JSON o la lista di dizionari. L'**esportazione in Python** lo converte come gli altri moduli.
