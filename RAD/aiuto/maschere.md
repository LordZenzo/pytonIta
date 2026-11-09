# Maschere collegate ai dati

Una **maschera** è una finestra che mostra e modifica i record di una tabella: un elenco, i campi di un record e i pulsanti per cercare, aggiungere, salvare ed eliminare. PitStudio la crea **da solo** partendo da una tabella.

![Una maschera creata dalla tabella «clienti»](immagini/maschera.png)

## Come si crea

1. Apri un progetto e il database (SQLite o MySQL, vedi «I database»).
2. Nella scheda del database scegli a sinistra la tabella.
3. Premi **▤ Maschera…** (oppure *Database → Crea una maschera dalla tabella…*) e scrivi il nome della finestra.

PitStudio crea nel progetto:

| File | A cosa serve |
|---|---|
| `nome.form.json` e `nome_ui.pit` | la finestra, che si modifica **nel progettista** (la apre subito) |
| `nome.pit` | la logica già scritta: apre il database e collega i pulsanti. È tuo: aggiungici il codice che vuoi |
| `fonte_dati.pit` | il collegamento ai dati, usabile anche da altre finestre |

Per provarla: nel file `nome.pit` scegli *Esegui → Esegui il file corrente*.

## Cosa fa la maschera

- **Elenco** dei record (fino a 2000): scegliendone uno compaiono i suoi valori nei campi.
- **Cerca** trova i record che contengono il testo in una qualunque colonna; **Tutti** toglie la ricerca.
- **Nuovo** svuota i campi; **Salva** aggiunge il record o aggiorna quello scelto; **Elimina** lo toglie (chiede conferma); **Annulla** torna ai valori salvati.
- Controlla i dati prima di scrivere: un campo obbligatorio (*NOT NULL* senza valore predefinito) deve essere compilato e un campo numerico deve contenere un numero (la virgola va bene: `2,5`).
- Le colonne che il database riempie da solo (chiave con auto-incremento) si lasciano vuote.

## Personalizzarla

Apri la finestra nel progettista: sposta i campi, cambia i testi, i colori e il carattere, aggiungi altri componenti. I campi si chiamano `campo_<colonna>`, l'elenco `elenco_dati`, la riga di stato `etichetta_stato`.

Per fare lo stesso con una finestra disegnata a mano usa `fonte_dati`:

```
da fonte_dati importa FonteDati, MascheraDati

fonte = FonteDati.sqlite("dati.db", "clienti")
maschera = MascheraDati(fonte, se_stesso.elenco, {"nome": se_stesso.campo_nome, "citta": se_stesso.campo_citta}, se_stesso.stato)
maschera.ricarica()
```

Per MySQL: `FonteDati.con_mysql(server, porta, utente, password, database, "clienti")`. Nelle maschere create da PitStudio la **password viene chiesta all'avvio** e non è mai scritta nel file.

## Dopo

- *Esporta il progetto come Python* e *Crea l'eseguibile (.exe)* funzionano anche con le maschere: il database SQLite del progetto viene copiato insieme al resto.
