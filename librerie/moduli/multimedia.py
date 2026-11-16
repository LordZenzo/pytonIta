"""Multimedia: convertire, tagliare e guardare dentro i file audio e video con ffmpeg.
ffmpeg non e' incluso in pytonIta (pesa troppo e ha una licenza propria): il modulo lo cerca nel PATH, nella variabile
PITONIT_FFMPEG e nella cartella ~/.rad/ffmpeg; se manca, scarica_ffmpeg() lo scarica (solo se lo chiedi tu)."""
import hashlib as _hashlib
import os as _os
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import sys as _sistema
import tempfile as _tempfile
import urllib.request as _richieste
import zipfile as _zipfile

URL_FFMPEG = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"          # variante «essenziale»
URL_BASE_COMPLETA = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"       # variante «completa»
VARIANTI = {
    "essenziale": {"nome": "Essenziale", "dimensione_mb": 115, "sito": "https://www.gyan.dev/ffmpeg/builds/",
                   "descrizione": "Quello che serve quasi sempre: H.264, H.265, VP9, AAC, MP3, Opus, GIF e circa 530 filtri. Più leggera."},
    "completa": {"nome": "Completa", "dimensione_mb": 200, "sito": "https://github.com/BtbN/FFmpeg-Builds",
                 "descrizione": "L'ultima versione stabile compilata da BtbN, con più librerie dell'essenziale (di solito AV1, filtri per la "
                                "scheda video e altri formati: dopo il download ffmpeg.codificatori() e ffmpeg.filtri() dicono cosa c'è). "
                                "Circa il doppio del download."},
}
_ALIAS_VARIANTI = {"essentials": "essenziale", "essential": "essenziale", "base": "essenziale", "full": "completa", "completo": "completa"}
CARTELLA_FFMPEG = _os.path.join(_os.path.expanduser("~"), ".rad", "ffmpeg")
_SENZA_FINESTRA = 0x08000000 if _os.name == "nt" else 0          # niente finestra nera quando parte da un programma con finestre


class ErroreMultimedia(Exception):
    """ffmpeg non ha potuto fare quello che chiedevi."""


class FfmpegNonTrovato(ErroreMultimedia):
    """ffmpeg non e' installato (o non lo trovo)."""


def _nome_programma(nome):
    return nome + (".exe" if _os.name == "nt" else "")


def trova_ffmpeg(programma="ffmpeg"):
    """Percorso di ffmpeg (o di ffprobe) oppure None. Cerca: variabile PITONIT_FFMPEG, PATH, cartella ~/.rad/ffmpeg."""
    nome = _nome_programma(programma)
    scelta = _os.environ.get("PITONIT_FFMPEG", "")
    if scelta:
        for p in (scelta if _os.path.isfile(scelta) and _os.path.basename(scelta).lower().startswith(programma) else "",
                  _os.path.join(scelta, nome), _os.path.join(scelta, "bin", nome)):
            if p and _os.path.isfile(p):
                return p
    nel_path = _shutil.which(programma)
    if nel_path:
        return nel_path
    propria = _os.path.join(CARTELLA_FFMPEG, "bin", nome)
    return propria if _os.path.isfile(propria) else None


def _gestore_pacchetti():
    """Il gestore di pacchetti di questo computer: «winget», «brew», «apt», «dnf», «pacman», «zypper», oppure None."""
    if _os.name == "nt":
        return "winget"
    if _sistema.platform == "darwin":
        return "brew"
    for programma, gestore in (("apt-get", "apt"), ("dnf", "dnf"), ("pacman", "pacman"), ("zypper", "zypper")):
        if _shutil.which(programma):
            return gestore
    return None


