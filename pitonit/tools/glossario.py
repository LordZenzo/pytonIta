"""Glossario inglese -> italiano per la traduzione automatica dei nomi delle API.

Un nome come `get_current_value` viene diviso in parole (snake_case, camelCase),
ogni parola e' tradotta e il risultato e' ricomposto (`ottieni_valore_corrente`).
Se una parola non e' nel glossario il nome NON viene tradotto (e finisce nel
rapporto tools/non_tradotti.txt, dove si vede cosa aggiungere qui).
"""
import re

# parole singole (anche "incollate" come winfo, yview, columnconfigure)
G = {}


def _agg(testo):
    for parte in testo.split():
        en, _, it = parte.partition('=')
        G[en] = it


# --- verbi / azioni
_agg("""
get=ottieni set=imposta add=aggiungi remove=rimuovi delete=cancella del=cancella
create=crea make=crea new=nuovo open=apri close=chiudi read=leggi write=scrivi
load=carica save=salva dump=scarica store=memorizza fetch=recupera find=trova
search=cerca match=corrisponde replace=sostituisci insert=inserisci append=aggiungi
extend=estendi pop=estrai clear=svuota copy=copia move=sposta rename=rinomina
update=aggiorna reset=reimposta start=avvia stop=ferma run=esegui exec=esegui
execute=esegui call=chiama invoke=invoca send=invia recv=ricevi receive=ricevi
connect=connetti disconnect=disconnetti bind=associa unbind=dissocia
listen=ascolta accept=accetta check=controlla test=verifica validate=convalida
parse=analizza format=formatta convert=converti cast=converti encode=codifica
decode=decodifica compress=comprimi decompress=decomprimi sort=ordina
reverse=inverti shuffle=mescola filter=filtra map=mappa reduce=riduci
apply=applica join=unisci split=separa merge=unisci concat=concatena
group=raggruppa count=conta sum=somma mean=media median=mediana
draw=disegna paint=dipingi fill=riempi render=rendi show=mostra hide=nascondi
display=visualizza print=stampa log=registra warn=avvisa raise=solleva
throw=lancia catch=cattura handle=gestisci process=elabora wait=aspetta
sleep=dormi lock=blocca unlock=sblocca acquire=acquisisci release=rilascia
notify=notifica cancel=annulla abort=interrompi terminate=termina kill=uccidi
register=registra unregister=annulla_registrazione install=installa
uninstall=disinstalla import=importa export=esporta download=scarica
upload=carica_remoto request=richiesta respond=rispondi redirect=reindirizza
authenticate=autentica login=accedi logout=esci sign=firma verify=verifica
encrypt=cifra decrypt=decifra hash=impronta digest=digerisci
scale=scala rotate=ruota translate=trasla transpose=trasponi flip=capovolgi
crop=ritaglia resize=ridimensiona paste=incolla blend=fondi
select=seleziona deselect=deseleziona toggle=inverti focus=focus lift=porta_sopra
lower=porta_sotto raise_=solleva pack=impacchetta grid=griglia place=posiziona
configure=configura config=configura cget=ottieni_opzione
expand=espandi collapse=comprimi_vista scroll=scorri see=mostra
iterate=itera iter=itera enumerate=enumera walk=visita scan=scansiona
list=elenca ls=elenca dir=cartella glob=cerca rglob=cerca_ricorsivo
touch=tocca chmod=cambia_permessi chown=cambia_proprietario link=collega
unlink=scollega mkdir=crea_cartella rmdir=rimuovi_cartella makedirs=crea_cartelle
listdir=elenco_cartelle getcwd=cartella_corrente chdir=cambia_cartella
fork=biforca spawn=genera wrap=avvolgi unwrap=scarta_avvolgimento
dedent=rimuovi_rientro indent=rientra shorten=accorcia
seek=posiziona tell=posizione flush=svuota_buffer truncate=tronca
commit=conferma rollback=annulla_modifiche begin=inizia end=fine
bake=prepara build=costruisci compile=compila link_=collega
sample=campione choice=scelta choices=scelte randint=intero_casuale
seed=seme random=casuale uniform=uniforme gauss=gaussiana
normalize=normalizza quantize=quantizza round=arrotonda floor=pavimento
ceil=soffitto trunc=tronca clip=limita limit=limita
mark=segna unmark=smarca tag=tag untag=rimuovi_tag
undo=annulla redo=ripeti
""")

