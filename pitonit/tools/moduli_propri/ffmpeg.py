
"""ffmpeg in italiano: una libreria che AVVOLGE ffmpeg e ffprobe (senza includerli) e ne espone tutto
come funzioni, proprieta' e oggetti.

    importa ffmpeg

    ffmpeg.versione                       # versione installata (proprieta' del modulo)
    ffmpeg.filtri().cerca("blur")         # catalogo di tutti i filtri di QUESTA build di ffmpeg
    ffmpeg.aiuto_filtro("scale")          # le opzioni di un filtro, con tipo, valori e descrizione

    (ffmpeg.apri("film.mp4", inizio=10, durata=5)     # un comando si costruisce a catena
        .ridimensiona(larghezza=640)
        .velocita(2)
        .codec_video("libx264").qualita(23)
        .salva("scena.mp4"))

Tutto cio' che ffmpeg sa fare e' raggiungibile: opzioni con nome italiano (`codec_video`, `qualita`, ...), qualunque
altra opzione con `.opzione("-nome", valore)`, qualunque filtro con `.video.nome_filtro(...)` e `.audio.nome_filtro(...)`,
grafi complessi con `.filtro_complesso(...)` e, per tutto il resto, `ffmpeg.esegui_argomenti(...)`.
"""
import collections as _collezioni
import datetime as _data
import difflib as _difflib
import json as _json
import os as _os
import re as _re
import subprocess as _subprocess
import sys as _sistema
import tempfile as _tempfile
import threading as _thread
import time as _tempo_modulo

from multimedia import (trova_ffmpeg, scarica_ffmpeg, FfmpegNonTrovato, ErroreMultimedia, URL_FFMPEG,
                        CARTELLA_FFMPEG, _richiedi, _SENZA_FINESTRA)


class ErroreFfmpeg(ErroreMultimedia):
    """ffmpeg (o ffprobe) ha dato errore. Ha: .comando (la riga di comando), .codice, .messaggi (le ultime righe di ffmpeg)."""

    def __init__(self, testo, comando=None, codice=None, messaggi=None):
        super().__init__(testo)
        self.comando = comando
        self.codice = codice
        self.messaggi = messaggi or []


# =====================================================================================================
#  Oggetti semplici: voci di catalogo, flussi, ...
# =====================================================================================================
class Voce(dict):
    """Un dizionario a cui si accede anche come proprieta': voce.nome, voce.descrizione, ..."""

    def __getattr__(self, nome):
        try:
            return self[nome]
        except KeyError:
            raise AttributeError(nome) from None

    def __dir__(self):
        return sorted(set(list(self.keys()) + dir(dict)))


class Catalogo(list):
    """Elenco di Voce con una ricerca: filtri().cerca("blur"), codec().nome("h264")."""

    def cerca(self, testo, campi=("nome", "descrizione")):
        """Le voci che contengono `testo` (senza badare alle maiuscole) in uno dei campi."""
        t = testo.lower()
        return Catalogo(v for v in self if any(t in str(v.get(c, "")).lower() for c in campi))

    def nome(self, nome):
        """La voce che si chiama esattamente `nome` (poi per alias come 'mov,mp4', poi senza badare alle maiuscole), oppure None."""
        for v in self:
            if v.get("nome") == nome:
                return v
        for v in self:
            if nome in str(v.get("nome", "")).split(","):
                return v
        for v in self:
            if str(v.get("nome", "")).lower() == nome.lower():
                return v
        return None

    def nomi(self):
        return [v["nome"] for v in self]

    def filtra(self, **condizioni):
        """Le voci con questi valori: codec().filtra(tipo="video", codifica=True)."""
        return Catalogo(v for v in self if all(v.get(k) == x for k, x in condizioni.items()))

    def tabella(self, campi=("nome", "descrizione"), massimo=None):
        """Un testo con una voce per riga, da stampare."""
        righe = []
        for v in (self if massimo is None else self[:massimo]):
            righe.append("  ".join(str(v.get(c, "")).ljust(18) if i < len(campi) - 1 else str(v.get(c, ""))
                                   for i, c in enumerate(campi)))
        return "\n".join(righe)


# =====================================================================================================
#  Esecuzione di ffmpeg / ffprobe
# =====================================================================================================
_cache = {}


def _testo_comando(argomenti):
    if _os.name == "nt":
        return _subprocess.list2cmdline([str(a) for a in argomenti])
    import shlex
    return " ".join(shlex.quote(str(a)) for a in argomenti)


def _lancia_testo(programma, argomenti, memorizza=True):
    """Esegue ffmpeg/ffprobe e restituisce l'output di testo (stdout + stderr). Le risposte dei cataloghi si ricordano."""
    percorso = _richiedi(programma)
    chiave = (percorso, tuple(argomenti))
    if memorizza and chiave in _cache:
        return _cache[chiave]
    r = _subprocess.run([percorso, "-hide_banner"] + [str(a) for a in argomenti], capture_output=True, text=True,
                        encoding="utf-8", errors="replace", creationflags=_SENZA_FINESTRA, stdin=_subprocess.DEVNULL)
    uscita = (r.stdout or "") + (r.stderr or "")
    if memorizza:
        _cache[chiave] = uscita
    return uscita


def svuota_cache():
    """Dimentica i cataloghi letti da ffmpeg (utile dopo aver cambiato versione di ffmpeg)."""
    _cache.clear()


def esegui_argomenti(*argomenti, programma="ffmpeg", avanzamento=None, durata=None):
    """Lancia ffmpeg (o `programma="ffprobe"`) con gli argomenti che vuoi, tali e quali. Ritorna l'output di testo.
    La porta di servizio per tutto cio' che il resto della libreria non copre."""
    if programma == "ffmpeg" and (avanzamento or durata):
        c = Comando()
        c._grezzo = [str(a) for a in argomenti]
        return c.esegui(avanzamento=avanzamento)
    percorso = _richiedi(programma)
    comando = [percorso, "-hide_banner"] + [str(a) for a in argomenti]
    r = _subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace",
                        creationflags=_SENZA_FINESTRA, stdin=_subprocess.DEVNULL)
    if r.returncode != 0:
        raise ErroreFfmpeg(f"{programma} e' terminato con errore ({r.returncode}): " + " | ".join((r.stderr or "").strip().splitlines()[-3:]),
                           comando=_testo_comando(comando), codice=r.returncode, messaggi=(r.stderr or "").splitlines()[-30:])
    return (r.stdout or "") + (r.stderr or "")


# =====================================================================================================
#  Proprieta' del modulo: ffmpeg.versione, ffmpeg.percorso, ...
# =====================================================================================================
def _proprieta(nome):
    if nome == "percorso":
        return trova_ffmpeg("ffmpeg")
    if nome == "percorso_sonda":
        return trova_ffmpeg("ffprobe")
    if nome == "disponibile":
        return trova_ffmpeg("ffmpeg") is not None
    if nome == "versione":
        m = _re.search(r"version (\S+)", _lancia_testo("ffmpeg", ["-version"]))
        return m.group(1) if m else None
    if nome == "configurazione":
        m = _re.search(r"configuration:(.*)", _lancia_testo("ffmpeg", ["-version"]))
        return [x[2:] for x in m.group(1).split() if x.startswith("--")] if m else []
    if nome == "licenza":
        c = _proprieta("configurazione")
        return "GPL v3 (non libera)" if "enable-nonfree" in c else "GPL v3" if "enable-version3" in c and "enable-gpl" in c \
            else "GPL" if "enable-gpl" in c else "LGPL"
    if nome == "librerie":
        out = {}
        for r in _lancia_testo("ffmpeg", ["-version"]).splitlines():
            m = _re.match(r"(lib\w+)\s+(\S+)", r)
            if m:
                out[m.group(1)] = m.group(2)
        return out
    raise AttributeError(nome)


_PROPRIETA = ("percorso", "percorso_sonda", "disponibile", "versione", "configurazione", "licenza", "librerie")


def __getattr__(nome):
    if nome in _PROPRIETA:
        return _proprieta(nome)
    raise AttributeError(f"module 'ffmpeg' has no attribute {nome!r}")


def __dir__():
    return sorted(list(globals()) + list(_PROPRIETA))


# =====================================================================================================
#  Cataloghi: filtri, codec, formati, ...  (letti da QUESTA build di ffmpeg)
# =====================================================================================================
def _dopo_trattini(testo):
    righe = testo.splitlines()
    for i, r in enumerate(righe):
        if _re.match(r"^\s*-{3,}\s*$", r):
            return righe[i + 1:]
    return righe


def filtri(tipo=None):
    """Tutti i filtri di ffmpeg. Ogni voce: nome, descrizione, tipo ('video', 'audio', 'sorgente', 'altro'),
    ingressi, uscite, timeline, comandi. Con tipo='video' o 'audio' restringe l'elenco."""
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", ["-filters"])):
        m = _re.match(r"^ ([T.][S.][C.]?)\s+(\S+)\s+(\S+)\s+(.*)$", r)
        if not m:
            continue
        flag, nome, firma, desc = m.groups()
        ing, _, usc = firma.partition("->")
        t = "audio" if "A" in usc else "video" if "V" in usc else "altro"
        out.append(Voce(nome=nome, descrizione=desc.strip(), tipo=t, ingressi=ing, uscite=usc, sorgente=ing.startswith("|") or ing == "|",
                        timeline=flag[0] == "T", comandi=flag.endswith("C")))
    return out if tipo is None else out.filtra(tipo=tipo)


