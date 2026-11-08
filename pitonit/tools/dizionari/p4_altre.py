"""Altre librerie comuni. I nomi di funzioni, metodi e costanti sono tradotti
in automatico dal glossario; qui si scelgono i nomi dei moduli e delle classi."""

MODULI = {
    "asincronia": dict(orig="asyncio", nomi="""
        esegui=run aspetta=sleep raccogli=gather crea_attivita=create_task
        attendi_per=wait_for in_filo=to_thread
        Ciclo=AbstractEventLoop Attivita=Task Futuro=Future
        Coda=Queue CodaLifo=LifoQueue CodaPriorita=PriorityQueue
        Blocco=Lock Evento=Event Semaforo=Semaphore Condizione=Condition
        ErroreTimeout=TimeoutError ErroreAnnullato=CancelledError
        garantisci_futuro=ensure_future man_mano_completati=as_completed
        attendi_tutti=wait ottieni_ciclo=get_event_loop
        nuovo_ciclo=new_event_loop imposta_ciclo=set_event_loop
        apri_connessione=open_connection avvia_server=start_server
        crea_sottoprocesso_shell=create_subprocess_shell
        crea_sottoprocesso=create_subprocess_exec
        LettoreFlusso=StreamReader ScrittoreFlusso=StreamWriter
        proteggi=shield
    """, tipi={
        "AbstractEventLoop": """esegui_fino_al_completamento=run_until_complete
            esegui_per_sempre=run_forever ferma=stop chiudi=close
            crea_attivita=create_task chiama_dopo=call_later
            chiama_presto=call_soon esegui_in_esecutore=run_in_executor""",
        "Task": "annulla=cancel è_completata=done risultato=result",
        "Future": """risultato=result imposta_risultato=set_result
            imposta_eccezione=set_exception è_completato=done
            annulla=cancel aggiungi_richiamo=add_done_callback""",
        "Queue": """inserisci=put ottieni=get inserisci_senza_attesa=put_nowait
            ottieni_senza_attesa=get_nowait dimensione=qsize
            attivita_completata=task_done attendi_completamento=join""",
    }),
    "esecutori": dict(orig="concurrent.futures", nomi="""
        EsecutoreFili=ThreadPoolExecutor EsecutoreProcessi=ProcessPoolExecutor
        Futuro=Future man_mano_completati=as_completed aspetta=wait
        ErroreTimeout=TimeoutError ErroreAnnullato=CancelledError
        PRIMO_COMPLETATO=FIRST_COMPLETED TUTTI_COMPLETATI=ALL_COMPLETED
        PRIMA_ECCEZIONE=FIRST_EXCEPTION Esecutore=Executor
    """, tipi={
        "Executor": "invia=submit mappa=map spegni=shutdown",
        "Future": """risultato=result eccezione=exception annulla=cancel
            è_completato=done è_annullato=cancelled in_esecuzione=running
            aggiungi_richiamo=add_done_callback""",
    }),
    "multiprocesso": dict(orig="multiprocessing", nomi="""
        Processo=Process GruppoProcessi=Pool Coda=Queue CodaSemplice=SimpleQueue
        Gestore=Manager conta_cpu=cpu_count Blocco=Lock Evento=Event
        Valore=Value ArrayCondiviso=Array Tubo=Pipe
        processo_corrente=current_process imposta_metodo_avvio=set_start_method
        sostegno_congelato=freeze_support Semaforo=Semaphore
    """, tipi={
        "Process": """avvia=start unisci=join termina=terminate è_vivo=is_alive
            uccidi=kill nome=name demone=daemon codice_uscita=exitcode pid=pid""",
    }, extra="""
from multiprocessing.pool import Pool as _Pool
alias_tipo(_Pool, {'mappa': 'map', 'mappa_stella': 'starmap',
    'applica_asincrono': 'apply_async', 'mappa_asincrona': 'map_async',
    'chiudi': 'close', 'unisci': 'join', 'termina': 'terminate',
    'mappa_non_ordinata': 'imap_unordered', 'mappa_pigra': 'imap'})
"""),
    "cronometro": dict(orig="timeit", nomi="misura=timeit ripeti=repeat contatore=default_timer Cronometro=Timer",
                       tipi={"Timer": "misura=timeit ripeti=repeat"},
                       opz="numero=number ripetizioni=repeat preparazione=setup istruzione=stmt",
                       extra="""
from _italiano import traduci_kw as _tr
misura = _tr(misura, _OPZ)
ripeti = _tr(ripeti, _OPZ)
"""),
    "albero_sintattico": dict(orig="ast", nomi="""
        analizza=parse scarica=dump valuta_letterale=literal_eval visita=walk
        VisitatoreNodi=NodeVisitor TrasformatoreNodi=NodeTransformer
        Nodo=AST ripara_posizioni=fix_missing_locations
        copia_posizione=copy_location ottieni_docstring=get_docstring
        ottieni_sorgente=get_source_segment annulla_analisi=unparse
    """),
    "analisi_comandi": dict(orig="shlex", nomi="separa=split proteggi=quote unisci=join Lessico=shlex"),
    "matematica_complessa": dict(orig="cmath", nomi="""
        radice_quadrata=sqrt fase=phase modulo_polare=polar
        da_polare=rect esponenziale=exp logaritmo=log
    """),
    "tipi_python": dict(orig="types", nomi="""
        SpazioNomiSemplice=SimpleNamespace TipoFunzione=FunctionType
        TipoMetodo=MethodType TipoModulo=ModuleType TipoGeneratore=GeneratorType
        TipoLambda=LambdaType TipoNessuno=NoneType
        ProxyMappaturaSolaLettura=MappingProxyType
        crea_classe=new_class
    """),
    "raccolta_rifiuti": dict(orig="gc", nomi="""
        raccogli=collect abilita=enable disabilita=disable
        è_abilitato=isenabled statistiche=get_stats
    """),
    "codifiche": dict(orig="codecs", nomi="""
        apri=open codifica=encode decodifica=decode cerca=lookup
        registra=register ottieni_codificatore=getencoder
        ottieni_decodificatore=getdecoder BOM_UTF8=BOM_UTF8
    """),
    "unicode_dati": dict(orig="unicodedata", nomi="""
        normalizza=normalize nome=name categoria=category
        cerca_nome=lookup numerico=numeric decimale=decimal
        direzione=bidirectional è_normalizzato=is_normalized
    """),
    "differenze": dict(orig="difflib", nomi="""
        ConfrontatoreSequenze=SequenceMatcher DifferenzaTesto=Differ
        differenze_unificate=unified_diff differenze_contesto=context_diff
        trova_simili=get_close_matches differenza_html=HtmlDiff
        confronta_righe=ndiff
    """, tipi={"SequenceMatcher": """rapporto=ratio rapporto_rapido=quick_ratio
        blocchi_corrispondenti=get_matching_blocks codici_operazione=get_opcodes
        imposta_sequenze=set_seqs"""}),
    "registro_windows": dict(orig="winreg", nomi="""
        apri_chiave=OpenKey crea_chiave=CreateKey chiudi_chiave=CloseKey
        leggi_valore=QueryValueEx scrivi_valore=SetValueEx
        elimina_valore=DeleteValue elimina_chiave=DeleteKey
        enumera_chiave=EnumKey enumera_valore=EnumValue
        CHIAVE_UTENTE_CORRENTE=HKEY_CURRENT_USER
        CHIAVE_MACCHINA_LOCALE=HKEY_LOCAL_MACHINE
        CHIAVE_RADICE_CLASSI=HKEY_CLASSES_ROOT TESTO=REG_SZ
        INTERO_32=REG_DWORD TESTO_ESPANDIBILE=REG_EXPAND_SZ
        ACCESSO_LETTURA=KEY_READ ACCESSO_SCRITTURA=KEY_WRITE
        ACCESSO_TUTTO=KEY_ALL_ACCESS
    """),
    "tipi_c.utilita": dict(orig="ctypes.util", nomi="trova_libreria=find_library"),
    "tipi_mime": dict(orig="mimetypes", nomi="""
        indovina_tipo=guess_type indovina_estensione=guess_extension
        indovina_tutte_estensioni=guess_all_extensions
        aggiungi_tipo=add_type inizializza=init
    """),
    "ftp": dict(orig="ftplib", nomi="Ftp=FTP FtpSicuro=FTP_TLS ErroreFtp=all_errors", tipi={
        "FTP": """accedi=login elenca_cartella=nlst elenco=dir
            cambia_cartella=cwd scarica_binario=retrbinary
            scarica_righe=retrlines invia_binario=storbinary
            invia_righe=storlines cancella=delete rinomina=rename
            crea_cartella=mkd rimuovi_cartella=rmd esci=quit chiudi=close
            cartella_corrente=pwd dimensione=size"""}),
    "sicurezza_ssl": dict(orig="ssl", nomi="""
        crea_contesto_predefinito=create_default_context ContestoSsl=SSLContext
        ErroreSsl=SSLError VERSIONE_OPENSSL=OPENSSL_VERSION
        richiedi_certificato=CERT_REQUIRED nessun_certificato=CERT_NONE
    """, tipi={"SSLContext": """avvolgi_presa=wrap_socket
        carica_catena_certificati=load_cert_chain
        carica_certificati_verifica=load_verify_locations
        imposta_protocolli=set_ciphers"""}),
    "indirizzi_ip": dict(orig="ipaddress", nomi="""
        indirizzo_ip=ip_address rete_ip=ip_network interfaccia_ip=ip_interface
        IndirizzoIPv4=IPv4Address IndirizzoIPv6=IPv6Address
        ReteIPv4=IPv4Network ReteIPv6=IPv6Network
    """),
    "archivio_tar": dict(orig="tarfile", nomi="""
        apri=open ArchivioTar=TarFile InfoTar=TarInfo è_tar=is_tarfile
        ErroreTar=TarError
    """, tipi={"TarFile": """aggiungi=add estrai_tutto=extractall estrai=extract
        elenco_nomi=getnames elenco_membri=getmembers ottieni_membro=getmember
        chiudi=close elenca=list"""}),
    "compressione_bz2": dict(orig="bz2", nomi="apri=open comprimi=compress decomprimi=decompress FileBz2=BZ2File"),
    "compressione_lzma": dict(orig="lzma", nomi="apri=open comprimi=compress decomprimi=decompress FileLzma=LZMAFile"),
    "archivio_chiave_valore": dict(orig="shelve", nomi="apri=open Archivio=Shelf"),
    "colori_conversioni": dict(orig="colorsys", nomi="""
        rgb_in_hsv=rgb_to_hsv hsv_in_rgb=hsv_to_rgb rgb_in_hls=rgb_to_hls
        hls_in_rgb=hls_to_rgb rgb_in_yiq=rgb_to_yiq yiq_in_rgb=yiq_to_rgb
    """),
    "tartaruga": dict(orig="turtle", nomi="""
        Tartaruga=Turtle Schermo=Screen TartarugaGrezza=RawTurtle
        avanti=forward indietro=backward sinistra=left destra=right
        alza_penna=penup abbassa_penna=pendown vai_a=goto colore=color
        colore_penna=pencolor colore_riempimento=fillcolor
        inizia_riempimento=begin_fill termina_riempimento=end_fill
        cerchio=circle velocita=speed ciclo_principale=mainloop
        spessore_penna=pensize nascondi_tartaruga=hideturtle
        mostra_tartaruga=showturtle cancella=clear reimposta=reset
        scrivi=write imposta_posizione=setpos imposta_direzione=setheading
        punto=dot timbro=stamp esci_al_clic=exitonclick
        imposta_sfondo=bgcolor titolo=title ascolta=listen
        al_tasto=onkey al_clic=onscreenclick dopo=ontimer posizione=position
        direzione=heading distanza=distance
    """, tipi={"RawTurtle": """avanti=forward indietro=backward
        sinistra=left destra=right alza_penna=penup abbassa_penna=pendown
        vai_a=goto colore=color cerchio=circle velocita=speed"""}),
    "test_documentazione": dict(orig="doctest", nomi="verifica_modulo=testmod verifica_file=testfile"),
    "registro.gestori": dict(orig="logging.handlers", nomi="""
        GestoreFileRotante=RotatingFileHandler
        GestoreFileOrario=TimedRotatingFileHandler GestoreSocket=SocketHandler
        GestoreSmtp=SMTPHandler GestoreHttp=HTTPHandler
        GestoreCoda=QueueHandler AscoltatoreCoda=QueueListener
        GestoreMemoria=MemoryHandler
    """),
    "posta.mime": dict(orig="email.mime.text", nomi="TestoMime=MIMEText"),
    "posta.mime_multiparte": dict(orig="email.mime.multipart", nomi="MultiparteMime=MIMEMultipart"),
    "posta.mime_base": dict(orig="email.mime.base", nomi="BaseMime=MIMEBase"),
    "posta.mime_immagine": dict(orig="email.mime.image", nomi="ImmagineMime=MIMEImage"),
    "posta.utilita": dict(orig="email.utils", nomi="""
        formatta_data=formatdate analizza_data=parsedate_to_datetime
        formatta_indirizzo=formataddr analizza_indirizzo=parseaddr
        crea_id_messaggio=make_msgid
    """),
    "xml_dom": dict(orig="xml.dom.minidom", nomi="analizza=parse analizza_testo=parseString Documento=Document"),
    "opzioni_riga_comando": dict(orig="getopt", nomi="analizza=getopt analizza_misto=gnu_getopt ErroreOpzione=GetoptError"),
    "interfaccia.trascina": dict(orig="tkinter.dnd", nomi="trascina_inizia=dnd_start"),
    "contesti_variabili": dict(orig="contextvars", nomi="""
        VariabileContesto=ContextVar copia_contesto=copy_context Contesto=Context
    """),
    "grafi": dict(orig="graphlib", nomi="OrdinatoreTopologico=TopologicalSorter ErroreCiclo=CycleError"),
    "installazione_python": dict(orig="sysconfig", nomi="ottieni_percorsi=get_paths ottieni_variabile_config=get_config_var"),
    "parole_chiave": dict(orig="keyword", nomi="""
        è_parola_chiave=iskeyword elenco_parole_chiave=kwlist
        elenco_parole_chiave_morbide=softkwlist
    """),
    "gettext_traduzioni": dict(orig="gettext", nomi="traduci=gettext installa=install"),
}
