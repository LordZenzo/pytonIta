"""Genera la galleria di icone di PitStudio: ogni icona è disegnata qui con linee e forme semplici (24x24, tratto di 2) e salvata in due colori:
<nome>.png (scuro, per i fondi chiari), <nome>_chiaro.png (chiaro, per i fondi scuri) e <nome>_colore.png (a colori, per qualunque fondo), più indice.json con categoria e parole chiave.
Si lancia con Python (serve Pillow) dalla cartella RAD\\icone:  python _genera.py
Le icone sono disegni originali di PitStudio, usabili liberamente nei programmi fatti con PitStudio."""
import json
import math
import os

from PIL import Image, ImageDraw

QUI = os.path.dirname(os.path.abspath(__file__))
S = 8                      # sovracampionamento
DIM = 24
SCURO = (31, 41, 51, 255)
CHIARO = (232, 236, 241, 255)


class G:
    def __init__(se, colore):
        se.im = Image.new("RGBA", (DIM * S, DIM * S), (0, 0, 0, 0))
        se.d = ImageDraw.Draw(se.im)
        se.c = colore
        se.w = int(2 * S)

    def _p(se, pt):
        return (pt[0] * S, pt[1] * S)

    def pt(se, x, y, r=None):
        r = (se.w / 2) if r is None else r * S
        se.d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=se.c)

    def L(se, *pts):                       # linea spezzata con estremi arrotondati
        for a, b in zip(pts, pts[1:]):
            se.d.line([se._p(a), se._p(b)], fill=se.c, width=se.w)
        for a in pts:
            se.pt(*a)

    def Lc(se, *pts):                      # poligono chiuso (solo contorno)
        se.L(*pts, pts[0])

    def F(se, *pts):                       # poligono pieno
        se.d.polygon([se._p(a) for a in pts], fill=se.c)

    def C(se, cx, cy, r):                  # cerchio (contorno)
        se.d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), outline=se.c, width=se.w)

    def D(se, cx, cy, r=1.4):              # cerchio pieno
        se.d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=se.c)

    def R(se, x, y, w, h, r=2):            # rettangolo arrotondato (contorno)
        se.d.rounded_rectangle((x * S, y * S, (x + w) * S, (y + h) * S), radius=r * S, outline=se.c, width=se.w)

    def RF(se, x, y, w, h, r=1):           # rettangolo arrotondato pieno
        se.d.rounded_rectangle((x * S, y * S, (x + w) * S, (y + h) * S), radius=r * S, fill=se.c)

    def A(se, cx, cy, r, a0, a1):          # arco: gradi, 0 = ore 3, in senso orario
        se.d.arc(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), a0, a1, fill=se.c, width=se.w)
        for a in (a0, a1):
            se.pt(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))

    def EA(se, cx, cy, rx, ry, a0=0, a1=360, passi=40):     # ellisse o suo arco (gradi), a segmenti
        pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / passi)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / passi))) for i in range(passi + 1)]
        se.L(*pts)

    def fine(se):
        return se.im.resize((DIM, DIM), Image.LANCZOS)


# ------------------------------------------------------------------ pezzi riutilizzabili
def pagina(g, piega=True):
    g.L((6, 3), (14, 3), (19, 8), (19, 21), (6, 21), (6, 3))
    if piega:
        g.L((14, 3), (14, 8), (19, 8))


def freccia(g, x0, y0, x1, y1, testa=3.2):
    g.L((x0, y0), (x1, y1))
    a = math.atan2(y1 - y0, x1 - x0)
    for d in (2.5, -2.5):
        g.L((x1, y1), (x1 - testa * math.cos(a + d / 3.2 * 0.62), y1 - testa * math.sin(a + d / 3.2 * 0.62)))


def cartella(g):
    g.L((3, 7), (3, 19), (21, 19), (21, 9), (11, 9), (9, 6), (4, 6), (3, 7))


def ingranaggio(g, cx=12, cy=12, r=4, dente=8.5):
    g.C(cx, cy, r)
    for i in range(8):
        a = math.radians(i * 45)
        g.L((cx + (r + 2.2) * math.cos(a), cy + (r + 2.2) * math.sin(a)), (cx + dente * math.cos(a), cy + dente * math.sin(a)))


def riga_testo(g, y, x0=5, x1=19):
    g.L((x0, y), (x1, y))


ICONE = {}      # nome -> (categoria, parole, funzione)


def icona(nome, categoria, parole=""):
    def deco(f):
        ICONE[nome] = (categoria, parole, f)
        return f
    return deco


# ================================================================== File e documenti
@icona("nuovo", "File e documenti", "nuovo crea aggiungi file pagina")
def _(g):
    pagina(g)
    g.L((12.5, 12), (12.5, 18)), g.L((9.5, 15), (15.5, 15))


@icona("apri", "File e documenti", "apri cartella aperta")
def _(g):
    g.L((3, 8), (3, 19), (18, 19)), g.L((3, 8), (4, 6), (9, 6), (11, 8), (18, 8), (18, 11))
    g.L((3, 19), (6, 11), (22, 11), (18, 19))


@icona("cartella", "File e documenti", "cartella directory")
def _(g):
    cartella(g)


@icona("cartella_nuova", "File e documenti", "cartella nuova crea")
def _(g):
    cartella(g)
    g.L((12, 11.5), (12, 16.5)), g.L((9.5, 14), (14.5, 14))


@icona("salva", "File e documenti", "salva dischetto")
def _(g):
    g.L((4, 4), (17, 4), (20, 7), (20, 20), (4, 20), (4, 4))
    g.L((8, 4), (8, 9), (15, 9), (15, 4)), g.L((8, 20), (8, 14), (16, 14), (16, 20))


