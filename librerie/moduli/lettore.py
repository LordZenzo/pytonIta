"""Lettore audio e video per pytonIta: avvolge un lettore esterno (oggi VLC, poi mpv) senza includerlo.

    importa lettore

    p = lettore.Lettore()                  # sceglie da solo il motore disponibile (o quello preferito)
    p.apri("film.mp4")                     # parte da solo
    p.pausa();  p.riprendi()
    p.posizione = 120                      # vai al secondo 120
    p.volume = 60                          # da 0 a 100
    p.attendi_fine()

Gli stessi comandi valgono per tutti i motori: cambia solo `Lettore(motore="vlc")` o `Lettore(motore="mpv")`.
In una finestra tkinter: `lettore.PannelloLettore(radice)` e' un riquadro completo, con video e controlli.
Il motore va installato a parte (`lettore.motori()` dice quali ci sono e come procurarsi gli altri).
"""
import ctypes as _ctypes
import json as _json
import os as _os
import subprocess as _subprocess
import sys as _sistema
import threading as _thread
import time as _tempo

try:
    import tkinter as _tk
    from tkinter import ttk as _ttk
except ImportError:                  # senza tkinter (alcune installazioni Linux) il pannello non c'e'
    _tk = None
    _ttk = None


class ErroreLettore(Exception):
    """Il lettore non ha potuto fare quello che chiedevi."""


class MotoreNonTrovato(ErroreLettore):
    """Nessun motore (VLC, mpv) e' installato, oppure quello scelto non c'e'."""


class MotoreNonSupportato(ErroreLettore):
    """Il motore scelto non sa fare questa cosa."""


class Voce(dict):
    """Un dizionario a cui si accede anche come proprieta': voce.nome, voce.id, ..."""

    def __getattr__(self, nome):
        try:
            return self[nome]
        except KeyError:
            raise AttributeError(nome) from None


STATI = ("fermo", "caricamento", "in_riproduzione", "in_pausa", "finito", "errore")
CONFIGURAZIONE = _os.path.join(_os.path.expanduser("~"), ".rad", "lettore.json")


# =====================================================================================================
#  Il contratto dei motori: tutto cio' che un motore deve saper fare (i nomi sono uguali per tutti)
# =====================================================================================================
class Motore:
    """Base dei motori. Un motore nuovo (mpv, ...) implementa questi metodi e si registra in _MOTORI."""
    nome = ""
    descrizione = ""
    installazione = ""
    sito = ""

    @classmethod
    def trova(cls):
        """Dove si trova il motore sul computer (cartella o file), oppure None."""
        return None

    def __init__(self, finestra, opzioni):
        raise NotImplementedError

    # riproduzione
    def apri(self, sorgente): raise NotImplementedError
    def riproduci(self): raise NotImplementedError
    def pausa(self, attiva=True): raise NotImplementedError
    def ferma(self): raise NotImplementedError
    def stato(self): raise NotImplementedError
    # tempo e suono
    def posizione(self): raise NotImplementedError
    def imposta_posizione(self, secondi): raise NotImplementedError
    def durata(self): raise NotImplementedError
    def volume(self): raise NotImplementedError
    def imposta_volume(self, valore): raise NotImplementedError
    def muto(self): raise NotImplementedError
    def imposta_muto(self, attivo): raise NotImplementedError
    def velocita(self): raise NotImplementedError
    def imposta_velocita(self, fattore): raise NotImplementedError
    # video
    def dimensioni(self): raise NotImplementedError
    def istantanea(self, file): raise NotImplementedError
    def fotogramma_avanti(self): raise NotImplementedError
    # tracce
    def tracce_audio(self): raise NotImplementedError
    def imposta_traccia_audio(self, id_): raise NotImplementedError
    def tracce_sottotitoli(self): raise NotImplementedError
    def imposta_sottotitoli(self, id_): raise NotImplementedError
    def carica_sottotitoli(self, file): raise NotImplementedError
    def passa_clic(self):
        """Fa arrivare i clic sul video alla finestra che lo contiene (i motori che disegnano in una finestra propria ne hanno bisogno)."""
        return None

    def chiudi(self): raise NotImplementedError


# =====================================================================================================
#  Motore VLC (libvlc, caricata con ctypes: nessuna dipendenza da installare)
# =====================================================================================================
class _Descrizione(_ctypes.Structure):
    pass


_Descrizione._fields_ = [("i_id", _ctypes.c_int), ("psz_name", _ctypes.c_char_p), ("p_next", _ctypes.POINTER(_Descrizione))]
_ID_STATO_VLC = {0: "fermo", 1: "caricamento", 2: "caricamento", 3: "in_riproduzione", 4: "in_pausa", 5: "fermo", 6: "finito", 7: "errore"}
_librerie_vlc = {}


def _cartella_vlc():
    """La cartella di VLC (con libvlc.dll e plugins), oppure None."""
    scelta = _os.environ.get("PITONIT_VLC", "")
    candidati = [scelta] if scelta else []
    if _os.name == "nt":
        for base in (_os.environ.get("ProgramFiles", r"C:\Program Files"), _os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                     _os.path.join(_os.environ.get("LOCALAPPDATA", ""), "Programs")):
            candidati.append(_os.path.join(base, "VideoLAN", "VLC"))
        import shutil
        nel_path = shutil.which("vlc")
        if nel_path:
            candidati.append(_os.path.dirname(nel_path))
        for c in candidati:
            if c and _os.path.isfile(_os.path.join(c, "libvlc.dll")):
                return c
        return None
    if _sistema.platform == "darwin":
        c = "/Applications/VLC.app/Contents/MacOS/lib"
        return c if _os.path.isfile(_os.path.join(c, "libvlc.dylib")) else None
    import ctypes.util
    return ctypes.util.find_library("vlc") or None