# per ogni programma e gestore: [(etichetta, comando, nota)]. Il comando si copia e si incolla nel terminale cosi' com'e'.
_COMANDI = {
    "ffmpeg": {
        "apt": [("Completo", "sudo apt update && sudo apt install ffmpeg",
                 "Il pacchetto della distribuzione: ffmpeg con tutte le sue librerie (x264, x265, VP9, AV1, filtri...)."),
                ("Essenziale", "sudo apt update && sudo apt install --no-install-recommends ffmpeg",
                 "Solo le dipendenze indispensabili. Su Ubuntu 24.10 il pacchetto non ha raccomandazioni, quindi e' uguale al completo: su Linux la "
                 "distribuzione offre una sola build.")],
        "dnf": [("Completo", "sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm && "
                             "sudo dnf install ffmpeg --allowerasing",
                 "Fedora: il ffmpeg con tutti i codec e' nel repository RPM Fusion (il primo comando lo aggiunge)."),
                ("Essenziale", "sudo dnf install ffmpeg-free",
                 "La build di Fedora, senza i codec coperti da brevetti (niente H.264/H.265).")],
        "pacman": [("Completo", "sudo pacman -S ffmpeg", "La build completa di Arch."),
                   ("Essenziale", "sudo pacman -S ffmpeg-headless", "Come ffmpeg ma senza le librerie per schermo e finestre (meno dipendenze).")],
        "zypper": [("Completo", "sudo zypper install ffmpeg",
                    "openSUSE: per tutti i codec serve il repository Packman (https://en.opensuse.org/Additional_package_repositories).")],
        "brew": [("Completo", "brew install ffmpeg", "Con Homebrew.")],
        "winget": [("Completo", "winget install ffmpeg", "Oppure scaricalo da PitStudio (Strumenti > ffmpeg).")],
    },
    "vlc": {
        "apt": [("VLC", "sudo apt update && sudo apt install vlc", "")],
        "dnf": [("VLC", "sudo dnf install vlc", "Su Fedora VLC e' nel repository RPM Fusion: aggiungilo prima (vedi i comandi di ffmpeg).")],
        "pacman": [("VLC", "sudo pacman -S vlc", "")],
        "zypper": [("VLC", "sudo zypper install vlc", "Da Packman, come ffmpeg.")],
        "brew": [("VLC", "brew install --cask vlc", "")],
        "winget": [("VLC", "winget install VideoLAN.VLC", "")],
    },
    "mpv": {
        "apt": [("mpv", "sudo apt update && sudo apt install mpv", "")],
        "dnf": [("mpv", "sudo dnf install mpv", "Su Fedora mpv e' nel repository RPM Fusion.")],
        "pacman": [("mpv", "sudo pacman -S mpv", "")],
        "zypper": [("mpv", "sudo zypper install mpv", "")],
        "brew": [("mpv", "brew install mpv", "")],
        "winget": [("mpv", "winget install mpv", "")],
    },
}


def comandi_installazione(programma="ffmpeg"):
    """I comandi da copiare per installare ffmpeg, vlc o mpv con il gestore di pacchetti di questo computer: una lista di dizionari
    {etichetta, comando, nota}. Per ffmpeg ci sono la versione «Completo» e quella «Essenziale». Se il gestore non si riconosce restituisce
    i comandi di tutti i gestori comuni, con il nome del gestore davanti all'etichetta."""
    if programma not in _COMANDI:
        raise ValueError("programma sconosciuto: scegli tra " + ", ".join(_COMANDI))
    tabella = _COMANDI[programma]
    gestore = _gestore_pacchetti()
    if gestore in tabella:
        return [dict(etichetta=e, comando=c, nota=n) for e, c, n in tabella[gestore]]
    return [dict(etichetta=f"{g}: {e}", comando=c, nota=n) for g in ("apt", "dnf", "pacman", "zypper") for e, c, n in tabella.get(g, [])]


def istruzioni_ffmpeg():
    """Come procurarsi ffmpeg su questo computer (un testo da mostrare a chi ne ha bisogno)."""
    if _gestore_pacchetti() == "winget":
        return ("Scrivi multimedia.scarica_ffmpeg() per scaricarlo (circa 115 MB, dal sito ufficiale), oppure usa Strumenti > ffmpeg in PitStudio, "
                "oppure installalo tu (Windows: winget install ffmpeg).")
    voci = comandi_installazione("ffmpeg")
    if _gestore_pacchetti() is None:
        return "Installa il pacchetto ffmpeg con il gestore di pacchetti della tua distribuzione. Per esempio:\n" + "\n".join(f"  {v['comando']}" for v in voci[:4])
    return "Installalo con il gestore di pacchetti:\n" + "\n".join(f"  {v['etichetta']}: {v['comando']}" for v in voci)


def _richiedi(programma):
    p = trova_ffmpeg(programma)
    if not p:
        raise FfmpegNonTrovato("ffmpeg non e' installato. " + istruzioni_ffmpeg())
    return p