@icona("salva_come", "File e documenti", "salva con nome")
def _(g):
    g.L((4, 4), (16, 4), (19, 7), (19, 11)), g.L((4, 4), (4, 20), (11, 20))
    g.L((8, 4), (8, 8), (14, 8), (14, 4)), g.L((13, 20), (13, 17), (20, 10), (22, 12), (15, 19), (13, 20))


@icona("stampa", "File e documenti", "stampa stampante")
def _(g):
    g.L((7, 9), (7, 3), (17, 3), (17, 9)), g.R(3, 9, 18, 8, 2), g.L((7, 14), (17, 14), (17, 21), (7, 21), (7, 14))
    g.D(18, 12, 0.9)


@icona("file", "File e documenti", "file pagina vuoto")
def _(g):
    pagina(g)


@icona("documento", "File e documenti", "documento testo pagina")
def _(g):
    pagina(g), riga_testo(g, 12, 9, 16), riga_testo(g, 15.5, 9, 16), riga_testo(g, 19, 9, 13)


@icona("documenti", "File e documenti", "documenti copie pagine")
def _(g):
    g.L((9, 3), (16, 3), (20, 7), (20, 17), (9, 17), (9, 3)), g.L((16, 3), (16, 7), (20, 7))
    g.L((5, 7), (5, 21), (15, 21))


@icona("esporta", "File e documenti", "esporta esci condividi freccia fuori")
def _(g):
    g.L((9, 8), (5, 8), (5, 21), (19, 21), (19, 8), (15, 8)), freccia(g, 12, 15, 12, 3)


@icona("importa", "File e documenti", "importa entra freccia dentro")
def _(g):
    g.L((9, 8), (5, 8), (5, 21), (19, 21), (19, 8), (15, 8)), freccia(g, 12, 3, 12, 15)


@icona("scarica", "File e documenti", "scarica download")
def _(g):
    freccia(g, 12, 3, 12, 15), g.L((4, 15), (4, 20), (20, 20), (20, 15))


@icona("carica", "File e documenti", "carica upload")
def _(g):
    freccia(g, 12, 15, 12, 3), g.L((4, 15), (4, 20), (20, 20), (20, 15))


@icona("allegato", "File e documenti", "allegato graffetta")
def _(g):
    g.L((8, 12), (14.5, 5.5), (18.5, 9.5), (9, 19), (5, 15), (13, 7))


@icona("archivio", "File e documenti", "archivio scatola")
def _(g):
    g.R(3, 4, 18, 5, 1), g.L((5, 9), (5, 20), (19, 20), (19, 9)), g.L((10, 13), (14, 13))


# ================================================================== Modifica
@icona("copia", "Modifica", "copia duplica")
def _(g):
    g.R(8, 8, 13, 13, 2), g.L((16, 8), (16, 5), (5, 5), (5, 16), (8, 16))


@icona("taglia", "Modifica", "taglia forbici")
def _(g):
    g.C(6.5, 17, 3), g.C(17.5, 17, 3), g.L((8.5, 14.5), (17, 3)), g.L((15.5, 14.5), (7, 3))


@icona("incolla", "Modifica", "incolla appunti")
def _(g):
    g.L((9, 5), (6, 5), (6, 21), (18, 21), (18, 5), (15, 5)), g.R(9, 3, 6, 4, 1.5)
    riga_testo(g, 12, 9, 15), riga_testo(g, 16, 9, 15)


@icona("annulla", "Modifica", "annulla indietro undo")
def _(g):
    g.L((9, 5), (4, 10), (9, 15)), g.L((4, 10), (14, 10)), g.A(14, 15, 5, -90, 90)


@icona("ripeti", "Modifica", "ripeti avanti redo")
def _(g):
    g.L((15, 5), (20, 10), (15, 15)), g.L((20, 10), (10, 10)), g.A(10, 15, 5, 90, 270)


@icona("elimina", "Modifica", "elimina cestino cancella")
def _(g):
    g.L((4, 6), (20, 6)), g.L((9, 6), (9, 3), (15, 3), (15, 6)), g.L((6, 6), (7, 21), (17, 21), (18, 6))
    g.L((10, 10), (10, 17)), g.L((14, 10), (14, 17))


@icona("matita", "Modifica", "matita modifica scrivi")
def _(g):
    g.Lc((4, 20), (5, 15), (16, 4), (20, 8), (9, 19)), g.L((13, 7), (17, 11))


@icona("pennello", "Modifica", "pennello disegna colore")
def _(g):
    g.L((20, 4), (11, 13)), g.L((9, 13), (13, 13), (13, 17), (7, 21), (4, 21), (5, 15), (9, 13))


@icona("grassetto", "Modifica", "grassetto bold testo")
def _(g):
    g.L((7, 4), (7, 20)), g.L((7, 4), (13, 4), (16, 6), (16, 10), (13, 12), (7, 12)), g.L((13, 12), (17, 14), (17, 18), (14, 20), (7, 20))


@icona("corsivo", "Modifica", "corsivo italic testo")
def _(g):
    g.L((10, 4), (18, 4)), g.L((6, 20), (14, 20)), g.L((14, 4), (10, 20))


@icona("sottolineato", "Modifica", "sottolineato underline testo")
def _(g):
    g.L((7, 4), (7, 12), (9, 16), (15, 16), (17, 12), (17, 4)), g.L((5, 21), (19, 21))


@icona("allinea_sinistra", "Modifica", "allinea sinistra testo")
def _(g):
    riga_testo(g, 5, 4, 20), riga_testo(g, 10, 4, 14), riga_testo(g, 15, 4, 20), riga_testo(g, 20, 4, 14)