def _istruzioni(windows, mac, comando_apt, comando_dnf, comando_pacman, nome):
    """Come installare un programma su questo computer: il comando giusto per Windows, macOS o la distribuzione Linux in uso."""
    if _os.name == "nt":
        return windows
    if _sistema.platform == "darwin":
        return mac
    import shutil
    for programma, comando in (("apt-get", comando_apt), ("dnf", comando_dnf), ("pacman", comando_pacman)):
        if shutil.which(programma):
            return comando
    return f"installa il pacchetto {nome} con il gestore di pacchetti della tua distribuzione"


def _come_installare(programma):
    """I comandi per installare un motore (vlc, mpv) con il gestore di pacchetti del computer, separati da « | »."""
    try:
        import multimedia
        return " | ".join(v["comando"] for v in multimedia.comandi_installazione(programma))
    except Exception:
        return f"installa il pacchetto {programma} con il gestore di pacchetti della tua distribuzione"


def _come_installare_vlc():
    if _os.name == "nt":
        return "winget install VideoLAN.VLC  (oppure lettore.installa_motore('vlc'))"
    return _come_installare("vlc")


def _carica_vlc():
    cartella = _cartella_vlc()
    if not cartella:
        raise MotoreNonTrovato("VLC non e' installato. Installalo (" + _come_installare_vlc() + ") "
                               "oppure indica la sua cartella nella variabile PITONIT_VLC.")
    if cartella in _librerie_vlc:
        return _librerie_vlc[cartella]
    if _os.name == "nt":
        _os.add_dll_directory(cartella)
        _os.environ.setdefault("VLC_PLUGIN_PATH", _os.path.join(cartella, "plugins"))
        lib = _ctypes.CDLL(_os.path.join(cartella, "libvlc.dll"))
    elif _sistema.platform == "darwin":
        _os.environ.setdefault("VLC_PLUGIN_PATH", _os.path.join(_os.path.dirname(cartella), "plugins"))
        lib = _ctypes.CDLL(_os.path.join(cartella, "libvlc.dylib"))
    else:
        lib = _ctypes.CDLL(cartella)
    p, i, i64, f, s = _ctypes.c_void_p, _ctypes.c_int, _ctypes.c_int64, _ctypes.c_float, _ctypes.c_char_p

    def dichiara(nome, restype, *argtypes):
        funzione = getattr(lib, nome)
        funzione.restype = restype
        funzione.argtypes = list(argtypes)
    dichiara("libvlc_new", p, i, _ctypes.POINTER(s))
    dichiara("libvlc_release", None, p)
    dichiara("libvlc_get_version", s)
    dichiara("libvlc_media_new_path", p, p, s)
    dichiara("libvlc_media_new_location", p, p, s)
    dichiara("libvlc_media_release", None, p)
    dichiara("libvlc_media_player_new", p, p)
    dichiara("libvlc_media_player_release", None, p)
    dichiara("libvlc_media_player_set_media", None, p, p)
    dichiara("libvlc_media_player_play", i, p)
    dichiara("libvlc_media_player_set_pause", None, p, i)
    dichiara("libvlc_media_player_stop", None, p)
    dichiara("libvlc_media_player_get_state", i, p)
    dichiara("libvlc_media_player_get_time", i64, p)
    dichiara("libvlc_media_player_set_time", None, p, i64)
    dichiara("libvlc_media_player_get_length", i64, p)
    dichiara("libvlc_media_player_get_rate", f, p)
    dichiara("libvlc_media_player_set_rate", i, p, f)
    dichiara("libvlc_media_player_next_frame", None, p)
    dichiara("libvlc_audio_get_volume", i, p)
    dichiara("libvlc_audio_set_volume", i, p, i)
    dichiara("libvlc_audio_get_mute", i, p)
    dichiara("libvlc_audio_set_mute", None, p, i)
    dichiara("libvlc_video_take_snapshot", i, p, _ctypes.c_uint, s, _ctypes.c_uint, _ctypes.c_uint)
    dichiara("libvlc_video_get_size", i, p, _ctypes.c_uint, _ctypes.POINTER(_ctypes.c_uint), _ctypes.POINTER(_ctypes.c_uint))
    dichiara("libvlc_audio_get_track_description", _ctypes.POINTER(_Descrizione), p)
    dichiara("libvlc_audio_get_track", i, p)
    dichiara("libvlc_audio_set_track", i, p, i)
    dichiara("libvlc_video_get_spu_description", _ctypes.POINTER(_Descrizione), p)
    dichiara("libvlc_video_get_spu", i, p)
    dichiara("libvlc_video_set_spu", i, p, i)
    dichiara("libvlc_video_set_subtitle_file", i, p, s)
    dichiara("libvlc_track_description_list_release", None, _ctypes.POINTER(_Descrizione))
    dichiara("libvlc_video_set_mouse_input", None, p, _ctypes.c_uint)
    dichiara("libvlc_video_set_key_input", None, p, _ctypes.c_uint)
    if _os.name == "nt":
        dichiara("libvlc_media_player_set_hwnd", None, p, p)
    elif _sistema.platform != "darwin":
        dichiara("libvlc_media_player_set_xwindow", None, p, _ctypes.c_uint32)
    _librerie_vlc[cartella] = lib
    return lib