def versione_ffmpeg():
    """La prima riga di 'ffmpeg -version', oppure None se ffmpeg manca."""
    p = trova_ffmpeg()
    if not p:
        return None
    r = _subprocess.run([p, "-version"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                        creationflags=_SENZA_FINESTRA)
    return r.stdout.splitlines()[0] if r.stdout else None


def _esegui(argomenti, durata=None, avanzamento=None):
    """Lancia ffmpeg. Con `avanzamento` richiama avanzamento(frazione da 0 a 1) mentre lavora (serve la durata)."""
    comando = [_richiedi("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y"]
    if avanzamento and durata:
        comando += ["-progress", "pipe:1", "-nostats"]
    comando += [str(a) for a in argomenti]
    with _tempfile.TemporaryFile() as errori:
        processo = _subprocess.Popen(comando, stdout=_subprocess.PIPE if (avanzamento and durata) else _subprocess.DEVNULL,
                                     stderr=errori, stdin=_subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace",
                                     creationflags=_SENZA_FINESTRA)
        if avanzamento and durata:
            for riga in processo.stdout:
                if riga.startswith("out_time_us=") or riga.startswith("out_time_ms="):
                    try:
                        avanzamento(max(0.0, min(1.0, int(riga.split("=", 1)[1]) / 1e6 / durata)))
                    except ValueError:
                        pass
            avanzamento(1.0)
        processo.wait()
        if processo.returncode != 0:
            errori.seek(0)
            testo = errori.read().decode("utf-8", "replace").strip().splitlines()
            raise ErroreMultimedia("ffmpeg non e' riuscito: " + (" | ".join(testo[-3:]) or f"codice {processo.returncode}"))


def info(file):
    """Cosa c'e' dentro un file audio o video: {'formato', 'durata', 'dimensione', 'video': [...], 'audio': [...]}."""
    import json
    sonda = _richiedi("ffprobe")
    if not _os.path.isfile(file):
        raise FileNotFoundError(f"File non trovato: {file}")
    r = _subprocess.run([sonda, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(file)],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=_SENZA_FINESTRA)
    if r.returncode != 0:
        raise ErroreMultimedia("Non riesco a leggere il file: " + (r.stderr.strip().splitlines() or ["formato sconosciuto"])[-1])
    dati = json.loads(r.stdout or "{}")
    formato = dati.get("format", {})
    esito = {"file": str(file), "formato": formato.get("format_name", ""), "durata": float(formato.get("duration", 0) or 0),
             "dimensione": int(formato.get("size", 0) or 0), "video": [], "audio": []}
    for s in dati.get("streams", []):
        if s.get("codec_type") == "video":
            num, _, den = (s.get("avg_frame_rate") or "0/1").partition("/")
            fps = round(float(num) / float(den), 3) if den and float(den) else 0.0
            esito["video"].append({"codec": s.get("codec_name"), "larghezza": s.get("width"), "altezza": s.get("height"), "fps": fps})
        elif s.get("codec_type") == "audio":
            esito["audio"].append({"codec": s.get("codec_name"), "canali": s.get("channels"),
                                   "frequenza": int(s.get("sample_rate", 0) or 0)})
    return esito


def durata_di(file):
    """Durata in secondi di un file audio o video."""
    return info(file)["durata"]


def _controlla(origine, destinazione, sovrascrivi=False):
    if not _os.path.isfile(origine):
        raise FileNotFoundError(f"File non trovato: {origine}")
    uguali = _os.path.normcase(_os.path.abspath(origine)) == _os.path.normcase(_os.path.abspath(destinazione))
    if not uguali and _os.path.exists(destinazione):
        try:
            uguali = _os.path.samefile(origine, destinazione)
        except OSError:
            uguali = False
    if uguali:
        raise ErroreMultimedia("Il file di destinazione deve essere diverso dall'originale: altrimenti l'originale andrebbe perso.")
    if not sovrascrivi and _os.path.exists(destinazione):
        raise ErroreMultimedia(f"Il file di destinazione esiste gia': {destinazione}. Per sostituirlo usa sovrascrivi=True; altrimenti scegli un altro nome.")
    cartella = _os.path.dirname(_os.path.abspath(destinazione))
    _os.makedirs(cartella, exist_ok=True)
    return _os.path.abspath(destinazione)


def converti(origine, destinazione, avanzamento=None, sovrascrivi=False):
    """Converte un file nel formato scelto dall'estensione di `destinazione` (.mp3, .wav, .ogg, .mp4, .gif, ...)."""
    destinazione = _controlla(origine, destinazione, sovrascrivi)
    _esegui(["-i", origine, destinazione], durata=durata_di(origine) if avanzamento else None, avanzamento=avanzamento)
    return destinazione


def estrai_audio(video, destinazione, avanzamento=None, sovrascrivi=False):
    """Salva solo l'audio di un video (ad esempio 'film.mp4' -> 'colonna.mp3')."""
    destinazione = _controlla(video, destinazione, sovrascrivi)
    _esegui(["-i", video, "-vn", destinazione], durata=durata_di(video) if avanzamento else None, avanzamento=avanzamento)
    return destinazione


def taglia(origine, destinazione, inizio=0, fine=None, avanzamento=None, sovrascrivi=False):
    """Salva il pezzo tra `inizio` e `fine` (in secondi). Senza `fine` va fino in fondo."""
    destinazione = _controlla(origine, destinazione, sovrascrivi)
    if fine is not None and fine <= inizio:
        raise ValueError("`fine` deve essere dopo `inizio`")
    totale = (fine if fine is not None else durata_di(origine)) - inizio
    argomenti = ["-i", origine, "-ss", inizio] + (["-to", fine] if fine is not None else []) + [destinazione]
    _esegui(argomenti, durata=totale if avanzamento else None, avanzamento=avanzamento)
    return destinazione


def fotogramma(video, tempo, destinazione, sovrascrivi=False):
    """Salva come immagine (.png, .jpg) il fotogramma di un video al secondo `tempo`."""
    destinazione = _controlla(video, destinazione, sovrascrivi)
    _esegui(["-ss", tempo, "-i", video, "-frames:v", 1, destinazione])
    return destinazione


def riduci(video, destinazione, larghezza=640, avanzamento=None, sovrascrivi=False):
    """Salva il video con la larghezza scelta (l'altezza segue, senza deformare)."""
    destinazione = _controlla(video, destinazione, sovrascrivi)
    _esegui(["-i", video, "-vf", f"scale={int(larghezza)}:-2", destinazione],
            durata=durata_di(video) if avanzamento else None, avanzamento=avanzamento)
    return destinazione


def a_wav(file, destinazione=None):
    """Converte un file audio (mp3, ogg, m4a, ...) in .wav, cosi' lo puo' suonare il modulo suono."""
    if destinazione is None:
        destinazione = _os.path.join(_tempfile.gettempdir(), "pitonit_suono",
                                     _hashlib.md5(_os.path.abspath(file).encode("utf-8")).hexdigest() + ".wav")
    if _os.path.isfile(destinazione) and _os.path.getmtime(destinazione) >= _os.path.getmtime(file):
        return destinazione
    return converti(file, destinazione, sovrascrivi=True)          # e' una copia temporanea: si rifa' quando serve


def _sha256_atteso(url):
    try:
        with _richieste.urlopen(_richieste.Request(url + ".sha256", headers={"User-Agent": "pytonIta"}), timeout=30) as r:
            return r.read().decode("ascii", "replace").split()[0].strip().lower()
    except Exception:
        return None


def varianti_ffmpeg():
    """Le versioni di ffmpeg che si possono scaricare: lista di dizionari (chiave, nome, dimensione_mb, descrizione, sito)."""
    return [dict(v, chiave=k) for k, v in VARIANTI.items()]


def _chiave_variante(variante):
    chiave = _ALIAS_VARIANTI.get(str(variante).lower(), str(variante).lower())
    if chiave not in VARIANTI:
        raise ErroreMultimedia(f"Versione di ffmpeg sconosciuta: {variante!r}. Scegli tra: " + ", ".join(VARIANTI))
    return chiave


def _risolvi_variante(chiave):
    """(indirizzo, impronta SHA-256) dell'archivio da scaricare per la variante scelta."""
    if chiave == "essenziale":
        return URL_FFMPEG, _sha256_atteso(URL_FFMPEG)
    # completa: l'ultima serie stabile (ffmpeg-nX.Y-latest-win64-gpl-X.Y.zip) dall'elenco delle impronte; se non c'e', la «master»
    try:
        with _richieste.urlopen(_richieste.Request(URL_BASE_COMPLETA + "checksums.sha256", headers={"User-Agent": "pytonIta"}), timeout=30) as r:
            righe = r.read().decode("utf-8", "replace").splitlines()
    except Exception:
        return URL_BASE_COMPLETA + "ffmpeg-master-latest-win64-gpl.zip", None
    stabili, master = [], None
    for riga in righe:
        parti = riga.split()
        if len(parti) != 2:
            continue
        impronta, nome = parti[0].lower(), parti[1].lstrip("*")
        m = _re.match(r"^ffmpeg-n(\d+)\.(\d+)-latest-win64-gpl-\1\.\2\.zip$", nome)
        if m:
            stabili.append(((int(m.group(1)), int(m.group(2))), nome, impronta))
        elif nome == "ffmpeg-master-latest-win64-gpl.zip":
            master = (nome, impronta)
    if stabili:
        _, nome, impronta = max(stabili)
    elif master:
        nome, impronta = master
    else:
        raise ErroreMultimedia("Non trovo la versione completa di ffmpeg nell'elenco online: riprova piu' tardi.")
    return URL_BASE_COMPLETA + nome, impronta


def variante_installata(cartella=CARTELLA_FFMPEG):
    """Quale versione hai scaricato con scarica_ffmpeg(): dizionario (variante, archivio, data) oppure None."""
    import json
    try:
        with open(_os.path.join(cartella, "variante.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def scarica_ffmpeg(url=None, cartella=CARTELLA_FFMPEG, avanzamento=None, sha256=None, interrompi=None, variante="essenziale"):
    """Scarica ffmpeg in `cartella` e restituisce il percorso di ffmpeg. `variante`: 'essenziale' (circa 115 MB, quello che serve quasi
    sempre) oppure 'completa' (circa 200 MB, con quasi tutte le librerie; si accetta anche 'essentials' e 'full'). Se scegli l'altra
    versione, sostituisce quella gia' scaricata. Controlla l'impronta SHA-256. `avanzamento(byte_scaricati, byte_totali)` e `interrompi()`
    sono facoltativi. Con `url=` si scarica un archivio qualunque (con `sha256=`). Funziona solo su Windows (altrove: apt, brew, ...)."""
    if _os.name != "nt":
        raise ErroreMultimedia("Il download automatico e' solo per Windows. " + istruzioni_ffmpeg())
    chiave = None
    if url is None:
        chiave = _chiave_variante(variante)
        url, atteso = _risolvi_variante(chiave)
        atteso = (sha256 or atteso or "").lower()
    else:
        atteso = (sha256 or _sha256_atteso(url) or "").lower()
    if not atteso:
        raise ErroreMultimedia("Non riesco a ottenere l'impronta di controllo del file: riprova piu' tardi.")
    _os.makedirs(cartella, exist_ok=True)
    zip_temp = _os.path.join(cartella, "scaricamento.zip.parte")
    impronta = _hashlib.sha256()
    nuovi = []
    try:
        with _richieste.urlopen(_richieste.Request(url, headers={"User-Agent": "pytonIta"}), timeout=60) as r, open(zip_temp, "wb") as f:
            totale = int(r.headers.get("Content-Length", 0) or 0)
            fatti = 0
            while True:
                blocco = r.read(1 << 20)
                if not blocco:
                    break
                f.write(blocco)
                impronta.update(blocco)
                fatti += len(blocco)
                if avanzamento:
                    avanzamento(fatti, totale)
                if interrompi and interrompi():
                    raise ErroreMultimedia("Download interrotto.")
        if impronta.hexdigest().lower() != atteso:
            raise ErroreMultimedia("Il file scaricato non corrisponde all'impronta attesa: non lo uso.")
        cartella_bin = _os.path.join(cartella, "bin")
        _os.makedirs(cartella_bin, exist_ok=True)
        trovati = []
        with _zipfile.ZipFile(zip_temp) as z:
            for voce in z.infolist():
                nome = _os.path.basename(voce.filename).lower()
                if nome in ("ffmpeg.exe", "ffprobe.exe") and "/bin/" in voce.filename.replace("\\", "/"):
                    temporaneo = _os.path.join(cartella_bin, nome + ".nuovo")
                    nuovi.append((temporaneo, _os.path.join(cartella_bin, nome)))
                    with z.open(voce) as sorgente, open(temporaneo, "wb") as dest:
                        _shutil.copyfileobj(sorgente, dest)
                    trovati.append(nome)
        if "ffmpeg.exe" not in trovati:
            raise ErroreMultimedia("Nell'archivio scaricato non c'e' ffmpeg.exe.")
        try:
            for temporaneo, definitivo in nuovi:
                _os.replace(temporaneo, definitivo)
        except PermissionError:
            raise ErroreMultimedia("ffmpeg e' in uso da un altro programma: chiudilo e riprova.") from None
        nuovi = []
        import json
        import datetime
        with open(_os.path.join(cartella, "variante.json"), "w", encoding="utf-8") as f:
            json.dump({"variante": chiave or "personalizzata", "archivio": url.rsplit("/", 1)[-1], "data": datetime.date.today().isoformat()}, f)
    finally:
        for temporaneo, _ in nuovi:
            if _os.path.exists(temporaneo):
                _os.remove(temporaneo)
        if _os.path.exists(zip_temp):
            _os.remove(zip_temp)
    return _os.path.join(cartella, "bin", "ffmpeg.exe")