@icona("allinea_centro", "Modifica", "allinea centro testo")
def _(g):
    riga_testo(g, 5, 4, 20), riga_testo(g, 10, 7, 17), riga_testo(g, 15, 4, 20), riga_testo(g, 20, 7, 17)


@icona("allinea_destra", "Modifica", "allinea destra testo")
def _(g):
    riga_testo(g, 5, 4, 20), riga_testo(g, 10, 10, 20), riga_testo(g, 15, 4, 20), riga_testo(g, 20, 10, 20)


@icona("elenco_puntato", "Modifica", "elenco puntato lista")
def _(g):
    for y in (6, 12, 18):
        g.D(5, y, 1.3), g.L((10, y), (20, y))


@icona("elenco_numerato", "Modifica", "elenco numerato lista numeri")
def _(g):
    for y in (6, 12, 18):
        g.L((4, y - 2), (5.5, y - 3.5), (5.5, y + 2)), g.L((10, y), (20, y))


@icona("tabella", "Modifica", "tabella celle griglia")
def _(g):
    g.R(3, 4, 18, 16, 2), g.L((3, 10), (21, 10)), g.L((3, 15), (21, 15)), g.L((10, 4), (10, 20))


@icona("righello", "Modifica", "righello misura")
def _(g):
    g.R(2, 8, 20, 8, 1.5)
    for x in (6, 10, 14, 18):
        g.L((x, 8), (x, 12))


# ================================================================== Frecce e navigazione
@icona("indietro", "Frecce", "indietro sinistra freccia")
def _(g):
    g.L((20, 12), (4, 12)), g.L((10, 6), (4, 12), (10, 18))


@icona("avanti", "Frecce", "avanti destra freccia")
def _(g):
    g.L((4, 12), (20, 12)), g.L((14, 6), (20, 12), (14, 18))


@icona("su", "Frecce", "su alto freccia")
def _(g):
    g.L((12, 20), (12, 4)), g.L((6, 10), (12, 4), (18, 10))


@icona("giu", "Frecce", "giù basso freccia")
def _(g):
    g.L((12, 4), (12, 20)), g.L((6, 14), (12, 20), (18, 14))


@icona("chevron_sinistra", "Frecce", "sinistra chevron indietro")
def _(g):
    g.L((15, 5), (8, 12), (15, 19))


@icona("chevron_destra", "Frecce", "destra chevron avanti")
def _(g):
    g.L((9, 5), (16, 12), (9, 19))


@icona("chevron_su", "Frecce", "su chevron")
def _(g):
    g.L((5, 15), (12, 8), (19, 15))


@icona("chevron_giu", "Frecce", "giù chevron")
def _(g):
    g.L((5, 9), (12, 16), (19, 9))


@icona("espandi", "Frecce", "espandi allarga ingrandisci")
def _(g):
    g.L((14, 4), (20, 4), (20, 10)), g.L((20, 4), (13, 11)), g.L((10, 20), (4, 20), (4, 14)), g.L((4, 20), (11, 13))


@icona("comprimi", "Frecce", "comprimi riduci")
def _(g):
    g.L((20, 10), (14, 10), (14, 4)), g.L((14, 10), (21, 3)), g.L((4, 14), (10, 14), (10, 20)), g.L((10, 14), (3, 21))


@icona("aggiorna", "Frecce", "aggiorna ricarica refresh")
def _(g):
    g.A(12, 12, 8, -30, 250), g.L((18, 3), (19.5, 7.5), (15, 9))


@icona("scambia", "Frecce", "scambia sposta swap")
def _(g):
    g.L((4, 8), (20, 8)), g.L((16, 4), (20, 8), (16, 12)), g.L((20, 16), (4, 16)), g.L((8, 12), (4, 16), (8, 20))


@icona("ordina", "Frecce", "ordina su giù")
def _(g):
    g.L((8, 20), (8, 4)), g.L((4, 8), (8, 4), (12, 8)), g.L((16, 4), (16, 20)), g.L((12, 16), (16, 20), (20, 16))


@icona("schermo_intero", "Frecce", "schermo intero fullscreen")
def _(g):
    g.L((4, 9), (4, 4), (9, 4)), g.L((15, 4), (20, 4), (20, 9)), g.L((20, 15), (20, 20), (15, 20)), g.L((9, 20), (4, 20), (4, 15))


@icona("esci", "Frecce", "esci logout uscita")
def _(g):
    g.L((10, 4), (4, 4), (4, 20), (10, 20)), freccia(g, 9, 12, 21, 12)


@icona("accedi", "Frecce", "accedi login entra")
def _(g):
    g.L((14, 4), (20, 4), (20, 20), (14, 20)), freccia(g, 3, 12, 15, 12)


# ================================================================== Interfaccia
@icona("home", "Interfaccia", "home casa pagina iniziale")
def _(g):
    g.L((3, 11), (12, 3), (21, 11)), g.L((6, 9), (6, 20), (18, 20), (18, 9)), g.L((10, 20), (10, 14), (14, 14), (14, 20))


@icona("menu", "Interfaccia", "menu hamburger")
def _(g):
    riga_testo(g, 6, 4, 20), riga_testo(g, 12, 4, 20), riga_testo(g, 18, 4, 20)


@icona("piu", "Interfaccia", "più aggiungi")
def _(g):
    g.L((12, 4), (12, 20)), g.L((4, 12), (20, 12))


@icona("meno", "Interfaccia", "meno togli")
def _(g):
    g.L((4, 12), (20, 12))


@icona("chiudi", "Interfaccia", "chiudi croce x")
def _(g):
    g.L((5, 5), (19, 19)), g.L((19, 5), (5, 19))