# --- sostantivi
_agg("""
name=nome names=nomi value=valore values=valori key=chiave keys=chiavi
item=elemento items=elementi element=elemento elements=elementi
entry=voce entries=voci field=campo fields=campi column=colonna columns=colonne
row=riga rows=righe cell=cella cells=celle table=tabella frame=riquadro
data=dati dict=dizionario dictionary=dizionario list_=lista tuple=tupla set_=insieme
array=array matrix=matrice vector=vettore index=indice indices=indici
size=dimensione length=lunghezza len=lunghezza width=larghezza height=altezza
depth=profondita shape=forma dim=dimensione dimension=dimensione dimensions=dimensioni
type=tipo types=tipi kind=genere mode=modalita level=livello
text=testo string=stringa str=testo char=carattere chars=caratteri
character=carattere word=parola words=parole line=linea lines=linee
byte=byte bytes=byte bit=bit bits=bit number=numero int=intero integer=intero
float=decimale double=doppio bool=booleano boolean=booleano
file=file files=file folder=cartella directory=cartella path=percorso
paths=percorsi parent=genitore parents=genitori child=figlio children=figli
root=radice base=base home=casa cwd=cartella_corrente tmp=temporaneo
temp=temporaneo stem=nome_senza_estensione suffix=suffisso suffixes=suffissi
extension=estensione ext=estensione drive=unita anchor=ancora part=parte
parts=parti stat=statistiche stats=statistiche info=informazioni
time=tempo date=data datetime=data_ora day=giorno days=giorni month=mese
months=mesi year=anno years=anni hour=ora hours=ore minute=minuto minutes=minuti
second=secondo seconds=secondi microsecond=microsecondo millisecond=millisecondo
timestamp=timestamp timezone=fuso_orario tz=fuso zone=zona week=settimana
weekday=giorno_settimana today=oggi now=adesso utc=utc local=locale
clock=orologio timer=timer timeout=tempo_massimo delay=ritardo interval=intervallo
duration=durata deadline=scadenza
object=oggetto objects=oggetti class=classe instance=istanza method=metodo
function=funzione func=funzione callback=richiamo handler=gestore hook=gancio
event=evento events=eventi signal=segnale error=errore errors=errori
exception=eccezione warning=avviso message=messaggio messages=messaggi
status=stato state=stato code=codice result=risultato results=risultati
output=output input=ingresso stdin=ingresso_standard stdout=uscita_standard
stderr=errore_standard stream=flusso buffer=buffer queue=coda stack=pila
heap=mucchio tree=albero node=nodo nodes=nodi graph=grafo edge=arco
window=finestra windows=finestre widget=widget widgets=widget button=pulsante
label=etichetta entry_=campo_testo canvas=tela menu=menu scrollbar=barra_scorrimento
listbox=elenco checkbutton=casella_selezione radiobutton=pulsante_opzione
scale_=cursore spinbox=campo_numerico toplevel=finestra_secondaria
screen=schermo display_=schermo monitor=monitor pixel=pixel pixels=pixel
color=colore colors=colori colour=colore background=sfondo foreground=primo_piano
font=carattere fonts=caratteri image=immagine images=immagini icon=icona
bitmap=bitmap cursor=cursore border=bordo margin=margine padding=imbottitura
pad=margine spacing=spaziatura align=allinea alignment=allineamento
justify=giustifica wrap_=a_capo side=lato fill_=riempimento sticky=aggancia
weight=peso
page=pagina pages=pagine sheet=foglio book=libro document=documento
paragraph=paragrafo section=sezione header=intestazione headers=intestazioni
footer=piede title=titolo subject=oggetto author=autore creator=creatore
keyword=parola_chiave keywords=parole_chiave template=modello style=stile
styles=stili theme=tema format_=formato pattern=modello regex=regex
group_=gruppo groups=gruppi span=intervallo start_=inizio stop_=fine
step=passo steps=passi begin_=inizio
url=url uri=uri host=host hostname=nome_host port=porta address=indirizzo
socket=presa server=server client=client connection=connessione
protocol=protocollo proxy=proxy cookie=cookie cookies=cookie session=sessione
user=utente users=utenti password=password token=token auth=autenticazione
login_=accesso account=account permission=permesso permissions=permessi
mode_=modalita owner=proprietario group__=gruppo
thread=filo threads=fili process=processo processes=processi pid=pid
task=attivita tasks=attivita worker=lavoratore pool=gruppo_lavoratori
job=lavoro daemon=demone barrier=barriera condition=condizione
semaphore=semaforo event_=evento
database=database db=database cursor_=cursore connection_=connessione
query=interrogazione statement=istruzione script=script schema=schema
record=record records=record table_=tabella view=vista index_=indice
row_=riga transaction=transazione savepoint=punto_di_salvataggio
version=versione platform=piattaforma system=sistema os=sistema_operativo
machine=macchina processor=processore architecture=architettura
environment=ambiente env=ambiente variable=variabile variables=variabili
argument=argomento arguments=argomenti args=argomenti kwargs=argomenti_con_nome
param=parametro params=parametri parameter=parametro parameters=parametri
option=opzione options=opzioni flag=bandiera flags=bandiere default=predefinito
defaults=predefiniti config_=configurazione setting=impostazione
settings=impostazioni property=proprieta attribute=attributo attributes=attributi
attr=attributo attrs=attributi member=membro members=membri
module=modulo modules=moduli package=pacchetto library=libreria lib=libreria
source=sorgente target=destinazione dest=destinazione destination=destinazione
origin=origine
source_=sorgente
content=contenuto contents=contenuti body=corpo payload=dati_trasportati
reason=motivo cause=causa context=contesto scope=ambito namespace=spazio_nomi
global_=globale locals=locali globals=globali
memory=memoria cache=cache pool_=gruppo storage=archivio disk=disco usage=uso
space=spazio free=libero total=totale used=usato capacity=capacita
count_=conteggio sum_=somma total_=totale average=media avg=media
min=minimo max=massimo minimum=minimo maximum=massimo range=intervallo
sequence=sequenza collection=collezione counter=contatore
random_=casuale number_=numero digit=cifra digits=cifre letter=lettera
letters=lettere punctuation=punteggiatura whitespace=spazi space_=spazio
tab=scheda tabs=schede newline=a_capo_riga
plot=traccia figure=figura axes=assi axis=asse subplot=sottografico
subplots=sottografici legend=legenda grid_=griglia tick=tacca ticks=tacche
xlabel=etichetta_x ylabel=etichetta_y zlabel=etichetta_z xlim=limiti_x
ylim=limiti_y zlim=limiti_z xticks=tacche_x yticks=tacche_y
xscale=scala_x yscale=scala_y xaxis=asse_x yaxis=asse_y bar=barre
barh=barre_orizzontali hist=istogramma histogram=istogramma
scatter=dispersione pie=torta boxplot=scatola_baffi imshow=mostra_immagine
colorbar=barra_colori cmap=mappa_colori marker=marcatore linestyle=stile_linea
linewidth=spessore_linea alpha=trasparenza
dataframe=tabella_dati series=serie groupby=raggruppa_per
frame_=riquadro csv=csv json=json xml=xml html=html pdf=pdf excel=excel
sql=sql sqlite=sqlite zip=zip gzip=gzip tar=tar
""")