def codec(tipo=None):
    """Tutti i codec noti. Voce: nome, descrizione, tipo ('video', 'audio', 'sottotitoli', 'dati', 'allegato'),
    decodifica, codifica, solo_intra, con_perdita, senza_perdita, codificatori, decodificatori."""
    tipi = {"V": "video", "A": "audio", "S": "sottotitoli", "D": "dati", "T": "allegato"}
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", ["-codecs"])):
        m = _re.match(r"^ ([D.])([E.])([VASDT.])([I.])([L.])([S.]) (\S+)\s+(.*)$", r)
        if not m:
            continue
        d, e, t, i, l, s, nome, desc = m.groups()
        cod = _re.search(r"\(encoders: ([^)]*)\)", desc)
        dec = _re.search(r"\(decoders: ([^)]*)\)", desc)
        desc = _re.sub(r"\s*\((en|de)coders: [^)]*\)", "", desc).strip()
        out.append(Voce(nome=nome, descrizione=desc, tipo=tipi.get(t, "altro"), decodifica=d == "D", codifica=e == "E", solo_intra=i == "I",
                        con_perdita=l == "L", senza_perdita=s == "S",
                        codificatori=cod.group(1).split() if cod else ([nome] if e == "E" else []),
                        decodificatori=dec.group(1).split() if dec else ([nome] if d == "D" else [])))
    return out if tipo is None else out.filtra(tipo=tipo)


def _codificatori_o_decodificatori(opzione, tipo):
    tipi = {"V": "video", "A": "audio", "S": "sottotitoli"}
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", [opzione])):
        m = _re.match(r"^ ([VAS.])([F.])([S.])([X.])([B.])([D.]) (\S+)\s+(.*)$", r)
        if not m:
            continue
        t, f, s, x, b, d, nome, desc = m.groups()
        out.append(Voce(nome=nome, descrizione=desc.strip(), tipo=tipi.get(t, "altro"), fette=f == "F", thread=s == "S",
                        sperimentale=x == "X", hardware=("nvenc" in nome or "qsv" in nome or "amf" in nome or "vaapi" in nome or "_mf" in nome)))
    return out if tipo is None else out.filtra(tipo=tipo)


def codificatori(tipo=None):
    """I codificatori disponibili (libx264, aac, libmp3lame, ...). Voce: nome, descrizione, tipo, hardware, sperimentale."""
    return _codificatori_o_decodificatori("-encoders", tipo)


def decodificatori(tipo=None):
    """I decodificatori disponibili."""
    return _codificatori_o_decodificatori("-decoders", tipo)


def formati(solo=None):
    """I formati di contenitore (mp4, mkv, wav, ...). Voce: nome, descrizione, lettura, scrittura, dispositivo.
    solo='lettura' o 'scrittura' restringe l'elenco."""
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", ["-formats"])):
        m = _re.match(r"^ ([D ])([E ])([d ]?)\s+(\S+)\s+(.*)$", r)
        if not m:
            continue
        d, e, dev, nome, desc = m.groups()
        out.append(Voce(nome=nome, descrizione=desc.strip(), lettura=d == "D", scrittura=e == "E", dispositivo=dev == "d",
                        estensioni=nome.split(",")))
    if solo == "lettura":
        return out.filtra(lettura=True)
    if solo == "scrittura":
        return out.filtra(scrittura=True)
    return out


def formati_pixel():
    """I formati dei pixel (yuv420p, rgb24, ...). Voce: nome, componenti, bit_per_pixel, profondita, ingresso, uscita, hardware, paletta."""
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", ["-pix_fmts"])):
        m = _re.match(r"^([I.])([O.])([H.])([P.])([B.])\s+(\S+)\s+(\d+)\s+(\d+)\s*(\S*)$", r)
        if m:
            i, o, h, p, b, nome, comp, bit, prof = m.groups()
            out.append(Voce(nome=nome, componenti=int(comp), bit_per_pixel=int(bit), profondita=prof, ingresso=i == "I",
                            uscita=o == "O", hardware=h == "H", paletta=p == "P"))
    return out


def formati_campione():
    """I formati dei campioni audio (s16, flt, ...). Voce: nome, bit."""
    out = Catalogo()
    for r in _lancia_testo("ffmpeg", ["-sample_fmts"]).splitlines():
        m = _re.match(r"^(\w+)\s+(\d+)\s*$", r)
        if m:
            out.append(Voce(nome=m.group(1), bit=int(m.group(2))))
    return out


def layout_canali():
    """I layout dei canali audio (mono, stereo, 5.1, ...). Voce: nome, descrizione (o canali)."""
    out = Catalogo()
    sezione = ""
    for r in _lancia_testo("ffmpeg", ["-layouts"]).splitlines():
        if r.rstrip().endswith(":"):
            sezione = r.strip().rstrip(":").lower()
            continue
        m = _re.match(r"^(\S+)\s+(.+)$", r)
        if m and m.group(1) != "NAME":
            out.append(Voce(nome=m.group(1), descrizione=m.group(2).strip(), genere="canale" if sezione.startswith("individual") else "layout"))
    return out


def protocolli():
    """I protocolli di rete e di file (file, http, rtmp, ...). Voce: nome, ingresso, uscita."""
    ing, usc, sez = set(), set(), None
    for r in _lancia_testo("ffmpeg", ["-protocols"]).splitlines():
        if r.strip() == "Input:":
            sez = "i"
        elif r.strip() == "Output:":
            sez = "o"
        elif sez and r.startswith("  "):
            (ing if sez == "i" else usc).add(r.strip())
    return Catalogo(Voce(nome=n, ingresso=n in ing, uscita=n in usc) for n in sorted(ing | usc))


def dispositivi():
    """I dispositivi di acquisizione e riproduzione (dshow, gdigrab, lavfi, ...)."""
    out = Catalogo()
    for r in _dopo_trattini(_lancia_testo("ffmpeg", ["-devices"])):
        m = _re.match(r"^ ([D ])([E ])\s+(\S+)\s*(.*)$", r)
        if m:
            out.append(Voce(nome=m.group(3), descrizione=m.group(4).strip(), lettura=m.group(1) == "D", scrittura=m.group(2) == "E"))
    return out


def accelerazioni():
    """Le accelerazioni hardware (cuda, dxva2, d3d11va, ...)."""
    righe = _lancia_testo("ffmpeg", ["-hwaccels"]).splitlines()
    return [r.strip() for r in righe[1:] if r.strip()]


def filtri_bitstream():
    """I filtri sui bitstream (h264_mp4toannexb, ...)."""
    righe = _lancia_testo("ffmpeg", ["-bsfs"]).splitlines()
    return [r.strip() for r in righe[1:] if r.strip() and not r.endswith(":")]


def colori():
    """I nomi dei colori noti a ffmpeg, con il codice esadecimale. Voce: nome, codice."""
    out = Catalogo()
    for r in _lancia_testo("ffmpeg", ["-colors"]).splitlines():
        m = _re.match(r"^(\w+)\s+(#[0-9a-fA-F]{6,8})\s*$", r)
        if m:
            out.append(Voce(nome=m.group(1), codice=m.group(2)))
    return out


# ---- aiuto su un filtro, un codec o un formato: le opzioni con tipo, valori e descrizione
_TIPI = {"int": "intero", "int64": "intero", "uint64": "intero", "float": "decimale", "double": "decimale", "string": "testo",
         "boolean": "booleano", "flags": "insieme di opzioni", "duration": "durata", "color": "colore", "rational": "frazione",
         "image_size": "dimensioni", "pix_fmt": "formato pixel", "sample_fmt": "formato campione", "binary": "binario",
         "dictionary": "dizionario", "video_rate": "fotogrammi al secondo", "channel_layout": "layout canali", "const": "costante"}


def _opzioni_da_aiuto(testo):
    opzioni, ultima = [], None
    for r in testo.splitlines():
        m = _re.match(r"^\s{1,4}-?(\S+)\s+<(\w+)>\s+([.A-Z]{8,12})\s*(.*)$", r)
        if m:
            nome, tipo, flag, resto = m.groups()
            intervallo = _re.search(r"\(from ([^ ]+) to ([^ )]+)\)", resto)
            predefinito = _re.search(r'\(default ("[^"]*"|[^)]*)\)', resto)
            desc = _re.sub(r"\s*\((from [^)]*|default [^)]*)\)", "", resto).strip()
            ultima = Voce(nome=nome, tipo=_TIPI.get(tipo, tipo), tipo_ffmpeg=tipo, descrizione=desc, valori_ammessi=[],
                          predefinito=(predefinito.group(1).strip('"') if predefinito else None),
                          minimo=intervallo.group(1) if intervallo else None, massimo=intervallo.group(2) if intervallo else None,
                          flag=flag)
            opzioni.append(ultima)
            continue
        m = _re.match(r"^\s{5,}(\S+)\s+(\S+)\s+([.A-Z]{8,12})\s*(.*)$", r)
        if m and ultima is not None:
            ultima["valori_ammessi"].append(Voce(nome=m.group(1), valore=m.group(2), descrizione=m.group(4).strip()))
    return opzioni


def _aiuto(tipo, nome):
    testo = _lancia_testo("ffmpeg", ["-h", f"{tipo}={nome}"])
    if _re.search(r"Unknown|No such|not found", testo.splitlines()[0] if testo.strip() else "Unknown", _re.I):
        raise ErroreFfmpeg(f"ffmpeg non conosce {tipo} {nome!r}")
    riga = next((r.strip() for r in testo.splitlines() if r.strip()), "")
    descrizione = ""
    for r in testo.splitlines()[1:4]:
        if r.startswith("  ") and "AVOptions" not in r and ":" not in r[:3]:
            descrizione = r.strip()
            break
    return Voce(nome=nome, titolo=riga, descrizione=descrizione, opzioni=_opzioni_da_aiuto(testo), testo=testo)


def aiuto_filtro(nome):
    """Cosa fa un filtro e quali opzioni ha: aiuto_filtro('scale').opzioni -> elenco di (nome, tipo, predefinito, minimo, massimo, valori_ammessi, descrizione)."""
    return _aiuto("filter", nome)


def aiuto_codificatore(nome):
    """Le opzioni di un codificatore (es. 'libx264')."""
    return _aiuto("encoder", nome)


def aiuto_decodificatore(nome):
    """Le opzioni di un decodificatore."""
    return _aiuto("decoder", nome)