@icona("spunta", "Interfaccia", "spunta ok conferma")
def _(g):
    g.L((4, 13), (9, 18), (20, 6))


@icona("cerca", "Interfaccia", "cerca lente trova")
def _(g):
    g.C(10.5, 10.5, 6.5), g.L((15.5, 15.5), (21, 21))


@icona("zoom_piu", "Interfaccia", "zoom ingrandisci")
def _(g):
    g.C(10.5, 10.5, 6.5), g.L((15.5, 15.5), (21, 21)), g.L((10.5, 8), (10.5, 13)), g.L((8, 10.5), (13, 10.5))


@icona("zoom_meno", "Interfaccia", "zoom riduci")
def _(g):
    g.C(10.5, 10.5, 6.5), g.L((15.5, 15.5), (21, 21)), g.L((8, 10.5), (13, 10.5))


@icona("impostazioni", "Interfaccia", "impostazioni ingranaggio opzioni")
def _(g):
    ingranaggio(g)


@icona("regolazioni", "Interfaccia", "regolazioni cursori impostazioni")
def _(g):
    g.L((4, 7), (20, 7)), g.L((4, 17), (20, 17)), g.C(9, 7, 2.5), g.C(15, 17, 2.5)


@icona("filtro", "Interfaccia", "filtro imbuto")
def _(g):
    g.Lc((3, 4), (21, 4), (14, 12), (14, 20), (10, 18), (10, 12))


@icona("finestra", "Interfaccia", "finestra riquadro")
def _(g):
    g.R(3, 4, 18, 16, 2), g.L((3, 9), (21, 9)), g.D(6.5, 6.5, 0.8), g.D(9.5, 6.5, 0.8)


@icona("barra_laterale", "Interfaccia", "barra laterale pannello sinistra layout")
def _(g):
    g.R(3, 4, 18, 16, 2), g.L((9, 4), (9, 20))


@icona("pannello_basso", "Interfaccia", "pannello basso layout")
def _(g):
    g.R(3, 4, 18, 16, 2), g.L((3, 15), (21, 15))


@icona("griglia", "Interfaccia", "griglia riquadri")
def _(g):
    for x, y in ((4, 4), (14, 4), (4, 14), (14, 14)):
        g.R(x, y, 6, 6, 1.5)


@icona("elenco", "Interfaccia", "elenco righe lista")
def _(g):
    for y in (6, 12, 18):
        g.L((4, y), (6, y)), g.L((10, y), (20, y))


@icona("altro", "Interfaccia", "altro tre puntini orizzontali")
def _(g):
    for x in (5, 12, 19):
        g.D(x, 12, 1.6)


@icona("altro_verticale", "Interfaccia", "altro tre puntini verticali")
def _(g):
    for y in (5, 12, 19):
        g.D(12, y, 1.6)


@icona("aiuto", "Interfaccia", "aiuto domanda")
def _(g):
    g.C(12, 12, 9), g.L((9.5, 9.5), (10, 8), (12, 7), (14, 8), (14.5, 10), (12, 12), (12, 14)), g.D(12, 17, 1.1)


@icona("info", "Interfaccia", "informazioni info")
def _(g):
    g.C(12, 12, 9), g.L((12, 11), (12, 17)), g.D(12, 7.6, 1.1)


@icona("avviso", "Interfaccia", "avviso attenzione pericolo")
def _(g):
    g.Lc((12, 3.5), (22, 20.5), (2, 20.5)), g.L((12, 9.5), (12, 14.5)), g.D(12, 17.5, 1.1)


@icona("errore", "Interfaccia", "errore sbagliato")
def _(g):
    g.C(12, 12, 9), g.L((8.5, 8.5), (15.5, 15.5)), g.L((15.5, 8.5), (8.5, 15.5))


@icona("ok", "Interfaccia", "ok riuscito conferma")
def _(g):
    g.C(12, 12, 9), g.L((7.5, 12.5), (10.5, 15.5), (16.5, 8.5))


@icona("lucchetto", "Interfaccia", "lucchetto chiuso sicurezza")
def _(g):
    g.R(5, 10, 14, 11, 2), g.L((8, 10), (8, 7), (9.5, 4), (14.5, 4), (16, 7), (16, 10)), g.D(12, 15.5, 1.3)


@icona("lucchetto_aperto", "Interfaccia", "lucchetto aperto sblocca")
def _(g):
    g.R(5, 10, 14, 11, 2), g.L((8, 10), (8, 7), (9.5, 4), (14.5, 4), (16, 6)), g.D(12, 15.5, 1.3)


@icona("chiave", "Interfaccia", "chiave password")
def _(g):
    g.C(8, 15, 4.5), g.L((11.5, 11.5), (20, 3)), g.L((16, 7), (19, 10)), g.L((18, 5), (21, 8))


@icona("occhio", "Interfaccia", "occhio vedi mostra")
def _(g):
    g.L((2, 12), (6, 7), (12, 5), (18, 7), (22, 12), (18, 17), (12, 19), (6, 17), (2, 12)), g.C(12, 12, 3)


@icona("occhio_barrato", "Interfaccia", "occhio barrato nascondi")
def _(g):
    g.L((2, 12), (6, 7), (12, 5), (18, 7), (22, 12), (18, 17), (12, 19), (6, 17), (2, 12)), g.C(12, 12, 3), g.L((4, 20), (20, 4))


@icona("tag", "Interfaccia", "etichetta tag prezzo")
def _(g):
    g.Lc((3, 12), (12, 3), (21, 3), (21, 12), (12, 21)), g.D(16.5, 7.5, 1.4)