# --- aggettivi / avverbi / preposizioni
_agg("""
is=è has=ha can=puo_essere with=con without=senza from=da to=in of=di
by=per in=in on=su at=a as=come and=e or=o not=non all=tutti any=qualsiasi
no=nessun none=nessuno only=solo also=anche if=se else=altrimenti
for=per while=mentre try=prova except=eccetto finally=infine
true=vero false=falso null=nullo nan=non_numero inf=infinito
pi=pigreco e_=nepero
current=corrente last=ultimo first=primo next=successivo prev=precedente
previous=precedente old=vecchio before=prima after=dopo
absolute=assoluto relative=relativo main=principale raw=grezzo
empty=vuoto full=completo partial=parziale sorted=ordinato
unique=unico valid=valido invalid=non_valido visible=visibile hidden=nascosto
active=attivo inactive=inattivo disabled=disabilitato enabled=abilitato
normal=normale selected=selezionato readonly=sola_lettura writable=scrivibile
readable=leggibile executable=eseguibile
left=sinistra right=destra top=alto bottom=basso center=centro centre=centro
middle=mezzo horizontal=orizzontale vertical=verticale
north=nord south=sud east=est west=ovest
upper=maiuscolo lower_=minuscolo title_=titolo capitalize=capitalizza
swapcase=inverti_maiuscole strip=elimina_spazi lstrip=elimina_spazi_sinistra
rstrip=elimina_spazi_destra startswith=inizia_con endswith=finisce_con
ljust=allinea_a_sinistra rjust=allinea_a_destra zfill=riempi_zeri
sync=sincrono async=asincrono blocking=bloccante nonblocking=non_bloccante
safe=sicuro unsafe=non_sicuro strict=rigido lazy=pigro eager=immediato
recursive=ricorsivo recursion=ricorsione deep=profondo shallow=superficiale
binary=binario hex=esadecimale octal=ottale decimal=decimale
signed=con_segno unsigned=senza_segno little=piccolo big=grande endian=endian
short=corto long=lungo wide=largo narrow=stretto
single=singolo multiple=multiplo multi=multi double_=doppio triple=triplo
simple=semplice complex=complesso
public=pubblico private=privato static=statico dynamic=dinamico
auto=automatico manual=manuale custom=personalizzato
internal=interno external=esterno
inline=in_linea
case=maiuscole_minuscole ignore=ignora insensitive=senza_distinzione
sensitive=con_distinzione
verbose=dettagliato quiet=silenzioso debug=debug info_=informazione
critical=critico fatal=fatale
required=obbligatorio optional=opzionale mandatory=obbligatorio
exact=esatto approximately=approssimativamente almost=quasi
equal=uguale equals=uguale same=stesso different=diverso
greater=maggiore less=minore larger=piu_grande smaller=piu_piccolo
between=tra inside=dentro outside=fuori above=sopra below=sotto
over=sopra under=sotto next_=successivo
many=molti one=uno two=due three=tre once=una_volta
again=ancora back=indietro forward=avanti up=su down=giu
out=fuori off=spento
up_=su
ok=ok yes=si no_=no cancel_=annulla retry=riprova abort_=interrompi
ask=chiedi askopenfilename=chiedi_file_da_aprire
asksaveasfilename=chiedi_file_da_salvare askdirectory=chiedi_cartella
askstring=chiedi_testo askinteger=chiedi_intero askfloat=chiedi_decimale
askyesno=chiedi_si_no askokcancel=chiedi_ok_annulla
askquestion=chiedi_domanda askretrycancel=chiedi_riprova_annulla
askyesnocancel=chiedi_si_no_annulla askcolor=chiedi_colore
showinfo=mostra_info showwarning=mostra_avviso showerror=mostra_errore
""")