def aiuto_scrittore(nome):
    """Le opzioni di un formato in scrittura (muxer, es. 'mp4')."""
    return _aiuto("muxer", nome)


def aiuto_lettore(nome):
    """Le opzioni di un formato in lettura (demuxer)."""
    return _aiuto("demuxer", nome)


def aiuto(argomento="long"):
    """Il testo d'aiuto di ffmpeg: aiuto() (opzioni principali), aiuto('full') (tutte), aiuto('filter=scale'), ..."""
    return _lancia_testo("ffmpeg", ["-h", argomento])


# =====================================================================================================
#  ffprobe: guardare dentro un file
# =====================================================================================================
_ETICHETTE = {"codec_name": "codec", "codec_long_name": "codec_esteso", "profile": "profilo", "width": "larghezza", "height": "altezza",
              "pix_fmt": "formato_pixel", "sample_rate": "frequenza", "channels": "canali", "channel_layout": "layout",
              "bit_rate": "bitrate", "nb_frames": "fotogrammi", "display_aspect_ratio": "rapporto", "index": "indice",
              "start_time": "inizio", "sample_fmt": "formato_campione", "bits_per_raw_sample": "bit_per_campione", "level": "livello",
              "field_order": "ordine_campi", "color_space": "spazio_colore", "color_range": "intervallo_colore", "tags": "tag"}
_TIPI_FLUSSO = {"video": "video", "audio": "audio", "subtitle": "sottotitoli", "data": "dati", "attachment": "allegato"}


def _numero(v):
    try:
        f = float(v)
        return int(f) if f == int(f) and "." not in str(v) else f
    except (TypeError, ValueError):
        return v


def _frazione(v):
    try:
        n, _, d = str(v).partition("/")
        return round(float(n) / float(d), 3) if d and float(d) else 0.0
    except ValueError:
        return 0.0


class Flusso(Voce):
    """Un flusso del file (video, audio, sottotitoli, ...): .tipo, .codec, .larghezza, .altezza, .fps, .canali, .frequenza, .lingua, ..."""

    def __init__(self, dati):
        super().__init__()
        for k, v in dati.items():
            self[_ETICHETTE.get(k, k)] = _numero(v) if k in ("width", "height", "channels", "sample_rate", "bit_rate", "nb_frames", "index",
                                                             "bits_per_raw_sample", "level") else v
        self["tipo"] = _TIPI_FLUSSO.get(dati.get("codec_type"), dati.get("codec_type"))
        self["fps"] = _frazione(dati.get("avg_frame_rate") or dati.get("r_frame_rate") or "0/1") if self["tipo"] == "video" else None
        self["durata"] = float(dati["duration"]) if dati.get("duration") not in (None, "N/A") else None
        tag = dati.get("tags", {}) or {}
        self["lingua"] = tag.get("language")
        self["titolo"] = tag.get("title")
        self["tag"] = tag
        self["rotazione"] = next((int(s.get("rotation", 0)) for s in dati.get("side_data_list", []) if "rotation" in s), 0)

    def __repr__(self):
        if self.tipo == "video":
            return f"<Flusso {self.indice} video {self.codec} {self.larghezza}x{self.altezza} {self.fps} fps>"
        if self.tipo == "audio":
            return f"<Flusso {self.indice} audio {self.codec} {self.canali} canali {self.frequenza} Hz>"
        return f"<Flusso {self.indice} {self.tipo} {self.get('codec')}>"


class Sonda:
    """Tutto cio' che ffprobe sa di un file. Proprieta': file, formato, durata, dimensione, bitrate, flussi, video, audio,
    sottotitoli, capitoli, tag, dati (la risposta completa di ffprobe)."""

    def __init__(self, file, **opzioni):
        self.file = str(file)
        argomenti = ["-v", "error", "-print_format", "json", "-show_format", "-show_streams", "-show_chapters", "-show_programs"]
        for k, v in opzioni.items():
            argomenti += [f"-{k}", str(v)]
        if not _os.path.exists(self.file) and "://" not in self.file:
            raise FileNotFoundError(f"File non trovato: {file}")
        sonda = _richiedi("ffprobe")
        comando = [sonda] + argomenti + [self.file]
        r = _subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            creationflags=_SENZA_FINESTRA, stdin=_subprocess.DEVNULL)
        if r.returncode != 0:
            raise ErroreFfmpeg("Non riesco a leggere il file: " + ((r.stderr or "").strip().splitlines() or ["formato sconosciuto"])[-1],
                               comando=_testo_comando(comando), codice=r.returncode, messaggi=(r.stderr or "").splitlines()[-10:])
        self.dati = _json.loads(r.stdout or "{}")
        f = self.dati.get("format", {})
        self.formato = f.get("format_name", "")
        self.formato_esteso = f.get("format_long_name", "")
        self.durata = float(f.get("duration", 0) or 0)
        self.dimensione = int(f.get("size", 0) or 0)
        self.bitrate = int(f.get("bit_rate", 0) or 0)
        self.inizio = float(f.get("start_time", 0) or 0)
        self.tag = f.get("tags", {}) or {}
        self.flussi = [Flusso(s) for s in self.dati.get("streams", [])]
        self.capitoli = [Voce(indice=c.get("id"), inizio=float(c.get("start_time", 0)), fine=float(c.get("end_time", 0)),
                              titolo=(c.get("tags") or {}).get("title")) for c in self.dati.get("chapters", [])]

    @property
    def video(self):
        return [f for f in self.flussi if f.tipo == "video"]

    @property
    def audio(self):
        return [f for f in self.flussi if f.tipo == "audio"]

    @property
    def sottotitoli(self):
        return [f for f in self.flussi if f.tipo == "sottotitoli"]

    @property
    def ha_video(self):
        return bool(self.video)

    @property
    def ha_audio(self):
        return bool(self.audio)

    @property
    def risoluzione(self):
        """(larghezza, altezza) del primo video, oppure None."""
        v = self.video
        return (v[0].larghezza, v[0].altezza) if v else None

    @property
    def fps(self):
        v = self.video
        return v[0].fps if v else None

    def json(self, rientro=2):
        return _json.dumps(self.dati, indent=rientro, ensure_ascii=False)

    def riassunto(self):
        """Un testo di poche righe con le cose principali."""
        righe = [f"{_os.path.basename(self.file)}: {self.formato}, {self.durata:.2f} s, {self.dimensione / 1048576:.2f} MB"]
        righe += ["  " + repr(f) for f in self.flussi]
        return "\n".join(righe)

    def __repr__(self):
        return f"<Sonda {_os.path.basename(self.file)} {self.formato} {self.durata:.2f}s {len(self.flussi)} flussi>"


def sonda(file, **opzioni):
    """Guarda dentro un file audio o video: ffmpeg.sonda('film.mp4').video[0].larghezza."""
    return Sonda(file, **opzioni)


