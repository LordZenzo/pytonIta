"""Modulo italiano per `argparse` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import argparse as _orig
from argparse import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

AnalizzatoreArgomenti = _ott(_orig, 'ArgumentParser')
SpazioNomi = _ott(_orig, 'Namespace')
ErroreTipoArgomento = _ott(_orig, 'ArgumentTypeError')
TipoFile = _ott(_orig, 'FileType')
FormattatoreTestoGrezzo = _ott(_orig, 'RawTextHelpFormatter')
FormattatoreValoriPredefiniti = _ott(_orig, 'ArgumentDefaultsHelpFormatter')
SOPPRIMI = _ott(_orig, 'SUPPRESS')
RESTO = _ott(_orig, 'REMAINDER')
ErroreArgomento = _ott(_orig, 'ArgumentError')
_OPZ = {'aiuto': 'help', 'predefinito': 'default', 'tipo': 'type', 'obbligatorio': 'required', 'azione': 'action', 'numero_argomenti': 'nargs', 'scelte': 'choices', 'metavariabile': 'metavar', 'destinazione': 'dest', 'costante': 'const', 'descrizione': 'description', 'programma': 'prog', 'uso': 'usage', 'epilogo': 'epilog', 'classe_formato': 'formatter_class', 'aggiungi_aiuto': 'add_help', 'genitori': 'parents', 'versione': 'version'}
_VAL = {'action': {'memorizza': 'store', 'memorizza_vero': 'store_true', 'memorizza_falso': 'store_false', 'aggiungi': 'append', 'conta': 'count', 'versione': 'version', 'memorizza_costante': 'store_const'}}
kw_tipo(_ott(_orig, 'ArgumentParser'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, '_ActionsContainer'), ['add_argument'], _OPZ, _VAL)
kw_tipo(_ott(_orig, '_SubParsersAction'), ['add_parser'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'ArgumentParser'), {'analizza_argomenti': 'parse_args', 'analizza_argomenti_noti': 'parse_known_args', 'aggiungi_sottoanalizzatori': 'add_subparsers', 'aggiungi_gruppo': 'add_argument_group', 'aggiungi_gruppo_esclusivo': 'add_mutually_exclusive_group', 'stampa_aiuto': 'print_help', 'stampa_uso': 'print_usage', 'errore': 'error', 'imposta_predefiniti': 'set_defaults', 'formatta_aiuto': 'format_help', 'esci': 'exit'})
alias_tipo(_ott(_orig, '_ActionsContainer'), {'aggiungi_argomento': 'add_argument'})
alias_tipo(_ott(_orig, '_SubParsersAction'), {'aggiungi_analizzatore': 'add_parser'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'OPZIONALE': 'OPTIONAL', 'ANALIZZATORE': 'PARSER'}
_AUTO_TIPI = {'Action': {'formatta_uso': 'format_usage'}, 'ArgumentParser': {'errore': 'error', 'formatta_aiuto': 'format_help', 'formatta_uso': 'format_usage', 'analizza_argomenti': 'parse_args', 'stampa_aiuto': 'print_help', 'stampa_uso': 'print_usage'}, 'BooleanOptionalAction': {'formatta_uso': 'format_usage'}, 'HelpFormatter': {'aggiungi_argomento': 'add_argument', 'aggiungi_argomenti': 'add_arguments', 'aggiungi_testo': 'add_text', 'aggiungi_uso': 'add_usage', 'fine_sezione': 'end_section', 'formatta_aiuto': 'format_help', 'avvia_sezione': 'start_section'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
