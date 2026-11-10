"""Modulo italiano per `sqlite3` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import sqlite3 as _orig
from sqlite3 import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

connetti = _ott(_orig, 'connect')
Connessione = _ott(_orig, 'Connection')
Cursore = _ott(_orig, 'Cursor')
Riga = _ott(_orig, 'Row')
ErroreDatabase = _ott(_orig, 'Error')
ErroreDiIntegrita = _ott(_orig, 'IntegrityError')
ErroreOperativo = _ott(_orig, 'OperationalError')
ErroreDiProgrammazione = _ott(_orig, 'ProgrammingError')
ErroreDiInterfaccia = _ott(_orig, 'InterfaceError')
ErroreDiDati = _ott(_orig, 'DataError')
versione_sqlite = _ott(_orig, 'sqlite_version')
versione = _ott(_orig, 'version')
registra_adattatore = _ott(_orig, 'register_adapter')
registra_convertitore = _ott(_orig, 'register_converter')
PARSE_TIPI_DICHIARATI = _ott(_orig, 'PARSE_DECLTYPES')
PARSE_NOMI_COLONNE = _ott(_orig, 'PARSE_COLNAMES')
completa_istruzione = _ott(_orig, 'complete_statement')
alias_tipo(_ott(_orig, 'Connection'), {'cursore': 'cursor', 'esegui': 'execute', 'esegui_molti': 'executemany', 'esegui_script': 'executescript', 'conferma': 'commit', 'annulla': 'rollback', 'chiudi': 'close', 'crea_funzione': 'create_function', 'crea_aggregato': 'create_aggregate', 'totale_modifiche': 'total_changes', 'copia_di_riserva': 'backup', 'interrompi_query': 'interrupt', 'in_transazione': 'in_transaction', 'fabbrica_righe': 'row_factory', 'scarica': 'iterdump', 'fabbrica_testo': 'text_factory'})
alias_tipo(_ott(_orig, 'Cursor'), {'esegui': 'execute', 'esegui_molti': 'executemany', 'esegui_script': 'executescript', 'ottieni_uno': 'fetchone', 'ottieni_molti': 'fetchmany', 'ottieni_tutti': 'fetchall', 'chiudi': 'close', 'ultimo_id_riga': 'lastrowid', 'numero_righe': 'rowcount', 'descrizione': 'description', 'dimensione_array': 'arraysize'})
alias_tipo(_ott(_orig, 'Row'), {'chiavi': 'keys'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'data_da_tacche': 'DateFromTicks', 'SQLITE_INTERROMPI': 'SQLITE_ABORT', 'SQLITE_INTERROMPI_ANNULLA_MODIFICHE': 'SQLITE_ABORT_ROLLBACK', 'SQLITE_AUTENTICAZIONE': 'SQLITE_AUTH', 'SQLITE_AUTENTICAZIONE_UTENTE': 'SQLITE_AUTH_USER', 'SQLITE_VINCOLO': 'SQLITE_CONSTRAINT', 'SQLITE_VINCOLO_CONTROLLA': 'SQLITE_CONSTRAINT_CHECK', 'SQLITE_VINCOLO_FUNZIONE': 'SQLITE_CONSTRAINT_FUNCTION', 'SQLITE_VINCOLO_ATTIVA': 'SQLITE_CONSTRAINT_TRIGGER', 'SQLITE_VINCOLO_UNICO': 'SQLITE_CONSTRAINT_UNIQUE', 'SQLITE_CORROTTO': 'SQLITE_CORRUPT', 'SQLITE_CORROTTO_INDICE': 'SQLITE_CORRUPT_INDEX', 'SQLITE_CORROTTO_SEQUENZA': 'SQLITE_CORRUPT_SEQUENCE', 'SQLITE_CREA_INDICE': 'SQLITE_CREATE_INDEX', 'SQLITE_CREA_TABELLA': 'SQLITE_CREATE_TABLE', 'SQLITE_CREA_TEMPORANEO_INDICE': 'SQLITE_CREATE_TEMP_INDEX', 'SQLITE_CREA_TEMPORANEO_TABELLA': 'SQLITE_CREATE_TEMP_TABLE', 'SQLITE_CREA_TEMPORANEO_ATTIVA': 'SQLITE_CREATE_TEMP_TRIGGER', 'SQLITE_CREA_TEMPORANEO_VISTA': 'SQLITE_CREATE_TEMP_VIEW', 'SQLITE_CREA_ATTIVA': 'SQLITE_CREATE_TRIGGER', 'SQLITE_CREA_VISTA': 'SQLITE_CREATE_VIEW', 'SQLITE_CANCELLA': 'SQLITE_DELETE', 'SQLITE_STACCA': 'SQLITE_DETACH', 'SQLITE_RILASCIA_INDICE': 'SQLITE_DROP_INDEX', 'SQLITE_RILASCIA_TABELLA': 'SQLITE_DROP_TABLE', 'SQLITE_RILASCIA_TEMPORANEO_INDICE': 'SQLITE_DROP_TEMP_INDEX', 'SQLITE_RILASCIA_TEMPORANEO_TABELLA': 'SQLITE_DROP_TEMP_TABLE', 'SQLITE_RILASCIA_TEMPORANEO_ATTIVA': 'SQLITE_DROP_TEMP_TRIGGER', 'SQLITE_RILASCIA_TEMPORANEO_VISTA': 'SQLITE_DROP_TEMP_VIEW', 'SQLITE_RILASCIA_ATTIVA': 'SQLITE_DROP_TRIGGER', 'SQLITE_RILASCIA_VISTA': 'SQLITE_DROP_VIEW', 'SQLITE_VUOTO': 'SQLITE_EMPTY', 'SQLITE_ERRORE': 'SQLITE_ERROR', 'SQLITE_ERRORE_RIPROVA': 'SQLITE_ERROR_RETRY', 'SQLITE_FORMATO': 'SQLITE_FORMAT', 'SQLITE_COMPLETO': 'SQLITE_FULL', 'SQLITE_FUNZIONE': 'SQLITE_FUNCTION', 'SQLITE_IGNORA': 'SQLITE_IGNORE', 'SQLITE_INSERISCI': 'SQLITE_INSERT', 'SQLITE_INTERNO': 'SQLITE_INTERNAL', 'SQLITE_LIMITA_COLONNA': 'SQLITE_LIMIT_COLUMN', 'SQLITE_LIMITA_LUNGHEZZA': 'SQLITE_LIMIT_LENGTH', 'SQLITE_LIMITA_COME_MODELLO_LUNGHEZZA': 'SQLITE_LIMIT_LIKE_PATTERN_LENGTH', 'SQLITE_LIMITA_SQL_LUNGHEZZA': 'SQLITE_LIMIT_SQL_LENGTH', 'SQLITE_LIMITA_ATTIVA_PROFONDITA': 'SQLITE_LIMIT_TRIGGER_DEPTH', 'SQLITE_LIMITA_VARIABILE_NUMERO': 'SQLITE_LIMIT_VARIABLE_NUMBER', 'SQLITE_LIMITA_LAVORATORE_FILI': 'SQLITE_LIMIT_WORKER_THREADS', 'SQLITE_BLOCCATO': 'SQLITE_LOCKED', 'SQLITE_OK_COLLEGAMENTO_SIMBOLICO': 'SQLITE_OK_SYMLINK', 'SQLITE_PROTOCOLLO': 'SQLITE_PROTOCOL', 'SQLITE_INTERVALLO': 'SQLITE_RANGE', 'SQLITE_LEGGI': 'SQLITE_READ', 'SQLITE_SOLA_LETTURA': 'SQLITE_READONLY', 'SQLITE_SOLA_LETTURA_CARTELLA': 'SQLITE_READONLY_DIRECTORY', 'SQLITE_SOLA_LETTURA_ANNULLA_MODIFICHE': 'SQLITE_READONLY_ROLLBACK', 'SQLITE_RICORSIVO': 'SQLITE_RECURSIVE', 'SQLITE_REINDICIZZA': 'SQLITE_REINDEX', 'SQLITE_RIGA': 'SQLITE_ROW', 'SQLITE_PUNTO_DI_SALVATAGGIO': 'SQLITE_SAVEPOINT', 'SQLITE_SELEZIONA': 'SQLITE_SELECT', 'SQLITE_TRANSAZIONE': 'SQLITE_TRANSACTION', 'SQLITE_AGGIORNA': 'SQLITE_UPDATE', 'SQLITE_AVVISO': 'SQLITE_WARNING', 'tempo_da_tacche': 'TimeFromTicks', 'timestamp_da_tacche': 'TimestampFromTicks', 'sqlite_versione_informazione': 'sqlite_version_info'}
_AUTO_TIPI = {'Blob': {'chiudi': 'close', 'leggi': 'read', 'posiziona': 'seek', 'posizione': 'tell', 'scrivi': 'write'}, 'Connection': {'database_errore': 'DatabaseError', 'errore_interno': 'InternalError', 'non_supportato_errore': 'NotSupportedError', 'avviso': 'Warning', 'chiudi': 'close', 'conferma': 'commit', 'crea_funzione': 'create_function', 'crea_finestra_funzione': 'create_window_function', 'cursore': 'cursor', 'abilita_carica_estensione': 'enable_load_extension', 'esegui': 'execute', 'in_transazione': 'in_transaction', 'carica_estensione': 'load_extension', 'annulla_modifiche': 'rollback', 'riga_fabbrica': 'row_factory', 'imposta_avanzamento_gestore': 'set_progress_handler', 'imposta_traccia_richiamo': 'set_trace_callback', 'testo_fabbrica': 'text_factory'}, 'Cursor': {'chiudi': 'close', 'connessione': 'connection', 'descrizione': 'description', 'esegui': 'execute', 'riga_fabbrica': 'row_factory'}, 'Row': {'chiavi': 'keys'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
