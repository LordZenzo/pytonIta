"""Modulo italiano per `datetime` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import datetime as _orig
from datetime import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Data = _ott(_orig, 'date')
OraData = _ott(_orig, 'datetime')
Ora = _ott(_orig, 'time')
Differenza = _ott(_orig, 'timedelta')
FusoOrario = _ott(_orig, 'timezone')
InfoFuso = _ott(_orig, 'tzinfo')
ANNO_MINIMO = _ott(_orig, 'MINYEAR')
ANNO_MASSIMO = _ott(_orig, 'MAXYEAR')
UTC = _ott(_orig, 'UTC')
alias_tipo(_ott(_orig, 'date'), {'oggi': 'today', 'da_timestamp': 'fromtimestamp', 'da_ordinale': 'fromordinal', 'da_isoformato': 'fromisoformat', 'da_calendario_iso': 'fromisocalendar', 'sostituisci': 'replace', 'formatta': 'strftime', 'isoformato': 'isoformat', 'giorno_settimana': 'weekday', 'giorno_settimana_iso': 'isoweekday', 'calendario_iso': 'isocalendar', 'anno': 'year', 'mese': 'month', 'giorno': 'day', 'ordinale': 'toordinal', 'tupla_tempo': 'timetuple', 'ctime': 'ctime', 'minimo': 'min', 'massimo': 'max'})
alias_tipo(_ott(_orig, 'datetime'), {'adesso': 'now', 'adesso_utc': 'utcnow', 'combina': 'combine', 'analizza': 'strptime', 'ora': 'hour', 'minuto': 'minute', 'secondo': 'second', 'microsecondo': 'microsecond', 'ottieni_data': 'date', 'ottieni_ora': 'time', 'info_fuso': 'tzinfo', 'in_fuso': 'astimezone', 'timestamp': 'timestamp', 'da_timestamp_utc': 'utcfromtimestamp'})
alias_tipo(_ott(_orig, 'time'), {'ora': 'hour', 'minuto': 'minute', 'secondo': 'second', 'microsecondo': 'microsecond', 'isoformato': 'isoformat', 'formatta': 'strftime', 'sostituisci': 'replace'})
alias_tipo(_ott(_orig, 'timedelta'), {'giorni': 'days', 'secondi': 'seconds', 'microsecondi': 'microseconds', 'secondi_totali': 'total_seconds'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'date': {'tempo_creazione': 'ctime', 'giorno': 'day', 'da_isoformato': 'fromisoformat', 'massimo': 'max', 'minimo': 'min', 'mese': 'month', 'sostituisci': 'replace', 'risoluzione': 'resolution', 'formatta_tempo': 'strftime', 'oggi': 'today', 'giorno_settimana': 'weekday', 'anno': 'year'}, 'datetime': {'combina': 'combine', 'tempo_creazione': 'ctime', 'ora_legale': 'dst', 'da_isoformato': 'fromisoformat', 'ora': 'hour', 'massimo': 'max', 'microsecondo': 'microsecond', 'minimo': 'min', 'minuto': 'minute', 'adesso': 'now', 'sostituisci': 'replace', 'risoluzione': 'resolution', 'secondo': 'second', 'scostamento_utc': 'utcoffset'}, 'time': {'ora_legale': 'dst', 'da_isoformato': 'fromisoformat', 'ora': 'hour', 'massimo': 'max', 'microsecondo': 'microsecond', 'minimo': 'min', 'minuto': 'minute', 'sostituisci': 'replace', 'risoluzione': 'resolution', 'secondo': 'second', 'formatta_tempo': 'strftime', 'scostamento_utc': 'utcoffset'}, 'timedelta': {'giorni': 'days', 'massimo': 'max', 'minimo': 'min', 'risoluzione': 'resolution', 'secondi': 'seconds', 'secondi_totale': 'total_seconds'}, 'timezone': {'ora_legale': 'dst', 'massimo': 'max', 'minimo': 'min', 'scostamento_utc': 'utcoffset'}, 'tzinfo': {'ora_legale': 'dst', 'scostamento_utc': 'utcoffset'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