# --- parole "incollate" tipiche di tkinter, matplotlib, pandas, reportlab
_agg("""
winfo=info_finestra wm=gestore_finestre mainloop=ciclo_principale
screenwidth=larghezza_schermo screenheight=altezza_schermo
reqwidth=larghezza_richiesta reqheight=altezza_richiesta
rootx=x_radice rooty=y_radice pointerx=puntatore_x pointery=puntatore_y
ismapped=e_mappata toplevel_=finestra_principale
columnconfigure=configura_colonna rowconfigure=configura_riga
propagate=propaga forget=dimentica info__=informazioni slaves=elementi
bbox=rettangolo_contenitore coords=coordinate itemconfigure=configura_elemento
itemconfig=configura_elemento itemcget=ottieni_opzione_elemento
withtag=con_tag overlapping=sovrapposti closest=piu_vicino
yview=scorri_y xview=scorri_x moveto=sposta_a scroll_=scorri
iconbitmap=icona_bitmap iconphoto=icona_foto iconify=riduci_a_icona
deiconify=ripristina withdraw=nascondi_finestra overrideredirect=senza_cornice
transient=transitoria protocol_=protocollo resizable=ridimensionabile
geometry=geometria minsize=dimensione_minima maxsize=dimensione_massima
attributes=attributi topmost=in_primo_piano fullscreen=schermo_intero
curselection=selezione_corrente activate=attiva nearest=piu_vicino
tag_config=configura_tag tagconfigure=configura_tag
sash=divisore post=mostra_a popup=popup tk=tk
grab=cattura_input focus_=focus idle=inattivo idletasks=compiti_inattivi
after=dopo cancel__=annulla bell=suono clipboard=appunti selection=selezione
option=opzione event_generate=genera_evento generate=genera
getvar=ottieni_variabile setvar=imposta_variabile trace=traccia
addtag=aggiungi_tag tagbind=associa_tag taglower=porta_sotto tagraise=porta_sopra
photoimage=immagine zoom=ingrandisci subsample=sottocampiona
drawstring=disegna_testo drawimage=disegna_immagine drawcentredstring=disegna_testo_centrato
showpage=nuova_pagina setfont=imposta_carattere stringwidth=larghezza_testo
setfillcolor=imposta_colore_riempimento setstrokecolor=imposta_colore_tratto
setlinewidth=imposta_spessore_linea rect=rettangolo circle=cerchio
ellipse=ellisse arc=arco savestate=salva_stato restorestate=ripristina_stato
pagesize=dimensione_pagina pagesizes=dimensioni_pagina
units=unita inch=pollice mm=mm cm=cm
loc=etichetta iloc=posizione at_=in_punto iat=in_posizione
fillna=riempi_nulli dropna=elimina_nulli isna=e_nullo notna=non_nullo
read_csv=leggi_csv to_csv=scrivi_csv
""")


