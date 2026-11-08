"""Segnala parole chiave INGLESI (e True/False/None) usati per sbaglio in file .pit."""
import keyword, sys, tokenize, io
PERMESSE = {"in", "lambda"}
IT_KW = set("Falso Nessuno Vero e come asserisci asincrono attendi interrompi classe continua definisci elimina altrimenti_se altrimenti eccetto infine per da globale se importa è nonlocale non o passa solleva ritorna prova mentre con produci".split())
def controlla(p):
    n = 0
    prec = ""
    for t in tokenize.generate_tokens(io.StringIO(open(p, encoding="utf-8").read()).readline):
        if t.type == tokenize.NAME and t.string in IT_KW and (prec in (".", "definisci", "classe") or prec == "come" and t.string in ("e", "o") and False):
            print(f"{p}:{t.start[0]}: '{t.string}' usato come nome (e' una parola chiave italiana)")
            n += 1
        if t.type not in (tokenize.NL, tokenize.COMMENT):
            prec = t.string
        if t.type == tokenize.NAME and keyword.iskeyword(t.string) and t.string not in PERMESSE:
            # un attributo come .async o .print non e' un problema; qui solo parole riservate
            print(f"{p}:{t.start[0]}: '{t.string}'")
            n += 1
    return n
tot = sum(controlla(p) for p in sys.argv[1:])
sys.exit(1 if tot else 0)
