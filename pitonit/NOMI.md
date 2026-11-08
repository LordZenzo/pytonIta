# Revisione dei nomi italiani (punto 4)

Obiettivo: togliere gli attriti più evidenti per chi scrive in italiano, **senza** cambiare le parole del linguaggio (i programmi già scritti continuano a funzionare).

## Cosa è stato fatto

### 1. Parole chiave usabili come nomi
Parole italiane molto naturali sono anche parole chiave: `classe` (la 3ª A), `con` (connessione), `prova`, `da`/`a` (intervalli), `elimina`, `produci`, `importa`…
Il lexer (`Parser/pegen.c`, `_it_keyword_is_name`) ora legge una parola riservata come **nome** quando in quel punto una parola chiave non potrebbe comparire:

| Situazione | Esempio |
|---|---|
| dopo un punto | `cane.classe`, `oggetto.importa` |
| nome di funzione o classe | `definisci elimina(x):`, `classe con:` — e da lì in poi la parola resta un nome in tutto il file, anche come istruzione `elimina(5)` |
| prima di `=`, `,`, `)`, `]`, `}`, `:` , `.`, operatori di confronto | `classe = "3A"`, `intervallo(da, a)`, `{classe: 1}`, `definisci f(da=1, con=2)`, `lambda con: con + 1` |
| dopo operatori, `(`, `,`, `=`, `ritorna`, `se`, `in`, `non`… | `x = classe`, `stampa(prova)`, `ritorna da + con` |
| dopo `per`, `come`, `globale`, `nonlocale`, `importa` | `per da in lista`, `importa x come con` |
| dopo `:` per le istruzioni composte | `{a: classe}` |

Le regole sono prudenti: nel dubbio la parola resta una parola chiave. A inizio istruzione (`se x:`, `classe Cane:`, `prova:`) niente cambia.
Resta riservato soprattutto ciò che apre un'istruzione.

Verifica: 218 moduli della libreria standard di Python (circa 137 000 righe) tradotti in italiano con `py2pit` hanno un albero sintattico identico all'originale; i 70 programmi `.pit` del progetto compilano; i 131 esempi delle lezioni e tutti i test di PitStudio passano.

### 2. Bug corretti trovati lungo la strada
- **`e` / `o` a fine riga** (condizioni su più righe): `se (a e` ↵ `b):` dava errore. Ora la riga può terminare con `e`/`o` (anche con `\` o un commento).
- `py2pit`: `from . import x` lasciava `import` in inglese.

### 3. Opzioni con nome in italiano
Le funzioni predefinite accettavano solo le opzioni inglesi (`key=`, `reverse=`, `encoding=`…): ora anche `chiave=`, `inverso=`, `predefinito=`, `inizio=`, `cifre=`, `codifica=`, `modalita=`, `errori=`, `a_capo=`, `separatore=`, `fine=`, `svuota=`, `max_divisioni=`, `rigoroso=`, `conteggio=`… Vedi la guida (*Il linguaggio → Opzioni con nome in italiano*).
Per i tipi scritti in C (`lista`, `testo`) serve la nuova funzione interna `_imposta_nel_tipo` (`Python/bltinmodule.c`).

### 4. Messaggi d'errore
Tradotti i messaggi del parser e dell'esecuzione che erano rimasti in inglese (blocco indentato dopo `se`/`per`/…, «Forse hai dimenticato una virgola?», «troppi valori da decomprimere», `'ritorna' fuori da una funzione`, ecc.).

### 5. `elimina(x)` è una chiamata
`elimina` (cioè `del`) attaccato alla parentesi si legge come un nome: `elimina(x)` chiama la funzione `elimina`; per cancellare un nome si scrive `elimina x` (o `elimina lista[0]`). Una parola definita con `definisci`/`classe` resta un nome per tutto il file.

## Cosa non è stato cambiato (e perché)
- **Le parole chiave non sono state rinominate**: `se`, `per`, `classe`… restano uguali. Cambiarle romperebbe i programmi esistenti e, senza prove con utenti veri, non sappiamo quali sarebbero migliori.
- **`se_stesso`** è solo una convenzione: il primo parametro dei metodi si può chiamare come si vuole (`io`, `questo`). Le lezioni mantengono `se_stesso` perché è coerente con le librerie e con la guida.
- **`e` e `o`** restano parole chiave solo come operatori tra due valori (già così).
- **I nomi dei tipi nei messaggi** (`list`, `str`, `int`) e `tipo(7)` → `<class 'int'>` restano inglesi.
- L'**evidenziazione dell'editor** colora ancora come parole chiave i nomi come `classe` usati da variabile (è un colore, non un errore).

## Da fare quando ci saranno prove con utenti
- Quali parole chiave generano più errori? (conviene registrare gli errori di sintassi più frequenti).
- Valutare sinonimi più brevi/naturali (per esempio `ripeti`/`mentre`, `restituisci`/`ritorna`) **in aggiunta** alle parole attuali.
- Rivedere la qualità dei nomi tradotti automaticamente nelle librerie meno usate.
