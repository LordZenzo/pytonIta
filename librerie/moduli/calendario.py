"""Modulo italiano per `calendar` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import calendar as _orig
from calendar import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

intervallo_mese = _ott(_orig, 'monthrange')
è_bisestile = _ott(_orig, 'isleap')
giorni_bisestili = _ott(_orig, 'leapdays')
mese_testo = _ott(_orig, 'month')
calendario_anno = _ott(_orig, 'calendar')
calendario_mese = _ott(_orig, 'monthcalendar')
giorno_settimana = _ott(_orig, 'weekday')
nomi_giorni = _ott(_orig, 'day_name')
nomi_giorni_brevi = _ott(_orig, 'day_abbr')
nomi_mesi = _ott(_orig, 'month_name')
nomi_mesi_brevi = _ott(_orig, 'month_abbr')
imposta_primo_giorno = _ott(_orig, 'setfirstweekday')
tempo_utc = _ott(_orig, 'timegm')
Calendario = _ott(_orig, 'Calendar')
CalendarioTesto = _ott(_orig, 'TextCalendar')
LUNEDI = _ott(_orig, 'MONDAY')
MARTEDI = _ott(_orig, 'TUESDAY')
MERCOLEDI = _ott(_orig, 'WEDNESDAY')
GIOVEDI = _ott(_orig, 'THURSDAY')
VENERDI = _ott(_orig, 'FRIDAY')
SABATO = _ott(_orig, 'SATURDAY')
DOMENICA = _ott(_orig, 'SUNDAY')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'HTMLCalendar': {'classe_css_mese': 'cssclass_month', 'classe_css_mese_testa': 'cssclass_month_head', 'classe_css_anno': 'cssclass_year', 'classe_css_anno_testa': 'cssclass_year_head'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
