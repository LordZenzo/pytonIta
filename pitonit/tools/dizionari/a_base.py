"""Moduli di base (math, random, time, sys, os, ...)."""

MODULI = {
    "matematica": dict(orig="math", nomi="""
        radice_quadrata=sqrt pigreco=pi numero_di_nepero=e tau=tau
        pavimento=floor soffitto=ceil seno=sin coseno=cos tangente=tan
        arcoseno=asin arcocoseno=acos arcotangente=atan arcotangente2=atan2
        seno_iperbolico=sinh coseno_iperbolico=cosh tangente_iperbolica=tanh
        logaritmo=log logaritmo_10=log10 logaritmo_2=log2 logaritmo_1_piu=log1p
        esponenziale=exp esponenziale_meno_1=expm1 fattoriale=factorial
        mcd=gcd mcm=lcm infinito=inf gradi=degrees radianti=radians
        valore_assoluto=fabs tronca=trunc ipotenusa=hypot distanza=dist
        potenza_decimale=pow combinazioni=comb permutazioni=perm
        è_nan=isnan è_infinito=isinf è_finito=isfinite è_vicino=isclose
        somma_esatta=fsum prodotto=prod radice_intera=isqrt resto=fmod
        copia_segno=copysign
    """),
    "casuale": dict(orig="random", nomi="""
        scelta=choice scelte=choices intero_casuale=randint
        intervallo_casuale=randrange mescola=shuffle campione=sample
        decimale_casuale=random uniforme=uniform imposta_seme=seed
        gaussiana=gauss normale=normalvariate triangolare=triangular
        bit_casuali=getrandbits byte_casuali=randbytes
    """),
    "tempo": dict(orig="time", nomi="""
        aspetta=sleep adesso=time orario_locale=localtime orario_utc=gmtime
        formatta_tempo=strftime analizza_tempo=strptime
        contatore_prestazioni=perf_counter contatore_monotono=monotonic
        ora_testo=ctime crea_tempo=mktime fuso_orario=timezone
        tempo_processo=process_time nanosecondi=time_ns
        struttura_tempo=struct_time
    """),
    "sistema": dict(orig="sys", nomi="""
        argomenti=argv percorso=path piattaforma=platform versione=version
        informazioni_versione=version_info ingresso_standard=stdin
        uscita_standard=stdout errore_standard=stderr moduli=modules
        eseguibile=executable ottieni_limite_ricorsione=getrecursionlimit
        imposta_limite_ricorsione=setrecursionlimit termina=exit
        dimensione_oggetto=getsizeof dimensione_massima=maxsize
        prefisso=prefix codifica_predefinita=getdefaultencoding
        eccezione_corrente=exc_info conteggio_riferimenti=getrefcount
        ordine_byte=byteorder
    """),
    "sistema_operativo": dict(orig="os", nomi="""
        cartella_corrente=getcwd cambia_cartella=chdir
        elenco_cartelle=listdir crea_cartella=mkdir crea_cartelle=makedirs
        rimuovi_file=remove rimuovi_cartella=rmdir
        rimuovi_cartelle=removedirs rinomina=rename sostituisci=replace
        ambiente=environ ottieni_ambiente=getenv imposta_ambiente=putenv
        separatore=sep separatore_percorsi=pathsep fine_riga=linesep
        nome_sistema=name esegui_comando=system
        scansiona=scandir visita=walk avvia_file=startfile
        ottieni_pid=getpid termina_processo=kill statistiche_file=stat
        conta_cpu=cpu_count dimensione_terminale=get_terminal_size
        file_nullo=devnull ottieni_utente=getlogin apri_descrittore=open
    """, extra="""
from . import percorso
alias_tipo(_orig.DirEntry, {'nome': 'name', 'percorso_completo': 'path',
    'è_file': 'is_file', 'è_cartella': 'is_dir', 'è_collegamento': 'is_symlink',
    'statistiche': 'stat'})
alias_tipo(type(_orig.stat('.')), {'dimensione': 'st_size', 'modifica_tempo': 'st_mtime',
    'creazione_tempo': 'st_ctime', 'accesso_tempo': 'st_atime', 'modalita': 'st_mode'})
"""),
    "sistema_operativo.percorso": dict(orig="os.path", nomi="""
        esiste=exists è_file=isfile è_cartella=isdir unisci=join
        dividi=split dividi_estensione=splitext nome_base=basename
        nome_cartella=dirname assoluto=abspath normalizza=normpath
        dimensione=getsize modifica_tempo=getmtime creazione_tempo=getctime
        espandi_utente=expanduser espandi_variabili=expandvars
        relativo=relpath è_assoluto=isabs percorso_reale=realpath
        è_collegamento=islink prefisso_comune=commonpath
        stesso_file=samefile dividi_unità=splitdrive
    """),
    "collezioni": dict(orig="collections", nomi="""
        contatore=Counter dizionario_ordinato=OrderedDict
        dizionario_predefinito=defaultdict coda_doppia=deque
        tupla_con_nome=namedtuple mappa_concatenata=ChainMap
    """, tipi={
        "Counter": "elementi=elements più_comuni=most_common sottrai=subtract totale=total",
        "deque": """aggiungi_a_destra=append aggiungi_a_sinistra=appendleft
                    estrai_da_destra=pop estrai_da_sinistra=popleft ruota=rotate
                    estendi_a_sinistra=extendleft""",
        "OrderedDict": "sposta_alla_fine=move_to_end",
    }),
    "percorso": dict(orig="pathlib", nomi="""
        Percorso=Path PercorsoPuro=PurePath PercorsoWindows=WindowsPath
    """, tipi={
        "PurePath": """nome=name suffisso=suffix suffissi=suffixes
            nome_senza_estensione=stem genitore=parent genitori=parents
            parti=parts unità=drive radice=root è_assoluto=is_absolute
            unisci_percorso=joinpath con_nome=with_name
            con_suffisso=with_suffix con_nome_senza_estensione=with_stem
            relativo_a=relative_to è_relativo_a=is_relative_to
            in_posix=as_posix corrisponde=match""",
        "Path": """esiste=exists è_file=is_file è_cartella=is_dir
            crea_cartella=mkdir leggi_testo=read_text scrivi_testo=write_text
            leggi_byte=read_bytes scrivi_byte=write_bytes apri=open
            elimina_file=unlink rimuovi_cartella=rmdir rinomina=rename
            sostituisci=replace elenca=iterdir cerca=glob
            cerca_ricorsivo=rglob statistiche=stat risolvi=resolve
            assoluto=absolute espandi_utente=expanduser casa=home
            cartella_corrente=cwd tocca=touch è_collegamento=is_symlink
            proprietario=owner visita=walk""",
    }),
    "espressioni_regolari": dict(orig="re", nomi="""
        cerca=search corrisponde=match corrisponde_tutto=fullmatch
        trova_tutti=findall trova_iterando=finditer sostituisci=sub
        sostituisci_conta=subn separa=split compila=compile
        proteggi=escape IGNORA_MAIUSCOLE=IGNORECASE MULTIRIGA=MULTILINE
        PUNTO_TUTTO=DOTALL VERBOSO=VERBOSE ERRORE=error
        Modello=Pattern Corrispondenza=Match
    """, tipi={
        "Pattern": """cerca=search corrisponde=match corrisponde_tutto=fullmatch
            trova_tutti=findall trova_iterando=finditer sostituisci=sub
            sostituisci_conta=subn separa=split""",
        "Match": """gruppo=group gruppi=groups dizionario_gruppi=groupdict
            inizio=start fine=end intervallo=span""",
    }),
    "funzioni_utili": dict(orig="functools", nomi="""
        riduci=reduce parziale=partial memorizza=lru_cache
        memorizza_tutto=cache confronto_a_chiave=cmp_to_key
        ordinamento_totale=total_ordering avvolgi=wraps
        aggiorna_avvolgimento=update_wrapper singolo_dispatch=singledispatch
        parziale_metodo=partialmethod proprietà_memorizzata=cached_property
    """),
    "iteratori": dict(orig="itertools", nomi="""
        catena=chain combinazioni=combinations
        combinazioni_con_ripetizione=combinations_with_replacement
        permutazioni=permutations prodotto_cartesiano=product ripeti=repeat
        accumula=accumulate ciclo=cycle conta=count fetta=islice
        zip_più_lungo=zip_longest raggruppa=groupby comprimi=compress
        prendi_mentre=takewhile salta_mentre=dropwhile
        copia_iteratore=tee mappa_stella=starmap a_coppie=pairwise
        a_blocchi=batched filtra_falsi=filterfalse
    """),
    "dati_classe": dict(orig="dataclasses", nomi="""
        classe_dati=dataclass campo=field campi=fields
        come_dizionario=asdict come_tupla=astuple sostituisci=replace
        è_classe_dati=is_dataclass
    """),
    "formato_json": dict(orig="json", nomi="""
        carica=load carica_testo=loads scarica=dump scarica_testo=dumps
        ErroreDecodificaJson=JSONDecodeError DecodificatoreJson=JSONDecoder
        CodificatoreJson=JSONEncoder
    """, extra="""
from _italiano import traduci_kw as _tr, ponte as _ponte
_O = {'rientro': 'indent', 'ordina_chiavi': 'sort_keys', 'solo_ascii': 'ensure_ascii',
      'predefinito': 'default', 'separatori': 'separators', 'hook_oggetto': 'object_hook',
      'classe': 'cls'}
for _n in ('scarica', 'scarica_testo', 'carica', 'carica_testo'):
    globals()[_n] = _tr(globals()[_n], _O)
_ponte(_orig.JSONEncoder, {'default': 'predefinito'})
"""),
}