# =====================================================================================================
#  Il comando: si costruisce a catena
# =====================================================================================================
def _tempo(v):
    """Secondi (numero), 'HH:MM:SS(.mmm)' o timedelta -> testo per ffmpeg."""
    if isinstance(v, _data.timedelta):
        v = v.total_seconds()
    if isinstance(v, (int, float)):
        return ("%.3f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
    return str(v)


def _secondi(v):
    """Come _tempo ma in numero di secondi (per i conti)."""
    if isinstance(v, _data.timedelta):
        return v.total_seconds()
    if isinstance(v, (int, float)):
        return float(v)
    parti = str(v).split(":")
    s = 0.0
    for p in parti:
        s = s * 60 + float(p)
    return s


def _scrivi_valore(v):
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return ("%.6f" % v).rstrip("0").rstrip(".")
    return str(v)


def _fuga(v):
    """Un valore dentro un filtro. Se contiene caratteri speciali dei grafi (barra rovesciata, apice, due punti, virgola,
    punto e virgola, parentesi quadre, spazi) lo mette tra apici e protegge dentro: barra raddoppiata, due punti con barra,
    apice = chiudi l'apice, scrivilo con la barra, riapri (regole di ffmpeg)."""
    t = _scrivi_valore(v)
    if not _re.search(r"[\\':,;\[\]\s]", t):
        return t
    B = chr(92)
    return "'" + t.replace(B, B + B).replace(":", B + ":").replace("'", "'" + B + "''") + "'"


def _senza_apici(testo):
    """Il testo di un filtro senza il contenuto dei valori tra apici (per leggerne la struttura)."""
    return _re.sub(r"'(?:[^']|'\\'')*'", "''", testo)


def _filtro(nome, posizionali=(), opzioni=None):
    """'nome=a:b:k=v' con i valori protetti. Gli argomenti con valore None si saltano."""
    parti = [_fuga(p) for p in posizionali if p is not None]
    for k, v in (opzioni or {}).items():
        if v is not None:
            parti.append(f"{k}={_fuga(v)}")
    return nome + ("=" + ":".join(parti) if parti else "")


def _percorso_filtro(p):
    """Un percorso di file dentro un filtro (subtitles, movie, ...): barre dritte e due punti protetti."""
    return _fuga(_os.path.abspath(str(p)).replace("\\", "/"))


class Avanzamento(Voce):
    """Lo stato di una elaborazione: .frazione (0-1, se la durata e' nota), .tempo (secondi di filmato fatti),
    .fotogrammi, .fps, .velocita (1.0 = tempo reale), .dimensione (byte), .bitrate, .terminato."""


class Risultato(Voce):
    """Come e' andata: .uscite (i file creati), .durata_elaborazione, .comando, .messaggi (righe di log di ffmpeg), .avanzamento."""


class _Filtri:
    """c.video.<nome filtro>(...) e c.audio.<nome filtro>(...): qualunque filtro di ffmpeg, anche quelli senza nome italiano."""

    def __init__(self, comando, tipo):
        object.__setattr__(self, "_c", comando)
        object.__setattr__(self, "_t", tipo)

    def __getattr__(self, nome):
        if nome.startswith("__"):
            raise AttributeError(nome)

        def aggiungi(*posizionali, **opzioni):
            self._c._filtro_su(self._t, _filtro(nome, posizionali, opzioni))
            return self._c
        aggiungi.__name__ = nome
        aggiungi.__doc__ = f"Aggiunge il filtro {self._t} '{nome}' (vedi ffmpeg.aiuto_filtro({nome!r}))."
        return aggiungi

    def __call__(self, nome, *posizionali, **opzioni):
        """c.video('scale', 640, -2) oppure c.video('scale', w=640, h=-2)."""
        self._c._filtro_su(self._t, _filtro(nome, posizionali, opzioni))
        return self._c

    def __dir__(self):
        try:
            return sorted(set(f.nome for f in filtri(self._t)))
        except Exception:
            return []


class _Uscita:
    def __init__(self):
        self.opzioni = []          # argomenti prima del file di uscita
        self.passi = []            # ('v'|'a', 'filtro') oppure ('sovrapponi', indice, x, y, opzioni)
        self.mappe = []
        self.file = None

    def vuota(self):
        return not (self.opzioni or self.passi or self.mappe)


class Comando:
    """Un comando di ffmpeg che si costruisce a catena. Ogni metodo restituisce il comando stesso.

    1. ingressi:   ffmpeg.apri("a.mp4", inizio=10)  /  .aggiungi("b.mp3")  /  .sorgente("testsrc=duration=3")
    2. cosa fare:  .ridimensiona(...)  .volume(...)  .codec_video(...)  .opzione("-crf", 20)  .video.hflip()
    3. dove:       .uscita("fuori.mp4")  (si puo' ripetere per piu' uscite)  oppure  .salva("fuori.mp4") che poi lancia
    4. eseguire:   .esegui()  oppure  .avvia()  (in sottofondo)
    Proprieta': .argomenti  .riga_di_comando  .durata_prevista  .ingressi  .uscite"""

    def __init__(self):
        self._globali = []
        self._ingressi = []         # [(opzioni, file)]
        self._uscite = []           # [_Uscita con file]
        self._corrente = _Uscita()
        self._complesso = []        # grafi scritti a mano
        self._grezzo = None         # lista di argomenti tali e quali (porta di servizio)
        self.video = _Filtri(self, "v")
        self.audio = _Filtri(self, "a")

    # ---- ingressi
    def aggiungi(self, file, **opzioni):
        """Aggiunge un ingresso (file, URL o dispositivo). Opzioni dell'ingresso: inizio, fine, durata, ripeti, formato, fps, risoluzione,
        ritmo_reale, accelerazione, e qualunque altra con il nome di ffmpeg (es. framerate=30, loop=1)."""
        self._ingressi.append((_opzioni_ingresso(opzioni), str(file)))
        return self

    def sorgente(self, descrizione, **opzioni):
        """Aggiunge un ingresso virtuale di lavfi: .sorgente('testsrc=duration=3:size=320x240'), .sorgente('sine=frequency=440:duration=2')."""
        self._ingressi.append((["-f", "lavfi"] + _opzioni_ingresso(opzioni), str(descrizione)))
        return self

    def impostazioni_globali(self, *argomenti):
        """Opzioni globali di ffmpeg, tali e quali: .impostazioni_globali('-loglevel', 'warning', '-threads', 4)."""
        self._globali += [str(a) for a in argomenti]
        return self

    def livello_log(self, livello="error"):
        """quiet, panic, fatal, error, warning, info, verbose, debug, trace."""
        return self.impostazioni_globali("-loglevel", livello)

    def senza_conferme(self):
        return self.impostazioni_globali("-y")

    def non_sovrascrivere(self):
        """Se il file di uscita esiste gia', ffmpeg si ferma."""
        self._globali = [g for g in self._globali if g != "-y"] + ["-n"]
        return self

    # ---- opzioni di uscita (generiche)
    def opzione(self, nome, valore=None, flusso=None):
        """Qualunque opzione dell'uscita, col nome di ffmpeg: .opzione('-crf', 20), .opzione('-b', '2M', flusso='v:0'), .opzione('-shortest')."""
        nome = nome if str(nome).startswith("-") else "-" + str(nome)
        if flusso:
            nome += ":" + str(flusso)
        self._corrente.opzioni.append(nome)
        if valore is not None:
            self._corrente.opzioni.append(_scrivi_valore(valore))
        return self

    def mappa(self, specifica, **opzioni):
        """-map: .mappa('0:v:0'), .mappa('1:a'), .mappa('0:a?')  (con '-' davanti esclude: .mappa('-0:s'))."""
        self._corrente.opzioni += ["-map", str(specifica)]
        return self

    def metadati(self, **valori):
        """Titolo, artista, ...: .metadati(title='Prova', artist='Io'). Per un flusso: .metadati_flusso('a:0', language='ita')."""
        for k, v in valori.items():
            self._corrente.opzioni += ["-metadata", f"{k}={v}"]
        return self

    def metadati_flusso(self, flusso, **valori):
        for k, v in valori.items():
            self._corrente.opzioni += [f"-metadata:s:{flusso}", f"{k}={v}"]
        return self

    def senza_metadati(self):
        self._corrente.opzioni += ["-map_metadata", "-1"]
        return self

    # ---- filtri
    def _filtro_su(self, tipo, testo):
        self._corrente.passi.append((tipo, testo))
        return self

    def filtro(self, nome, *posizionali, **opzioni):
        """Un filtro video qualunque: .filtro('hue', s=0)  (come .video('hue', s=0))."""
        return self._filtro_su("v", _filtro(nome, posizionali, opzioni))

    def filtro_audio(self, nome, *posizionali, **opzioni):
        """Un filtro audio qualunque: .filtro_audio('aecho', 0.8, 0.9, 1000, 0.3)."""
        return self._filtro_su("a", _filtro(nome, posizionali, opzioni))

    def filtro_complesso(self, descrizione, mappa=None):
        """Un grafo di filtri scritto a mano (-filter_complex): .filtro_complesso('[0:v][1:v]overlay=10:10[v]', mappa=['[v]', '0:a'])."""
        self._complesso.append(str(descrizione))
        for m in ([mappa] if isinstance(mappa, str) else (mappa or [])):
            self._corrente.opzioni += ["-map", m]
        return self

    # ---- uscite
    def uscita(self, file, **opzioni):
        """Chiude l'uscita corrente indicando il file. Le opzioni con nome si applicano a questa uscita (es. codec_video='libx264', qualita=23).
        Dopo si puo' descrivere un'altra uscita."""
        for nome, valore in opzioni.items():
            metodo = getattr(self, nome, None)
            if callable(metodo) and nome in _OPZIONI_USCITA:
                metodo(valore) if valore is not True else metodo()
            else:
                self.opzione(nome, None if valore is True else valore)
        self._corrente.file = str(file)
        self._uscite.append(self._corrente)
        self._corrente = _Uscita()
        return self

    def salva(self, file, avanzamento=None, fermata=None, controlla=False, **opzioni):
        """uscita(file) e poi esegui(): il modo piu' corto per finire. Ritorna il Risultato."""
        return self.uscita(file, **opzioni).esegui(avanzamento=avanzamento, fermata=fermata, controlla=controlla)

    @property
    def ingressi(self):
        return [f for _, f in self._ingressi]

    @property
    def uscite(self):
        return [u.file for u in self._uscite]

    # ---- composizione
    def _grafo(self, u):
        """Dalle operazioni dell'uscita ai pezzi di comando: (grafo_complesso | None, -vf, -af, mappe aggiuntive)."""
        passi = u.passi
        if not any(p[0] == "sovrapponi" for p in passi):
            vf = ",".join(p[1] for p in passi if p[0] == "v")
            af = ",".join(p[1] for p in passi if p[0] == "a")
            return None, vf, af, []
        # con le sovrapposizioni serve un grafo: la catena video passa da etichetta a etichetta
        pezzi, corrente, n = [], "[0:v]", 0
        catena = []
        for p in passi:
            if p[0] == "v":
                catena.append(p[1])
            elif p[0] == "sovrapponi":
                n += 1
                if catena:
                    pezzi.append(f"{corrente}{','.join(catena)}[c{n}]")
                    corrente, catena = f"[c{n}]", []
                _, indice, x, y, extra = p
                pezzi.append(f"{corrente}[{indice}:v]overlay=x={_fuga(x)}:y={_fuga(y)}{extra}[o{n}]")
                corrente = f"[o{n}]"
        if catena:
            pezzi.append(f"{corrente}{','.join(catena)}[fine]")
            corrente = "[fine]"
        af = ",".join(p[1] for p in passi if p[0] == "a")
        return ";".join(pezzi), "", af, [corrente]

    @property
    def argomenti(self):
        """La lista degli argomenti da dare a ffmpeg (senza il percorso del programma)."""
        if self._grezzo is not None:
            return list(self._grezzo)
        if not self._ingressi and not self._complesso:
            raise ErroreFfmpeg("Manca l'ingresso: usa ffmpeg.apri('file') oppure .aggiungi('file').")
        uscite = list(self._uscite)
        if not uscite:
            raise ErroreFfmpeg("Manca l'uscita: usa .uscita('file') oppure .salva('file').")
        argomenti = ["-hide_banner"] + (["-y"] if "-n" not in self._globali and "-y" not in self._globali else []) + list(self._globali)
        for opzioni, file in self._ingressi:
            argomenti += opzioni + ["-i", file]
        if self._complesso:
            argomenti += ["-filter_complex", ";".join(self._complesso)]
        for u in uscite:
            grafo, vf, af, mappe = self._grafo(u)
            if grafo:
                argomenti += ["-filter_complex", grafo]
                if not any(a == "-map" for a in u.opzioni):
                    argomenti += ["-map", mappe[0], "-map", "0:a?"]
            if vf:
                argomenti += ["-vf", vf]
            if af:
                argomenti += ["-af", af]
            argomenti += u.opzioni + [u.file]
        return argomenti

    @property
    def riga_di_comando(self):
        """La riga di comando completa, da copiare in un terminale."""
        return _testo_comando([_richiedi("ffmpeg") if trova_ffmpeg() else "ffmpeg"] + [str(a) for a in self.argomenti])

    def __str__(self):
        return self.riga_di_comando

    @property
    def durata_prevista(self):
        """Quanti secondi di filmato produrra' l'uscita (dai file in ingresso e dalle opzioni inizio/fine/durata/velocita), o None."""
        try:
            if not self._ingressi:
                return None
            opzioni, file = self._ingressi[0]
            if "-t" in opzioni:
                base = _secondi(opzioni[opzioni.index("-t") + 1])
            else:
                base = Sonda(file).durata
                if "-ss" in opzioni:
                    base -= _secondi(opzioni[opzioni.index("-ss") + 1])
                if "-to" in opzioni:
                    base = min(base, _secondi(opzioni[opzioni.index("-to") + 1]) - (_secondi(opzioni[opzioni.index("-ss") + 1]) if "-ss" in opzioni else 0))
            u = self._uscite[0] if self._uscite else self._corrente
            if "-t" in u.opzioni:
                base = min(base, _secondi(u.opzioni[u.opzioni.index("-t") + 1]))
            for tipo, f in u.passi:
                m = _re.match(r"setpts=PTS/([\d.]+)$", f) if tipo == "v" else None
                if m:
                    base /= float(m.group(1))
            return max(base, 0.0)
        except Exception:
            return None

    # ---- esecuzione
    def controlla(self):
        """Confronta filtri e opzioni usati con quelli di questa build di ffmpeg. Ritorna la lista dei problemi (vuota = tutto bene)."""
        problemi = []
        noti = {f.nome: f for f in filtri()}
        usati = [(t, f) for u in self._uscite + [self._corrente] for t, f in u.passi if t in ("v", "a")]
        for tipo, testo in usati:
            for parte in _senza_apici(testo).split(","):
                nome, _, resto = parte.partition("=")
                if nome not in noti:
                    vicini = _difflib.get_close_matches(nome, list(noti), n=3)
                    problemi.append(f"filtro sconosciuto: {nome}" + (f" (forse {', '.join(vicini)}?)" if vicini else ""))
                    continue
                if "=" in resto:
                    try:
                        validi = {o.nome for o in aiuto_filtro(nome).opzioni}
                    except ErroreFfmpeg:
                        continue
                    for m in _re.finditer(r"(?:^|:)([A-Za-z_]\w*)=", resto):
                        if validi and m.group(1) not in validi:
                            vicini = _difflib.get_close_matches(m.group(1), list(validi), n=3)
                            problemi.append(f"{nome}: opzione sconosciuta {m.group(1)!r}" + (f" (forse {', '.join(vicini)}?)" if vicini else ""))
        return problemi

    def avvia(self, avanzamento=None):
        """Lancia ffmpeg in sottofondo e ritorna subito un Processo (con .aspetta(), .ferma(), .avanzamento, .in_corso)."""
        return Processo(self, avanzamento)

    def esegui(self, avanzamento=None, fermata=None, controlla=False):
        """Lancia ffmpeg e aspetta la fine. `avanzamento(stato)` e' chiamata di continuo con un Avanzamento; `fermata()` ritorna True per
        interrompere. Ritorna un Risultato; se ffmpeg da' errore solleva ErroreFfmpeg (con .comando e .messaggi)."""
        if controlla:
            problemi = self.controlla()
            if problemi:
                raise ErroreFfmpeg("Il comando ha dei problemi: " + "; ".join(problemi))
        p = self.avvia(avanzamento)
        while p.in_corso:
            if fermata and fermata():
                p.ferma()
                break
            _tempo_modulo.sleep(0.02)
        return p.aspetta()


class Processo:
    """Un ffmpeg in esecuzione. .in_corso, .avanzamento (l'ultimo stato), .codice, .aspetta(tempo=None) -> Risultato, .ferma()."""

    def __init__(self, comando, avanzamento=None):
        self.comando = comando
        self._argomenti = [_richiedi("ffmpeg")] + [str(a) for a in comando.argomenti]
        self._durata = comando.durata_prevista if comando._grezzo is None else None
        self._chiama = avanzamento
        self.avanzamento = Avanzamento(frazione=0.0 if self._durata else None, tempo=0.0, fotogrammi=0, fps=0.0, velocita=0.0, dimensione=0,
                                       bitrate=None, terminato=False)
        self._log = _collezioni.deque(maxlen=5000)
        self._fermato = False
        self._inizio = _tempo_modulo.time()
        extra = ["-progress", "pipe:1", "-nostats"]
        a = self._argomenti
        self._processo = _subprocess.Popen(a[:1] + extra + a[1:], stdout=_subprocess.PIPE, stderr=_subprocess.PIPE, stdin=_subprocess.PIPE,
                                           text=True, encoding="utf-8", errors="replace", creationflags=_SENZA_FINESTRA)
        self._t_err = _thread.Thread(target=self._leggi_errori, daemon=True)
        self._t_out = _thread.Thread(target=self._leggi_progresso, daemon=True)
        self._t_err.start()
        self._t_out.start()

    def _leggi_errori(self):
        for riga in self._processo.stderr:
            self._log.append(riga.rstrip())

    def _leggi_progresso(self):
        blocco = {}
        for riga in self._processo.stdout:
            k, _, v = riga.strip().partition("=")
            blocco[k] = v
            if k == "progress":
                self._aggiorna(blocco)
                blocco = {}

    def _aggiorna(self, b):
        def num(chiave, f=float, predefinito=0):
            try:
                return f(b.get(chiave, predefinito))
            except ValueError:
                return predefinito
        t = max(num("out_time_us", int) / 1e6, num("out_time_ms", int) / 1e6) if b.get("out_time_us", "N/A") != "N/A" else 0.0
        velocita = b.get("speed", "0x").strip().rstrip("x")
        a = self.avanzamento
        a.update(tempo=t, fotogrammi=num("frame", int), fps=num("fps"), dimensione=num("total_size", int),
                 velocita=float(velocita) if velocita not in ("", "N/A") else 0.0, bitrate=b.get("bitrate"),
                 terminato=b.get("progress") == "end")
        a["frazione"] = (1.0 if a.terminato else min(1.0, t / self._durata)) if self._durata else (1.0 if a.terminato else None)
        if self._chiama:
            try:
                self._chiama(a)
            except Exception:
                pass

    @property
    def in_corso(self):
        return self._processo.poll() is None

    @property
    def codice(self):
        return self._processo.poll()

    def ferma(self):
        """Chiede a ffmpeg di finire ordinatamente (come premere Q): il file fatto fin qui resta valido."""
        self._fermato = True
        try:
            self._processo.stdin.write("q")
            self._processo.stdin.flush()
        except (OSError, ValueError):
            pass
        try:
            self._processo.wait(timeout=5)
        except _subprocess.TimeoutExpired:
            self._processo.terminate()

    def aspetta(self, tempo=None):
        """Aspetta la fine. Ritorna un Risultato, oppure solleva ErroreFfmpeg se ffmpeg e' fallito."""
        try:
            self._processo.wait(timeout=tempo)
        except _subprocess.TimeoutExpired:
            raise ErroreFfmpeg("ffmpeg non ha ancora finito") from None
        self._t_out.join(2)
        self._t_err.join(2)
        testo = _testo_comando(self._argomenti)
        if self._processo.returncode != 0 and not self._fermato:
            messaggi = list(self._log)
            raise ErroreFfmpeg("ffmpeg non e' riuscito: " + (" | ".join([m for m in messaggi if m][-3:]) or f"codice {self._processo.returncode}"),
                               comando=testo, codice=self._processo.returncode, messaggi=messaggi)
        if self._chiama and not self.avanzamento.terminato:
            self.avanzamento.update(frazione=1.0, terminato=True)
            try:
                self._chiama(self.avanzamento)
            except Exception:
                pass
        return Risultato(uscite=list(self.comando.uscite) if self.comando._grezzo is None else [], durata_elaborazione=_tempo_modulo.time() - self._inizio,
                         comando=testo, messaggi=list(self._log), avanzamento=self.avanzamento, fermato=self._fermato)


# =====================================================================================================
#  Metodi con nome italiano: opzioni, filtri, scorciatoie  (si aggiungono a Comando da tabelle)
# =====================================================================================================
def _opzioni_ingresso(opzioni):
    mappa = {"inizio": "-ss", "fine": "-to", "durata": "-t", "ripeti": "-stream_loop", "formato": "-f", "fps": "-framerate",
             "risoluzione": "-video_size", "ritmo_reale": "-re", "accelerazione": "-hwaccel", "codec_video": "-c:v", "codec_audio": "-c:a",
             "frequenza_audio": "-ar", "canali": "-ac", "formato_pixel": "-pix_fmt", "ritardo": "-itsoffset", "ora_sistema": "-use_wallclock_as_timestamps"}
    out = []
    for k, v in opzioni.items():
        flag = mappa.get(k, k if k.startswith("-") else "-" + k)
        out.append(flag)
        if v is not True and v is not None:
            out.append(_tempo(v) if k in ("inizio", "fine", "durata", "ritardo") else _scrivi_valore(v))
    return out


def apri(file, **opzioni):
    """Comincia un comando con un file in ingresso: ffmpeg.apri('film.mp4', inizio=10, durata=5)."""
    return Comando().aggiungi(file, **opzioni)


def nuovo():
    """Un comando vuoto (per partire da sorgenti o da .aggiungi(...))."""
    return Comando()


# nome -> (opzione di ffmpeg, spiegazione). Il valore passato diventa il parametro; metodo senza valore = opzione senza parametro.
_OPZIONI_USCITA = {
    "codec_video": ("-c:v", "Il codificatore video: 'libx264', 'libx265', 'libvpx-vp9', 'mpeg4', 'copy' (senza ricodificare), ..."),
    "codec_audio": ("-c:a", "Il codificatore audio: 'aac', 'libmp3lame', 'libopus', 'flac', 'pcm_s16le', 'copy', ..."),
    "codec_sottotitoli": ("-c:s", "Il codec dei sottotitoli: 'srt', 'mov_text', 'ass', 'copy', ..."),
    "copia": ("-c", "Copia tutti i flussi senza ricodificarli (veloce, nessuna perdita). Con un valore: il codec per tutti i flussi."),
    "qualita": ("-crf", "Qualita' costante per x264/x265/vp9 (0 = perfetta, 18 = ottima, 23 = normale, 28 = bassa)."),
    "qualita_audio": ("-q:a", "Qualita' audio a scala (per mp3: 0 = migliore, 9 = peggiore)."),
    "bitrate_video": ("-b:v", "Bitrate del video: '2M', '800k', ..."),
    "bitrate_audio": ("-b:a", "Bitrate dell'audio: '192k', '128k', ..."),
    "bitrate_massimo": ("-maxrate", "Bitrate massimo del video (si usa con 'buffer')."),
    "buffer": ("-bufsize", "Dimensione del buffer di controllo del bitrate."),
    "fps": ("-r", "Fotogrammi al secondo dell'uscita."),
    "risoluzione": ("-s", "Dimensioni dell'uscita: '1280x720'. Per ridimensionare bene usa .ridimensiona(...)."),
    "rapporto": ("-aspect", "Rapporto d'aspetto: '16:9', '4:3'."),
    "frequenza_audio": ("-ar", "Campionamento audio in Hz: 44100, 48000."),
    "canali": ("-ac", "Numero di canali audio: 1 (mono), 2 (stereo), 6 (5.1)."),
    "layout_canali": ("-channel_layout", "Layout dei canali: 'mono', 'stereo', '5.1'."),
    "formato_pixel": ("-pix_fmt", "Formato dei pixel: 'yuv420p' (il piu' compatibile), 'rgb24', 'gray', ..."),
    "formato_campione": ("-sample_fmt", "Formato dei campioni audio: 's16', 'fltp', ..."),
    "formato": ("-f", "Il contenitore, se non si capisce dall'estensione: 'mp4', 'matroska', 'wav', 'null', 'image2', ..."),
    "preset": ("-preset", "Velocita' contro dimensione per x264/x265: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow."),
    "profilo": ("-profile:v", "Profilo del codec video: 'baseline', 'main', 'high', ..."),
    "livello": ("-level", "Livello del codec video: '4.0', '4.1', ..."),
    "tune": ("-tune", "Ottimizzazione di x264: 'film', 'animation', 'grain', 'stillimage', 'zerolatency', ..."),
    "durata": ("-t", "Ferma l'uscita dopo questi secondi (o 'HH:MM:SS')."),
    "inizio": ("-ss", "Salta questi secondi dell'ingresso prima di scrivere l'uscita."),
    "fine": ("-to", "Ferma l'uscita a questo istante."),
    "fotogrammi": ("-frames:v", "Scrive solo questo numero di fotogrammi video."),
    "campioni_audio": ("-frames:a", "Scrive solo questo numero di frame audio."),
    "senza_video": ("-vn", "Niente video nell'uscita."),
    "senza_audio": ("-an", "Niente audio nell'uscita."),
    "senza_sottotitoli": ("-sn", "Niente sottotitoli nell'uscita."),
    "senza_dati": ("-dn", "Niente flussi di dati nell'uscita."),
    "il_piu_corto": ("-shortest", "Finisce quando finisce il flusso piu' corto."),
    "ottimizza_web": ("-movflags +faststart", "mp4 pronto per lo streaming (l'indice all'inizio del file)."),
    "thread": ("-threads", "Quanti thread usare (0 = automatico)."),
    "gop": ("-g", "Distanza massima tra fotogrammi chiave (la lunghezza del GOP)."),
    "b_frames": ("-bf", "Numero massimo di fotogrammi B consecutivi."),
    "qscale_video": ("-q:v", "Qualita' video a scala (per jpeg: 2 = ottima, 31 = pessima)."),
    "tag_video": ("-tag:v", "Tag del codec video (es. 'hvc1' per h265 su Apple)."),
    "ripeti": ("-stream_loop", "Ripete l'ingresso (si usa prima dell'ingresso: preferisci apri(..., ripeti=3))."),
    "formato_tempo": ("-fps_mode", "Gestione del tempo dei fotogrammi: 'cfr', 'vfr', 'passthrough', 'drop'."),
    "accelerazione": ("-hwaccel", "Decodifica con la scheda video: 'cuda', 'd3d11va', 'dxva2', 'auto'."),
    "sottotitoli_incisi": ("-c:s", "(vedi sottotitoli())"),
    "metadati_globali": ("-map_metadata", "Da quale ingresso copiare i metadati (-1 = nessuno)."),
    "capitoli": ("-map_chapters", "Da quale ingresso copiare i capitoli (-1 = nessuno)."),
    "limita_dimensione": ("-fs", "Ferma l'uscita a questa dimensione in byte."),
    "passaggio": ("-pass", "Primo o secondo passaggio della codifica a due passaggi (1 o 2)."),
    "file_statistiche": ("-passlogfile", "Prefisso dei file di statistiche per la codifica a due passaggi."),
}
_SENZA_VALORE = {"senza_video", "senza_audio", "senza_sottotitoli", "senza_dati", "il_piu_corto", "ottimizza_web"}


def _crea_opzione(nome, flag, spiegazione):
    if nome in _SENZA_VALORE:
        def metodo(self, attivo=True):
            if attivo:
                self._corrente.opzioni += flag.split()
            return self
    else:
        def metodo(self, valore, flusso=None):
            if nome in ("inizio", "fine", "durata"):
                valore = _tempo(valore)
            base = flag.split()
            nome_flag = base[0] + (":" + str(flusso) if flusso else "")
            self._corrente.opzioni += [nome_flag] + base[1:] + [_scrivi_valore(valore)]
            return self
    metodo.__name__ = nome
    metodo.__doc__ = spiegazione
    return metodo


for _nome, (_flag, _spiegazione) in _OPZIONI_USCITA.items():
    if _nome not in ("copia", "sottotitoli_incisi"):
        setattr(Comando, _nome, _crea_opzione(_nome, _flag, _spiegazione))


def _copia(self, codec=None):
    """Copia i flussi senza ricodificarli (veloce, nessuna perdita)."""
    self._corrente.opzioni += ["-c", codec or "copy"]
    return self


Comando.copia = _copia


# ---- filtri con nome italiano
def _aggiungi_filtro(nome):
    def decoratore(f):
        f.__name__ = nome
        setattr(Comando, nome, f)
        return f
    return decoratore


@_aggiungi_filtro("ridimensiona")
def _ridimensiona(self, larghezza=None, altezza=None, adatta=False, algoritmo=None, pari=True):
    """Cambia le dimensioni. Solo la larghezza (o l'altezza): l'altro lato segue, senza deformare. Con `adatta=True` e tutti e due i valori
    l'immagine sta dentro la cornice senza deformarsi (con bande nere). `algoritmo`: 'bicubic', 'lanczos', 'neighbor', ..."""
    if larghezza is None and altezza is None:
        raise ValueError("Serve almeno la larghezza o l'altezza")
    w = larghezza if larghezza is not None else (-2 if pari else -1)
    h = altezza if altezza is not None else (-2 if pari else -1)
    opz = {"flags": algoritmo}
    if adatta and larghezza and altezza:
        self._filtro_su("v", _filtro("scale", (), {"w": w, "h": h, "force_original_aspect_ratio": "decrease", "flags": algoritmo}))
        return self._filtro_su("v", _filtro("pad", (), {"w": w, "h": h, "x": "(ow-iw)/2", "y": "(oh-ih)/2"}))
    return self._filtro_su("v", _filtro("scale", (w, h), opz))


@_aggiungi_filtro("ritaglia")
def _ritaglia(self, larghezza, altezza, x=None, y=None):
    """Ritaglia un rettangolo. Senza x e y il rettangolo e' al centro."""
    return self._filtro_su("v", _filtro("crop", (larghezza, altezza, x if x is not None else "(in_w-out_w)/2", y if y is not None else "(in_h-out_h)/2")))


@_aggiungi_filtro("ruota")
def _ruota(self, gradi, colore="black"):
    """Ruota il video: 90, 180, 270 in modo esatto; altri angoli (in gradi) con sfondo `colore`."""
    g = gradi % 360
    if g == 90:
        return self._filtro_su("v", "transpose=1")
    if g == 180:
        return self._filtro_su("v", "hflip,vflip")
    if g == 270:
        return self._filtro_su("v", "transpose=2")
    if g == 0:
        return self
    return self._filtro_su("v", _filtro("rotate", (f"{g}*PI/180",), {"fillcolor": colore}))


@_aggiungi_filtro("ribalta_orizzontale")
def _ribalta_orizzontale(self):
    """Specchia il video da sinistra a destra."""
    return self._filtro_su("v", "hflip")


@_aggiungi_filtro("ribalta_verticale")
def _ribalta_verticale(self):
    """Capovolge il video."""
    return self._filtro_su("v", "vflip")


@_aggiungi_filtro("velocita")
def _velocita(self, fattore):
    """Accelera (2 = doppia velocita') o rallenta (0.5 = meta') video e audio insieme."""
    if fattore <= 0:
        raise ValueError("il fattore deve essere maggiore di zero")
    self._filtro_su("v", f"setpts=PTS/{_scrivi_valore(float(fattore))}")
    return self.velocita_audio(fattore)


@_aggiungi_filtro("velocita_audio")
def _velocita_audio(self, fattore):
    """Cambia solo la velocita' dell'audio senza cambiarne il tono (atempo, a catena se serve)."""
    f = float(fattore)
    while f > 2.0:
        self._filtro_su("a", "atempo=2")
        f /= 2.0
    while f < 0.5:
        self._filtro_su("a", "atempo=0.5")
        f /= 0.5
    return self._filtro_su("a", f"atempo={_scrivi_valore(f)}")


@_aggiungi_filtro("inverti")
def _inverti(self):
    """Riproduce video e audio al contrario (tiene tutto in memoria: per filmati brevi)."""
    return self._filtro_su("v", "reverse")._filtro_su("a", "areverse")


@_aggiungi_filtro("sfoca")
def _sfoca(self, intensita=5):
    """Sfocatura gaussiana (intensita' = sigma)."""
    return self._filtro_su("v", _filtro("gblur", (), {"sigma": intensita}))


@_aggiungi_filtro("nitidezza")
def _nitidezza(self, quantita=1.0):
    """Rende piu' nitida l'immagine (0 = niente, 1 = media, 5 = massima)."""
    return self._filtro_su("v", _filtro("unsharp", (), {"luma_msize_x": 5, "luma_msize_y": 5, "luma_amount": quantita}))


@_aggiungi_filtro("colore_immagine")
def _colore_immagine(self, luminosita=None, contrasto=None, saturazione=None, gamma=None):
    """Regola luminosita' (-1..1, 0 = invariata), contrasto (default 1), saturazione (default 1), gamma (default 1)."""
    return self._filtro_su("v", _filtro("eq", (), {"brightness": luminosita, "contrast": contrasto, "saturation": saturazione, "gamma": gamma}))


@_aggiungi_filtro("bianco_e_nero")
def _bianco_e_nero(self):
    """Toglie i colori."""
    return self._filtro_su("v", "hue=s=0")


@_aggiungi_filtro("negativo")
def _negativo(self):
    """Inverte i colori."""
    return self._filtro_su("v", "negate")


@_aggiungi_filtro("seppia")
def _seppia(self):
    """Effetto seppia."""
    return self._filtro_su("v", "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131")


@_aggiungi_filtro("vignetta")
def _vignetta(self, angolo="PI/5"):
    """Scurisce i bordi."""
    return self._filtro_su("v", _filtro("vignette", (angolo,)))


@_aggiungi_filtro("deinterlaccia")
def _deinterlaccia(self):
    """Toglie le righe da interlacciamento (yadif)."""
    return self._filtro_su("v", "yadif")


@_aggiungi_filtro("cambia_fps")
def _cambia_fps(self, fps):
    """Cambia i fotogrammi al secondo duplicando o saltando fotogrammi (a differenza di .fps(), che e' un'opzione dell'uscita)."""
    return self._filtro_su("v", _filtro("fps", (fps,)))


@_aggiungi_filtro("cornice")
def _cornice(self, larghezza, altezza, x=None, y=None, colore="black"):
    """Mette il video al centro di una cornice piu' grande (bande)."""
    return self._filtro_su("v", _filtro("pad", (larghezza, altezza, x if x is not None else "(ow-iw)/2", y if y is not None else "(oh-ih)/2", colore)))


@_aggiungi_filtro("testo")
def _testo(self, scritta, x="(w-text_w)/2", y="(h-text_h)/2", dimensione=24, colore="white", sfondo=None, bordo=None, font=None,
           da_secondi=None, a_secondi=None, opacita=None):
    """Scrive un testo sul video. x e y sono espressioni (centro di default). `font` e' un file .ttf. Compare solo tra `da_secondi` e `a_secondi`."""
    scritta = str(scritta).replace("'", "’")          # un apice dritto manda in crash drawtext di ffmpeg: si usa quello tipografico
    scritta = str(scritta).replace("'", "’")      # un apice dritto manda in crash drawtext di ffmpeg: si usa quello tipografico
    opz = {"text": scritta, "x": x, "y": y, "fontsize": dimensione, "fontcolor": colore if opacita is None else f"{colore}@{opacita}"}
    if sfondo:
        opz.update(box=1, boxcolor=sfondo, boxborderw=8)
    if bordo:
        opz.update(borderw=bordo, bordercolor="black")
    if font:
        opz["fontfile"] = _os.path.abspath(font).replace("\\", "/")
    elif _os.name == "nt":
        for candidato in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"):
            if _os.path.exists(candidato):
                opz["fontfile"] = candidato
                break
    if da_secondi is not None or a_secondi is not None:
        inizio, fine = da_secondi if da_secondi is not None else 0, a_secondi if a_secondi is not None else 1e9
        opz["enable"] = f"between(t,{inizio},{fine})"
    return self._filtro_su("v", _filtro("drawtext", (), opz))


@_aggiungi_filtro("sottotitoli")
def _sottotitoli(self, file, stile=None):
    """Incide nel video i sottotitoli di un file .srt o .ass. `stile`: ad esempio 'FontSize=24,PrimaryColour=&H00FFFF&'."""
    testo = "subtitles=" + _percorso_filtro(file)
    if stile:
        testo += ":force_style=" + _fuga(stile)
    return self._filtro_su("v", testo)


@_aggiungi_filtro("sovrapponi")
def _sovrapponi(self, immagine, x=10, y=10, opzioni_ingresso=None):
    """Mette un'immagine (logo, filigrana) o un altro video sopra il video. x e y: pixel o espressioni come 'W-w-10' (angolo in basso a destra)."""
    self.aggiungi(immagine, **(opzioni_ingresso or {}))
    self._corrente.passi.append(("sovrapponi", len(self._ingressi) - 1, x, y, ""))
    return self


@_aggiungi_filtro("dissolvenza_ingresso")
def _dissolvenza_ingresso(self, durata=1.0, inizio=0, audio=True, colore="black"):
    """Entra dal nero (e l'audio dal silenzio) in `durata` secondi."""
    self._filtro_su("v", _filtro("fade", (), {"t": "in", "st": inizio, "d": durata, "color": colore}))
    return self._filtro_su("a", _filtro("afade", (), {"t": "in", "st": inizio, "d": durata})) if audio else self


@_aggiungi_filtro("dissolvenza_uscita")
def _dissolvenza_uscita(self, durata=1.0, a_partire_da=None, audio=True, colore="black"):
    """Esce verso il nero. `a_partire_da` (secondi): se manca si calcola dalla durata del filmato in uscita."""
    if a_partire_da is None:
        totale = self.durata_prevista
        if totale is None:
            raise ValueError("Non conosco la durata: indica a_partire_da=")
        a_partire_da = max(0.0, totale - durata)
    self._filtro_su("v", _filtro("fade", (), {"t": "out", "st": a_partire_da, "d": durata, "color": colore}))
    return self._filtro_su("a", _filtro("afade", (), {"t": "out", "st": a_partire_da, "d": durata})) if audio else self


@_aggiungi_filtro("volume")
def _volume(self, fattore):
    """Alza o abbassa il volume: 0.5 = meta', 2 = doppio, '6dB', '-3dB'."""
    return self._filtro_su("a", _filtro("volume", (fattore,)))


@_aggiungi_filtro("normalizza_volume")
def _normalizza_volume(self, obiettivo=-16.0, picco=-1.5, intervallo=11.0):
    """Porta il volume a un livello costante (loudnorm, EBU R128): obiettivo in LUFS."""
    return self._filtro_su("a", _filtro("loudnorm", (), {"I": obiettivo, "TP": picco, "LRA": intervallo}))


@_aggiungi_filtro("passa_basso")
def _passa_basso(self, frequenza):
    """Lascia passare solo i suoni piu' gravi della frequenza (Hz)."""
    return self._filtro_su("a", _filtro("lowpass", (), {"f": frequenza}))


@_aggiungi_filtro("passa_alto")
def _passa_alto(self, frequenza):
    """Lascia passare solo i suoni piu' acuti della frequenza (Hz)."""
    return self._filtro_su("a", _filtro("highpass", (), {"f": frequenza}))


@_aggiungi_filtro("equalizzatore")
def _equalizzatore(self, frequenza, guadagno, larghezza=100):
    """Alza o abbassa (dB) una banda di frequenze."""
    return self._filtro_su("a", _filtro("equalizer", (), {"f": frequenza, "width_type": "h", "w": larghezza, "g": guadagno}))


@_aggiungi_filtro("eco")
def _eco(self, ritardo_ms=500, decadimento=0.4):
    """Aggiunge un'eco."""
    return self._filtro_su("a", _filtro("aecho", (0.8, 0.9, ritardo_ms, decadimento)))


@_aggiungi_filtro("ritardo_audio")
def _ritardo_audio(self, millisecondi):
    """Ritarda l'audio (utile per risincronizzare)."""
    return self._filtro_su("a", _filtro("adelay", (f"{int(millisecondi)}|{int(millisecondi)}",)))


@_aggiungi_filtro("riduci_rumore")
def _riduci_rumore(self, decibel=12):
    """Toglie il fruscio di fondo (afftdn)."""
    return self._filtro_su("a", _filtro("afftdn", (), {"nr": decibel}))


@_aggiungi_filtro("inverti_audio")
def _inverti_audio(self):
    """Riproduce l'audio al contrario."""
    return self._filtro_su("a", "areverse")


@_aggiungi_filtro("togli_silenzi")
def _togli_silenzi(self, soglia_db=-50, durata_minima=0.5):
    """Toglie le pause di silenzio piu' lunghe di `durata_minima` secondi."""
    return self._filtro_su("a", _filtro("silenceremove", (), {"stop_periods": -1, "stop_duration": durata_minima, "stop_threshold": f"{soglia_db}dB"}))


# ---- uscite con nome
@_aggiungi_filtro("miniature_ogni")
def _miniature_ogni(self, secondi, larghezza=None):
    """Un fotogramma ogni `secondi` secondi (per salvare una sequenza di immagini: .salva('img_%03d.png'))."""
    self._filtro_su("v", _filtro("fps", (f"1/{secondi}",)))
    return self.ridimensiona(larghezza=larghezza) if larghezza else self


# =====================================================================================================
#  Sorgenti pronte (ingressi virtuali)
# =====================================================================================================
def tono(frequenza=440, durata=1.0, frequenza_audio=44100):
    """Un comando che parte da un tono puro: ffmpeg.tono(440, 2).salva('la.wav')."""
    return Comando().sorgente(_filtro("sine", (), {"frequency": frequenza, "duration": durata, "sample_rate": frequenza_audio}))


def silenzio(durata=1.0, frequenza_audio=44100, layout="stereo"):
    """Un comando che parte dal silenzio."""
    return Comando().sorgente(_filtro("anullsrc", (), {"r": frequenza_audio, "cl": layout}), durata=durata)


def colore(colore="black", dimensioni="1280x720", durata=5.0, fps=25):
    """Un comando che parte da un fondo tinta unita."""
    return Comando().sorgente(_filtro("color", (), {"c": colore, "s": dimensioni, "d": durata, "r": fps}))


def schema_di_prova(dimensioni="640x360", durata=5.0, fps=25):
    """Un comando che parte dallo schema di prova di ffmpeg (testsrc): comodo per provare."""
    return Comando().sorgente(_filtro("testsrc", (), {"size": dimensioni, "duration": durata, "rate": fps}))


# =====================================================================================================
#  Ricette: le cose che si fanno piu' spesso, gia' fatte
# =====================================================================================================
def _nuovo_file(percorso):
    _os.makedirs(_os.path.dirname(_os.path.abspath(percorso)), exist_ok=True)
    return _os.path.abspath(percorso)


def converti(origine, destinazione, avanzamento=None, **opzioni):
    """Converte un file nel formato dell'estensione di `destinazione`. Opzioni in piu' = quelle di uscita (codec_video='libx264', qualita=23, ...)."""
    return apri(origine).salva(_nuovo_file(destinazione), avanzamento=avanzamento, **opzioni)


def estrai_audio(video, destinazione, avanzamento=None, **opzioni):
    """Salva solo l'audio ('film.mp4' -> 'colonna.mp3')."""
    return apri(video).senza_video().salva(_nuovo_file(destinazione), avanzamento=avanzamento, **opzioni)


def taglia(origine, destinazione, inizio=0, fine=None, durata=None, ricodifica=True, avanzamento=None):
    """Salva il pezzo tra `inizio` e `fine` (o lungo `durata`), in secondi. Con ricodifica=False e' istantaneo ma preciso solo ai fotogrammi chiave."""
    opzioni = {"inizio": inizio}
    if durata is not None:
        opzioni["durata"] = durata
    elif fine is not None:
        opzioni["durata"] = _secondi(fine) - _secondi(inizio)
    c = apri(origine, **opzioni)
    if not ricodifica:
        c.copia()
    return c.salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def fotogramma(video, tempo, destinazione, larghezza=None):
    """Salva come immagine il fotogramma al secondo `tempo`."""
    c = apri(video, inizio=tempo).fotogrammi(1)
    if larghezza:
        c.ridimensiona(larghezza=larghezza)
    return c.salva(_nuovo_file(destinazione))


def estrai_fotogrammi(video, cartella, ogni_secondi=1.0, formato="png", larghezza=None, avanzamento=None):
    """Salva un'immagine ogni `ogni_secondi` secondi in `cartella` (immagine_0001.png, ...). Ritorna la lista dei file."""
    _os.makedirs(cartella, exist_ok=True)
    c = apri(video).miniature_ogni(ogni_secondi, larghezza)
    c.salva(_os.path.join(cartella, f"immagine_%04d.{formato}"), avanzamento=avanzamento)
    return sorted(_os.path.join(cartella, f) for f in _os.listdir(cartella) if f.startswith("immagine_") and f.endswith("." + formato))


def riduci(video, destinazione, larghezza=640, qualita=26, avanzamento=None):
    """Video piu' piccolo (larghezza in pixel, qualita' x264: piu' alto = piu' leggero)."""
    return apri(video).ridimensiona(larghezza=larghezza).codec_video("libx264").qualita(qualita).formato_pixel("yuv420p") \
        .ottimizza_web().salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def gif(video, destinazione, inizio=0, durata=None, larghezza=480, fps=12, avanzamento=None):
    """Una GIF animata di buona qualita' (con tavolozza di colori ottimizzata)."""
    c = apri(video, inizio=inizio, **({"durata": durata} if durata else {}))
    c.filtro_complesso(f"[0:v]fps={fps},scale={larghezza}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse[g]", mappa="[g]")
    return c.salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def concatena(file, destinazione, ricodifica=False, avanzamento=None):
    """Unisce piu' file uno dopo l'altro. Senza ricodifica i file devono avere gli stessi codec e parametri; con ricodifica=True vanno bene tutti."""
    file = [_os.path.abspath(str(f)) for f in file]
    if len(file) < 2:
        raise ValueError("Servono almeno due file")
    if not ricodifica:
        with _tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as elenco:
            for f in file:
                elenco.write("file '" + f.replace("\\", "/").replace("'", "'\\''") + "'\n")
        try:
            return Comando().aggiungi(elenco.name, formato="concat", safe="0").copia().salva(_nuovo_file(destinazione), avanzamento=avanzamento)
        finally:
            _os.remove(elenco.name)
    c = Comando()
    for f in file:
        c.aggiungi(f)
    n = len(file)
    c.filtro_complesso("".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]", mappa=["[v]", "[a]"])
    return c.salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def sostituisci_audio(video, audio, destinazione, avanzamento=None):
    """Il video con un altro audio (il video non si ricodifica)."""
    return Comando().aggiungi(video).aggiungi(audio).mappa("0:v:0").mappa("1:a:0").copia().il_piu_corto() \
        .salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def togli_audio(video, destinazione, avanzamento=None):
    """Il video senza audio (senza ricodificarlo)."""
    return apri(video).senza_audio().copia().salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def filigrana(video, immagine, destinazione, x="W-w-10", y="H-h-10", avanzamento=None):
    """Mette un logo sopra il video (di default in basso a destra)."""
    return apri(video).sovrapponi(immagine, x, y).salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def dividi_in_segmenti(file, durata_segmento, modello, avanzamento=None):
    """Taglia un file in pezzi lunghi `durata_segmento` secondi senza ricodificare: modello='parte_%03d.mp4'."""
    return apri(file).copia().formato("segment").opzione("-segment_time", durata_segmento).opzione("-reset_timestamps", 1) \
        .salva(_nuovo_file(modello), avanzamento=avanzamento)


def onda_audio(file, destinazione, dimensioni="1200x300", colore="#2a7de1"):
    """Un'immagine con la forma d'onda dell'audio."""
    c = apri(file)
    c.filtro_complesso(f"[0:a]aformat=channel_layouts=mono,showwavespic=s={dimensioni}:colors={_fuga(colore)}[w]", mappa="[w]").fotogrammi(1)
    return c.salva(_nuovo_file(destinazione))


def spettrogramma(file, destinazione, dimensioni="1200x500"):
    """Un'immagine con lo spettro dell'audio."""
    c = apri(file)
    c.filtro_complesso(f"[0:a]showspectrumpic=s={dimensioni}[s]", mappa="[s]").fotogrammi(1)
    return c.salva(_nuovo_file(destinazione))


def foglio_di_miniature(video, destinazione, colonne=4, righe=4, larghezza=320):
    """Un'unica immagine con tante miniature del video (colonne x righe), a intervalli uguali."""
    totale = Sonda(video).durata
    passo = max(totale / (colonne * righe), 0.04)
    c = apri(video).filtro("fps", f"1/{passo:.4f}").filtro("scale", larghezza, -1).filtro("tile", f"{colonne}x{righe}").fotogrammi(1)
    return c.salva(_nuovo_file(destinazione))


def normalizza_volume(file, destinazione, obiettivo=-16.0, avanzamento=None):
    """Volume costante con la normalizzazione EBU R128 (loudnorm); il video non si ricodifica."""
    return apri(file).normalizza_volume(obiettivo).codec_video("copy").salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def rileva_silenzi(file, soglia_db=-40, durata_minima=0.5):
    """Trova le pause di silenzio: ritorna una lista di (inizio, fine) in secondi."""
    c = apri(file).livello_log("info").filtro_audio("silencedetect", noise=f"{soglia_db}dB", d=durata_minima).formato("null")
    risultato = c.salva("-")
    testo = "\n".join(risultato.messaggi)
    inizi = [float(x) for x in _re.findall(r"silence_start: (-?[\d.]+)", testo)]
    fini = [float(x) for x in _re.findall(r"silence_end: (-?[\d.]+)", testo)]
    return list(zip(inizi, fini))


def volume_massimo(file):
    """Il volume medio e di picco di un file, in dB: ritorna {'medio': ..., 'picco': ...}."""
    c = apri(file).livello_log("info").filtro_audio("volumedetect").formato("null")
    testo = "\n".join(c.salva("-").messaggi)
    medio = _re.search(r"mean_volume: (-?[\d.]+) dB", testo)
    picco = _re.search(r"max_volume: (-?[\d.]+) dB", testo)
    return {"medio": float(medio.group(1)) if medio else None, "picco": float(picco.group(1)) if picco else None}


def immagini_in_video(modello, destinazione, fps=25, audio=None, avanzamento=None):
    """Una sequenza di immagini (modello='img_%04d.png') diventa un video."""
    c = apri(modello, fps=fps)
    if audio:
        c.aggiungi(audio).il_piu_corto()
    return c.codec_video("libx264").formato_pixel("yuv420p").salva(_nuovo_file(destinazione), avanzamento=avanzamento)


def cattura_schermo(destinazione, durata=5, fps=20, avanzamento=None):
    """Registra lo schermo di Windows (gdigrab) per `durata` secondi."""
    if _os.name != "nt":
        raise ErroreFfmpeg("La cattura dello schermo con questo metodo e' solo per Windows.")
    return Comando().aggiungi("desktop", formato="gdigrab", fps=fps, durata=durata).codec_video("libx264").preset("ultrafast") \
        .formato_pixel("yuv420p").salva(_nuovo_file(destinazione), avanzamento=avanzamento)
