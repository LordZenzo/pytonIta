# Lezione 29 · Pubblicare un sito

**Obiettivo:** portare un sito fatto con `server_web` dal tuo computer a un server su Internet, in modo sicuro: modalità produzione, proxy HTTPS, limiti di richieste e controllo prima di partire.

## Dal tuo computer a Internet

Sul tuo computer il sito ascolta solo **te** (`127.0.0.1`). Su Internet lo vedono tutti, anche chi cerca di **romperlo**: indovinare le password, mandare milioni di richieste, sfruttare ogni dettaglio che l'errore di una pagina rivela. Pubblicare bene vuol dire:

1. un **server di produzione** al posto di `app.avvia()`: `app.avvia_produzione()` usa **waitress**, incluso in PitStudio;
2. un **proxy davanti** (Caddy, nginx) che gestisce **HTTPS** e il certificato;
3. la **modalità produzione** e le regolazioni di sicurezza;
4. **limiti** su ciò che si può chiedere al sito, e un controllo prima di partire.

*Progetto → Prepara per la pubblicazione (sito web)…* scrive tutto quello che serve per i punti 1 e 2 (Docker con Caddy, systemd, chiave segreta, istruzioni). Questa lezione spiega i punti 3 e 4.

## Modalità produzione

`app.configura(produzione=Vero)` cambia tre cose: l'errore di una pagina **non mostra più i dettagli** (un visitatore vedrebbe nomi di file e di variabili), ma un **codice** come `Codice: 3fa9c1d2e4b7`; i dettagli completi restano nel registro, con lo stesso codice, così quando qualcuno ti scrive «ho visto l'errore 3fa9c1d2e4b7» sai quale cercare. `/docs` si spegne (l'elenco delle rotte aiuta chi attacca) e i file statici vengono ricordati dal browser per un'ora.

```pit sintassi
app.configura(produzione=Vero, registro_file="logs/accessi.log", registro_errori="logs/errori.log")
```

I registri hanno la **rotazione**: quando un file arriva a 5 MB si archivia e se ne apre uno nuovo (se ne tengono cinque), così il disco non si riempie.

## Il controllo prima di pubblicare

`app.controlla_produzione()` guarda la configurazione e ti dice cosa manca. Ogni voce ha una **gravità** (`errore`: non pubblicare così; `attenzione`; `nota`) e la **correzione**. `app.avvia_produzione()` lo fa da solo e **non parte** se trova un errore.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.invia("/accedi")(lambda: "ok")
per problema in app.controlla_produzione():
    stampa(problema["gravita"], "-", problema["problema"][:48])
```

```output
errore - Il sito non e' in modalita' produzione: un error
errore - La chiave segreta e' temporanea: le sessioni si
errore - Mancano gli host ammessi: il sito risponderebbe
attenzione - Ci sono rotte che modificano dati (POST/PUT/DELE
attenzione - I cookie di sessione non sono marcati «Secure» e
attenzione - Le pagine di accesso/registrazione (/accedi) non
nota - Non c'e' un registro degli accessi su file.
```

Ecco un sito configurato bene:

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare", produzione=Vero, host_ammessi=["esempio.it"],
              proxy_fidato=Vero, csrf=Vero)


@app.invia("/accedi")
@app.limita(5, 60)
definisci accedi():
    ritorna "ok"


stampa([p["gravita"] per p in app.controlla_produzione("127.0.0.1") se p["gravita"] != "nota"])
```

```output
[]
```

La chiave segreta **non va scritta nel programma**: si legge dall'ambiente. `app.configura_da_ambiente("SITO_")` legge `SITO_CHIAVE_SEGRETA`, `SITO_PRODUZIONE`, `SITO_HOST_AMMESSI`… dalle variabili d'ambiente o da un file `.env` (che **non si mette mai su GitHub**). Il progetto preparato da PitStudio ha già un `.env` con una chiave casuale.

## Dietro un proxy HTTPS

Il proxy (Caddy) parla HTTPS con i visitatori e passa al tuo sito la richiesta **in chiaro**, aggiungendo intestazioni che dicono la verità: `X-Forwarded-For` (l'indirizzo vero del visitatore), `X-Forwarded-Proto` (era https?) e `X-Forwarded-Host` (quale nome ha scritto). Senza `proxy_fidato` il sito le **ignora**, perché chiunque potrebbe scriverle per mentire. Con `proxy_fidato=Vero` le legge. Altre regolazioni utili: `host_ammessi` (i soli nomi con cui rispondere) e `forza_https` (chi arriva in HTTP viene mandato a HTTPS).

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(proxy_fidato=Vero, host_ammessi=["esempio.it"], forza_https=Vero)


@app.rotta("/chi")
definisci chi(richiesta):
    ritorna {"ip": richiesta.indirizzo_cliente}


r = app.simula("/chi", host="esempio.it")
stampa(r.stato, r.intestazioni["Location"])
r = app.simula("/chi", host="esempio.it", indirizzo="10.0.0.2", intestazioni={"X-Forwarded-Proto": "https", "X-Forwarded-For": "9.9.9.9"})
stampa(r.stato, r.dati)
stampa(app.simula("/chi", host="cattivo.it").stato)
```

```output
308 https://esempio.it/chi
200 {'ip': '9.9.9.9'}
400
```

- la prima richiesta è in HTTP: il sito la manda a HTTPS (308);
- la seconda arriva dal proxy (`10.0.0.2`) con le intestazioni: l'indirizzo che vale è quello del visitatore, `9.9.9.9`;
- la terza usa un nome che non è nell'elenco: 400.

`proxy_fidato=Vero` fida di **chiunque** si colleghi: va bene solo se il sito è raggiungibile **soltanto dal proxy** (con Docker, la porta non si pubblica). Altrimenti si elencano le reti del proxy: `proxy_fidato=["10.0.0.0/8"]`.

## Limiti e blocco degli accessi

Una pagina di accesso senza limiti si può **indovinare** provando milioni di password. `@app.limita(richieste, secondi)` (sotto `@app.rotta`) ammette al massimo quel numero di richieste per indirizzo IP; oltre il limite la risposta è **429** con `Retry-After`.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/accedi")
@app.limita(2, 60)
definisci accedi():
    ritorna "ok"


per volta in intervallo_di(3):
    stampa(app.simula("/accedi", indirizzo="1.2.3.4").stato)
stampa(app.simula("/accedi", indirizzo="5.6.7.8").stato)
```

```output
200
200
429
200
```

Per bloccare chi sbaglia **la password** (e non chi usa il sito normalmente) ci sono `accesso_fallito`, `accesso_bloccato` e `accesso_riuscito`: si usano con una chiave (di solito nome utente e indirizzo) dentro la rotta di accesso, e `configura(limite_accessi=(tentativi, finestra, blocco))` ne regola i numeri.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(limite_accessi=(3, 60, 30))
chiave = "ada|1.2.3.4"
per tentativo in intervallo_di(3):
    stampa(app.accesso_fallito(chiave))
stampa(app.accesso_bloccato(chiave) > 0)
app.accesso_riuscito(chiave)
stampa(app.accesso_bloccato(chiave))
```

```output
0
0
30
Vero
0
```

Al terzo errore la chiave resta **bloccata per 30 secondi** (in pratica si userebbero 15 minuti): chi indovina le password va avanti lentissimo. I contatori stanno nella memoria del programma: con più processi ognuno ha i suoi, quindi per siti grandi si usano limiti anche nel proxy.

## File statici e compressione

I file statici (stili, immagini, script) vengono inviati **a pezzi** (anche se sono video da centinaia di megabyte), con **ETag** e **Last-Modified**: il browser li ricorda e la volta dopo chiede solo «è cambiato?»; se no, il sito risponde **304** senza rimandare nulla. Con l'intestazione **Range** si possono chiedere solo certi byte (serve a video, audio e download ripresi). I testi (HTML, JSON, CSS, JavaScript) si **comprimono** da soli con gzip quando il browser lo accetta. I file nascosti (`.env`, `.git`) **non si servono mai**.

```pit
importa server_web
importa os
importa tempfile

cartella = tempfile.mkdtemp()
open(os.path.join(cartella, "a.txt"), "w").write("ciao")
app = server_web.Applicazione(registro=Falso)
app.statici("/s", cartella)

prima = app.simula("/s/a.txt")
stampa(prima.stato)
dopo = app.simula("/s/a.txt", intestazioni={"If-None-Match": prima.intestazioni["ETag"]})
stampa(dopo.stato, dopo.corpo)
```

```output
200
304 b''
```

Per far scaricare un file con un nome scelto da te: `server_web.invia_file(percorso, nome="relazione.pdf", scarica=Vero)`; se il nome del file arriva dall'**utente** usa `app.invia_da_cartella(cartella, nome)`, che non permette di uscire dalla cartella.

## Pubblicare con Docker

*Progetto → Prepara per la pubblicazione (sito web)…* converte il progetto in Python e scrive la cartella `pubblicazione/`:

| File | A cosa serve |
|---|---|
| `Dockerfile` | il contenitore del sito (Python, waitress, un utente senza privilegi, il controllo di stato) |
| `docker-compose.yml` | il sito + **Caddy** davanti, che prende da solo il certificato HTTPS; la porta del sito non si pubblica |
| `Caddyfile` | il dominio e il collegamento al sito |
| `.env` | le regolazioni, con una **chiave segreta casuale** (si crea una volta sola, **non va su GitHub**) |
| `sito.service` | l'alternativa senza Docker: un servizio systemd con le protezioni |
| `LEGGIMI_PUBBLICAZIONE.md` | i passi, uno per uno: dominio, server, DNS, firewall, aggiornamenti, copie di sicurezza |

Con un dominio e un server (un VPS con Linux costa pochi euro al mese) bastano `docker compose up -d --build` e dopo un minuto il sito è su `https://tuodominio`.

**Cosa resta a te:** aggiornare il server, fare le copie di sicurezza dei dati, guardare i registri, e se il sito tratta dati personali o pagamenti farlo controllare da chi se ne intende. `server_web` è fatto bene per piccoli siti e strumenti, ma non è un servizio gestito.

## Esercizi

1. Configura un sito per la produzione (chiave, host, proxy, CSRF) e stampa quanti problemi di gravità `errore` o `attenzione` restano. Deve dire 0.
2. Scrivi una rotta `/contatti` limitata a 1 richiesta ogni 60 secondi per indirizzo e controlla che la seconda dia 429 e che un altro indirizzo possa usarla.
3. Imposta con `os.environ` `SITO_PRODUZIONE=1` e `SITO_HOST_AMMESSI=esempio.it` e leggili con `configura_da_ambiente`: stampa `produzione` e `host_ammessi`.

## Soluzioni

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare", produzione=Vero, host_ammessi=["esempio.it"], proxy_fidato=Vero, csrf=Vero)
stampa(lunghezza_di([p per p in app.controlla_produzione("127.0.0.1") se p["gravita"] != "nota"]))
```

```output
0
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/contatti")
@app.limita(1, 60)
definisci contatti():
    ritorna "ok"


stampa(app.simula("/contatti", indirizzo="1.1.1.1").stato)
stampa(app.simula("/contatti", indirizzo="1.1.1.1").stato)
stampa(app.simula("/contatti", indirizzo="2.2.2.2").stato)
```

```output
200
429
200
```

```pit
importa os
importa server_web

os.environ["SITO_PRODUZIONE"] = "1"
os.environ["SITO_HOST_AMMESSI"] = "esempio.it"
app = server_web.Applicazione(registro=Falso)
app.configura_da_ambiente("SITO_")
stampa(app.produzione, app.host_ammessi)
```

```output
Vero ['esempio.it']
```
