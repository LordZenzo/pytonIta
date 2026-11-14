# Lezione 19 · Gli oggetti più a fondo

**Obiettivo:** far comportarsi i tuoi oggetti come i tipi di Python (sommarli, confrontarli, contarli), e capire quando usare l'ereditarietà e quando invece mettere un oggetto dentro un altro.

Questa lezione continua la [lezione 13](#lezione-13): lì hai visto classi, metodi ed ereditarietà.

## Metodi speciali

I nomi con due trattini bassi (`__inizializza__`, `__testo__`…) sono **metodi speciali**: Python li chiama da solo quando usi un operatore o una funzione. Ecco una frazione che si può sommare e confrontare:

```pit
classe Frazione:
    definisci __inizializza__(se_stesso, numeratore, denominatore):
        se_stesso.numeratore = numeratore
        se_stesso.denominatore = denominatore

    definisci __testo__(se_stesso):
        ritorna f"{se_stesso.numeratore}/{se_stesso.denominatore}"

    definisci __somma__(se_stesso, altra):
        num = se_stesso.numeratore * altra.denominatore + altra.numeratore * se_stesso.denominatore
        ritorna Frazione(num, se_stesso.denominatore * altra.denominatore)

    definisci __uguale__(se_stesso, altra):
        ritorna se_stesso.numeratore * altra.denominatore == altra.numeratore * se_stesso.denominatore

    definisci __minore__(se_stesso, altra):
        ritorna se_stesso.numeratore * altra.denominatore < altra.numeratore * se_stesso.denominatore

mezzo = Frazione(1, 2)
terzo = Frazione(1, 3)
stampa(mezzo + terzo)
stampa(Frazione(1, 2) == Frazione(2, 4))
stampa(terzo < mezzo)
```

```output
5/6
Vero
Vero
```

I più usati:

| Metodo | Quando viene chiamato |
|---|---|
| `__inizializza__` | alla creazione: `Frazione(1, 2)` |
| `__testo__` | `stampa(oggetto)` e `tipo_testo(oggetto)` |
| `__somma__` | `a + b` |
| `__uguale__` | `a == b` |
| `__minore__` | `a < b` (e permette di ordinare) |
| `__lunghezza__` | `lunghezza_di(oggetto)` |
| `__chiama__` | `oggetto(...)` come una funzione |

```pit
classe Squadra:
    definisci __inizializza__(se_stesso, *giocatori):
        se_stesso.giocatori = tipo_lista(giocatori)

    definisci __lunghezza__(se_stesso):
        ritorna lunghezza_di(se_stesso.giocatori)

s = Squadra("Anna", "Luca", "Sara")
stampa(lunghezza_di(s))
```

```output
3
```

## Attributi di classe

Un dato scritto **dentro la classe**, fuori dai metodi, è condiviso da tutti gli oggetti:

```pit
classe Libro:
    totale = 0

    definisci __inizializza__(se_stesso, titolo):
        se_stesso.titolo = titolo
        Libro.totale += 1

Libro("Il barone rampante")
Libro("Se una notte d'inverno")
stampa(Libro.totale)
```

```output
2
```

`se_stesso.titolo` è diverso per ogni libro; `Libro.totale` è uno solo, di tutta la classe.

## Una proprietà calcolata

A volte un valore si può **calcolare** dagli altri dati. Con `@attributo_calcolato` lo usi come un normale attributo, senza parentesi, e resta sempre aggiornato:

```pit
classe Cerchio:
    definisci __inizializza__(se_stesso, raggio):
        se_stesso.raggio = raggio

    @attributo_calcolato
    definisci area(se_stesso):
        ritorna 3.14159 * se_stesso.raggio ** 2

c = Cerchio(2)
stampa(c.area)
c.raggio = 3
stampa(c.area)
```

```output
12.56636
28.27431
```

## Estendere una classe e richiamare quella di base

Una classe figlia può **riusare** il metodo della classe di base con `classe_base()`:

```pit
classe Persona:
    definisci __inizializza__(se_stesso, nome):
        se_stesso.nome = nome

    definisci presentati(se_stesso):
        ritorna f"Sono {se_stesso.nome}"

classe Studente(Persona):
    definisci __inizializza__(se_stesso, nome, classe_frequentata):
        classe_base().__init__(nome)
        se_stesso.classe_frequentata = classe_frequentata

    definisci presentati(se_stesso):
        ritorna classe_base().presentati() + f" e frequento la {se_stesso.classe_frequentata}"

stampa(Studente("Anna", "3A").presentati())
stampa(isinstance(Studente("Luca", "2B"), Persona))
```

```output
Sono Anna e frequento la 3A
Vero
```

`isinstance(oggetto, Classe)` dice se un oggetto è di quella classe (o di una sua figlia).

## «È un» oppure «ha un»?

Un errore comune è usare l'ereditarietà dappertutto. Fatti una domanda:

- uno `Studente` **è una** `Persona` → ereditarietà: `classe Studente(Persona)`;
- un'`Auto` **ha un** `Motore` → **composizione**: l'auto contiene un oggetto motore.

```pit
classe Motore:
    definisci __inizializza__(se_stesso, cavalli):
        se_stesso.cavalli = cavalli

    definisci descrizione(se_stesso):
        ritorna f"{se_stesso.cavalli} cavalli"

classe Auto:
    definisci __inizializza__(se_stesso, modello, cavalli):
        se_stesso.modello = modello
        se_stesso.motore = Motore(cavalli)

    definisci scheda(se_stesso):
        ritorna f"{se_stesso.modello}: {se_stesso.motore.descrizione()}"

stampa(Auto("Panda", 70).scheda())
```

```output
Panda: 70 cavalli
```

Regola pratica: se non riesci a dire «X **è un** Y», probabilmente ti serve la composizione.

## Esercizi

1. Crea la classe `Vettore(x, y)` con `__somma__` (somma componente per componente) e `__testo__` che stampa `(x, y)`. Stampa `Vettore(1, 2) + Vettore(3, 4)`.
2. Crea `Conto` con un attributo di classe `numero_conti` che conta quanti conti sono stati creati.
3. Una classe `Forma` ha un metodo `area()` che restituisce 0. `Quadrato(lato)` lo ridefinisce. Stampa l'area di `Quadrato(4)` e controlla con `isinstance` che sia anche una `Forma`.

## Soluzioni

```pit
classe Vettore:
    definisci __inizializza__(se_stesso, x, y):
        se_stesso.x = x
        se_stesso.y = y

    definisci __somma__(se_stesso, altro):
        ritorna Vettore(se_stesso.x + altro.x, se_stesso.y + altro.y)

    definisci __testo__(se_stesso):
        ritorna f"({se_stesso.x}, {se_stesso.y})"

stampa(Vettore(1, 2) + Vettore(3, 4))
```

```output
(4, 6)
```

```pit
classe Conto:
    numero_conti = 0

    definisci __inizializza__(se_stesso):
        Conto.numero_conti += 1

Conto()
Conto()
Conto()
stampa(Conto.numero_conti)
```

```output
3
```

```pit
classe Forma:
    definisci area(se_stesso):
        ritorna 0

classe Quadrato(Forma):
    definisci __inizializza__(se_stesso, lato):
        se_stesso.lato = lato

    definisci area(se_stesso):
        ritorna se_stesso.lato ** 2

q = Quadrato(4)
stampa(q.area(), isinstance(q, Forma))
```

```output
16 Vero
```