class MotoreVlc(Motore):
    nome = "vlc"
    descrizione = "VLC (libvlc): legge quasi ogni formato, con sottotitoli, tracce multiple e flussi di rete."
    sito = "https://www.videolan.org/vlc/"
    winget = "VideoLAN.VLC"

    @classmethod
    def _installazione(cls):
        return f"{_come_installare_vlc()}  |  {cls.sito}"

    @classmethod
    def trova(cls):
        return _cartella_vlc()

    def __init__(self, finestra, opzioni):
        self._lib = _carica_vlc()
        argomenti = [b"--quiet", b"--no-video-title-show", b"--no-snapshot-preview", b"--no-stats"] + [o.encode("utf-8") for o in (opzioni or [])]
        vettore = (_ctypes.c_char_p * len(argomenti))(*argomenti)
        self._vettore = vettore
        self._istanza = self._lib.libvlc_new(len(argomenti), vettore)
        if not self._istanza:
            raise ErroreLettore("VLC non si e' avviato (libvlc_new ha fallito).")
        self._lettore = self._lib.libvlc_media_player_new(self._istanza)
        self._media = None
        self._chiuso = False
        self._finestra = finestra
        if finestra:
            if _os.name == "nt":
                self._lib.libvlc_media_player_set_hwnd(self._lettore, _ctypes.c_void_p(finestra))
            elif _sistema.platform != "darwin":
                self._lib.libvlc_media_player_set_xwindow(self._lettore, finestra)
            else:
                raise MotoreNonSupportato("Su macOS il video dentro una finestra non e' ancora supportato: usa Lettore() senza finestra.")

    @property
    def versione(self):
        return self._lib.libvlc_get_version().decode("utf-8", "replace")

    def apri(self, sorgente):
        testo = str(sorgente)
        if "://" in testo:
            media = self._lib.libvlc_media_new_location(self._istanza, testo.encode("utf-8"))
        else:
            if not _os.path.exists(testo):
                raise FileNotFoundError(f"File non trovato: {sorgente}")
            media = self._lib.libvlc_media_new_path(self._istanza, _os.path.abspath(testo).encode("utf-8"))
        if not media:
            raise ErroreLettore(f"VLC non riesce ad aprire: {sorgente}")
        self._lib.libvlc_media_player_set_media(self._lettore, media)
        if self._media:
            self._lib.libvlc_media_release(self._media)
        self._media = media

    def riproduci(self):
        if self._lib.libvlc_media_player_play(self._lettore) != 0:
            raise ErroreLettore("VLC non riesce a far partire il file.")

    def pausa(self, attiva=True):
        self._lib.libvlc_media_player_set_pause(self._lettore, 1 if attiva else 0)

    def ferma(self):
        self._lib.libvlc_media_player_stop(self._lettore)

    def stato(self):
        return _ID_STATO_VLC.get(self._lib.libvlc_media_player_get_state(self._lettore), "fermo")

    def posizione(self):
        return max(self._lib.libvlc_media_player_get_time(self._lettore), 0) / 1000.0

    def imposta_posizione(self, secondi):
        self._lib.libvlc_media_player_set_time(self._lettore, int(max(secondi, 0) * 1000))

    def durata(self):
        return max(self._lib.libvlc_media_player_get_length(self._lettore), 0) / 1000.0

    def volume(self):
        return max(self._lib.libvlc_audio_get_volume(self._lettore), 0)

    def imposta_volume(self, valore):
        self._lib.libvlc_audio_set_volume(self._lettore, int(max(0, min(200, valore))))

    def muto(self):
        return self._lib.libvlc_audio_get_mute(self._lettore) == 1

    def imposta_muto(self, attivo):
        self._lib.libvlc_audio_set_mute(self._lettore, 1 if attivo else 0)

    def velocita(self):
        return round(self._lib.libvlc_media_player_get_rate(self._lettore), 3)

    def imposta_velocita(self, fattore):
        if self._lib.libvlc_media_player_set_rate(self._lettore, float(fattore)) != 0:
            raise ErroreLettore("Questa velocita' non e' possibile con questo file.")

    def dimensioni(self):
        w, h = _ctypes.c_uint(0), _ctypes.c_uint(0)
        if self._lib.libvlc_video_get_size(self._lettore, 0, _ctypes.byref(w), _ctypes.byref(h)) != 0:
            return (0, 0)
        return (w.value, h.value)

    def istantanea(self, file):
        percorso = _os.path.abspath(str(file))
        if self._lib.libvlc_video_take_snapshot(self._lettore, 0, percorso.encode("utf-8"), 0, 0) != 0:
            raise ErroreLettore("Non c'e' un video da fotografare.")
        fine = _tempo.time() + 3
        while _tempo.time() < fine:
            if _os.path.isfile(percorso) and _os.path.getsize(percorso) > 0:
                return percorso
            _tempo.sleep(0.05)
        raise ErroreLettore("L'istantanea non e' stata salvata.")

    def fotogramma_avanti(self):
        self._lib.libvlc_media_player_next_frame(self._lettore)

    def _elenco(self, funzione, scelta):
        lista = funzione(self._lettore)
        attuale = scelta(self._lettore)
        out = []
        p = lista
        while p:
            voce = p.contents
            out.append(Voce(id=voce.i_id, nome=(voce.psz_name or b"").decode("utf-8", "replace"), attiva=voce.i_id == attuale))
            p = voce.p_next
        if lista:
            self._lib.libvlc_track_description_list_release(lista)
        return out

    def tracce_audio(self):
        return self._elenco(self._lib.libvlc_audio_get_track_description, self._lib.libvlc_audio_get_track)

    def imposta_traccia_audio(self, id_):
        self._lib.libvlc_audio_set_track(self._lettore, int(id_))

    def tracce_sottotitoli(self):
        return self._elenco(self._lib.libvlc_video_get_spu_description, self._lib.libvlc_video_get_spu)

    def imposta_sottotitoli(self, id_):
        self._lib.libvlc_video_set_spu(self._lettore, -1 if id_ is None else int(id_))

    def carica_sottotitoli(self, file):
        if not _os.path.isfile(str(file)):
            raise FileNotFoundError(f"File non trovato: {file}")
        if self._lib.libvlc_video_set_subtitle_file(self._lettore, _os.path.abspath(str(file)).encode("utf-8")) != 1:
            raise ErroreLettore("VLC non riesce a leggere i sottotitoli.")

    def passa_clic(self):
        """Disabilita le finestre del video di VLC (classe 'VLC video ...'): un clic su una finestra disabilitata va a quella che la contiene,
        e cosi' tkinter riceve <Button-1> e il resto. VLC le crea quando il video parte, quindi va richiamato ogni tanto."""
        if not self._finestra:
            return
        if _os.name != "nt":
            if _sistema.platform != "darwin":      # X11: senza eventi selezionati dal video, mouse e tastiera salgono alla finestra che lo contiene
                self._lib.libvlc_video_set_mouse_input(self._lettore, 0)
                self._lib.libvlc_video_set_key_input(self._lettore, 0)
            return
        user32 = _ctypes.windll.user32
        trovate = []
        callback_tipo = _ctypes.WINFUNCTYPE(_ctypes.c_bool, _ctypes.c_void_p, _ctypes.c_void_p)

        def esamina(handle, _):
            nome = _ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(_ctypes.c_void_p(handle), nome, 64)
            if nome.value.startswith("VLC video") and user32.IsWindowEnabled(_ctypes.c_void_p(handle)):
                trovate.append(handle)
            return True
        user32.EnumChildWindows(_ctypes.c_void_p(self._finestra), callback_tipo(esamina), None)
        for handle in trovate:
            user32.EnableWindow(_ctypes.c_void_p(handle), False)

    def chiudi(self):
        if self._chiuso:
            return
        self._chiuso = True
        self._lib.libvlc_media_player_stop(self._lettore)
        self._lib.libvlc_media_player_release(self._lettore)
        if self._media:
            self._lib.libvlc_media_release(self._media)
        self._lib.libvlc_release(self._istanza)


