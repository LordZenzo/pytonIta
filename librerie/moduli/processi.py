"""Modulo italiano per `subprocess` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import subprocess as _orig
from subprocess import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

esegui = _ott(_orig, 'run')
Processo = _ott(_orig, 'Popen')
controlla_output = _ott(_orig, 'check_output')
controlla_chiamata = _ott(_orig, 'check_call')
chiama = _ott(_orig, 'call')
TUBO = _ott(_orig, 'PIPE')
USCITA_STANDARD = _ott(_orig, 'STDOUT')
NULLO = _ott(_orig, 'DEVNULL')
ErroreProcesso = _ott(_orig, 'CalledProcessError')
ErroreTimeoutProcesso = _ott(_orig, 'TimeoutExpired')
RisultatoProcesso = _ott(_orig, 'CompletedProcess')
ErroreSottoprocesso = _ott(_orig, 'SubprocessError')
_OPZ = {'cattura_output': 'capture_output', 'testo': 'text', 'controlla': 'check', 'cartella_lavoro': 'cwd', 'tempo_massimo': 'timeout', 'ambiente': 'env', 'ingresso': 'input', 'codifica': 'encoding', 'ingresso_standard': 'stdin', 'uscita_standard': 'stdout', 'errore_standard': 'stderr', 'argomenti': 'args', 'nascondi_console': 'creationflags'}
_VAL = {}
kw_tipo(_ott(_orig, 'Popen'), ['__init__'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'Popen'), {'aspetta': 'wait', 'comunica': 'communicate', 'termina': 'terminate', 'uccidi': 'kill', 'interroga': 'poll', 'codice_ritorno': '@returncode', 'invia_segnale': 'send_signal', 'pid': '@pid'})
alias_tipo(_ott(_orig, 'CompletedProcess'), {'codice_ritorno': '@returncode', 'output': '@stdout', 'errore': '@stderr', 'controlla_ritorno': 'check_returncode'})

from _italiano import traduci_kw as _tr
for _n in ('esegui', 'controlla_output', 'controlla_chiamata', 'chiama'):
    globals()[_n] = _tr(globals()[_n], _OPZ)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'SOPRA_PRIORITA_NORMALE_CLASSE': 'ABOVE_NORMAL_PRIORITY_CLASS', 'SOTTO_PRIORITA_NORMALE_CLASSE': 'BELOW_NORMAL_PRIORITY_CLASS', 'CREA_ERRORE_PREDEFINITO_MODALITA': 'CREATE_DEFAULT_ERROR_MODE', 'CREA_NUOVO_PROCESSO_GRUPPO': 'CREATE_NEW_PROCESS_GROUP', 'CREA_NO_FINESTRA': 'CREATE_NO_WINDOW', 'PRIORITA_ALTO_CLASSE': 'HIGH_PRIORITY_CLASS', 'PRIORITA_INATTIVO_CLASSE': 'IDLE_PRIORITY_CLASS', 'PRIORITA_NORMALE_CLASSE': 'NORMAL_PRIORITY_CLASS'}
_AUTO_TIPI = {'CalledProcessError': {'uscita_standard': 'stdout'}, 'Handle': {'chiudi': 'Close', 'stacca': 'Detach', 'chiuso': 'closed'}, 'Popen': {'uccidi': 'kill', 'invia_segnale': 'send_signal', 'termina': 'terminate', 'aspetta': 'wait'}, 'STARTUPINFO': {'copia': 'copy'}, 'TimeoutExpired': {'uscita_standard': 'stdout'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
