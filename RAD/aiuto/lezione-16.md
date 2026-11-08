# Lezione 16 · Progetto finale

**Obiettivo:** mettere insieme tutto in due programmi completi.

## Progetto 1 · Indovina il numero

Il computer pensa un numero da 1 a 100 e tu cerchi di indovinarlo: ti dice se è più alto o più basso. Usa: variabili, cicli, decisioni, `leggi`, un errore gestito e una libreria.

```pit
importa casuale

definisci chiedi_numero(messaggio):
    """Chiede un numero intero e insiste finché l'utente non lo scrive bene."""
    mentre Vero:
        prova:
            ritorna intero(leggi(messaggio))
        eccetto ErroreDiValore:
            stampa("Devi scrivere un numero intero.")

segreto = casuale.intero_casuale(1, 100)
tentativi = 0
stampa("Ho pensato un numero da 1 a 100. Prova a indovinarlo!")

mentre Vero:
    scelta = chiedi_numero("Il tuo numero: ")
    tentativi += 1
    se scelta < segreto:
        stampa("Più alto")
    altrimenti_se scelta > segreto:
        stampa("Più basso")
    altrimenti:
        stampa(f"Bravo! Hai indovinato in {tentativi} tentativi.")
        interrompi
```

```esempio
Ho pensato un numero da 1 a 100. Prova a indovinarlo!
Il tuo numero: 50
Più basso
Il tuo numero: 25
Più alto
Il tuo numero: ventidue
Devi scrivere un numero intero.
Il tuo numero: 37
Bravo! Hai indovinato in 4 tentativi.
```

**Provalo e poi miglioralo:**

- limita i tentativi a 7 e rivela il numero se li finisci;
- alla fine chiedi «Vuoi giocare ancora?» e ricomincia;
- salva in un file il **record** (il minor numero di tentativi) e mostralo.

## Progetto 2 · Rubrica telefonica

Una rubrica che salva i contatti su file. Usa: dizionari, funzioni, file JSON, un menu con ciclo e gestione degli errori.

```pit
importa formato_json
importa sistema_operativo

FILE = "rubrica.json"

definisci carica():
    se sistema_operativo.percorso.esiste(FILE):
        con apri(FILE, codifica="utf-8") come f:
            ritorna formato_json.carica(f)
    ritorna {}

definisci salva(rubrica):
    con apri(FILE, "w", codifica="utf-8") come f:
        formato_json.scarica(rubrica, f, indent=2, ensure_ascii=Falso)

definisci mostra(rubrica):
    se non rubrica:
        stampa("La rubrica è vuota.")
        ritorna
    per nome in sorted(rubrica):
        stampa(f"  {nome:<12} {rubrica[nome]}")

definisci menu():
    stampa()
    stampa("1) Elenco   2) Aggiungi   3) Cerca   4) Cancella   0) Esci")
    ritorna leggi("Scelta: ").elimina_spazi()

rubrica = carica()
mentre Vero:
    scelta = menu()
    se scelta == "1":
        mostra(rubrica)
    altrimenti_se scelta == "2":
        nome = leggi("Nome: ").elimina_spazi()
        telefono = leggi("Telefono: ").elimina_spazi()
        se nome e telefono:
            rubrica[nome] = telefono
            salva(rubrica)
            stampa("Salvato.")
    altrimenti_se scelta == "3":
        parte = leggi("Cerca: ").minuscolo()
        trovati = {n: t per n, t in rubrica.elementi() se parte in n.minuscolo()}
        mostra(trovati)
    altrimenti_se scelta == "4":
        nome = leggi("Nome da cancellare: ").elimina_spazi()
        se nome in rubrica:
            elimina rubrica[nome]
            salva(rubrica)
            stampa("Cancellato.")
        altrimenti:
            stampa("Non c'è nessuno con quel nome.")
    altrimenti_se scelta == "0":
        stampa("Arrivederci!")
        interrompi
    altrimenti:
        stampa("Scelta non valida.")
```

```esempio
1) Elenco   2) Aggiungi   3) Cerca   4) Cancella   0) Esci
Scelta: 2
Nome: Anna
Telefono: 333 1234567
Salvato.
```

**Idee per continuare:**

- trasforma la rubrica in una **classe** `Rubrica` con i metodi `aggiungi`, `cerca`, `cancella`;
- costruiscile una **finestra** con il progettista (lezione 15);
- usa il **debugger** (lezione 12) per seguire cosa succede quando aggiungi un contatto.

## Hai finito!

Ora conosci le basi della programmazione: **variabili, decisioni, cicli, liste, dizionari, funzioni, file, errori, classi, librerie e finestre**. Da qui puoi:

- esplorare il [riferimento del linguaggio](#linguaggio) e le [librerie in italiano](#librerie);
- costruire programmi a blocchi con le [mattonelle](#mattonelle);
- chiedere aiuto all'[assistente AI](#assistente): sa leggere il tuo progetto e spiegarti gli errori;
- guardare i programmi di esempio nella cartella `esempi` di pitonit.

Il consiglio più importante: **scrivi programmi che ti interessano** (un gioco, un archivio dei tuoi libri, un convertitore). Si impara programmando.