# =====================================================================================================
#  Quali motori ci sono, quale si usa
# =====================================================================================================
_MOTORI = {"vlc": MotoreVlc}
_ELENCO_FUTURI = {"mpv": ("mpv: moderno e leggero, ottima resa video e posizionamento preciso.",
                          "https://mpv.io/installation/  (Linux: sudo apt install mpv; macOS: brew install mpv; Windows: winget search mpv)", "https://mpv.io/")}


def motori():
    """I motori che conosco: lista di Voce (nome, descrizione, disponibile, percorso, implementato, installazione, sito, predefinito)."""
    scelto = motore_predefinito(solo_nome=True)
    out = []
    for nome, classe in _MOTORI.items():
        percorso = classe.trova()
        out.append(Voce(nome=nome, descrizione=classe.descrizione, disponibile=bool(percorso), percorso=percorso or None, implementato=True,
                        installazione=classe._installazione() if hasattr(classe, '_installazione') else classe.installazione, sito=classe.sito, predefinito=nome == scelto))
    for nome, (descrizione, installazione, sito) in _ELENCO_FUTURI.items():
        if nome not in _MOTORI:
            out.append(Voce(nome=nome, descrizione=descrizione, disponibile=False, percorso=None, implementato=False,
                            installazione=_come_installare(nome) if nome == "mpv" else installazione, sito=sito, predefinito=False))
    return out


def motori_disponibili():
    """I nomi dei motori installati e pronti: ['vlc']."""
    return [m.nome for m in motori() if m.disponibile]


def motore_predefinito(solo_nome=False):
    """Il motore preferito: dalla variabile PITONIT_LETTORE, dal file ~/.rad/lettore.json, altrimenti il primo disponibile."""
    scelta = _os.environ.get("PITONIT_LETTORE", "")
    if not scelta:
        try:
            with open(CONFIGURAZIONE, encoding="utf-8") as f:
                scelta = _json.load(f).get("motore", "")
        except (OSError, ValueError):
            scelta = ""
    if scelta in _MOTORI and _MOTORI[scelta].trova():
        return scelta
    for nome, classe in _MOTORI.items():
        if classe.trova():
            return nome
    return None if solo_nome else scelta or None