@icona("stella", "Interfaccia", "stella preferito")
def _(g):
    pts = []
    for i in range(10):
        r = 9 if i % 2 == 0 else 4
        a = math.radians(-90 + i * 36)
        pts.append((12 + r * math.cos(a), 12.5 + r * math.sin(a)))
    g.Lc(*pts)


@icona("cuore", "Interfaccia", "cuore mi piace")
def _(g):
    g.L((12, 20), (4, 12), (4, 8), (7, 5), (10, 5), (12, 8), (14, 5), (17, 5), (20, 8), (20, 12), (12, 20))


@icona("segnalibro", "Interfaccia", "segnalibro preferiti")
def _(g):
    g.Lc((6, 3), (18, 3), (18, 21), (12, 16), (6, 21))


@icona("bandiera", "Interfaccia", "bandiera segnala")
def _(g):
    g.L((5, 21), (5, 3)), g.L((5, 4), (19, 4), (16, 8.5), (19, 13), (5, 13))


@icona("posizione", "Interfaccia", "posizione segnaposto mappa")
def _(g):
    g.L((12, 21), (6, 13), (5, 9), (8, 4.5), (12, 3.5), (16, 4.5), (19, 9), (18, 13), (12, 21)), g.C(12, 9.5, 2.5)


@icona("link", "Interfaccia", "link collegamento catena")
def _(g):
    g.L((10, 14), (14, 10)), g.L((11, 7), (13, 5), (18, 5), (20, 7), (20, 10), (17, 13)), g.L((13, 17), (11, 19), (6, 19), (4, 17), (4, 14), (7, 11))


@icona("condividi", "Interfaccia", "condividi invia")
def _(g):
    g.C(18, 5.5, 2.5), g.C(6, 12, 2.5), g.C(18, 18.5, 2.5), g.L((8.2, 10.8), (15.8, 6.7)), g.L((8.2, 13.2), (15.8, 17.3))


# ================================================================== Comunicazione
@icona("mail", "Comunicazione", "mail posta lettera")
def _(g):
    g.R(3, 5, 18, 14, 2), g.L((3.5, 6.5), (12, 13), (20.5, 6.5))


@icona("telefono", "Comunicazione", "telefono chiama")
def _(g):
    g.L((6, 3), (9, 3), (10.5, 8), (8.5, 10), (13, 15), (15, 13.5), (20, 15), (20, 18), (17, 21), (9, 18), (4, 10), (3, 5), (6, 3))


@icona("chat", "Comunicazione", "chat messaggio fumetto")
def _(g):
    g.L((4, 4), (20, 4), (20, 16), (11, 16), (6, 21), (6, 16), (4, 16), (4, 4)), riga_testo(g, 9, 8, 16), riga_testo(g, 12.5, 8, 13)


@icona("campana", "Comunicazione", "campana notifica avviso")
def _(g):
    g.L((5, 17), (7, 15), (7, 10), (9, 6), (12, 5), (15, 6), (17, 10), (17, 15), (19, 17), (5, 17)), g.L((10, 20), (14, 20))


@icona("utente", "Comunicazione", "utente persona profilo")
def _(g):
    g.C(12, 8, 4), g.L((4, 21), (5, 16), (9, 14), (15, 14), (19, 16), (20, 21))


@icona("utenti", "Comunicazione", "utenti persone gruppo")
def _(g):
    g.C(9, 8, 3.5), g.L((2.5, 20), (3.5, 15), (7, 13.5), (11, 13.5), (14.5, 15), (15.5, 20)), g.A(16, 8, 3, -60, 120), g.L((17, 14), (20, 15), (21.5, 20))


@icona("globo", "Comunicazione", "globo mondo web internet")
def _(g):
    g.C(12, 12, 9), g.EA(12, 12, 4, 9), g.L((3, 12), (21, 12))


@icona("wifi", "Comunicazione", "wifi rete wireless")
def _(g):
    g.A(12, 18, 14, -135, -45), g.A(12, 18, 9, -135, -45), g.A(12, 18, 4.5, -135, -45), g.D(12, 19, 1.4)


@icona("nuvola", "Comunicazione", "nuvola cloud")
def _(g):
    g.A(8, 15, 4, 90, 270), g.A(12, 10, 5, 180, 360), g.A(17, 14, 5, -90, 90), g.L((8, 19), (17, 19)), g.L((8, 11), (9, 10))


@icona("nuvola_carica", "Comunicazione", "nuvola carica upload cloud")
def _(g):
    g.A(8, 15, 4, 90, 270), g.A(12, 10, 5, 180, 360), g.A(17, 14, 5, -90, 90), g.L((8, 19), (10, 19)), g.L((14, 19), (17, 19)), freccia(g, 12, 21, 12, 12)


# ================================================================== Media
@icona("play", "Media", "play avvia riproduci")
def _(g):
    g.Lc((7, 4), (19, 12), (7, 20))


@icona("pausa", "Media", "pausa ferma")
def _(g):
    g.L((8, 4), (8, 20)), g.L((16, 4), (16, 20))


@icona("stop", "Media", "stop interrompi")
def _(g):
    g.R(5, 5, 14, 14, 2)


@icona("avanti_veloce", "Media", "avanti veloce")
def _(g):
    g.Lc((3, 5), (12, 12), (3, 19)), g.Lc((12, 5), (21, 12), (12, 19))


@icona("indietro_veloce", "Media", "indietro veloce")
def _(g):
    g.Lc((21, 5), (12, 12), (21, 19)), g.Lc((12, 5), (3, 12), (12, 19))


@icona("registra", "Media", "registra rec")
def _(g):
    g.C(12, 12, 9), g.D(12, 12, 4.5)


@icona("volume", "Media", "volume audio altoparlante")
def _(g):
    g.Lc((3, 9), (7, 9), (12, 5), (12, 19), (7, 15), (3, 15)), g.A(12, 12, 5, -50, 50), g.A(12, 12, 9, -50, 50)


