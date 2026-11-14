# ffmpeg: audio e video

La libreria `ffmpeg` **avvolge** ffmpeg e ffprobe: non li include, li comanda. Tutto quello che ffmpeg sa fare si scrive come funzioni, proprietà e oggetti, in italiano, e si legge come una frase. È pensata per chi non vuole imparare la riga di comando di ffmpeg (che è potentissima e quasi illeggibile), ma anche per chi la conosce e vuole poterla costruire a pezzi dentro un programma.

```pit sintassi
importa ffmpeg

(ffmpeg.apri("film.mp4", inizio=10, durata=5)      # prendi 5 secondi a partire dal decimo
    .ridimensiona(larghezza=640)                   # larghi 640 pixel
    .velocita(2)                                   # a velocità doppia
    .codec_video("libx264").qualita(23)            # H.264, qualità normale
    .salva("scena.mp4"))
```

## Prima di cominciare: serve ffmpeg

ffmpeg non è incluso in PitStudio (pesa 100 MB e ha una licenza propria). La libreria lo cerca da sola: nel `PATH`, nella variabile `PITONIT_FFMPEG` e nella cartella `.rad\ffmpeg` della tua cartella utente. Se non c'è:

- **Strumenti → ffmpeg: audio e video…** spiega cosa succede e, solo dopo il tuo consenso, lo scarica dal sito ufficiale (controllando l'impronta SHA-256 del file);
- oppure `multimedia.scarica_ffmpeg()` da un programma;
- oppure lo installi tu (Windows: `winget install ffmpeg`).

```pit sintassi
importa ffmpeg

stampa(ffmpeg.disponibile)     # Vero se ffmpeg si trova
stampa(ffmpeg.versione)        # la versione installata
stampa(ffmpeg.percorso)        # dove si trova
stampa(ffmpeg.licenza)         # LGPL, GPL o GPL v3
```

Anche `ffmpeg.percorso_sonda` (ffprobe), `ffmpeg.configurazione` (le opzioni con cui è stato compilato) e `ffmpeg.librerie` (le versioni di libavcodec e compagnia) sono proprietà del modulo. Se ffmpeg manca, le funzioni sollevano `FfmpegNonTrovato`, con il messaggio che spiega come procurarselo.

## Due finestre per guardare

Nel menu **Strumenti** ci sono due strumenti per chi vuole *vedere* prima di scrivere:

- **Esplora ffmpeg (filtri, codec, formati)…**: sfogli e cerchi filtri video e audio, codec, codificatori, decodificatori, formati, pixel, campioni, layout dei canali, protocolli, dispositivi e colori **della tua build di ffmpeg**. Scelta una voce, a destra compaiono le sue opzioni (tipo, intervallo, valore predefinito, valori ammessi) e un **esempio di codice** pronto da copiare con un clic.
- **Informazioni su un file audio o video…**: scegli un file e vedi formato, durata, dimensione, bitrate, risoluzione, i flussi (video, audio, sottotitoli) con i loro codec, i tag, i capitoli e una miniatura (per l'audio, la forma d'onda). Puoi copiare il riassunto o il JSON completo di ffprobe.

## Un comando si costruisce a catena

Ogni comando ha tre parti, e ogni metodo restituisce il comando stesso, quindi si concatenano:

1. **gli ingressi**: `ffmpeg.apri("a.mp4")` comincia il comando; `.aggiungi("b.mp3")` ne aggiunge un altro; `.sorgente("testsrc=duration=3")` aggiunge un ingresso virtuale;
2. **cosa fare**: filtri (`.ridimensiona(...)`, `.volume(...)`) e opzioni (`.codec_video("libx264")`, `.qualita(23)`);
3. **dove scrivere**: `.uscita("fuori.mp4")` chiude l'uscita; `.salva("fuori.mp4")` fa lo stesso e poi **esegue**.

Le opzioni di un ingresso si danno ad `apri` o `aggiungi`: `inizio`, `fine`, `durata`, `ripeti`, `formato`, `fps`, `risoluzione`, `ritmo_reale`, `accelerazione`, `ritardo`, e qualunque altra con il nome di ffmpeg (`apri("a.mp4", loop=1)`).

Per **vedere** cosa verrebbe lanciato, senza lanciarlo:

```pit sintassi
comando = ffmpeg.apri("a.mp4").ridimensiona(larghezza=640).uscita("b.mp4")
stampa(comando.argomenti)         # la lista degli argomenti
stampa(comando.riga_di_comando)   # la riga completa, da copiare in un terminale
stampa(comando.durata_prevista)   # quanti secondi di filmato produrrà
```

### Più uscite in un colpo solo

```pit sintassi
(ffmpeg.apri("film.mp4")
    .ridimensiona(larghezza=1280).codec_video("libx264").uscita("film_hd.mp4")
    .ridimensiona(larghezza=320).codec_video("libx264").senza_audio().uscita("anteprima.mp4")
    .esegui())
```

Ogni `.uscita(...)` chiude una uscita e ne comincia un'altra: filtri e opzioni valgono per l'uscita che si sta descrivendo.

## Le opzioni di uscita

Un metodo per ogni opzione più usata. Quelle che mancano si danno con `.opzione("-nome", valore)`, e per un flusso preciso `.opzione("-b", "128k", flusso="a:0")`.

| Metodo | Opzione di ffmpeg | A cosa serve |
|---|---|---|
| `codec_video(...)` | `-c:v` | Il codificatore video: 'libx264', 'libx265', 'libvpx-vp9', 'mpeg4', 'copy' (senza ricodificare), ... |
| `codec_audio(...)` | `-c:a` | Il codificatore audio: 'aac', 'libmp3lame', 'libopus', 'flac', 'pcm_s16le', 'copy', ... |
| `codec_sottotitoli(...)` | `-c:s` | Il codec dei sottotitoli: 'srt', 'mov_text', 'ass', 'copy', ... |
| `copia(...)` | `-c` | Copia tutti i flussi senza ricodificarli (veloce, nessuna perdita). Con un valore: il codec per tutti i flussi. |
| `qualita(...)` | `-crf` | Qualita' costante per x264/x265/vp9 (0 = perfetta, 18 = ottima, 23 = normale, 28 = bassa). |
| `qualita_audio(...)` | `-q:a` | Qualita' audio a scala (per mp3: 0 = migliore, 9 = peggiore). |
| `bitrate_video(...)` | `-b:v` | Bitrate del video: '2M', '800k', ... |
| `bitrate_audio(...)` | `-b:a` | Bitrate dell'audio: '192k', '128k', ... |
| `bitrate_massimo(...)` | `-maxrate` | Bitrate massimo del video (si usa con 'buffer'). |
| `buffer(...)` | `-bufsize` | Dimensione del buffer di controllo del bitrate. |
| `fps(...)` | `-r` | Fotogrammi al secondo dell'uscita. |
| `risoluzione(...)` | `-s` | Dimensioni dell'uscita: '1280x720'. Per ridimensionare bene usa .ridimensiona(...). |
| `rapporto(...)` | `-aspect` | Rapporto d'aspetto: '16:9', '4:3'. |
| `frequenza_audio(...)` | `-ar` | Campionamento audio in Hz: 44100, 48000. |
| `canali(...)` | `-ac` | Numero di canali audio: 1 (mono), 2 (stereo), 6 (5.1). |
| `layout_canali(...)` | `-channel_layout` | Layout dei canali: 'mono', 'stereo', '5.1'. |
| `formato_pixel(...)` | `-pix_fmt` | Formato dei pixel: 'yuv420p' (il piu' compatibile), 'rgb24', 'gray', ... |
| `formato_campione(...)` | `-sample_fmt` | Formato dei campioni audio: 's16', 'fltp', ... |
| `formato(...)` | `-f` | Il contenitore, se non si capisce dall'estensione: 'mp4', 'matroska', 'wav', 'null', 'image2', ... |
| `preset(...)` | `-preset` | Velocita' contro dimensione per x264/x265: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow. |
| `profilo(...)` | `-profile:v` | Profilo del codec video: 'baseline', 'main', 'high', ... |
| `livello(...)` | `-level` | Livello del codec video: '4.0', '4.1', ... |
| `tune(...)` | `-tune` | Ottimizzazione di x264: 'film', 'animation', 'grain', 'stillimage', 'zerolatency', ... |
| `durata(...)` | `-t` | Ferma l'uscita dopo questi secondi (o 'HH:MM:SS'). |
| `inizio(...)` | `-ss` | Salta questi secondi dell'ingresso prima di scrivere l'uscita. |
| `fine(...)` | `-to` | Ferma l'uscita a questo istante. |
| `fotogrammi(...)` | `-frames:v` | Scrive solo questo numero di fotogrammi video. |
| `campioni_audio(...)` | `-frames:a` | Scrive solo questo numero di frame audio. |
| `senza_video(...)` | `-vn` | Niente video nell'uscita. |
| `senza_audio(...)` | `-an` | Niente audio nell'uscita. |
| `senza_sottotitoli(...)` | `-sn` | Niente sottotitoli nell'uscita. |
| `senza_dati(...)` | `-dn` | Niente flussi di dati nell'uscita. |
| `il_piu_corto(...)` | `-shortest` | Finisce quando finisce il flusso piu' corto. |
| `ottimizza_web(...)` | `-movflags +faststart` | mp4 pronto per lo streaming (l'indice all'inizio del file). |
| `thread(...)` | `-threads` | Quanti thread usare (0 = automatico). |
| `gop(...)` | `-g` | Distanza massima tra fotogrammi chiave (la lunghezza del GOP). |
| `b_frames(...)` | `-bf` | Numero massimo di fotogrammi B consecutivi. |
| `qscale_video(...)` | `-q:v` | Qualita' video a scala (per jpeg: 2 = ottima, 31 = pessima). |
| `tag_video(...)` | `-tag:v` | Tag del codec video (es. 'hvc1' per h265 su Apple). |
| `ripeti(...)` | `-stream_loop` | Ripete l'ingresso (si usa prima dell'ingresso: preferisci apri(..., ripeti=3)). |
| `formato_tempo(...)` | `-fps_mode` | Gestione del tempo dei fotogrammi: 'cfr', 'vfr', 'passthrough', 'drop'. |
| `accelerazione(...)` | `-hwaccel` | Decodifica con la scheda video: 'cuda', 'd3d11va', 'dxva2', 'auto'. |
| `metadati_globali(...)` | `-map_metadata` | Da quale ingresso copiare i metadati (-1 = nessuno). |
| `capitoli(...)` | `-map_chapters` | Da quale ingresso copiare i capitoli (-1 = nessuno). |
| `limita_dimensione(...)` | `-fs` | Ferma l'uscita a questa dimensione in byte. |
| `passaggio(...)` | `-pass` | Primo o secondo passaggio della codifica a due passaggi (1 o 2). |
| `file_statistiche(...)` | `-passlogfile` | Prefisso dei file di statistiche per la codifica a due passaggi. |

Altro: `.mappa("0:v:0")` sceglie i flussi (`-map`), `.metadati(title="Prova", artist="Io")`, `.metadati_flusso("a:0", language="ita")`, `.senza_metadati()`, `.impostazioni_globali("-threads", 4)`, `.livello_log("warning")`, `.non_sovrascrivere()`.

## I filtri

### Video

| Metodo | Cosa fa |
|---|---|
| `ridimensiona(larghezza=None, altezza=None, adatta=False, algoritmo=None, pari=True)` | Cambia le dimensioni. Solo la larghezza (o l'altezza): l'altro lato segue, senza deformare. Con `adatta=True` e tutti e due i valori l'immagine sta dentro la cornice senza deformarsi (con bande nere). `algoritmo`: 'bicubic', 'lanczos', 'neighbor', ... |
| `ritaglia(larghezza, altezza, x=None, y=None)` | Ritaglia un rettangolo. Senza x e y il rettangolo e' al centro. |
| `ruota(gradi, colore='black')` | Ruota il video: 90, 180, 270 in modo esatto; altri angoli (in gradi) con sfondo `colore`. |
| `ribalta_orizzontale()` | Specchia il video da sinistra a destra. |
| `ribalta_verticale()` | Capovolge il video. |
| `velocita(fattore)` | Accelera (2 = doppia velocita') o rallenta (0.5 = meta') video e audio insieme. |
| `inverti()` | Riproduce video e audio al contrario (tiene tutto in memoria: per filmati brevi). |
| `sfoca(intensita=5)` | Sfocatura gaussiana (intensita' = sigma). |
| `nitidezza(quantita=1.0)` | Rende piu' nitida l'immagine (0 = niente, 1 = media, 5 = massima). |
| `colore_immagine(luminosita=None, contrasto=None, saturazione=None, gamma=None)` | Regola luminosita' (-1..1, 0 = invariata), contrasto (default 1), saturazione (default 1), gamma (default 1). |
| `bianco_e_nero()` | Toglie i colori. |
| `negativo()` | Inverte i colori. |
| `seppia()` | Effetto seppia. |
| `vignetta(angolo='PI/5')` | Scurisce i bordi. |
| `deinterlaccia()` | Toglie le righe da interlacciamento (yadif). |
| `cambia_fps(fps)` | Cambia i fotogrammi al secondo duplicando o saltando fotogrammi (a differenza di .fps(), che e' un'opzione dell'uscita). |
| `cornice(larghezza, altezza, x=None, y=None, colore='black')` | Mette il video al centro di una cornice piu' grande (bande). |
| `testo(scritta, x='(w-text_w)/2', y='(h-text_h)/2', dimensione=24, colore='white', sfondo=None, bordo=None, font=None, da_secondi=None, a_secondi=None, opacita=None)` | Scrive un testo sul video. x e y sono espressioni (centro di default). `font` e' un file .ttf. Compare solo tra `da_secondi` e `a_secondi`. |
| `sottotitoli(file, stile=None)` | Incide nel video i sottotitoli di un file .srt o .ass. `stile`: ad esempio 'FontSize=24,PrimaryColour=&H00FFFF&'. |
| `sovrapponi(immagine, x=10, y=10, opzioni_ingresso=None)` | Mette un'immagine (logo, filigrana) o un altro video sopra il video. x e y: pixel o espressioni come 'W-w-10' (angolo in basso a destra). |
| `dissolvenza_ingresso(durata=1.0, inizio=0, audio=True, colore='black')` | Entra dal nero (e l'audio dal silenzio) in `durata` secondi. |
| `dissolvenza_uscita(durata=1.0, a_partire_da=None, audio=True, colore='black')` | Esce verso il nero. `a_partire_da` (secondi): se manca si calcola dalla durata del filmato in uscita. |
| `miniature_ogni(secondi, larghezza=None)` | Un fotogramma ogni `secondi` secondi (per salvare una sequenza di immagini: .salva('img_%03d.png')). |

### Audio

| Metodo | Cosa fa |
|---|---|
| `volume(fattore)` | Alza o abbassa il volume: 0.5 = meta', 2 = doppio, '6dB', '-3dB'. |
| `normalizza_volume(obiettivo=-16.0, picco=-1.5, intervallo=11.0)` | Porta il volume a un livello costante (loudnorm, EBU R128): obiettivo in LUFS. |
| `passa_basso(frequenza)` | Lascia passare solo i suoni piu' gravi della frequenza (Hz). |
| `passa_alto(frequenza)` | Lascia passare solo i suoni piu' acuti della frequenza (Hz). |
| `equalizzatore(frequenza, guadagno, larghezza=100)` | Alza o abbassa (dB) una banda di frequenze. |
| `eco(ritardo_ms=500, decadimento=0.4)` | Aggiunge un'eco. |
| `ritardo_audio(millisecondi)` | Ritarda l'audio (utile per risincronizzare). |
| `velocita_audio(fattore)` | Cambia solo la velocita' dell'audio senza cambiarne il tono (atempo, a catena se serve). |
| `riduci_rumore(decibel=12)` | Toglie il fruscio di fondo (afftdn). |
| `inverti_audio()` | Riproduce l'audio al contrario. |
| `togli_silenzi(soglia_db=-50, durata_minima=0.5)` | Toglie le pause di silenzio piu' lunghe di `durata_minima` secondi. |

### Qualunque altro filtro

ffmpeg ha centinaia di filtri. Quelli senza un metodo italiano si usano con `.video` e `.audio`: il nome è quello di ffmpeg.

```pit sintassi
(ffmpeg.apri("a.mp4")
    .video.hue(s=0.5)                                # il filtro «hue» con l'opzione s=0.5
    .video.noise(alls=10)
    .audio.chorus(0.5, 0.9, 50, 0.4, 0.25, 2)        # gli argomenti senza nome vanno per posizione
    .salva("b.mp4"))
```

`.filtro("nome", ...)` e `.filtro_audio("nome", ...)` fanno lo stesso. I valori con caratteri speciali (due punti, virgole, apici…) vengono protetti da soli. Per un **grafo** di filtri con più ingressi e uscite si scrive a mano:

```pit sintassi
(ffmpeg.apri("a.mp4").aggiungi("b.mp4")
    .filtro_complesso("[0:v][1:v]hstack=inputs=2[v]", mappa=["[v]", "0:a"])     # due video affiancati
    .salva("affiancati.mp4"))
```

### Sbagliare un nome non è un dramma

`.controlla()` confronta filtri e opzioni con quelli di **questa** build di ffmpeg e dà una lista di problemi, con il suggerimento giusto:

```pit sintassi
problemi = ffmpeg.apri("a.mp4").video.scal(640, -2).uscita("b.mp4").controlla()
stampa(problemi)       # ['filtro sconosciuto: scal (forse scale, zscale, scale_qsv?)']
```

`.esegui(controlla=Vero)` e `.salva("b.mp4", controlla=Vero)` lo fanno prima di partire.

## Eseguire

- `.esegui()` (e `.salva(...)`) lancia ffmpeg e **aspetta**; ritorna un `Risultato` con `.uscite`, `.durata_elaborazione`, `.comando` e `.messaggi`;
- `.avvia()` lancia ffmpeg **in sottofondo** e ritorna subito un `Processo`: `.in_corso`, `.avanzamento`, `.aspetta()`, `.ferma()`;
- se ffmpeg dà errore, `ErroreFfmpeg` ha `.comando` (la riga lanciata), `.codice` e `.messaggi` (le ultime righe di ffmpeg).

### Una barra di avanzamento

```pit sintassi
definisci mostra(stato):
    se stato.frazione è non Nessuno:
        stampa(f"{stato.frazione:.0%}  ({stato.fotogrammi} fotogrammi, {stato.velocita}x)")

ffmpeg.apri("film.mp4").ridimensiona(larghezza=640).salva("piccolo.mp4", avanzamento=mostra)
```

Lo stato ha `.frazione` (da 0 a 1, se la durata è nota), `.tempo` (secondi di filmato fatti), `.fotogrammi`, `.fps`, `.velocita` (1.0 = tempo reale), `.dimensione` e `.terminato`.

### Fermarsi a metà

```pit sintassi
processo = ffmpeg.apri("film.mp4").codec_video("libx265").uscita("film265.mp4").avvia()
# ... più tardi ...
processo.ferma()                 # come premere Q: il file fatto fin qui resta valido
risultato = processo.aspetta()
```

Con `.esegui(fermata=funzione)` la funzione viene chiamata di continuo: se ritorna `Vero`, ffmpeg si ferma.

## Guardare dentro un file (ffprobe)

```pit sintassi
s = ffmpeg.sonda("film.mp4")
stampa(s.durata, s.risoluzione, s.fps)          # 125.4 (1920, 1080) 25.0
stampa(s.video[0].codec, s.audio[0].canali)     # h264 2
stampa(s.riassunto())
```

La `Sonda` ha: `file`, `formato`, `durata`, `dimensione`, `bitrate`, `inizio`, `tag`, `flussi`, `video`, `audio`, `sottotitoli`, `capitoli`, `ha_video`, `ha_audio`, `risoluzione`, `fps`, `dati` (la risposta completa di ffprobe) e `json()`. Ogni flusso ha `tipo`, `codec`, `larghezza`, `altezza`, `fps`, `formato_pixel`, `canali`, `frequenza`, `bitrate`, `durata`, `lingua`, `titolo`, `rotazione`, `tag`.

## Scoprire cosa sa fare ffmpeg

I cataloghi si leggono da **questa** build di ffmpeg, quindi non mentono mai su cosa c'è. Ognuno è un elenco con una ricerca: `.cerca("testo")`, `.nome("nome")`, `.nomi()`, `.filtra(campo=valore)`.

| Funzione | Cosa elenca |
|---|---|
| `ffmpeg.filtri()` | tutti i filtri (`nome`, `descrizione`, `tipo`: video o audio, `timeline`); `filtri("audio")` per restringere |
| `ffmpeg.codec()` | i codec (`tipo`, `codifica`, `decodifica`, `con_perdita`, `codificatori`, `decodificatori`) |
| `ffmpeg.codificatori()` / `decodificatori()` | `libx264`, `aac`, `libmp3lame`, … (`hardware` dice se usano la scheda video) |
| `ffmpeg.formati()` | i contenitori (`mp4`, `mkv`, `wav`, …): `lettura`, `scrittura`; `formati("scrittura")` |
| `ffmpeg.formati_pixel()` / `formati_campione()` | `yuv420p`, `rgb24`, … / `s16`, `fltp`, … |
| `ffmpeg.layout_canali()` | `mono`, `stereo`, `5.1`, … |
| `ffmpeg.protocolli()` / `dispositivi()` | `file`, `http`, `rtmp`, … / `gdigrab`, `dshow`, `lavfi`, … |
| `ffmpeg.accelerazioni()` / `filtri_bitstream()` / `colori()` | accelerazioni hardware, filtri sui bitstream, nomi dei colori |

```pit sintassi
stampa(ffmpeg.filtri().cerca("blur").nomi())              # ['avgblur', 'avgblur_opencl', 'avgblur_vulkan', 'blurdetect', 'boxblur', ...]
stampa(ffmpeg.codificatori("video").cerca("264").tabella())
```

E per ogni filtro, codec o formato, **le sue opzioni** con tipo, intervallo, valore predefinito e valori ammessi:

```pit sintassi
per opzione in ffmpeg.aiuto_filtro("scale").opzioni:
    stampa(opzione.nome, opzione.tipo, opzione.predefinito, opzione.descrizione)
```

`ffmpeg.aiuto_codificatore("libx264")`, `aiuto_decodificatore(...)`, `aiuto_scrittore("mp4")`, `aiuto_lettore(...)` e `ffmpeg.aiuto("full")` (il testo d'aiuto completo di ffmpeg) fanno il resto.

## Sorgenti pronte

Per provare, o per partire da zero: `ffmpeg.tono(440, 2)`, `ffmpeg.silenzio(1)`, `ffmpeg.colore("red", "640x360", durata=3)`, `ffmpeg.schema_di_prova()`. Sono comandi già avviati: `ffmpeg.tono(440, 2).salva("la.wav")`. E con `.sorgente("descrizione")` si aggiunge qualunque ingresso virtuale di ffmpeg.

## Le cose che si fanno di più, già fatte

| Funzione | Cosa fa |
|---|---|
| `ffmpeg.converti(origine, destinazione, avanzamento=None, **opzioni)` | Converte un file nel formato dell'estensione di `destinazione`. Opzioni in piu' = quelle di uscita (codec_video='libx264', qualita=23, ...). |
| `ffmpeg.estrai_audio(video, destinazione, avanzamento=None, **opzioni)` | Salva solo l'audio ('film.mp4' -> 'colonna.mp3'). |
| `ffmpeg.taglia(origine, destinazione, inizio=0, fine=None, durata=None, ricodifica=True, avanzamento=None)` | Salva il pezzo tra `inizio` e `fine` (o lungo `durata`), in secondi. Con ricodifica=False e' istantaneo ma preciso solo ai fotogrammi chiave. |
| `ffmpeg.fotogramma(video, tempo, destinazione, larghezza=None)` | Salva come immagine il fotogramma al secondo `tempo`. |
| `ffmpeg.estrai_fotogrammi(video, cartella, ogni_secondi=1.0, formato='png', larghezza=None, avanzamento=None)` | Salva un'immagine ogni `ogni_secondi` secondi in `cartella` (immagine_0001.png, ...). Ritorna la lista dei file. |
| `ffmpeg.riduci(video, destinazione, larghezza=640, qualita=26, avanzamento=None)` | Video piu' piccolo (larghezza in pixel, qualita' x264: piu' alto = piu' leggero). |
| `ffmpeg.gif(video, destinazione, inizio=0, durata=None, larghezza=480, fps=12, avanzamento=None)` | Una GIF animata di buona qualita' (con tavolozza di colori ottimizzata). |
| `ffmpeg.concatena(file, destinazione, ricodifica=False, avanzamento=None)` | Unisce piu' file uno dopo l'altro. Senza ricodifica i file devono avere gli stessi codec e parametri; con ricodifica=True vanno bene tutti. |
| `ffmpeg.sostituisci_audio(video, audio, destinazione, avanzamento=None)` | Il video con un altro audio (il video non si ricodifica). |
| `ffmpeg.togli_audio(video, destinazione, avanzamento=None)` | Il video senza audio (senza ricodificarlo). |
| `ffmpeg.filigrana(video, immagine, destinazione, x='W-w-10', y='H-h-10', avanzamento=None)` | Mette un logo sopra il video (di default in basso a destra). |
| `ffmpeg.dividi_in_segmenti(file, durata_segmento, modello, avanzamento=None)` | Taglia un file in pezzi lunghi `durata_segmento` secondi senza ricodificare: modello='parte_%03d.mp4'. |
| `ffmpeg.onda_audio(file, destinazione, dimensioni='1200x300', colore='#2a7de1')` | Un'immagine con la forma d'onda dell'audio. |
| `ffmpeg.spettrogramma(file, destinazione, dimensioni='1200x500')` | Un'immagine con lo spettro dell'audio. |
| `ffmpeg.foglio_di_miniature(video, destinazione, colonne=4, righe=4, larghezza=320)` | Un'unica immagine con tante miniature del video (colonne x righe), a intervalli uguali. |
| `ffmpeg.normalizza_volume(file, destinazione, obiettivo=-16.0, avanzamento=None)` | Volume costante con la normalizzazione EBU R128 (loudnorm); il video non si ricodifica. |
| `ffmpeg.rileva_silenzi(file, soglia_db=-40, durata_minima=0.5)` | Trova le pause di silenzio: ritorna una lista di (inizio, fine) in secondi. |
| `ffmpeg.volume_massimo(file)` | Il volume medio e di picco di un file, in dB: ritorna {'medio': ..., 'picco': ...}. |
| `ffmpeg.immagini_in_video(modello, destinazione, fps=25, audio=None, avanzamento=None)` | Una sequenza di immagini (modello='img_%04d.png') diventa un video. |
| `ffmpeg.cattura_schermo(destinazione, durata=5, fps=20, avanzamento=None)` | Registra lo schermo di Windows (gdigrab) per `durata` secondi. |

```pit sintassi
ffmpeg.converti("canzone.wav", "canzone.mp3")
ffmpeg.taglia("film.mp4", "scena.mp4", inizio=10, fine=25)
ffmpeg.gif("film.mp4", "clip.gif", inizio=3, durata=2, larghezza=320)
ffmpeg.concatena(["a.mp4", "b.mp4"], "ab.mp4", ricodifica=Vero)
stampa(ffmpeg.rileva_silenzi("lezione.mp3"))          # [(12.3, 14.8), (40.1, 42.0), ...]
```

## Per tutto il resto

`ffmpeg.esegui_argomenti("-i", "a.mp4", "-f", "null", "-")` lancia ffmpeg con gli argomenti che vuoi, tali e quali (e `programma="ffprobe"` per ffprobe). Così non c'è niente di ffmpeg che resti fuori.

## Da sapere

- **Il nome del file di uscita decide il formato** (`.mp4`, `.mp3`, `.gif`, `.png`…), a meno di `.formato("...")`.
- **Con `copia()` non si ricodifica**: è istantaneo e senza perdita, ma i tagli sono precisi solo ai fotogrammi chiave.
- **Il testo sul video** (`.testo(...)`) usa un font di Windows (Arial) se non indichi `font="file.ttf"`; l'apice dritto `'` viene scritto come `’`, perché manda in crash ffmpeg.
- **Windows e il download di ffmpeg**: il download automatico c'è solo su Windows; altrove ffmpeg si installa con il gestore di pacchetti (apt, brew, …).
- **ffplay** (il lettore di ffmpeg) non è incluso nel download di PitStudio: per ascoltare un file usa il modulo `suono`.
- **Licenza**: ffmpeg non è parte di pytonIta e ha la sua licenza (`ffmpeg.licenza` dice quale ha la tua copia).
- Se esporti il progetto come Python, `ffmpeg.py` e `multimedia.py` vengono copiati accanto al programma.
