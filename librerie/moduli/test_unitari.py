"""Modulo italiano per `unittest` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import unittest as _orig
from unittest import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

CasoDiTest = _ott(_orig, 'TestCase')
principale = _ott(_orig, 'main')
SuiteDiTest = _ott(_orig, 'TestSuite')
CaricatoreTest = _ott(_orig, 'TestLoader')
EsecutoreTestTestuale = _ott(_orig, 'TextTestRunner')
salta = _ott(_orig, 'skip')
salta_se = _ott(_orig, 'skipIf')
salta_a_meno_che = _ott(_orig, 'skipUnless')
fallimento_atteso = _ott(_orig, 'expectedFailure')
_OPZ = {'flusso': 'stream', 'dettaglio': 'verbosity', 'esci': 'exit', 'argv': 'argv'}
_VAL = {}
kw_tipo(_ott(_orig, 'TextTestRunner'), ['__init__'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'TestCase'), {'asserisci_uguale': 'assertEqual', 'asserisci_diverso': 'assertNotEqual', 'asserisci_vero': 'assertTrue', 'asserisci_falso': 'assertFalse', 'asserisci_è': 'assertIs', 'asserisci_non_è': 'assertIsNot', 'asserisci_nessuno': 'assertIsNone', 'asserisci_non_nessuno': 'assertIsNotNone', 'asserisci_in': 'assertIn', 'asserisci_non_in': 'assertNotIn', 'asserisci_istanza_di': 'assertIsInstance', 'asserisci_non_istanza_di': 'assertNotIsInstance', 'asserisci_solleva': 'assertRaises', 'asserisci_solleva_regex': 'assertRaisesRegex', 'asserisci_quasi_uguale': 'assertAlmostEqual', 'asserisci_maggiore': 'assertGreater', 'asserisci_maggiore_uguale': 'assertGreaterEqual', 'asserisci_minore': 'assertLess', 'asserisci_minore_uguale': 'assertLessEqual', 'asserisci_regex': 'assertRegex', 'asserisci_stessi_elementi': 'assertCountEqual', 'asserisci_liste_uguali': 'assertListEqual', 'asserisci_dizionari_uguali': 'assertDictEqual', 'asserisci_tuple_uguali': 'assertTupleEqual', 'asserisci_insiemi_uguali': 'assertSetEqual', 'asserisci_testo_uguale': 'assertMultiLineEqual', 'fallisci': 'fail', 'salta_test': 'skipTest', 'sotto_test': 'subTest', 'aggiungi_pulizia': 'addCleanup'})
alias_tipo(_ott(_orig, 'TextTestRunner'), {'esegui': 'run'})
alias_tipo(_ott(_orig, 'TestLoader'), {'carica_test_da_caso': 'loadTestsFromTestCase', 'carica_test_da_modulo': 'loadTestsFromModule', 'carica_test_da_nome': 'loadTestsFromName', 'scopri': 'discover'})
alias_tipo(_ott(_orig, 'TestResult'), {'test_eseguiti': '@testsRun', 'è_riuscito': 'wasSuccessful', 'fallimenti': '@failures', 'errori': '@errors', 'saltati': '@skipped'})

from _italiano import traduci_kw as _tr
principale = _tr(principale, _OPZ)

from _italiano import ponte as _ponte
_ponte(_orig.TestCase, {'setUp': 'prepara', 'tearDown': 'smonta',
                        'setUpClass': 'prepara_classe', 'tearDownClass': 'smonta_classe'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'aggiungi_modulo_pulisci': 'addModuleCleanup', 'entra_modulo_contesto': 'enterModuleContext', 'installa_gestore': 'installHandler', 'registra_risultato': 'registerResult', 'rimuovi_gestore': 'removeHandler', 'rimuovi_risultato': 'removeResult'}
_AUTO_TIPI = {'BaseTestSuite': {'aggiungi_verifica': 'addTest', 'aggiungi_test': 'addTests', 'esegui': 'run'}, 'FunctionTestCase': {'esegui_verifica': 'runTest', 'imposta_su': 'setUp', 'descrizione_corto': 'shortDescription', 'strappa_giu': 'tearDown'}, 'IsolatedAsyncioTestCase': {'aggiungi_pulisci_asincrono': 'addAsyncCleanup', 'insieme_asincrono_su': 'asyncSetUp', 'strappa_asincrono_giu': 'asyncTearDown', 'entra_contesto_asincrono': 'enterAsyncContext', 'ciclo_fabbrica': 'loop_factory', 'esegui': 'run'}, 'TestCase': {'aggiungi_classe_pulisci': 'addClassCleanup', 'aggiungi_pulisci': 'addCleanup', 'verifica_predefinito_risultato': 'defaultTestResult', 'entra_classe_contesto': 'enterClassContext', 'entra_contesto': 'enterContext', 'fallimento_eccezione': 'failureException', 'messaggio_lungo': 'longMessage', 'differenza_massimo': 'maxDiff', 'esegui': 'run', 'imposta_su': 'setUp', 'imposta_su_classe': 'setUpClass', 'descrizione_corto': 'shortDescription', 'salta_verifica': 'skipTest', 'strappa_giu': 'tearDown', 'strappa_giu_classe': 'tearDownClass'}, 'TestLoader': {'ottieni_verifica_maiuscole_minuscole_nomi': 'getTestCaseNames', 'carica_test_da_modulo': 'loadTestsFromModule', 'carica_test_da_nome': 'loadTestsFromName', 'carica_test_da_nomi': 'loadTestsFromNames', 'carica_test_da_verifica_maiuscole_minuscole': 'loadTestsFromTestCase', 'verifica_metodo_prefisso': 'testMethodPrefix'}, 'TestProgram': {'crea_test': 'createTests', 'modulo': 'module', 'analizza_argomenti': 'parseArgs', 'esegui_test': 'runTests'}, 'TestResult': {'aggiungi_durata': 'addDuration', 'aggiungi_errore': 'addError', 'aggiungi_fallimento': 'addFailure', 'aggiungi_salta': 'addSkip', 'aggiungi_successo': 'addSuccess', 'stampa_errori': 'printErrors', 'avvia_verifica': 'startTest', 'avvia_verifica_esegui': 'startTestRun', 'ferma': 'stop', 'ferma_verifica': 'stopTest', 'ferma_verifica_esegui': 'stopTestRun'}, 'TestSuite': {'esegui': 'run'}, 'TextTestResult': {'aggiungi_errore': 'addError', 'aggiungi_fallimento': 'addFailure', 'aggiungi_salta': 'addSkip', 'aggiungi_successo': 'addSuccess', 'ottieni_descrizione': 'getDescription', 'stampa_errore_lista': 'printErrorList', 'stampa_errori': 'printErrors', 'avvia_verifica': 'startTest'}, 'TextTestRunner': {'esegui': 'run'}, 'main': {'crea_test': 'createTests', 'modulo': 'module', 'analizza_argomenti': 'parseArgs', 'esegui_test': 'runTests'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