def imposta_motore_predefinito(nome):
    """Ricorda la scelta (nella cartella .rad): vale per tutti i programmi."""
    if nome != "auto" and nome not in _MOTORI:
        raise ErroreLettore(f"Motore sconosciuto: {nome!r}. Quelli che conosco: {', '.join(list(_MOTORI) + [n for n in _ELENCO_FUTURI if n not in _MOTORI])}")
    _os.makedirs(_os.path.dirname(CONFIGURAZIONE), exist_ok=True)
    with open(CONFIGURAZIONE, "w", encoding="utf-8") as f:
        _json.dump({"motore": "" if nome == "auto" else nome}, f)


def installa_motore(nome="vlc", avanzamento=None):
    """Installa un motore con winget (solo Windows). Windows chiede il permesso di amministratore: la scelta e' tua.
    Ritorna True se il motore risulta installato. `avanzamento(riga)` riceve le righe di testo di winget."""
    classe = _MOTORI.get(nome)
    if classe is None or not getattr(classe, "winget", ""):
        raise ErroreLettore(f"Non so installare {nome!r} da qui: {_ELENCO_FUTURI.get(nome, ('', 'vedi il sito del motore'))[1]}")
    if _os.name != "nt":
        raise ErroreLettore("L'installazione automatica e' solo per Windows: " + (classe._installazione() if hasattr(classe, "_installazione") else classe.installazione))
    import shutil
    if not shutil.which("winget"):
        raise ErroreLettore("winget non c'e' su questo computer: " + (classe._installazione() if hasattr(classe, "_installazione") else classe.installazione))
    processo = _subprocess.Popen(["winget", "install", "--id", classe.winget, "-e", "--accept-package-agreements", "--accept-source-agreements"],
                                 stdout=_subprocess.PIPE, stderr=_subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
                                 creationflags=0x08000000)
    for riga in processo.stdout:
        if avanzamento and riga.strip():
            avanzamento(riga.rstrip())
    processo.wait()
    return bool(classe.trova())


