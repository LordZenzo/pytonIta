# Lezione 15 · Le finestre

**Obiettivo:** creare un programma con una finestra, pulsanti e caselle di testo.

## Finora: la console. Adesso: la grafica

I programmi con finestre si basano sulla libreria `interfaccia`. Ogni elemento (etichetta, pulsante, casella) si chiama **widget**. Un programma grafico non va dall'alto in basso e finisce: **resta in attesa** degli eventi (clic, tasti) fino alla chiusura della finestra.

## La finestra più piccola

```pit sintassi
importa interfaccia come tk

finestra = tk.Finestra()
finestra.title("La mia prima finestra")
finestra.geometry("320x160")

etichetta = tk.Etichetta(finestra, testo="Ciao dal mondo grafico!")
etichetta.impacchetta(pady=40)

finestra.ciclo_principale()
```

Provala con **F5**: compare una finestra. `ciclo_principale()` è la riga che la tiene aperta. `impacchetta()` dice di collocare il widget nella finestra.

## Un pulsante che fa qualcosa

Un pulsante ha un **comando**: la funzione da eseguire quando lo clicchi.

```pit sintassi
importa interfaccia come tk

contatore = 0

definisci incrementa():
    globale contatore
    contatore += 1
    etichetta.configure(text=f"Clic: {contatore}")

finestra = tk.Finestra()
finestra.title("Contatore")
etichetta = tk.Etichetta(finestra, testo="Clic: 0", font=("Segoe UI", 20))
etichetta.impacchetta(padx=40, pady=20)
tk.Pulsante(finestra, testo="Clicca qui", comando=incrementa).impacchetta(pady=(0, 20))
finestra.ciclo_principale()
```

Nota `comando=incrementa` **senza parentesi**: passi la funzione, non la esegui subito.

## Leggere cosa ha scritto l'utente

```pit sintassi
importa interfaccia come tk

definisci saluta():
    nome = casella.get().elimina_spazi()
    risultato.configure(text=f"Ciao, {nome}!" se nome altrimenti "Scrivi il tuo nome")

finestra = tk.Finestra()
finestra.title("Saluto")
tk.Etichetta(finestra, testo="Come ti chiami?").impacchetta(padx=30, pady=(20, 4))
casella = tk.Casella(finestra, width=30)
casella.impacchetta(padx=30)
tk.Pulsante(finestra, testo="Saluta", comando=saluta).impacchetta(pady=10)
risultato = tk.Etichetta(finestra, testo="", font=("Segoe UI", 14))
risultato.impacchetta(pady=(0, 20))
finestra.ciclo_principale()
```

## Una calcolatrice di sconti

Mettiamo insieme caselle, un pulsante e un risultato, gestendo anche gli errori:

```pit sintassi
importa interfaccia come tk

definisci calcola():
    prova:
        prezzo = tipo_decimale(prezzo_casella.get().sostituisci(",", "."))
        sconto = tipo_decimale(sconto_casella.get().sostituisci(",", "."))
    eccetto ErroreDiValore:
        risultato.configure(text="Inserisci due numeri", fg="red")
        ritorna
    finale = prezzo * (1 - sconto / 100)
    risultato.configure(text=f"Prezzo finale: {finale:.2f} €", fg="black")

finestra = tk.Finestra()
finestra.title("Sconti")
tk.Etichetta(finestra, testo="Prezzo (€)").grid(row=0, column=0, padx=10, pady=8, sticky="e")
prezzo_casella = tk.Casella(finestra)
prezzo_casella.grid(row=0, column=1, padx=10)
tk.Etichetta(finestra, testo="Sconto (%)").grid(row=1, column=0, padx=10, pady=8, sticky="e")
sconto_casella = tk.Casella(finestra)
sconto_casella.grid(row=1, column=1, padx=10)
tk.Pulsante(finestra, testo="Calcola", comando=calcola).grid(row=2, column=0, columnspan=2, pady=10)
risultato = tk.Etichetta(finestra, testo="")
risultato.grid(row=3, column=0, columnspan=2, pady=(0, 14))
finestra.ciclo_principale()
```

Qui i widget sono collocati con `grid(row, column)`, una **griglia**: più ordinata quando hai molte caselle.

## Il progettista di finestre di PitStudio

Scrivere a mano la posizione di ogni widget è faticoso: PitStudio ha un **progettista grafico**.

1. *File → Nuova finestra* (o il pulsante 🪟 nella barra).
2. **Trascina** dalla palette (a sinistra) pulsanti, etichette e caselle sulla finestra; muovili e ridimensionali con il mouse.
3. Nel pannello **Proprietà** cambi testo, colori, nome del widget e il **gestore del clic**.
4. Premi **Esegui** per provare la finestra, oppure genera il codice `.pit` e continua a mano.

È il modo più veloce per costruire l'aspetto; poi scrivi tu la logica con le funzioni che hai imparato.

## Il mondo a blocchi

Se preferisci costruire la logica con i blocchi colorati, prova i [programmi a mattonelle](#mattonelle).

## Esercizi

1. Modifica il contatore aggiungendo un pulsante **Azzera**.
2. Crea una finestra con una casella e un pulsante che mostra la **lunghezza** del testo scritto.
3. Costruisci con il progettista una finestra con due pulsanti, **Rosso** e **Verde**, che cambiano il colore di sfondo di un'etichetta (suggerimento: `etichetta.configure(bg="red")`).

## Soluzione (esercizio 2)

```pit sintassi
importa interfaccia come tk

definisci misura():
    risultato.configure(text=f"{lunghezza_di(casella.get())} caratteri")

finestra = tk.Finestra()
finestra.title("Lunghezza")
casella = tk.Casella(finestra, width=30)
casella.impacchetta(padx=20, pady=(20, 8))
tk.Pulsante(finestra, testo="Misura", comando=misura).impacchetta()
risultato = tk.Etichetta(finestra, testo="")
risultato.impacchetta(pady=16)
finestra.ciclo_principale()
```
