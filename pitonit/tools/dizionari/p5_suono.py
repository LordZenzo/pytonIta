"""Suoni: riprodurre file .wav, fare dei beep, creare toni e piccole melodie.
Su Windows usa winsound (incluso in pitonit); altrove prova i lettori del sistema (afplay, paplay, aplay).
Il modulo originale e' wave (lettura e scrittura dei file .wav): resta sempre disponibile."""

MODULI = {
    "suono": dict(orig="wave", propria=True, doc="Suoni: riprodurre file .wav, fare dei beep, creare toni e piccole melodie", extra='''
apri_onda = _orig.open
ErroreOnda = _orig.Error
import math as _matematica
import os as _os
import struct as _struct
import subprocess as _subprocess
import sys as _sistema
import tempfile as _tempfile
try:
    import winsound as _ws
except ImportError:                       # non Windows
    _ws = None


class ErroreSuono(Exception):
    """Il suono non si puo' riprodurre (file mancante, nessun lettore audio, ...)."""


_processo = None


def _percorso(file):
    p = _os.path.abspath(_os.fspath(file))
    if not _os.path.isfile(p):
        raise FileNotFoundError(f"File audio non trovato: {file}")
    return p


def _come_wav(p):
    """I file che non sono .wav (mp3, ogg, m4a, ...) si convertono al volo con ffmpeg (modulo multimedia)."""
    if p.lower().endswith(".wav"):
        return p
    try:
        import multimedia
    except ImportError:
        raise ErroreSuono("Solo i file .wav si possono suonare senza ffmpeg") from None
    try:
        return multimedia.a_wav(p)
    except multimedia.ErroreMultimedia as errore:
        raise ErroreSuono(str(errore)) from None


def _lettore():
    """Comando del sistema per riprodurre un file (solo fuori da Windows)."""
    import shutil
    for nome in ("afplay", "paplay", "aplay"):
        if shutil.which(nome):
            return [nome]
    raise ErroreSuono("Nessun lettore audio trovato (serve afplay, paplay o aplay)")


def riproduci(file, attendi=True):
    """Suona un file .wav. Con attendi=True il programma aspetta la fine; con attendi=False parte e continua."""
    global _processo
    p = _come_wav(_percorso(file))
    if _ws:
        flag = _ws.SND_FILENAME | _ws.SND_NODEFAULT
        _ws.PlaySound(p, flag if attendi else flag | _ws.SND_ASYNC)
        return
    ferma()
    _processo = _subprocess.Popen(_lettore() + [p], stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL)     # i lettori di sistema scrivono messaggi: non servono
    if attendi:
        if _processo.wait() != 0:
            raise ErroreSuono("Il lettore audio del sistema non e' riuscito a suonare il file (manca la scheda audio, o il servizio audio non e' attivo?)")


def ripeti(file):
    """Suona un file .wav in ciclo, in sottofondo, finche' non si chiama ferma(). Solo Windows."""
    if not _ws:
        raise ErroreSuono("ripeti() funziona solo su Windows")
    _ws.PlaySound(_come_wav(_percorso(file)), _ws.SND_FILENAME | _ws.SND_NODEFAULT | _ws.SND_ASYNC | _ws.SND_LOOP)


def ferma():
    """Interrompe il suono in corso."""
    global _processo
    if _ws:
        _ws.PlaySound(None, _ws.SND_PURGE)
    elif _processo is not None:
        if _processo.poll() is None:
            _processo.terminate()
        _processo = None


_AVVISI = {"informazione": "MB_ICONASTERISK", "attenzione": "MB_ICONEXCLAMATION",
           "errore": "MB_ICONHAND", "domanda": "MB_ICONQUESTION", "standard": "MB_OK"}


def avviso(tipo="informazione"):
    """Il suono di sistema: informazione, attenzione, errore, domanda o standard. Solo Windows."""
    if tipo not in _AVVISI:
        raise ValueError("tipo sconosciuto: scegli tra " + ", ".join(_AVVISI))
    if _ws:
        _ws.MessageBeep(getattr(_ws, _AVVISI[tipo]))
    else:
        print("\\a", end="", flush=True)


def _scrivi_onda(file, campioni, campionamento):
    with _orig.open(_os.fspath(file), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(campionamento)
        f.writeframes(b"".join(_struct.pack("<h", c) for c in campioni))
    return _os.path.abspath(_os.fspath(file))


def _tono(frequenza, durata, volume, campionamento):
    """Campioni di un'onda sinusoidale (frequenza 0 = silenzio), con una breve dissolvenza per evitare i 'click'."""
    n = int(durata * campionamento)
    if frequenza <= 0:
        return [0] * n
    sfumatura = max(1, min(n // 2, int(0.005 * campionamento)))
    ampiezza = int(32767 * max(0.0, min(1.0, volume)))
    out = []
    for i in range(n):
        v = ampiezza * _matematica.sin(2 * _matematica.pi * frequenza * i / campionamento)
        if i < sfumatura:
            v *= i / sfumatura
        elif i >= n - sfumatura:
            v *= (n - i) / sfumatura
        out.append(int(v))
    return out


def crea_tono(file, frequenza=440, durata=1.0, volume=0.5, campionamento=44100):
    """Scrive un file .wav con una nota pura (frequenza in hertz, durata in secondi). Restituisce il percorso."""
    return _scrivi_onda(file, _tono(frequenza, durata, volume, campionamento), campionamento)


_SEMITONI = {"do": 0, "re": 2, "mi": 4, "fa": 5, "sol": 7, "la": 9, "si": 11}


def frequenza_nota(nome):
    """Frequenza in hertz di una nota: 'la4' = 440, 'do4' = do centrale, 'fa#3', 'sib4'. 'pausa' vale 0."""
    testo = nome.strip().lower()
    if testo in ("pausa", "p", "-"):
        return 0.0
    for base in ("sol", "do", "re", "mi", "fa", "la", "si"):
        if testo.startswith(base):
            resto = testo[len(base):]
            break
    else:
        raise ValueError(f"nota sconosciuta: {nome!r} (esempi: do4, fa#3, sib4, pausa)")
    alterazione = 0
    while resto[:1] in ("#", "b"):
        alterazione += 1 if resto[0] == "#" else -1
        resto = resto[1:]
    try:
        ottava = int(resto) if resto else 4
    except ValueError:
        raise ValueError(f"nota sconosciuta: {nome!r} (esempi: do4, fa#3, sib4, pausa)") from None
    midi = 12 * (ottava + 1) + _SEMITONI[base] + alterazione
    return 440.0 * 2 ** ((midi - 69) / 12)


def _melodia(note, tempo, volume, campionamento):
    campioni = []
    for voce in note:
        nome, battute = (voce, 1) if isinstance(voce, str) else voce
        campioni += _tono(frequenza_nota(nome), battute * 60.0 / tempo, volume, campionamento)
    return campioni


def crea_melodia(file, note, tempo=120, volume=0.5, campionamento=44100):
    """Scrive un .wav con una sequenza di note: [('do4', 1), ('mi4', 1), ('sol4', 2)].
    Ogni voce e' (nota, battute); una battuta e' un quarto. Il tempo e' in battute al minuto. 'pausa' e' il silenzio."""
    return _scrivi_onda(file, _melodia(note, tempo, volume, campionamento), campionamento)


def beep(frequenza=800, durata=0.3):
    """Un suono semplice: frequenza in hertz (37-32767), durata in secondi."""
    if _ws:
        _ws.Beep(int(max(37, min(32767, frequenza))), max(1, int(durata * 1000)))
        return
    with _tempfile.TemporaryDirectory() as cartella:
        riproduci(crea_tono(_os.path.join(cartella, "beep.wav"), frequenza, durata), attendi=True)


def suona(note, tempo=120, volume=0.5):
    """Suona subito una sequenza di note (come crea_melodia) e aspetta la fine."""
    with _tempfile.TemporaryDirectory() as cartella:
        riproduci(crea_melodia(_os.path.join(cartella, "melodia.wav"), note, tempo, volume), attendi=True)


def durata_di(file):
    """Durata in secondi di un file audio (i .wav si leggono da soli; per gli altri formati serve ffmpeg)."""
    p = _percorso(file)
    if not p.lower().endswith(".wav"):
        import multimedia
        return multimedia.durata_di(p)
    with _orig.open(p, "rb") as f:
        return f.getnframes() / float(f.getframerate())
'''),
}
