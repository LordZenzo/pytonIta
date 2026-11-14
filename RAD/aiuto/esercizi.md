# Esercizi guidati

Gli esercizi guidati ti fanno **scrivere il codice tu** e lo **controllano da soli**. Si aprono da *Aiuto → Esercizi guidati…* (o dalla carta «Esercizi guidati» della schermata di benvenuto).

## Come si fa

1. Scegli un esercizio dall'elenco: a destra c'è la **consegna** (cosa deve fare il programma) con un esempio.
2. Premi **Apri nell'editor**: PitStudio crea il file dell'esercizio nella cartella `esercizi` del progetto (se non hai un progetto aperto ne crea uno chiamato «Esercizi») con un po' di codice già pronto.
3. Scrivi il programma. Per leggere i dati usa `leggi_tastiera()` come nelle lezioni, per rispondere usa `stampa()`.
4. Premi **▶ Controlla**: il tuo programma viene eseguito più volte con ingressi diversi e l'uscita viene confrontata con quella attesa.
5. Se una prova non passa, ti dico cosa mi aspettavo e cosa ha scritto il tuo programma; se il programma va in errore o non finisce mai, lo dico. Gli spazi a fine riga e le righe vuote finali non contano.

Se ti blocchi, **💡 Suggerimento** dà un aiuto alla volta (dal più generico al più preciso) e **Soluzione** mostra una soluzione possibile: prova prima da solo!

Accanto a ogni esercizio compare ✓ quando l'hai risolto, e in fondo vedi quanti ne hai completati. I progressi restano salvati.

## Gli esercizi

Ventitré esercizi in ordine di difficoltà: stampare, numeri e variabili, decisioni con `se`, cicli, liste, stringhe, funzioni, dizionari, classi, e poi tuple e insiemi, comprehension, ricorsione, generatori, oggetti con metodi speciali, database SQLite e test.

## Per le classi

Il pulsante **Classe ▾** serve a insegnanti e allievi:

- **Esporta i miei progressi…** (allievo): salva in un file `.json` chi sei e quali esercizi hai completato, con il numero di tentativi. Il file si consegna all'insegnante.
- **Report della classe…** (insegnante): scegli i file dei progressi degli allievi e vedi una tabella con quanti esercizi ha fatto ognuno e quali sono i più difficili (i meno completati). Si può copiare negli appunti.
- **Crea un pacchetto con i miei esercizi…** (insegnante): mette in **un solo file** (`.pitesercizi`) tutti gli esercizi delle tue cartelle, con un titolo. Lo mandi agli allievi e basta.
- **Importa un pacchetto di esercizi…** (allievo): apre un file `.pitesercizi` dell'insegnante; gli esercizi compaiono nell'elenco. Il pacchetto contiene solo esercizi (file `.json`), mai programmi.
- Il file dei progressi comprende anche i **quiz delle lezioni** (quali sono superate e con che punteggio), e il report della classe mostra la colonna «Lezioni superate».
- **Aggiungi una cartella di esercizi…** (insegnante): puoi scrivere **esercizi tuoi** come file `.json` in una cartella e dare la cartella agli allievi. Ogni file contiene:

```
{
  "id": "somma_tre", "titolo": "Somma di tre numeri", "argomento": "Variabili", "livello": "Principiante",
  "consegna": "Leggi tre numeri e stampa la somma.",
  "iniziale": "# scrivi qui il tuo codice\n",
  "prove": [ {"ingresso": "1\n2\n3\n", "uscita": "6"}, {"ingresso": "0\n0\n0\n", "uscita": "0"} ],
  "suggerimenti": ["Leggi i numeri con leggi_tastiera() e trasformali con tipo_intero()."],
  "soluzione": "a = tipo_intero(leggi_tastiera(''))\n...",
  "ordine": 100
}
```