@icona("muto", "Media", "muto silenzio audio")
def _(g):
    g.Lc((3, 9), (7, 9), (12, 5), (12, 19), (7, 15), (3, 15)), g.L((16, 9), (21, 15)), g.L((21, 9), (16, 15))


@icona("musica", "Media", "musica nota")
def _(g):
    g.L((9, 18), (9, 5), (19, 3), (19, 16)), g.C(6.5, 18, 2.5), g.C(16.5, 16, 2.5)


@icona("video", "Media", "video film camera")
def _(g):
    g.R(3, 6, 12, 12, 2), g.Lc((15, 11), (21, 7), (21, 17), (15, 13))


@icona("immagine", "Media", "immagine foto paesaggio")
def _(g):
    g.R(3, 4, 18, 16, 2), g.C(8.5, 9.5, 1.8), g.L((4, 18), (10, 12), (14, 16), (17, 13), (21, 17))


@icona("fotocamera", "Media", "fotocamera foto scatta")
def _(g):
    g.L((3, 8), (7, 8), (9, 5), (15, 5), (17, 8), (21, 8), (21, 19), (3, 19), (3, 8)), g.C(12, 13, 3.5)


@icona("microfono", "Media", "microfono registra voce")
def _(g):
    g.R(9, 3, 6, 11, 3), g.A(12, 12, 7, 0, 180), g.L((12, 19), (12, 22))


@icona("schermo", "Media", "schermo monitor computer")
def _(g):
    g.R(3, 4, 18, 12, 2), g.L((9, 20), (15, 20)), g.L((12, 16), (12, 20))


@icona("cuffie", "Media", "cuffie audio ascolta")
def _(g):
    g.A(12, 13, 8, 180, 360), g.R(3.5, 13, 4, 7, 1.5), g.R(16.5, 13, 4, 7, 1.5)


# ================================================================== Sviluppo e dati
@icona("codice", "Sviluppo e dati", "codice programma parentesi")
def _(g):
    g.L((8, 6), (2, 12), (8, 18)), g.L((16, 6), (22, 12), (16, 18)), g.L((14, 4), (10, 20))


@icona("terminale", "Sviluppo e dati", "terminale console riga di comando")
def _(g):
    g.R(3, 4, 18, 16, 2), g.L((7, 9), (11, 12), (7, 15)), g.L((13, 15), (17, 15))


@icona("bug", "Sviluppo e dati", "bug errore insetto debug")
def _(g):
    g.R(8, 8, 8, 12, 4), g.L((9, 8), (9, 6), (11, 4)), g.L((15, 8), (15, 6), (13, 4)), g.L((8, 12), (4, 10)), g.L((16, 12), (20, 10))
    g.L((8, 16), (4, 18)), g.L((16, 16), (20, 18)), g.L((12, 10), (12, 19))


@icona("database", "Sviluppo e dati", "database dati archivio")
def _(g):
    g.EA(12, 6, 8, 3), g.L((4, 6), (4, 18)), g.L((20, 6), (20, 18)), g.EA(12, 12, 8, 3, 0, 180), g.EA(12, 18, 8, 3, 0, 180)


@icona("grafico_barre", "Sviluppo e dati", "grafico barre statistiche")
def _(g):
    g.L((3, 20), (21, 20)), g.R(5, 12, 3.5, 8, 1), g.R(10.2, 6, 3.5, 14, 1), g.R(15.5, 9, 3.5, 11, 1)


@icona("grafico_torta", "Sviluppo e dati", "grafico torta percentuale")
def _(g):
    g.C(12, 12, 9), g.L((12, 12), (12, 3)), g.L((12, 12), (19.5, 16.5))


@icona("grafico_linee", "Sviluppo e dati", "grafico linee andamento")
def _(g):
    g.L((3, 3), (3, 21), (21, 21)), g.L((6, 16), (10, 11), (14, 14), (20, 6))


@icona("server", "Sviluppo e dati", "server rack")
def _(g):
    g.R(3, 4, 18, 6, 1.5), g.R(3, 14, 18, 6, 1.5), g.D(7, 7, 1), g.D(7, 17, 1)


@icona("processore", "Sviluppo e dati", "processore cpu chip")
def _(g):
    g.R(6, 6, 12, 12, 2), g.R(10, 10, 4, 4, 0.5)
    for v in (9, 15):
        g.L((v, 3), (v, 6)), g.L((v, 18), (v, 21)), g.L((3, v), (6, v)), g.L((18, v), (21, v))


@icona("disco", "Sviluppo e dati", "disco hard disk memoria")
def _(g):
    g.R(3, 6, 18, 12, 2), g.L((3, 14), (21, 14)), g.D(17, 16.2, 0.9)


@icona("spina", "Sviluppo e dati", "spina plugin corrente")
def _(g):
    g.L((9, 3), (9, 8)), g.L((15, 3), (15, 8)), g.L((6, 8), (18, 8), (18, 13), (12, 18), (6, 13), (6, 8)), g.L((12, 18), (12, 21))


@icona("lampadina", "Sviluppo e dati", "lampadina idea")
def _(g):
    g.A(12, 10, 6.5, 140, 400), g.L((9, 17), (15, 17)), g.L((10, 20), (14, 20)), g.L((9.5, 14), (9.5, 17)), g.L((14.5, 14), (14.5, 17))


