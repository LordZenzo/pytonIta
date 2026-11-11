# Lezione 13 · Le classi

**Obiettivo:** costruire i propri «oggetti», che hanno dati e azioni.

## Perché le classi

Una **classe** è uno stampo per creare **oggetti**: un cane ha un nome e un'età (dati) e sa abbaiare (azioni). Invece di avere tante variabili sparse, raggruppi tutto in un oggetto.

## La prima classe

```pit
classe Cane:
    definisci __inizializza__(se_stesso, nome, eta):
        se_stesso.nome = nome
        se_stesso.eta = eta

    definisci abbaia(se_stesso):
        stampa(f"{se_stesso.nome} dice: Bau!")

    definisci compleanno(se_stesso):
        se_stesso.eta += 1

fido = Cane("Fido", 3)
rex = Cane("Rex", 5)
fido.abbaia()
fido.compleanno()
stampa(fido.nome, "ha", fido.eta, "anni")
stampa(rex.nome, "ha", rex.eta, "anni")
```

```output
Fido dice: Bau!
Fido ha 4 anni
Rex ha 5 anni
```

Come si legge:

- `classe Cane:` definisce lo stampo;
- `__inizializza__` è il **costruttore**: viene eseguito quando scrivi `Cane("Fido", 3)` e prepara i dati;
- **`se_stesso`** è l'oggetto stesso: `se_stesso.nome` è il nome *di questo* cane. È sempre il primo parametro dei metodi (ma non lo scrivi quando li chiami);
- le funzioni dentro la classe si chiamano **metodi**.

## Stampare un oggetto

Il metodo speciale `__testo__` dice come trasformare l'oggetto in testo:

```pit
classe Punto:
    definisci __inizializza__(se_stesso, x, y):
        se_stesso.x = x
        se_stesso.y = y

    definisci __testo__(se_stesso):
        ritorna f"({se_stesso.x}, {se_stesso.y})"

    definisci sposta(se_stesso, dx, dy):
        se_stesso.x += dx
        se_stesso.y += dy

p = Punto(1, 2)
stampa(p)
p.sposta(3, 3)
stampa(p)
```

```output
(1, 2)
(4, 5)
```

## Esempio: un conto in banca

```pit
classe Conto:
    definisci __inizializza__(se_stesso, titolare, saldo=0):
        se_stesso.titolare = titolare
        se_stesso.saldo = saldo

    definisci versa(se_stesso, importo):
        se_stesso.saldo += importo

    definisci preleva(se_stesso, importo):
        se importo > se_stesso.saldo:
            solleva ErroreDiValore("saldo insufficiente")
        se_stesso.saldo -= importo

conto = Conto("Anna", 100)
conto.versa(50)
conto.preleva(30)
stampa(conto.titolare, conto.saldo)
prova:
    conto.preleva(1000)
eccetto ErroreDiValore come errore:
    stampa("Errore:", errore)
```

```output
Anna 120
Errore: saldo insufficiente
```

## Ereditarietà

Una classe può **estenderne** un'altra, ereditando tutto e aggiungendo o cambiando qualcosa:

```pit
classe Animale:
    definisci __inizializza__(se_stesso, nome):
        se_stesso.nome = nome

    definisci verso(se_stesso):
        ritorna "..."

    definisci parla(se_stesso):
        stampa(f"{se_stesso.nome} fa {se_stesso.verso()}")

classe Gatto(Animale):
    definisci verso(se_stesso):
        ritorna "miao"

classe Mucca(Animale):
    definisci verso(se_stesso):
        ritorna "muuu"

per a in [Gatto("Micio"), Mucca("Bianca"), Animale("Boh")]:
    a.parla()
```

```output
Micio fa miao
Bianca fa muuu
Boh fa ...
```

## Quando usarle

Per programmi piccoli bastano funzioni e liste. Le classi diventano utili quando hai **cose** con più dati e comportamenti (giocatori, prodotti, conti, personaggi…).

## Esercizi

1. Crea la classe `Rettangolo` con base e altezza e i metodi `area()` e `perimetro()`.
2. Crea la classe `Contatore` con i metodi `incrementa()`, `azzera()` e un valore `valore`.
3. Crea `Cerchio(raggio)` con `area()` (usa 3.14159); poi `Studente` con nome e lista di voti e un metodo `media()`.

## Soluzioni

```pit
classe Rettangolo:
    definisci __inizializza__(se_stesso, base, altezza):
        se_stesso.base = base
        se_stesso.altezza = altezza

    definisci area(se_stesso):
        ritorna se_stesso.base * se_stesso.altezza

    definisci perimetro(se_stesso):
        ritorna 2 * (se_stesso.base + se_stesso.altezza)

r = Rettangolo(4, 3)
stampa(r.area(), r.perimetro())
```

```output
12 14
```

```pit
classe Contatore:
    definisci __inizializza__(se_stesso):
        se_stesso.valore = 0

    definisci incrementa(se_stesso):
        se_stesso.valore += 1

    definisci azzera(se_stesso):
        se_stesso.valore = 0

c = Contatore()
c.incrementa()
c.incrementa()
stampa(c.valore)
c.azzera()
stampa(c.valore)
```

```output
2
0
```

```pit
classe Studente:
    definisci __inizializza__(se_stesso, nome, voti):
        se_stesso.nome = nome
        se_stesso.voti = voti

    definisci media(se_stesso):
        ritorna somma_di(se_stesso.voti) / lunghezza_di(se_stesso.voti)

stampa(Studente("Anna", [8, 9, 10]).media())
```

```output
9.0
```
