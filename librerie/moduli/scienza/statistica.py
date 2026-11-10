"""Modulo italiano per `scipy.stats` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy.stats as _orig
from scipy.stats import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

normale = _ott(_orig, 'norm')
test_t_indipendenti = _ott(_orig, 'ttest_ind')
test_t_appaiati = _ott(_orig, 'ttest_rel')
correlazione_pearson = _ott(_orig, 'pearsonr')
correlazione_spearman = _ott(_orig, 'spearmanr')
regressione_lineare = _ott(_orig, 'linregress')
descrivi = _ott(_orig, 'describe')
punteggio_z = _ott(_orig, 'zscore')
test_chi_quadro = _ott(_orig, 'chisquare')
moda = _ott(_orig, 'mode')
asimmetria = _ott(_orig, 'skew')
curtosi = _ott(_orig, 'kurtosis')
test_normalita = _ott(_orig, 'shapiro')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'trasparenza': 'alpha', 'entropia': 'entropy', 'esponenziale': 'exp', 'registra': 'log', 'logistica': 'logistic', 'matrice_normale': 'matrix_normal', 'mediana_verifica': 'median_test', 'potenza': 'power', 'quantile_verifica': 'quantile_test', 'intero_casuale': 'randint', 'casuale_tabella': 'random_table', 'tronca': 'truncate', 'uniforme': 'uniform', 'uniforme_direzione': 'uniform_direction'}
_AUTO_TIPI = {'BootstrapMethod': {'metodo': 'method', 'casuale_stato': 'random_state'}, 'Covariance': {'da_diagonale': 'from_diagonal', 'forma': 'shape'}, 'Mixture': {'componenti': 'components', 'entropia': 'entropy', 'media': 'mean', 'mediana': 'median', 'campione': 'sample'}, 'PermutationMethod': {'casuale_stato': 'random_state'}, 'gaussian_kde': {'integra_riquadro': 'integrate_box'}, 'rv_discrete': {'entropia': 'entropy', 'intervallo': 'interval', 'media': 'mean', 'mediana': 'median', 'statistiche': 'stats'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