_agg("""
dropdown=menu_a_tendina checkbox=casella editor=editor box=riquadro
edit=modifica transform=trasformazione remote=remoto ctrl=ctrl action=azione
redraw=ridisegna position=posizione command=comando layout=disposizione
identify=identifica drop=rilascia seq=sequenza msg=messaggio standard=standard
adjust=regola construct=costruisci motion=movimento spectrum=spettro
destroy=distruggi press=premi solve=risolvi offset=scostamento col=colonna
categories=categorie positions=posizioni closed=chiuso inset=incasso
tooltip=suggerimento boxes=riquadri compare=confronta order=ordine
highlight=evidenzia enter=entra mouse=mouse rgb=rgb named=con_nome use=usa
loop=ciclo dtype=tipo_dati displayed=visualizzato constraint=vincolo
enable=abilita basic=base prepare=prepara manager=gestore logical=logico
ratio=rapporto ordered=ordinato separator=separatore rotation=rotazione
report=rapporto put=inserisci modified=modificato angle=angolo
contains=contiene integrate=integra dpi=risoluzione math=matematica
arrowkey=tasto_freccia gamma=gamma factory=fabbrica response=risposta
rgba=rgba identity=identita power=potenza gen=genera fix=correggi arrow=freccia
extent=estensione indicate=indica secondary=secondario drag=trascina
bindings=associazioni heights=altezze monotonic=monotono variant=variante
break=interrompi have=ha leave=esci location=posizione tests=test
grouped=raggruppato locs=posizioni zorder=ordine_z device=dispositivo
encoding=codifica combine=combina trigger=attiva supported=supportato
geturl=ottieni_url formatter=formattatore widths=larghezze present=presente
mapping=mappatura integral=integrale filename=nome_file comment=commento
newwin=nuova_finestra inferred=dedotto labels=etichette interactive=interattivo
pick=scegli fontfamily=famiglia_carattere repr=rappresentazione
reserved=riservato large=grande unknown=sconosciuto broken=rotto help=aiuto
blue=blu eval=valuta flash=lampeggia icursor=posizione_cursore exists=esiste
head=testa divide=dividi python=python newtab=nuova_scheda sock=presa
take=prendi slice=fetta levels=livelli derivative=derivata magnitude=ampiezza
detach=stacca inheritable=ereditabile dst=ora_legale utcoffset=scostamento_utc
unpack=spacchetta entity=entita cleanup=pulisci real=reale priority=priorita
clone=clona normalized=normalizzato outline=contorno annotation=annotazione
skew=asimmetria cascade=cascata expose=esponi includes=include
transparency=trasparenza peer=pari success=successo invert=inverti
itemsize=dimensione_elemento tobytes=in_byte tolist=in_lista extra=extra
family=famiglia broadcast=trasmetti fast=veloce patch=toppa bad=errato
failed=fallito astype=come_tipo diagonal=diagonale isin=e_in ndim=dimensioni
repeat=ripeti binomial=binomiale exponential=esponenziale entropy=entropia
engine=motore factor=fattore contour=contorno contourf=contorno_pieno
quiver=campo_vettoriale loglog=log_log semilogx=semilog_x semilogy=semilog_y
hexbin=esagoni hlines=linee_orizzontali vlines=linee_verticali
violinplot=grafico_violino stackplot=grafico_impilato stairs=gradini
polar=polare spy=struttura autoscale=scala_automatica properties=proprieta
tight=compatto frameon=con_cornice filetypes=tipi_file antialiased=antialiasing
bounds=limiti click=clic mouseclick=clic_mouse binding=associazione
spans=intervalli remainder=resto unnamed=senza_nome coroutine=coroutine
symlink=collegamento_simbolico ctime=tempo_creazione gid=gid subtract=sottrai
parser=analizzatore locale=localizzazione iterable=iterabile init=inizializza
low=basso resolution=risoluzione strftime=formatta_tempo locked=bloccato
reindex=reindicizza progress=avanzamento description=descrizione
debuglevel=livello_debug zero=zero form=forma gradient=gradiente push=inserisci
dash=tratteggio legal=legale distance=distanza describe=descrivi
extended=esteso block=blocco fontname=nome_carattere fontsize=dimensione_carattere
face=faccia delta=delta extract=estrai sel=selezione getboolean=ottieni_booleano
getint=ottieni_intero getdouble=ottieni_decimale initialize=inizializza
visibility=visibilita coord=coordinata ranges=intervalli manage=gestisci
flat=piatto solid=solido delimiter=delimitatore emit=emetti validation=convalida
failure=fallimento fileno=descrittore readline=leggi_riga seekable=posizionabile
cssclass=classe_css xor=xor_ multiply=moltiplica peek=sbircia created=creato
ehlo=saluta quantile=quantile searchsorted=cerca_ordinato nbytes=byte_totali
dtypes=tipi_dati isnull=e_nullo argsort=indici_ordinati codes=codici
reorder=riordina snap=aggancia reader=lettore point=punto basis=base
quad=integra_quadratura picker=selettore pads=imbottiture limits=limiti
percentage=percentuale currently=attualmente formatting=formattazione
prefix=prefisso hooks=ganci orig=originale access=accesso dup=duplica
supports=supporta fromkeys=da_chiavi pos=posizione service=servizio high=alto
fromisoformat=da_isoformato corrupt=corrotto like=come formats=formati
literal=letterale boundary=confine linear=lineare kwds=argomenti_con_nome
green=verde light=chiaro keep=mantieni direction=direzione starttag=tag_iniziale
norm=norma force=forza components=componenti checksum=somma_controllo
skip=salta tcl=tcl enclosed=racchiuso tkraise=porta_in_primo_piano
circulate=circola hold=trattieni quit=esci own=proprio fraction=frazione
aspect=proporzioni iconname=nome_icona dialect=dialetto disable=disabilita
tear=strappa diff=differenza using=usando unused=inutilizzato
canonical=canonico exp=esponenziale minus=meno conjugate=coniugato
imag=immaginario continuous=continuo pickle=serializza exc=eccezione
byteswap=inverti_byte frombytes=da_byte tofile=in_file generator=generatore
varargs=argomenti_variabili annotations=annotazioni contiguous=contiguo
positional=posizionale membership=appartenenza gateway=gateway early=anticipato
found=trovato authentication=autenticazione unavailable=non_disponibile
extensions=estensioni charset=set_caratteri cumulative=cumulativo prod=prodotto
diag=diagonale mod=modulo negative=negativo roots=radici squeeze=comprimi_dimensioni
counts=conteggi beta=beta logistic=logistica
""")

