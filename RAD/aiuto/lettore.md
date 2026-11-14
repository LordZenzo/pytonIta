# Lettore audio e video

Il modulo `lettore` riproduce audio e video **comandando un lettore esterno**. Oggi il motore è **VLC**; **mpv** arriverà come alternativa da scegliere. I comandi sono gli stessi per tutti i motori: cambia solo il nome del motore. Il lettore non è incluso in PitStudio: va installato a parte.

```pit sintassi
importa lettore

p = lettore.Lettore()                  # sceglie da solo il motore (quello preferito, o il primo disponibile)
p.apri("canzone.mp3")                  # e parte
p.pausa()
p.riprendi()
p.posizione = 90                       # vai al secondo 90
p.volume = 60                          # da 0 a 100
p.attendi_fine()
```

## Prima di cominciare: serve un motore

`lettore.motori()` elenca i motori che conosco, con questi campi: `nome`, `descrizione`, `disponibile`, `percorso`, `implementato`, `installazione` e `predefinito`. Se nessuno è installato, `Lettore()` solleva `MotoreNonTrovato` col comando per procurarselo.

- **VLC**: `winget install VideoLAN.VLC`, oppure `lettore.installa_motore("vlc")` (Windows chiede il permesso di amministratore), oppure dal sito. Se non si trova da solo, indica la sua cartella nella variabile `PITONIT_VLC`.
- **mpv**: in arrivo.

La scelta del motore si può dare a ogni lettore (`Lettore(motore="vlc")`), oppure ricordare per tutti i programmi con `lettore.imposta_motore_predefinito("vlc")` (o `"auto"`). Vale anche la variabile `PITONIT_LETTORE`.

## I comandi

| Comando | Cosa fa |
|---|---|
| `apri(sorgente, riproduci=Vero)` | carica un file o un indirizzo (`http://…`) e, di solito, parte |
| `riproduci()`, `pausa()`, `riprendi()`, `commuta()`, `ferma()` | i controlli di base (`commuta` alterna pausa e riproduzione) |
| `salta(secondi)` | avanti o indietro (negativo) di tot secondi |
| `fotogramma_avanti()` | in pausa, avanza di un fotogramma |
| `posizione` | il secondo attuale; si può assegnare per spostarsi |
| `frazione` | la posizione da 0 a 1; si può assegnare |
| `durata` | durata in secondi (0 finché il motore non la conosce) |
| `volume`, `muto` | da 0 a 100; si possono assegnare |
| `velocita` | 1.0 normale, 2.0 doppia, 0.5 metà; si può assegnare |
| `stato`, `in_riproduzione`, `in_pausa`, `finito` | cosa sta facendo: `fermo`, `caricamento`, `in_riproduzione`, `in_pausa`, `finito`, `errore` |
| `dimensioni` | `(larghezza, altezza)` del video, `(0, 0)` per l'audio |
| `tracce_audio`, `traccia_audio` | elenco delle tracce (`id`, `nome`, `attiva`) e quella scelta |
| `tracce_sottotitoli`, `sottotitoli`, `carica_sottotitoli(file)` | stessa cosa per i sottotitoli (`sottotitoli = Nessuno` li spegne) |
| `istantanea(file)` | salva il fotogramma che si vede come immagine |
| `attendi_fine(tempo_massimo=Nessuno)` | aspetta che il file finisca |
| `chiudi()` | libera tutto (si può anche usare `con lettore.Lettore() come p:`) |

`lettore.riproduci("file.mp3")` è la scorciatoia: apre un lettore e fa partire il file.

## Il video in una finestra

Con `Lettore()` senza altro, il motore apre la sua finestra. Per il video **dentro la tua finestra tkinter** si passa un widget:

```pit sintassi
importa interfaccia come tk
importa lettore

radice = tk.Finestra()
riquadro = tk.Riquadro(radice, larghezza=640, altezza=360)
riquadro.pack()
radice.update()

p = lettore.Lettore(riquadro)       # il video si disegna dentro il riquadro
p.apri("film.mp4")
radice.ciclo_principale()
```

Se vuoi anche i controlli già pronti (play/pausa, barra del tempo, volume, velocità, tracce, istantanea) c'è `lettore.PannelloLettore(radice)`: un riquadro completo.

```pit sintassi
pannello = lettore.PannelloLettore(radice)
pannello.pack(fill="both", expand=Vero)
pannello.apri("film.mp4")
```

## Reagire a quello che succede

```pit sintassi
p = lettore.Lettore()
p.quando("fine", lambda lett: stampa("finito!"))
p.quando("errore", lambda lett: stampa("qualcosa non va"))
p.apri("canzone.mp3")
p.avvia_controllo()        # controlla in un thread e fa scattare gli eventi
```

Gli eventi sono `avvio`, `pausa`, `fine`, `errore` e `cambio_stato`. Con tkinter, invece di `avvia_controllo()` chiama `p.controlla()` da un `after`: il `PannelloLettore` lo fa già.

## In PitStudio: Strumenti → Lettore audio e video…

Una finestra con il video, i controlli e un menu **Motore** (VLC; mpv appare come «in arrivo»). Se VLC manca, la finestra lo dice e propone **Installa VLC…**: solo dopo la tua conferma lancia winget. Sul video: clic (pausa), doppio clic o `f` (schermo intero), rotella (volume). Tasti: barra spaziatrice (pausa), ←/→ (5 secondi), ↑/↓ (volume), `m` (muto), Esc (esci dallo schermo intero). Anche la finestra **Informazioni su un file** ha il pulsante **Riproduci**.

## Da sapere

- **Il mouse sul video**: il video lo disegna il motore in una finestra sua, che di solito si «mangia» i clic. Per questo `Lettore` (con una finestra) rende quella finestra trasparente ai clic (`clic_attraverso`, attivo da solo): i clic arrivano al tuo riquadro e puoi usare `riquadro.bind("<Button-1>", ...)` come per qualunque widget. Il `PannelloLettore` lo usa così: **clic = pausa/riprendi, doppio clic = schermo intero** (in PitStudio), **rotella = volume**. Funziona se il lettore viene controllato di tanto in tanto (`controlla()`, `avvia_controllo()`, o il pannello, che lo fa da solo). Su macOS il video dentro una finestra non è ancora supportato.
- **Il motore è un programma a parte**, con la sua licenza: PitStudio non lo include né lo copia.
- Per spegnere il suono (prove, ambienti senza casse): `Lettore(opzioni=["--no-audio"])` con VLC.
- Se esporti il progetto come Python, `lettore.py` viene copiato accanto al programma.
- Per convertire, tagliare o guardare dentro i file multimediali c'è la libreria [ffmpeg](#ffmpeg).