@icona("razzo", "Sviluppo e dati", "razzo lancia avvia")
def _(g):
    g.L((12, 3), (16, 8), (16, 15), (8, 15), (8, 8), (12, 3)), g.L((8, 12), (5, 15), (5, 18), (8, 16)), g.L((16, 12), (19, 15), (19, 18), (16, 16))
    g.C(12, 9.5, 1.5), g.L((10.5, 18), (10.5, 21)), g.L((13.5, 18), (13.5, 20))


@icona("calcolatrice", "Sviluppo e dati", "calcolatrice calcola")
def _(g):
    g.R(5, 3, 14, 18, 2), g.R(8, 6, 8, 3, 0.5)
    for x in (9, 12, 15):
        for y in (13, 17):
            g.D(x, y, 0.9)


@icona("pacchetto", "Sviluppo e dati", "pacchetto scatola modulo")
def _(g):
    g.Lc((12, 3), (20, 7.5), (20, 16.5), (12, 21), (4, 16.5), (4, 7.5)), g.L((4, 7.5), (12, 12), (20, 7.5)), g.L((12, 12), (12, 21))


@icona("puzzle", "Sviluppo e dati", "puzzle estensione componente")
def _(g):
    g.L((4, 9), (9, 9), (9, 6), (11, 4), (13, 6), (13, 9), (18, 9), (18, 13), (20, 13), (21.5, 15), (20, 17), (18, 17), (18, 21), (4, 21), (4, 9))


@icona("forbici_codice", "Sviluppo e dati", "ramo git versioni")
def _(g):
    g.C(7, 5.5, 2.2), g.C(7, 18.5, 2.2), g.C(17, 9, 2.2), g.L((7, 7.7), (7, 16.3)), g.L((17, 11.2), (17, 12), (12, 14), (7, 15))


# ================================================================== Oggetti e vita quotidiana
@icona("orologio", "Oggetti", "orologio tempo ora")
def _(g):
    g.C(12, 12, 9), g.L((12, 7), (12, 12), (16, 14))


@icona("calendario", "Oggetti", "calendario data giorno")
def _(g):
    g.R(3, 5, 18, 16, 2), g.L((3, 10), (21, 10)), g.L((8, 3), (8, 7)), g.L((16, 3), (16, 7)), g.D(8, 14, 1), g.D(12, 14, 1), g.D(16, 14, 1), g.D(8, 17.5, 1)


@icona("batteria", "Oggetti", "batteria energia carica")
def _(g):
    g.R(3, 7, 16, 10, 2), g.L((21, 10.5), (21, 13.5)), g.L((6.5, 10.5), (6.5, 13.5)), g.L((10, 10.5), (10, 13.5))


@icona("carrello", "Oggetti", "carrello spesa acquisti")
def _(g):
    g.L((2, 4), (5, 4), (7, 15), (19, 15), (21, 7), (6, 7)), g.D(9, 19, 1.5), g.D(17, 19, 1.5)


@icona("borsa", "Oggetti", "borsa valigetta lavoro")
def _(g):
    g.R(3, 8, 18, 12, 2), g.L((9, 8), (9, 5), (15, 5), (15, 8)), g.L((3, 13), (21, 13))


@icona("regalo", "Oggetti", "regalo pacco dono")
def _(g):
    g.R(4, 10, 16, 10, 1.5), g.R(3, 7, 18, 3.5, 1), g.L((12, 7), (12, 20)), g.L((12, 7), (8, 4), (7, 6), (12, 7)), g.L((12, 7), (16, 4), (17, 6), (12, 7))


@icona("mappa", "Oggetti", "mappa cartina percorso")
def _(g):
    g.Lc((3, 6), (9, 4), (15, 6), (21, 4), (21, 18), (15, 20), (9, 18), (3, 20)), g.L((9, 4), (9, 18)), g.L((15, 6), (15, 20))


@icona("sole", "Oggetti", "sole giorno chiaro tema")
def _(g):
    g.C(12, 12, 4)
    for i in range(8):
        a = math.radians(i * 45)
        g.L((12 + 7 * math.cos(a), 12 + 7 * math.sin(a)), (12 + 9.5 * math.cos(a), 12 + 9.5 * math.sin(a)))


@icona("luna", "Oggetti", "luna notte scuro tema")
def _(g):
    g.EA(12, 12, 9, 9, 50, 310), g.EA(16, 12, 7.1, 7.1, 75.4, 284.6)


@icona("fulmine", "Oggetti", "fulmine veloce energia")
def _(g):
    g.Lc((13, 3), (5, 13), (11, 13), (10, 21), (19, 10), (13, 10))


@icona("fuoco", "Oggetti", "fuoco fiamma caldo")
def _(g):
    g.L((12, 21), (6, 17), (5, 12), (8, 8), (9, 10), (11, 4), (15, 8), (18, 13), (17, 18), (12, 21)), g.L((12, 17), (10, 14), (12, 12), (14, 15), (12, 17))


@icona("trofeo", "Oggetti", "trofeo premio coppa")
def _(g):
    g.L((7, 4), (17, 4), (17, 10), (14, 13), (10, 13), (7, 10), (7, 4)), g.L((7, 6), (3, 6), (4, 10), (7, 11)), g.L((17, 6), (21, 6), (20, 10), (17, 11))
    g.L((12, 13), (12, 17)), g.L((8, 20), (16, 20)), g.L((9, 17), (15, 17))


@icona("scudo", "Oggetti", "scudo protezione sicurezza")
def _(g):
    g.L((12, 3), (20, 6), (20, 12), (17, 17), (12, 21), (7, 17), (4, 12), (4, 6), (12, 3))


@icona("ingranaggi", "Oggetti", "strumenti attrezzi chiave inglese")
def _(g):
    g.L((15, 3), (19, 3), (21, 5), (21, 9), (18, 10), (6, 21), (3, 18), (14, 6), (15, 3))


