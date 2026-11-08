"""Priorita' 2 (parte A): dati, testo, file, sistema."""

PONTE = lambda classe, mappa: f"from _italiano import ponte as _ponte\n_ponte(_ott(_orig, {classe!r}), {mappa!r})"

MODULI = {
    "tabelle_csv": dict(orig="csv", nomi="""
        lettore=reader scrittore=writer LettoreDizionario=DictReader
        ScrittoreDizionario=DictWriter CITA_MINIMO=QUOTE_MINIMAL
        CITA_TUTTO=QUOTE_ALL CITA_NON_NUMERICI=QUOTE_NONNUMERIC
        CITA_NESSUNO=QUOTE_NONE Dialetto=Dialect ErroreCsv=Error
        rileva_formato=Sniffer
    """, tipi={
        "DictWriter": "scrivi_intestazione=writeheader scrivi_riga=writerow scrivi_righe=writerows",
        "DictReader": "nomi_campi=fieldnames",
    }, extra="""
from io import StringIO as _SIO
alias_tipo(type(_orig.writer(_SIO())), {'scrivi_riga': 'writerow', 'scrivi_righe': 'writerows'})
"""),
    "registro": dict(orig="logging", nomi="""
        ottieni_registratore=getLogger configura_base=basicConfig
        DEBUG=DEBUG INFORMAZIONE=INFO AVVISO=WARNING ERRORE=ERROR CRITICO=CRITICAL
        informazione=info avviso=warning errore=error critico=critical
        eccezione=exception Registratore=Logger Gestore=Handler
        GestoreFlusso=StreamHandler GestoreFile=FileHandler
        Formattatore=Formatter Filtro=Filter ottieni_nome_livello=getLevelName
        spegni=shutdown
    """, tipi={
        "Logger": """informazione=info avviso=warning errore=error critico=critical
            eccezione=exception imposta_livello=setLevel
            aggiungi_gestore=addHandler rimuovi_gestore=removeHandler
            ottieni_figlio=getChild ha_gestori=hasHandlers registra=log
            è_abilitato_per=isEnabledFor""",
        "Handler": "imposta_formattatore=setFormatter imposta_livello=setLevel aggiungi_filtro=addFilter chiudi=close",
    }, opz="""
        livello=level formato=format nome_file=filename modo_file=filemode
        formato_data=datefmt gestori=handlers codifica=encoding forza=force
        flusso=stream
    """, kw=[], extra="""
from _italiano import traduci_kw as _tr
configura_base = _tr(configura_base, {
    'livello': 'level', 'formato': 'format', 'nome_file': 'filename',
    'modo_file': 'filemode', 'formato_data': 'datefmt', 'gestori': 'handlers',
    'codifica': 'encoding', 'forza': 'force', 'flusso': 'stream'})
from _italiano import ponte as _ponte
_ponte(_orig.Handler, {'emit': 'emetti'})
_ponte(_orig.Formatter, {'format': 'formatta'})
_ponte(_orig.Filter, {'filter': 'filtra'})
"""),
    "test_unitari": dict(orig="unittest", nomi="""
        CasoDiTest=TestCase principale=main SuiteDiTest=TestSuite
        CaricatoreTest=TestLoader EsecutoreTestTestuale=TextTestRunner
        salta=skip salta_se=skipIf salta_a_meno_che=skipUnless
        fallimento_atteso=expectedFailure
    """, tipi={
        "TestCase": """
            asserisci_uguale=assertEqual asserisci_diverso=assertNotEqual
            asserisci_vero=assertTrue asserisci_falso=assertFalse
            asserisci_è=assertIs asserisci_non_è=assertIsNot
            asserisci_nessuno=assertIsNone asserisci_non_nessuno=assertIsNotNone
            asserisci_in=assertIn asserisci_non_in=assertNotIn
            asserisci_istanza_di=assertIsInstance
            asserisci_non_istanza_di=assertNotIsInstance
            asserisci_solleva=assertRaises
            asserisci_solleva_regex=assertRaisesRegex
            asserisci_quasi_uguale=assertAlmostEqual
            asserisci_maggiore=assertGreater
            asserisci_maggiore_uguale=assertGreaterEqual
            asserisci_minore=assertLess asserisci_minore_uguale=assertLessEqual
            asserisci_regex=assertRegex
            asserisci_stessi_elementi=assertCountEqual
            asserisci_liste_uguali=assertListEqual
            asserisci_dizionari_uguali=assertDictEqual
            asserisci_tuple_uguali=assertTupleEqual
            asserisci_insiemi_uguali=assertSetEqual
            asserisci_testo_uguale=assertMultiLineEqual
            fallisci=fail salta_test=skipTest sotto_test=subTest
            aggiungi_pulizia=addCleanup
        """,
        "TextTestRunner": "esegui=run",
        "TestLoader": """carica_test_da_caso=loadTestsFromTestCase
            carica_test_da_modulo=loadTestsFromModule
            carica_test_da_nome=loadTestsFromName scopri=discover""",
        "TestResult": """test_eseguiti=@testsRun è_riuscito=wasSuccessful
            fallimenti=@failures errori=@errors saltati=@skipped""",
    }, opz="flusso=stream dettaglio=verbosity esci=exit argv=argv", kw=[
        (["TextTestRunner"], ["__init__"])], extra="""
from _italiano import traduci_kw as _tr
principale = _tr(principale, _OPZ)

from _italiano import ponte as _ponte
_ponte(_orig.TestCase, {'setUp': 'prepara', 'tearDown': 'smonta',
                        'setUpClass': 'prepara_classe', 'tearDownClass': 'smonta_classe'})
"""),
    "copia": dict(orig="copy", nomi="copia=copy copia_profonda=deepcopy ErroreCopia=Error"),
    "stringhe": dict(orig="string", nomi="""
        lettere_ascii=ascii_letters minuscole_ascii=ascii_lowercase
        maiuscole_ascii=ascii_uppercase cifre=digits punteggiatura=punctuation
        spazi=whitespace stampabili=printable
        cifre_esadecimali=hexdigits cifre_ottali=octdigits
        capitalizza_parole=capwords Modello=Template Formattatore=Formatter
    """, tipi={"Template": "sostituisci=substitute sostituisci_sicuro=safe_substitute"}),
    "impronte": dict(orig="hashlib", nomi="""
        nuovo=new algoritmi_disponibili=algorithms_available
        algoritmi_garantiti=algorithms_guaranteed impronta_file=file_digest
        pbkdf2_hmac=pbkdf2_hmac scrypt=scrypt blake2b=blake2b blake2s=blake2s
    """, extra="""
alias_tipo(type(_orig.md5()), {'aggiorna': 'update', 'digerisci': 'digest',
                               'digerisci_esadecimale': 'hexdigest', 'copia': 'copy'})
"""),
    "file_temporanei": dict(orig="tempfile", nomi="""
        crea_cartella_temporanea=mkdtemp crea_file_temporaneo=mkstemp
        FileTemporaneo=TemporaryFile FileTemporaneoConNome=NamedTemporaryFile
        CartellaTemporanea=TemporaryDirectory
        FileTemporaneoInMemoria=SpooledTemporaryFile
        cartella_temporanea=gettempdir
    """, tipi={"TemporaryDirectory": "pulisci=cleanup nome=@name"}),
    "calendario": dict(orig="calendar", nomi="""
        intervallo_mese=monthrange è_bisestile=isleap
        giorni_bisestili=leapdays mese_testo=month calendario_anno=calendar
        calendario_mese=monthcalendar giorno_settimana=weekday
        nomi_giorni=day_name nomi_giorni_brevi=day_abbr nomi_mesi=month_name
        nomi_mesi_brevi=month_abbr imposta_primo_giorno=setfirstweekday
        tempo_utc=timegm Calendario=Calendar CalendarioTesto=TextCalendar
        LUNEDI=MONDAY MARTEDI=TUESDAY MERCOLEDI=WEDNESDAY GIOVEDI=THURSDAY
        VENERDI=FRIDAY SABATO=SATURDAY DOMENICA=SUNDAY
    """),
    "cerca_file": dict(orig="glob", nomi="cerca=glob cerca_iterando=iglob proteggi=escape"),
    "statistica": dict(orig="statistics", nomi="""
        media=mean media_decimale=fmean media_geometrica=geometric_mean
        media_armonica=harmonic_mean mediana=median mediana_bassa=median_low
        mediana_alta=median_high moda=mode mode_multiple=multimode
        deviazione_standard_popolazione=pstdev deviazione_standard=stdev
        varianza_popolazione=pvariance varianza=variance quantili=quantiles
        correlazione=correlation covarianza=covariance
        regressione_lineare=linear_regression
        DistribuzioneNormale=NormalDist ErroreStatistica=StatisticsError
    """),
    "decimali": dict(orig="decimal", nomi="""
        Decimale=Decimal ottieni_contesto=getcontext imposta_contesto=setcontext
        contesto_locale=localcontext Contesto=Context
        ARROTONDA_MEZZO_SU=ROUND_HALF_UP ARROTONDA_MEZZO_PARI=ROUND_HALF_EVEN
        ARROTONDA_GIU=ROUND_DOWN ARROTONDA_SU=ROUND_UP
        ARROTONDA_VERSO_BASSO=ROUND_FLOOR ARROTONDA_VERSO_ALTO=ROUND_CEILING
        OperazioneNonValida=InvalidOperation
        DivisionePerZeroDecimale=DivisionByZero
    """, tipi={
        "Decimal": """quantizza=quantize normalizza=normalize
            come_tupla=as_tuple è_nan=is_nan è_finito=is_finite
            aggiusta=adjusted""",
        "Context": "precisione=prec arrotondamento=rounding",
    }),
    "frazioni": dict(orig="fractions", nomi="Frazione=Fraction", tipi={
        "Fraction": """numeratore=numerator denominatore=denominator
            limita_denominatore=limit_denominator come_rapporto=as_integer_ratio"""}),
    "enumerazioni": dict(orig="enum", nomi="""
        Enumerazione=Enum EnumerazioneIntera=IntEnum Bandiera=Flag
        BandieraIntera=IntFlag automatico=auto unico=unique
        EnumerazioneTesto=StrEnum
    """, tipi={"Enum": "nome=name valore=value"}),
    "classi_astratte": dict(orig="abc", nomi="""
        ClasseAstratta=ABC MetaClasseAstratta=ABCMeta
        metodo_astratto=abstractmethod
    """),
    "contesti": dict(orig="contextlib", nomi="""
        gestore_contesto=contextmanager chiudi_alla_fine=closing
        sopprimi=suppress reindirizza_uscita=redirect_stdout
        reindirizza_errori=redirect_stderr PilaUscite=ExitStack
        contesto_nullo=nullcontext
        gestore_contesto_asincrono=asynccontextmanager
    """),
    "traccia_errori": dict(orig="traceback", nomi="""
        stampa_pila=print_stack formatta_pila=format_stack
        estrai_traccia=extract_tb estrai_pila=extract_stack
        EccezioneTraccia=TracebackException percorri_traccia=walk_tb
    """, extra="""
import sys as _sys
from _italiano import traduci_errore as _t


def formatta_eccezione(*a, **k):
    return _t(_orig.format_exc(*a, **k))


def stampa_eccezione(*a, **k):
    _sys.stderr.write(formatta_eccezione())


def formatta_eccezione_completa(*a, **k):
    return [_t(r) for r in _orig.format_exception(*a, **k)]


def stampa_eccezione_completa(*a, **k):
    _sys.stderr.write("".join(formatta_eccezione_completa(*a, **k)))
"""),
    "coda": dict(orig="queue", nomi="""
        Coda=Queue CodaLifo=LifoQueue CodaPriorita=PriorityQueue
        CodaSemplice=SimpleQueue Vuota=Empty Piena=Full
    """, tipi={
        "Queue": """inserisci=put ottieni=get
            inserisci_senza_attesa=put_nowait ottieni_senza_attesa=get_nowait
            dimensione=qsize è_vuota=empty è_piena=full
            attività_completata=task_done attendi_completamento=join""",
        "SimpleQueue": """inserisci=put ottieni=get
            inserisci_senza_attesa=put_nowait ottieni_senza_attesa=get_nowait
            dimensione=qsize è_vuota=empty""",
    }),
    "flussi": dict(orig="io", nomi="""
        FlussoTesto=StringIO FlussoByte=BytesIO InvolucroTesto=TextIOWrapper
        apri=open INIZIO=SEEK_SET POSIZIONE=SEEK_CUR FINE=SEEK_END
    """, tipi={
        "StringIO": "ottieni_valore=getvalue",
        "BytesIO": "ottieni_valore=getvalue ottieni_buffer=getbuffer",
    }),
    "corrispondenza_nomi": dict(orig="fnmatch", nomi="""
        corrisponde=fnmatch corrisponde_maiuscole=fnmatchcase filtra=filter
        traduci=translate
    """),
    "testo_a_capo": dict(orig="textwrap", nomi="""
        a_capo=wrap rimuovi_rientro=dedent rientra=indent accorcia=shorten
        riempi=fill AccapoTesto=TextWrapper
    """),
    "identificatori": dict(orig="uuid", nomi="""
        uuid_casuale=uuid4 uuid_da_orario=uuid1 uuid_da_nome=uuid5 Uuid=UUID
    """, tipi={"UUID": "esadecimale=hex byte=bytes intero=int"}),
    "base64_testo": dict(orig="base64", nomi="""
        codifica_base64=b64encode decodifica_base64=b64decode
        codifica_base64_url=urlsafe_b64encode
        decodifica_base64_url=urlsafe_b64decode
        codifica_base32=b32encode decodifica_base32=b32decode
        codifica_base16=b16encode decodifica_base16=b16decode
    """),
    "segreti": dict(orig="secrets", nomi="""
        token_esadecimale=token_hex token_byte=token_bytes token_url=token_urlsafe
        scelta=choice casuale_sotto=randbelow confronta_sicuro=compare_digest
    """),
    "struttura_binaria": dict(orig="struct", nomi="""
        impacchetta=pack spacchetta=unpack dimensione_calcolata=calcsize
        impacchetta_in=pack_into spacchetta_da=unpack_from
        StrutturaBinaria=Struct ErroreStruttura=error
    """),
    "array_numerici": dict(orig="array", nomi="array=array codici_tipo=typecodes", tipi={
        "array": """aggiungi=append estendi=extend inserisci=insert
            estrai=pop rimuovi=remove inverti=reverse conta=count indice=index
            a_lista=tolist a_byte=tobytes da_lista=fromlist da_byte=frombytes
            codice_tipo=typecode"""}),
    "bisezione": dict(orig="bisect", nomi="""
        bisezione=bisect bisezione_sinistra=bisect_left bisezione_destra=bisect_right
        inserisci_ordinato=insort inserisci_ordinato_sinistra=insort_left
        inserisci_ordinato_destra=insort_right
    """),
    "mucchio": dict(orig="heapq", nomi="""
        inserisci=heappush estrai=heappop ordina_mucchio=heapify
        sostituisci=heapreplace inserisci_ed_estrai=heappushpop
        n_maggiori=nlargest n_minori=nsmallest unisci_ordinati=merge
    """),
    "operatori": dict(orig="operator", nomi="""
        ottieni_elemento=itemgetter ottieni_attributo=attrgetter
        chiama_metodo=methodcaller somma=add sottrai=sub moltiplica=mul
        dividi=truediv dividi_intero=floordiv modulo=mod nega=neg
        uguale=eq diverso=ne minore=lt minore_uguale=le maggiore=gt
        maggiore_uguale=ge contiene=contains potenza=pow
    """),
    "piattaforma": dict(orig="platform", nomi="""
        sistema=system nome_nodo=node rilascio=release versione=version
        macchina=machine processore=processor piattaforma=platform
        versione_python=python_version architettura=architecture
        informazioni_sistema=uname
    """),
    "password_utente": dict(orig="getpass", nomi="chiedi_password=getpass ottieni_utente=getuser"),
    "segnali": dict(orig="signal", nomi="""
        imposta_gestore=signal SEGNALE_INTERRUZIONE=SIGINT
        SEGNALE_TERMINAZIONE=SIGTERM SEGNALE_PREDEFINITO=SIG_DFL
        SEGNALE_IGNORA=SIG_IGN
    """),
    "configurazione": dict(orig="configparser", nomi="""
        AnalizzatoreConfigurazione=ConfigParser
        AnalizzatoreConfigurazioneGrezzo=RawConfigParser
        ErroreConfigurazione=Error
    """, tipi={
        "RawConfigParser": """leggi=read leggi_testo=read_string
            leggi_file=read_file sezioni=sections ha_sezione=has_section
            ha_opzione=has_option opzioni=options ottieni=get
            ottieni_intero=getint ottieni_decimale=getfloat
            ottieni_booleano=getboolean scrivi=write elementi=items
            rimuovi_sezione=remove_section rimuovi_opzione=remove_option
            imposta=set aggiungi_sezione=add_section""",
        "ConfigParser": "imposta=set aggiungi_sezione=add_section",
    }),
    "stampa_bella": dict(orig="pprint", nomi="""
        stampa_formattata=pprint formatta=pformat StampanteFormattata=PrettyPrinter
    """),
    "alla_chiusura": dict(orig="atexit", nomi="registra=register annulla_registrazione=unregister"),
    "compressione_gzip": dict(orig="gzip", nomi="""
        apri=open comprimi=compress decomprimi=decompress FileGzip=GzipFile
    """),
    "archivio_zip": dict(orig="zipfile", nomi="""
        ArchivioZip=ZipFile InfoZip=ZipInfo COMPRESSO=ZIP_DEFLATED
        NON_COMPRESSO=ZIP_STORED è_zip=is_zipfile ZipNonValido=BadZipFile
    """, tipi={
        "ZipFile": """estrai_tutto=extractall estrai=extract
            elenco_nomi=namelist elenco_info=infolist scrivi=write
            scrivi_testo=writestr leggi=read apri=open chiudi=close
            testa=testzip ottieni_info=getinfo""",
        "ZipInfo": """nome_file=filename dimensione_file=file_size
            dimensione_compressa=compress_size""",
    }),
    "serializza": dict(orig="pickle", nomi="""
        scarica=dump scarica_in_byte=dumps carica=load carica_da_byte=loads
        ErroreSerializzazione=PickleError PROTOCOLLO_MASSIMO=HIGHEST_PROTOCOL
        PROTOCOLLO_PREDEFINITO=DEFAULT_PROTOCOL
    """),
    "localizzazione": dict(orig="locale", nomi="""
        imposta_locale=setlocale ottieni_locale=getlocale
        formatta_stringa=format_string valuta=currency
        testo_a_decimale=atof testo_a_intero=atoi LC_TUTTO=LC_ALL
        LC_NUMERICO=LC_NUMERIC LC_MONETARIO=LC_MONETARY LC_TEMPO=LC_TIME
    """),
    "browser_web": dict(orig="webbrowser", nomi="""
        apri=open apri_nuova_scheda=open_new_tab apri_nuova_finestra=open_new
        ottieni=get registra=register
    """),
    "ispezione": dict(orig="inspect", nomi="""
        ottieni_membri=getmembers firma=signature è_funzione=isfunction
        è_classe=isclass è_metodo=ismethod è_modulo=ismodule
        ottieni_sorgente=getsource ottieni_documentazione=getdoc
        ottieni_file=getfile pila=stack frame_corrente=currentframe
        è_generatore=isgenerator è_coroutine=iscoroutine
    """),
    "tipi_annotazioni": dict(orig="typing", nomi="""
        Lista=List Dizionario=Dict Opzionale=Optional Unione=Union Qualsiasi=Any
        Richiamabile=Callable Tupla=Tuple Insieme=Set Iterabile=Iterable
        Iteratore=Iterator Sequenza=Sequence Mappatura=Mapping
        VariabileDiTipo=TypeVar Generico=Generic Protocollo=Protocol
        TuplaConNome=NamedTuple DizionarioTipizzato=TypedDict Letterale=Literal
        Finale=Final VariabileDiClasse=ClassVar converti_tipo=cast
        CONTROLLO_TIPI=TYPE_CHECKING SeStesso=Self Annotato=Annotated
        ottieni_suggerimenti_tipo=get_type_hints sovraccarico=overload
        NessunRitorno=NoReturn Generatore=Generator
    """),
    "albero_xml": dict(orig="xml.etree.ElementTree", nomi="""
        analizza=parse da_testo=fromstring in_testo=tostring Elemento=Element
        SottoElemento=SubElement AlberoXml=ElementTree ErroreXml=ParseError
        indenta=indent
    """, tipi={
        "Element": """trova=find trova_tutti=findall trova_testo=findtext
            itera=iter aggiungi=append rimuovi=remove ottieni=get imposta=set
            testo=text coda=tail etichetta=tag attributi=attrib""",
        "ElementTree": "radice=getroot scrivi=write trova=find trova_tutti=findall",
    }),
    "toml_lettura": dict(orig="tomllib", nomi="carica=load carica_testo=loads"),
    "fusi_orari": dict(orig="zoneinfo", nomi="FusoOrarioNominato=ZoneInfo fusi_disponibili=available_timezones"),
}