# =====================================================================================================
#  Il lettore: gli stessi comandi per tutti i motori
# =====================================================================================================
class Lettore:
    """Un lettore audio/video. `finestra`: None (il motore apre la sua finestra), un numero (handle della finestra) o un widget tkinter
    dove disegnare il video. `motore`: 'vlc', 'mpv' o 'auto' (il preferito). `opzioni`: opzioni in piu' per il motore."""

    def __init__(self, finestra=None, motore="auto", opzioni=None):
        nome = motore_predefinito(solo_nome=True) if motore in (None, "auto") else motore
        if nome is None:
            raise MotoreNonTrovato("Nessun motore di riproduzione installato. " + " | ".join(f"{m.nome}: {m.installazione}" for m in motori()))
        if nome not in _MOTORI:
            raise MotoreNonTrovato(f"Il motore {nome!r} non e' disponibile. Quelli che conosco: " + ", ".join(m.nome + ("" if m.implementato else " (in arrivo)") for m in motori()))
        if finestra is not None and not isinstance(finestra, int):
            finestra = finestra.winfo_id()          # un widget tkinter: se ne usa la finestra
        self.motore = nome
        self._m = _MOTORI[nome](finestra, opzioni)
        self.clic_attraverso = finestra is not None      # i clic sul video arrivano alla finestra che lo contiene
        self.sorgente = None
        self._eventi = {}
        self._ultimo_stato = "fermo"
        self._thread = None
        self._fermo = _thread.Event()

    # ---- riproduzione
    def apri(self, sorgente, riproduci=True):
        """Carica un file o un indirizzo (http://, rtsp://, ...). Con riproduci=True parte subito."""
        self._m.apri(sorgente)
        self.sorgente = str(sorgente)
        if riproduci:
            self._m.riproduci()
            if self.clic_attraverso:
                self._m.passa_clic()
        return self

    def riproduci(self):
        """Fa partire (o ripartire dall'inizio, se era fermo o finito) il file aperto."""
        if self.sorgente is None:
            raise ErroreLettore("Non c'e' nessun file aperto: usa apri('file').")
        if self._m.stato() == "in_pausa":
            self._m.pausa(False)
        else:
            self._m.riproduci()
        return self

    def pausa(self):
        self._m.pausa(True)
        return self

    def riprendi(self):
        self._m.pausa(False)
        return self

    def commuta(self):
        """Pausa se sta suonando, riprende se e' in pausa (e riparte se e' fermo)."""
        stato = self._m.stato()
        if stato == "in_riproduzione":
            self.pausa()
        elif stato == "in_pausa":
            self.riprendi()
        else:
            self.riproduci()
        return self

    def ferma(self):
        self._m.ferma()
        return self

    def salta(self, secondi):
        """Avanti (positivo) o indietro (negativo) di tot secondi."""
        self.posizione = self.posizione + secondi
        return self

    def fotogramma_avanti(self):
        """Mette in pausa e avanza di un fotogramma."""
        self._m.fotogramma_avanti()
        return self

    # ---- proprieta'
    @property
    def stato(self):
        """'fermo', 'caricamento', 'in_riproduzione', 'in_pausa', 'finito' o 'errore'."""
        return self._m.stato()

    @property
    def in_riproduzione(self):
        return self.stato == "in_riproduzione"

    @property
    def in_pausa(self):
        return self.stato == "in_pausa"

    @property
    def finito(self):
        return self.stato == "finito"

    @property
    def posizione(self):
        """Secondo attuale (si puo' assegnare per spostarsi)."""
        return self._m.posizione()

    @posizione.setter
    def posizione(self, secondi):
        self._m.imposta_posizione(secondi)

    @property
    def durata(self):
        """Durata in secondi (0 finche' il motore non la conosce)."""
        return self._m.durata()

    @property
    def frazione(self):
        """Posizione da 0 a 1 (si puo' assegnare)."""
        d = self.durata
        return self.posizione / d if d else 0.0

    @frazione.setter
    def frazione(self, valore):
        self.posizione = max(0.0, min(1.0, valore)) * self.durata

    @property
    def volume(self):
        """Volume da 0 a 100 (si puo' assegnare)."""
        return self._m.volume()

    @volume.setter
    def volume(self, valore):
        self._m.imposta_volume(valore)

    @property
    def muto(self):
        return self._m.muto()

    @muto.setter
    def muto(self, attivo):
        self._m.imposta_muto(attivo)

    @property
    def velocita(self):
        """Velocita' di riproduzione: 1.0 normale, 2.0 doppia, 0.5 meta' (si puo' assegnare)."""
        return self._m.velocita()

    @velocita.setter
    def velocita(self, fattore):
        self._m.imposta_velocita(fattore)

    @property
    def dimensioni(self):
        """(larghezza, altezza) del video, (0, 0) per l'audio."""
        return self._m.dimensioni()

    @property
    def tracce_audio(self):
        """Le tracce audio: lista di Voce (id, nome, attiva)."""
        return self._m.tracce_audio()

    @property
    def traccia_audio(self):
        a = [t for t in self.tracce_audio if t.attiva]
        return a[0] if a else None

    @traccia_audio.setter
    def traccia_audio(self, id_):
        self._m.imposta_traccia_audio(id_.id if isinstance(id_, Voce) else id_)

    @property
    def tracce_sottotitoli(self):
        return self._m.tracce_sottotitoli()

    @property
    def sottotitoli(self):
        a = [t for t in self.tracce_sottotitoli if t.attiva]
        return a[0] if a else None

    @sottotitoli.setter
    def sottotitoli(self, id_):
        """Assegna l'id di una traccia (o un elemento di tracce_sottotitoli); None li spegne."""
        self._m.imposta_sottotitoli(id_.id if isinstance(id_, Voce) else id_)

    def carica_sottotitoli(self, file):
        """Aggiunge un file di sottotitoli (.srt, .ass, ...)."""
        self._m.carica_sottotitoli(file)
        return self

    def istantanea(self, file):
        """Salva il fotogramma che si vede come immagine (.png). Ritorna il percorso."""
        return self._m.istantanea(file)

    # ---- aspettare e reagire
    def attendi_fine(self, tempo_massimo=None):
        """Aspetta che il file finisca (o che passi `tempo_massimo` secondi). Ritorna True se e' finito."""
        fine = None if tempo_massimo is None else _tempo.time() + tempo_massimo
        _tempo.sleep(0.1)
        while True:
            stato = self.stato
            if stato in ("finito", "errore") or (stato == "fermo" and self.sorgente and self._ha_iniziato):
                return stato == "finito" or stato == "fermo"
            if stato == "in_riproduzione":
                self._ha_iniziato = True
            if fine is not None and _tempo.time() > fine:
                return False
            _tempo.sleep(0.05)

    _ha_iniziato = False

    def quando(self, evento, funzione):
        """Registra una funzione per un evento: 'fine', 'errore', 'avvio', 'pausa', 'cambio_stato'. Va chiamato controlla()
        (o avvia_controllo()) perche' scattino. La funzione riceve il lettore."""
        self._eventi.setdefault(evento, []).append(funzione)
        return self

    def controlla(self):
        """Guarda cosa e' cambiato dall'ultima volta e fa scattare gli eventi. Ritorna lo stato."""
        stato = self.stato
        if self.clic_attraverso:
            self._m.passa_clic()
        if stato != self._ultimo_stato:
            vecchio, self._ultimo_stato = self._ultimo_stato, stato
            nome = {"finito": "fine", "errore": "errore", "in_riproduzione": "avvio", "in_pausa": "pausa"}.get(stato)
            for e in ([nome] if nome else []) + ["cambio_stato"]:
                for funzione in self._eventi.get(e, []):
                    funzione(self)
        return stato

    def avvia_controllo(self, intervallo=0.2):
        """Fa scattare gli eventi da solo, in un thread (le funzioni partono da quel thread: con tkinter usa controlla() con after)."""
        if self._thread and self._thread.is_alive():
            return self
        self._fermo.clear()

        def lavoro():
            while not self._fermo.wait(intervallo):
                try:
                    self.controlla()
                except Exception:
                    return
        self._thread = _thread.Thread(target=lavoro, daemon=True)
        self._thread.start()
        return self

    # ---- chiudere
    def chiudi(self):
        self._fermo.set()
        self._m.chiudi()

    def __enter__(self):
        return self

    def __exit__(self, *errore):
        self.chiudi()

    def __repr__(self):
        return f"<Lettore {self.motore} {self.stato} {self.sorgente or '-'}>"


def riproduci(sorgente, finestra=None, motore="auto"):
    """Scorciatoia: apre un lettore e fa partire il file. Ritorna il Lettore (poi .attendi_fine(), .ferma(), ...)."""
    return Lettore(finestra, motore).apri(sorgente)