@icona("casa_lavoro", "Oggetti", "edificio azienda ufficio")
def _(g):
    g.R(5, 3, 14, 18, 1.5), g.L((9, 8), (9, 8)), g.D(9, 8, 1), g.D(15, 8, 1), g.D(9, 12, 1), g.D(15, 12, 1), g.L((10.5, 21), (10.5, 17), (13.5, 17), (13.5, 21))


@icona("libro", "Oggetti", "libro guida leggi")
def _(g):
    g.L((12, 6), (7, 4), (3, 4), (3, 18), (7, 18), (12, 20), (17, 18), (21, 18), (21, 4), (17, 4), (12, 6)), g.L((12, 6), (12, 20))


@icona("laurea", "Oggetti", "cappello laurea studio scuola")
def _(g):
    g.Lc((12, 5), (22, 10), (12, 15), (2, 10)), g.L((6, 12.5), (6, 17), (12, 20), (18, 17), (18, 12.5)), g.L((22, 10), (22, 16))


# ------------------------------------------------------------------ versione a colori
# Ogni categoria ha il suo colore; alcune icone hanno quello che «ci si aspetta» (cestino rosso, spunta verde, cartella gialla...).
# Le parti chiuse (dentro i contorni) si riempiono con lo stesso colore, più tenue.
COLORI_CATEGORIA = {
    "File e documenti": (59, 130, 246),
    "Modifica": (139, 92, 246),
    "Frecce": (20, 184, 166),
    "Interfaccia": (99, 102, 241),
    "Comunicazione": (14, 165, 233),
    "Media": (236, 72, 153),
    "Sviluppo e dati": (16, 185, 129),
    "Oggetti": (249, 115, 22),
}
COLORI_NOME = {
    "apri": (245, 158, 11), "cartella": (245, 158, 11), "cartella_nuova": (245, 158, 11), "archivio": (180, 120, 60),
    "elimina": (239, 68, 68), "errore": (239, 68, 68), "registra": (239, 68, 68), "stop": (239, 68, 68), "bug": (239, 68, 68), "cuore": (244, 63, 94),
    "fuoco": (249, 115, 22), "bandiera": (239, 68, 68), "occhio_barrato": (100, 116, 139),
    "spunta": (34, 197, 94), "ok": (34, 197, 94), "play": (34, 197, 94), "nuovo": (34, 197, 94), "piu": (34, 197, 94), "zoom_piu": (34, 197, 94),
    "avviso": (245, 158, 11), "stella": (250, 190, 20), "trofeo": (250, 190, 20), "lucchetto": (217, 119, 6), "lucchetto_aperto": (34, 197, 94),
    "campana": (245, 158, 11), "lampadina": (250, 190, 20), "sole": (250, 190, 20), "fulmine": (250, 190, 20), "chiave": (217, 119, 6),
    "info": (59, 130, 246), "aiuto": (59, 130, 246), "luna": (99, 102, 241), "meno": (239, 68, 68), "zoom_meno": (239, 68, 68),
    "salva": (59, 130, 246), "salva_come": (59, 130, 246), "stampa": (100, 116, 139), "impostazioni": (100, 116, 139), "regolazioni": (100, 116, 139),
    "ingranaggi": (100, 116, 139), "processore": (100, 116, 139), "disco": (100, 116, 139), "server": (100, 116, 139), "schermo": (100, 116, 139),
    "matita": (249, 115, 22), "pennello": (236, 72, 153), "mail": (59, 130, 246), "posizione": (239, 68, 68), "globo": (14, 165, 233),
    "grafico_barre": (34, 197, 94), "grafico_torta": (249, 115, 22), "grafico_linee": (59, 130, 246), "database": (14, 165, 233),
    "regalo": (236, 72, 153), "segnalibro": (239, 68, 68), "tag": (245, 158, 11), "libro": (59, 130, 246), "scudo": (34, 197, 94),
    "muto": (100, 116, 139), "spina": (34, 197, 94), "razzo": (239, 68, 68), "calendario": (239, 68, 68), "carrello": (34, 197, 94),
}


def a_colori(f, rgb):
    """L'icona nel suo colore, con l'interno delle forme chiuse (quello che il contorno non lascia raggiungere dall'esterno) riempito più tenue."""
    g = G(rgb + (255,))
    f(g)
    tratto = g.im
    maschera = tratto.split()[3].point(lambda v: 255 if v > 20 else 0)
    ImageDraw.floodfill(maschera, (0, 0), 128)
    interno = maschera.point(lambda v: 255 if v == 0 else 0)
    riempimento = Image.new("RGBA", tratto.size, rgb + (0,))
    riempimento.putalpha(interno.point(lambda v: 64 if v else 0))
    return Image.alpha_composite(riempimento, tratto).resize((DIM, DIM), Image.LANCZOS)


def main():
    assert len(ICONE) >= 100, len(ICONE)
    indice = []
    for nome, (categoria, parole, f) in sorted(ICONE.items(), key=lambda kv: (kv[1][0], kv[0])):
        for colore, suffisso in ((SCURO, ""), (CHIARO, "_chiaro")):
            g = G(colore)
            f(g)
            g.fine().save(os.path.join(QUI, f"{nome}{suffisso}.png"))
        a_colori(f, COLORI_NOME.get(nome, COLORI_CATEGORIA[categoria])).save(os.path.join(QUI, f"{nome}_colore.png"))
        indice.append({"nome": nome, "categoria": categoria, "parole": parole})
    with open(os.path.join(QUI, "indice.json"), "w", encoding="utf-8", newline="\n") as fo:
        json.dump(indice, fo, ensure_ascii=False, indent=1)
    print(len(indice), "icone")


if __name__ == "__main__":
    main()