AGGETTIVI_DOPO = {
    'corrente', 'predefinito', 'massimo', 'minimo', 'totale', 'completo',
    'relativo', 'assoluto', 'locale', 'globale', 'grezzo', 'vuoto',
    'principale', 'selezionato', 'attivo', 'visibile', 'nascosto',
    'valido', 'non_valido', 'unico', 'ordinato', 'opzionale',
    'obbligatorio', 'personalizzato', 'libero', 'normale', 'esterno',
    'interno', 'binario', 'esadecimale', 'ottale', 'sinistra', 'destra',
    'alto', 'basso', 'orizzontale', 'verticale', 'parziale', 'ricorsivo',
    'sicuro', 'rigido', 'dettagliato', 'singolo', 'multiplo', 'pubblico',
    'privato', 'statico', 'dinamico', 'automatico', 'manuale', 'sincrono',
    'asincrono', 'bloccante', 'disabilitato', 'abilitato', 'inattivo',
    'esatto', 'doppio', 'lungo', 'corto', 'semplice', 'complesso',
}

# parole che NON sono nomi (non vanno spostate dopo un aggettivo)
NON_NOMI = {
    'ottieni', 'imposta', 'aggiungi', 'rimuovi', 'elimina', 'crea', 'è', 'ha',
    'con', 'senza', 'da', 'in', 'di', 'per', 'su', 'a', 'come', 'e', 'o',
    'non', 'tra', 'dentro', 'fuori', 'sopra', 'sotto', 'solo', 'anche',
}