# =====================================================================================================
#  Un riquadro tkinter completo: video + controlli
# =====================================================================================================
def _minuti(secondi):
    totale = int(round(secondi))
    ore, resto = divmod(totale, 3600)
    minuti, sec = divmod(resto, 60)
    return f"{ore}:{minuti:02d}:{sec:02d}" if ore else f"{minuti}:{sec:02d}"


if _tk is not None:
    class PannelloLettore(_tk.Frame):
        """Un riquadro tkinter col video e i controlli (play/pausa, barra del tempo, volume, velocita', tracce, istantanea).
        `colori` (facoltativo): dizionario con pannello, primo_piano, tenue, campo, pulsante, accento."""

        VELOCITA = ("0.5", "0.75", "1", "1.25", "1.5", "2")

        def __init__(self, genitore, motore="auto", colori=None, opzioni=None, controlli=True):
            c = dict(pannello="#1e1f22", primo_piano="#e6e6e6", tenue="#9a9a9a", campo="#000000", pulsante="#2f3136", accento="#4f8cff")
            c.update(colori or {})
            super().__init__(genitore, background=c["pannello"])
            self.colori = c
            self._motore_scelto = motore
            self._opzioni = opzioni
            self.lettore = None
            self._trascina = False
            self._aggiorna_id = None
            self.video = _tk.Frame(self, background=c["campo"], width=640, height=360)
            self.video.pack(fill="both", expand=True)
            self.video.update_idletasks()
            self.su_doppio_clic = None          # funzione senza argomenti: la chiama il doppio clic sul video (di solito lo schermo intero)
            self._clic_id = None
            self.video.bind("<Button-1>", self._clic_video)
            self.video.bind("<Double-Button-1>", self._doppio_clic_video)
            self.video.bind("<MouseWheel>", self._rotella_video)
            self.video.configure(cursor="hand2")
            if controlli:
                self._costruisci_controlli()
            self.bind("<Destroy>", self._alla_chiusura)

        # ---- costruzione
        def _costruisci_controlli(self):
            c = self.colori
            barra = _tk.Frame(self, background=c["pannello"])
            barra.pack(fill="x", padx=8, pady=(6, 0))
            self.var_tempo = _tk.DoubleVar(value=0)
            self.scorrevole = _ttk.Scale(barra, from_=0, to=1000, variable=self.var_tempo, command=self._spostato)
            self.scorrevole.pack(side="left", fill="x", expand=True)
            self.scorrevole.bind("<ButtonPress-1>", lambda evento: setattr(self, "_trascina", True))
            self.scorrevole.bind("<ButtonRelease-1>", self._rilasciato)
            self.etichetta_tempo = _tk.Label(barra, text="0:00 / 0:00", width=13, background=c["pannello"], foreground=c["tenue"])
            self.etichetta_tempo.pack(side="left", padx=(8, 0))
            riga = _tk.Frame(self, background=c["pannello"])
            riga.pack(fill="x", padx=8, pady=6)

            def bottone(testo, comando, larghezza=3):
                b = _tk.Button(riga, text=testo, command=comando, width=larghezza, relief="flat", background=c["pulsante"],
                               foreground=c["primo_piano"], activebackground=c["accento"], activeforeground="#ffffff")
                b.pack(side="left", padx=2)
                return b
            self.b_indietro = bottone("⏪", lambda: self._comando(lambda: self.lettore.salta(-10)))
            self.b_play = bottone("▶", self.commuta)
            self.b_ferma = bottone("⏹", lambda: self._comando(lambda: self.lettore.ferma()))
            self.b_avanti = bottone("⏩", lambda: self._comando(lambda: self.lettore.salta(10)))
            self.b_foto = bottone("📷", self.istantanea)
            self.var_muto = _tk.BooleanVar(value=False)
            self.b_muto = _tk.Checkbutton(riga, text="🔇", variable=self.var_muto, command=self._muto, background=c["pannello"], foreground=c["primo_piano"],
                                          selectcolor=c["pulsante"], activebackground=c["pannello"])
            self.b_muto.pack(side="left", padx=(12, 0))
            self.var_volume = _tk.IntVar(value=80)
            self.volume_scala = _ttk.Scale(riga, from_=0, to=100, variable=self.var_volume, command=self._volume, length=90)
            self.volume_scala.pack(side="left", padx=4)
            self.var_velocita = _tk.StringVar(value="1")
            self.velocita_scelta = _ttk.Combobox(riga, textvariable=self.var_velocita, values=self.VELOCITA, width=5, state="readonly")
            self.velocita_scelta.pack(side="left", padx=(12, 0))
            self.velocita_scelta.bind("<<ComboboxSelected>>", self._velocita)
            _tk.Label(riga, text="x", background=c["pannello"], foreground=c["tenue"]).pack(side="left")
            self.menu_audio = _tk.Menubutton(riga, text="Audio ▾", relief="flat", background=c["pulsante"], foreground=c["primo_piano"])
            self.menu_audio.pack(side="left", padx=(12, 2))
            self._menu_audio = _tk.Menu(self.menu_audio, tearoff=0, postcommand=self._riempi_audio)
            self.menu_audio.configure(menu=self._menu_audio)
            self.menu_sotto = _tk.Menubutton(riga, text="Sottotitoli ▾", relief="flat", background=c["pulsante"], foreground=c["primo_piano"])
            self.menu_sotto.pack(side="left", padx=2)
            self._menu_sotto = _tk.Menu(self.menu_sotto, tearoff=0, postcommand=self._riempi_sotto)
            self.menu_sotto.configure(menu=self._menu_sotto)
            self.stato_testo = _tk.Label(riga, text="", background=c["pannello"], foreground=c["tenue"], anchor="e")
            self.stato_testo.pack(side="right", fill="x", expand=True)

        # ---- il mouse sul video (arriva grazie a clic_attraverso)
        def _clic_video(self, evento):
            """Un clic mette in pausa o fa ripartire; aspetta un attimo per capire se e' l'inizio di un doppio clic."""
            if self._clic_id:
                self.after_cancel(self._clic_id)
            self._clic_id = self.after(260, self._clic_semplice)

        def _clic_semplice(self):
            self._clic_id = None
            self.commuta()

        def _doppio_clic_video(self, evento):
            if self._clic_id:
                self.after_cancel(self._clic_id)
                self._clic_id = None
            if self.su_doppio_clic:
                self.su_doppio_clic()

        def _rotella_video(self, evento):
            if hasattr(self, "var_volume"):
                self.var_volume.set(max(0, min(100, self.var_volume.get() + (5 if evento.delta > 0 else -5))))
                self._volume(self.var_volume.get())

        # ---- il lettore
        def avvia(self):
            """Crea il lettore (la prima volta che serve) e comincia ad aggiornare i controlli."""
            if self.lettore is None:
                self.update_idletasks()
                self.lettore = Lettore(self.video, self._motore_scelto, self._opzioni)
                if hasattr(self, "var_volume"):
                    self.lettore.volume = self.var_volume.get()
                self._ciclo()
            return self.lettore

        def apri(self, sorgente, riproduci=True):
            self.avvia().apri(sorgente, riproduci)

        def commuta(self):
            self._comando(lambda: self.lettore.commuta())

        def _comando(self, funzione):
            try:
                if self.lettore is not None:
                    funzione()
            except (ErroreLettore, OSError) as errore:
                self._messaggio(str(errore))

        def _messaggio(self, testo):
            if hasattr(self, "stato_testo"):
                self.stato_testo.configure(text=testo[:80])

        def istantanea(self, file=None):
            if self.lettore is None:
                return None
            if file is None:
                from tkinter import filedialog
                file = filedialog.asksaveasfilename(parent=self, defaultextension=".png", filetypes=[("Immagine PNG", "*.png")], title="Salva l'istantanea")
            if file:
                try:
                    return self.lettore.istantanea(file)
                except (ErroreLettore, OSError) as errore:
                    self._messaggio(str(errore))
            return None

        def _muto(self):
            self._comando(lambda: setattr(self.lettore, "muto", self.var_muto.get()))

        def _volume(self, valore):
            self._comando(lambda: setattr(self.lettore, "volume", int(float(valore))))

        def _velocita(self, evento=None):
            self._comando(lambda: setattr(self.lettore, "velocita", float(self.var_velocita.get())))

        def _spostato(self, valore):
            if self._trascina and self.lettore is not None:
                self.etichetta_tempo.configure(text=f"{_minuti(float(valore) / 1000 * self.lettore.durata)} / {_minuti(self.lettore.durata)}")

        def _rilasciato(self, evento):
            self._trascina = False
            self._comando(lambda: setattr(self.lettore, "frazione", self.var_tempo.get() / 1000))

        def _riempi_menu(self, menu, voci, imposta, con_spento=False):
            menu.delete(0, "end")
            if con_spento:
                menu.add_command(label="Nessuno", command=lambda: imposta(None))
            for voce in voci:
                menu.add_command(label=("● " if voce.attiva else "   ") + voce.nome, command=lambda v=voce: imposta(v.id))
            if not voci:
                menu.add_command(label="(nessuna traccia)", state="disabled")

        def _riempi_audio(self):
            voci = self.lettore.tracce_audio if self.lettore else []
            self._riempi_menu(self._menu_audio, voci, lambda i: self._comando(lambda: setattr(self.lettore, "traccia_audio", i)))

        def _riempi_sotto(self):
            voci = self.lettore.tracce_sottotitoli if self.lettore else []
            self._riempi_menu(self._menu_sotto, [v for v in voci if v.id != -1], lambda i: self._comando(lambda: setattr(self.lettore, "sottotitoli", i)), con_spento=True)

        def _ciclo(self):
            """Aggiorna barra, tempo e pulsante ogni 200 ms e fa scattare gli eventi del lettore."""
            if self.lettore is None:
                return
            try:
                stato = self.lettore.controlla()
                if hasattr(self, "scorrevole"):
                    if not self._trascina:
                        self.var_tempo.set(self.lettore.frazione * 1000)
                        self.etichetta_tempo.configure(text=f"{_minuti(self.lettore.posizione)} / {_minuti(self.lettore.durata)}")
                    self.b_play.configure(text="⏸" if stato == "in_riproduzione" else "▶")
            except Exception:
                return
            self._aggiorna_id = self.after(200, self._ciclo)

        def _alla_chiusura(self, evento):
            if evento.widget is self and self.lettore is not None:
                if self._aggiorna_id:
                    try:
                        self.after_cancel(self._aggiorna_id)
                    except Exception:
                        pass
                try:
                    self.lettore.chiudi()
                except Exception:
                    pass
                self.lettore = None