_RE_CAMEL = re.compile(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


def dividi(nome):
    """'getCurrentValue' / 'get_current_value' -> ['get', 'current', 'value']."""
    parti = []
    for pezzo in nome.split('_'):
        if not pezzo:
            continue
        for p in _RE_CAMEL.split(pezzo):
            parti.append(p.lower())
    return parti


def traduci_nome(nome):
    """Restituisce (nome_italiano, parole_sconosciute)."""
    token = dividi(nome)
    if not token:
        return None, []
    # prova prima il nome intero (es. 'askopenfilename')
    if nome.lower() in G and len(token) == 1:
        return G[nome.lower()], []
    ita, ignote = [], []
    i = 0
    while i < len(token):
        # prova coppie incollate (es. 'read'+'csv' -> read_csv)
        if i + 1 < len(token):
            coppia = token[i] + '_' + token[i + 1]
            if coppia in G:
                ita.append(G[coppia])
                i += 2
                continue
        t = token[i]
        if t == 'to' and i == len(token) - 1 and i > 0:
            ita.append('fino_a')
        elif t == 'from' and i == len(token) - 1 and i > 0:
            ita.append('da')
        elif i > 0 and t + '_' in G:          # dopo il verbo: forma "sostantivo"
            ita.append(G[t + '_'])
        elif t in G:
            ita.append(G[t])
        elif t + '_' in G:
            ita.append(G[t + '_'])
        elif t.isdigit():
            ita.append(t)
        else:
            ignote.append(t)
        i += 1
    if ignote:
        return None, ignote
    # sposta gli aggettivi dopo il nome che li segue
    k = 0
    while k < len(ita) - 1:
        if ita[k] in AGGETTIVI_DOPO and ita[k + 1] not in NON_NOMI \
                and ita[k + 1] not in AGGETTIVI_DOPO:
            ita[k], ita[k + 1] = ita[k + 1], ita[k]
            k += 2
        else:
            k += 1
    risultato = '_'.join(ita)
    return risultato, []
