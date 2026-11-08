"""Priorita' 1 (escluso tkinter): ctypes, datetime, sqlite3, shutil, urllib,
threading, subprocess, argparse, requests, reportlab."""

MODULI = {
    # ------------------------------------------------------------- ctypes
    "tipi_c": dict(orig="ctypes", nomi="""
        dll_windows=windll dll_c=cdll LibreriaC=CDLL LibreriaWindows=WinDLL
                intero_c=c_int intero_senza_segno_c=c_uint lungo_c=c_long
        lungo_senza_segno_c=c_ulong corto_c=c_short
        corto_senza_segno_c=c_ushort byte_c=c_byte
        byte_senza_segno_c=c_ubyte carattere_c=c_char
        carattere_largo_c=c_wchar puntatore_testo_c=c_char_p
        puntatore_testo_largo_c=c_wchar_p puntatore_vuoto=c_void_p
        decimale_c=c_float doppio_c=c_double booleano_c=c_bool
        dimensione_c=c_size_t intero64_c=c_int64 intero64_senza_segno_c=c_uint64
        intero32_c=c_int32 intero32_senza_segno_c=c_uint32
        intero16_c=c_int16 intero16_senza_segno_c=c_uint16
        intero8_c=c_int8 intero8_senza_segno_c=c_uint8
        Struttura=Structure Unione=Union PUNTATORE=POINTER puntatore=pointer
        per_riferimento=byref dimensione_di=sizeof converti=cast
        crea_buffer_testo=create_string_buffer
        crea_buffer_unicode=create_unicode_buffer indirizzo_di=addressof
        sposta_memoria=memmove imposta_memoria=memset testo_a=string_at
        testo_largo_a=wstring_at TIPO_FUNZIONE_C=CFUNCTYPE
        TIPO_FUNZIONE_WINDOWS=WINFUNCTYPE ErroreArgomento=ArgumentError
        ultimo_errore=get_last_error imposta_ultimo_errore=set_last_error
        ErroreWindows=WinError formatta_errore=FormatError
        ottieni_ultimo_errore=GetLastError Array=Array dimensione_con_segno_c=c_ssize_t
    """),
    "tipi_c.windows": dict(orig="ctypes.wintypes", nomi="""
        MANIGLIA=HANDLE FINESTRA=HWND PAROLA=WORD DOPPIA_PAROLA=DWORD
        BOOLEANO=BOOL PUNTO=POINT RETTANGOLO=RECT LPARAM=LPARAM WPARAM=WPARAM
        ISTANZA=HINSTANCE MODULO=HMODULE MENU=HMENU ICONA=HICON
        PENNELLO=HBRUSH CONTESTO_DISPOSITIVO=HDC
        COSTANTE_TESTO=LPCWSTR COSTANTE_TESTO_C=LPCSTR LUNGO=LONG
        MESSAGGIO=MSG DIMENSIONE=SIZE INTERO_SENZA_SEGNO=UINT
    """),
    # ----------------------------------------------------------- datetime
    "data_ora": dict(orig="datetime", nomi="""
        Data=date OraData=datetime Ora=time Differenza=timedelta
        FusoOrario=timezone InfoFuso=tzinfo ANNO_MINIMO=MINYEAR
        ANNO_MASSIMO=MAXYEAR UTC=UTC
    """, tipi={
        "date": """oggi=today da_timestamp=fromtimestamp
            da_ordinale=fromordinal da_isoformato=fromisoformat
            da_calendario_iso=fromisocalendar sostituisci=replace
            formatta=strftime isoformato=isoformat
            giorno_settimana=weekday giorno_settimana_iso=isoweekday
            calendario_iso=isocalendar anno=year mese=month giorno=day
            ordinale=toordinal tupla_tempo=timetuple ctime=ctime
            minimo=min massimo=max""",
        "datetime": """adesso=now adesso_utc=utcnow combina=combine
            analizza=strptime ora=hour minuto=minute secondo=second
            microsecondo=microsecond ottieni_data=date ottieni_ora=time
            info_fuso=tzinfo in_fuso=astimezone timestamp=timestamp
            da_timestamp_utc=utcfromtimestamp""",
        "time": """ora=hour minuto=minute secondo=second
            microsecondo=microsecond isoformato=isoformat
            formatta=strftime sostituisci=replace""",
        "timedelta": """giorni=days secondi=seconds microsecondi=microseconds
            secondi_totali=total_seconds""",
    }),
    # ------------------------------------------------------------- sqlite3
    "database": dict(orig="sqlite3", nomi="""
        connetti=connect Connessione=Connection Cursore=Cursor Riga=Row
        ErroreDatabase=Error ErroreDiIntegrita=IntegrityError
        ErroreOperativo=OperationalError
        ErroreDiProgrammazione=ProgrammingError ErroreDiInterfaccia=InterfaceError
        ErroreDiDati=DataError versione_sqlite=sqlite_version versione=version
        registra_adattatore=register_adapter
        registra_convertitore=register_converter
        PARSE_TIPI_DICHIARATI=PARSE_DECLTYPES PARSE_NOMI_COLONNE=PARSE_COLNAMES
        completa_istruzione=complete_statement
    """, tipi={
        "Connection": """cursore=cursor esegui=execute esegui_molti=executemany
            esegui_script=executescript conferma=commit annulla=rollback
            chiudi=close crea_funzione=create_function
            crea_aggregato=create_aggregate totale_modifiche=total_changes
            copia_di_riserva=backup interrompi_query=interrupt
            in_transazione=in_transaction fabbrica_righe=row_factory
            scarica=iterdump fabbrica_testo=text_factory""",
        "Cursor": """esegui=execute esegui_molti=executemany
            esegui_script=executescript ottieni_uno=fetchone
            ottieni_molti=fetchmany ottieni_tutti=fetchall chiudi=close
            ultimo_id_riga=lastrowid numero_righe=rowcount
            descrizione=description dimensione_array=arraysize""",
        "Row": "chiavi=keys",
    }),
    # -------------------------------------------------------------- shutil
    "operazioni_file": dict(orig="shutil", nomi="""
        copia=copy copia_con_metadati=copy2 copia_contenuto=copyfileobj
        copia_file=copyfile copia_albero=copytree sposta=move
        elimina_albero=rmtree spazio_disco=disk_usage cerca_programma=which
        crea_archivio=make_archive estrai_archivio=unpack_archive
        dimensione_terminale=get_terminal_size copia_permessi=copymode
        copia_statistiche=copystat ErroreOperazioniFile=Error
        ignora_modelli=ignore_patterns cambia_proprietario=chown
    """),
    # -------------------------------------------------------------- urllib
    "rete_url": dict(orig="urllib", nomi=""),
    "rete_url.richiesta": dict(orig="urllib.request", nomi="""
        apri_url=urlopen Richiesta=Request costruisci_apri=build_opener
        scarica_in_file=urlretrieve installa_apri=install_opener
        GestoreProxy=ProxyHandler url_a_percorso=url2pathname
        percorso_a_url=pathname2url proxy_di_sistema=getproxies
    """, tipi={
        "Request": """aggiungi_intestazione=add_header ottieni_metodo=get_method
            ottieni_url=get_full_url ha_intestazione=has_header""",
    }),
    "rete_url.analisi": dict(orig="urllib.parse", nomi="""
        analizza_url=urlparse dividi_url=urlsplit unisci_url=urljoin
        codifica_url=quote codifica_url_piu=quote_plus
        decodifica_url=unquote decodifica_url_piu=unquote_plus
        codifica_parametri=urlencode analizza_query=parse_qs
        analizza_query_lista=parse_qsl componi_url=urlunparse
        rimuovi_frammento=urldefrag
    """),
    "rete_url.errori": dict(orig="urllib.error", nomi="""
        ErroreUrl=URLError ErroreHttp=HTTPError
        ErroreContenutoTroncato=ContentTooShortError
    """),
    # ----------------------------------------------------------- threading
    "thread": dict(orig="threading", nomi="""
        Filo=Thread Blocco=Lock Evento=Event Condizione=Condition
        Semaforo=Semaphore SemaforoLimitato=BoundedSemaphore
        Temporizzatore=Timer Barriera=Barrier locale=local
        filo_corrente=current_thread filo_principale=main_thread
        conta_attivi=active_count elenca_fili=enumerate
        identificatore=get_ident
    """, tipi={
        "Thread": """avvia=start unisci=join è_vivo=is_alive nome=name
            demone=daemon identificatore=ident""",
        "Lock": "acquisisci=acquire rilascia=release bloccato=locked",
        "Event": "imposta=set cancella=clear aspetta=wait è_impostato=is_set",
        "Condition": """acquisisci=@acquire rilascia=@release aspetta=wait
            notifica=notify notifica_tutti=notify_all
            attendi_condizione=wait_for""",
        "Semaphore": "acquisisci=acquire rilascia=release",
        "Timer": "annulla=cancel",
    }, extra="""
from _italiano import ponte as _ponte
_ponte(_orig.Thread, {'run': 'esegui'})
"""),
    # ---------------------------------------------------------- subprocess
    "processi": dict(orig="subprocess", nomi="""
        esegui=run Processo=Popen controlla_output=check_output
        controlla_chiamata=check_call chiama=call TUBO=PIPE
        USCITA_STANDARD=STDOUT NULLO=DEVNULL ErroreProcesso=CalledProcessError
        ErroreTimeoutProcesso=TimeoutExpired RisultatoProcesso=CompletedProcess
        ErroreSottoprocesso=SubprocessError
    """, tipi={
        "Popen": """aspetta=wait comunica=communicate termina=terminate
            uccidi=kill interroga=poll codice_ritorno=@returncode
            invia_segnale=send_signal pid=@pid""",
        "CompletedProcess": """codice_ritorno=@returncode output=@stdout
            errore=@stderr controlla_ritorno=check_returncode""",
    }, opz="""
        cattura_output=capture_output testo=text controlla=check
        cartella_lavoro=cwd tempo_massimo=timeout ambiente=env
        ingresso=input codifica=encoding ingresso_standard=stdin
        uscita_standard=stdout errore_standard=stderr argomenti=args
        nascondi_console=creationflags
    """, kw=[(["Popen"], ["__init__"])], extra="""
from _italiano import traduci_kw as _tr
for _n in ('esegui', 'controlla_output', 'controlla_chiamata', 'chiama'):
    globals()[_n] = _tr(globals()[_n], _OPZ)
"""),
    # ------------------------------------------------------------ argparse
    "argomenti": dict(orig="argparse", nomi="""
        AnalizzatoreArgomenti=ArgumentParser SpazioNomi=Namespace
        ErroreTipoArgomento=ArgumentTypeError TipoFile=FileType
        FormattatoreTestoGrezzo=RawTextHelpFormatter
        FormattatoreValoriPredefiniti=ArgumentDefaultsHelpFormatter
        SOPPRIMI=SUPPRESS RESTO=REMAINDER ErroreArgomento=ArgumentError
    """, tipi={
        "ArgumentParser": """analizza_argomenti=parse_args
            analizza_argomenti_noti=parse_known_args
            aggiungi_sottoanalizzatori=add_subparsers
            aggiungi_gruppo=add_argument_group
            aggiungi_gruppo_esclusivo=add_mutually_exclusive_group
            stampa_aiuto=print_help stampa_uso=print_usage errore=error
            imposta_predefiniti=set_defaults formatta_aiuto=format_help
            esci=exit""",
        "_ActionsContainer": "aggiungi_argomento=add_argument",
        "_SubParsersAction": "aggiungi_analizzatore=add_parser",
    }, opz="""
        aiuto=help predefinito=default tipo=type obbligatorio=required
        azione=action numero_argomenti=nargs scelte=choices
        metavariabile=metavar destinazione=dest costante=const
        descrizione=description programma=prog uso=usage epilogo=epilog
        classe_formato=formatter_class aggiungi_aiuto=add_help
        genitori=parents versione=version
    """, val={
        "action": """memorizza=store memorizza_vero=store_true
            memorizza_falso=store_false aggiungi=append conta=count
            versione=version memorizza_costante=store_const""",
    }, kw=[(["ArgumentParser"], ["__init__"]),
           (["_ActionsContainer"], ["add_argument"]),
           (["_SubParsersAction"], ["add_parser"])]),
    # ------------------------------------------------------------ requests
    "richieste": dict(orig="requests", nomi="""
        ottieni=get invia=post metti=put cancella=delete testa=head
        modifica=patch richiesta=request Sessione=Session
        ErroreRichiesta=RequestException ErroreConnessione=ConnectionError
        ErroreHttp=HTTPError ErroreTimeout=Timeout codici=codes
        Risposta=Response Richiesta=Request RichiestaPreparata=PreparedRequest
    """, tipi={
        "Response": """testo=text contenuto=content codice_stato=@status_code
            intestazioni=@headers solleva_per_stato=raise_for_status
            codifica=@encoding cookie=@cookies motivo=@reason
            itera_contenuto=iter_content itera_righe=iter_lines
            storia=@history riuscita=ok""",
        "Session": """ottieni=get invia=post metti=put cancella=delete
            testa=head richiesta=request chiudi=close""",
    }, opz="""
        parametri=params intestazioni=headers dati=data tempo_massimo=timeout
        autenticazione=auth verifica=verify segui_reindirizzamenti=allow_redirects
        flusso=stream file=files cookie=cookies proxy=proxies
    """, kw=[(["Session"], ["request", "get", "post", "put", "delete", "head"])],
        extra="""
from _italiano import traduci_kw as _tr
for _n in ('ottieni', 'invia', 'metti', 'cancella', 'testa', 'modifica', 'richiesta'):
    globals()[_n] = _tr(globals()[_n], _OPZ)
"""),
    # ----------------------------------------------------------- reportlab
    "rapporti_pdf": dict(orig="reportlab", nomi=""),
    "rapporti_pdf.tela": dict(orig="reportlab.pdfgen.canvas", nomi="Tela=Canvas", tipi={
        "Canvas": """disegna_testo=drawString
            disegna_testo_centrato=drawCentredString
            disegna_testo_a_destra=drawRightString disegna_immagine=drawImage
            linea=line linee=lines rettangolo=rect cerchio=circle
            ellisse=ellipse arco=arc imposta_carattere=setFont
            imposta_colore_riempimento=setFillColor
            imposta_colore_tratto=setStrokeColor
            imposta_colore_riempimento_rgb=setFillColorRGB
            imposta_colore_tratto_rgb=setStrokeColorRGB
            imposta_spessore_linea=setLineWidth nuova_pagina=showPage
            salva=save imposta_titolo=setTitle imposta_autore=setAuthor
            imposta_oggetto=setSubject salva_stato=saveState
            ripristina_stato=restoreState trasla=translate ruota=rotate
            scala=scale griglia=grid imposta_tratteggio=setDash
            imposta_dimensione_pagina=setPageSize oggetto_testo=beginText
            disegna_oggetto=drawText percorso=beginPath
            disegna_percorso=drawPath ritaglia=clipPath
            larghezza_testo=stringWidth""",
    }, opz="""
        dimensione_pagina=pagesize
    """, kw=[(["Canvas"], ["__init__"])]),
    "rapporti_pdf.dimensioni_pagina": dict(orig="reportlab.lib.pagesizes", nomi="""
        A4=A4 A3=A3 A5=A5 LETTERA=letter LEGALE=legal
        orizzontale=landscape verticale=portrait
    """),
    "rapporti_pdf.unita": dict(orig="reportlab.lib.units", nomi="""
        mm=mm cm=cm pollice=inch pica=pica
    """),
    "rapporti_pdf.colori": dict(orig="reportlab.lib.colors", nomi="""
        Colore=Color ColoreEsadecimale=HexColor nero=black bianco=white
        rosso=red verde=green blu=blue grigio=grey giallo=yellow
        arancione=orange viola=purple rosa=pink marrone=brown
        celeste=lightblue grigio_chiaro=lightgrey grigio_scuro=darkgrey
        trasparente=transparent
    """),
    "rapporti_pdf.stili": dict(orig="reportlab.lib.styles", nomi="""
        ottieni_stili_esempio=getSampleStyleSheet StileParagrafo=ParagraphStyle
    """, opz="""
        nome=name genitore=parent nome_carattere=fontName
        dimensione_carattere=fontSize interlinea=leading
        allineamento=alignment colore_testo=textColor spazio_dopo=spaceAfter
        spazio_prima=spaceBefore rientro_sinistro=leftIndent
        rientro_destro=rightIndent
    """, kw=[(["ParagraphStyle"], ["__init__"])]),
    "rapporti_pdf.allineamento": dict(orig="reportlab.lib.enums", nomi="""
        SINISTRA=TA_LEFT CENTRO=TA_CENTER DESTRA=TA_RIGHT GIUSTIFICATO=TA_JUSTIFY
    """),
    "rapporti_pdf.documento": dict(orig="reportlab.platypus", nomi="""
        ModelloDocumentoSemplice=SimpleDocTemplate Paragrafo=Paragraph
        Spaziatore=Spacer Tabella=Table StileTabella=TableStyle
        Immagine=Image InterruzionePagina=PageBreak
        MantieniInsieme=KeepTogether
    """, tipi={
        "SimpleDocTemplate": "costruisci=build",
        "Table": "imposta_stile=setStyle",
    }, opz="""
        dimensione_pagina=pagesize margine_sinistro=leftMargin
        margine_destro=rightMargin margine_alto=topMargin
        margine_basso=bottomMargin titolo=title autore=author
        larghezze_colonne=colWidths altezze_righe=rowHeights
        righe_ripetute=repeatRows larghezza=width altezza=height
        stile=style
    """, kw=[(["SimpleDocTemplate", "Table", "Image"], ["__init__"])]),
    "rapporti_pdf.caratteri": dict(orig="reportlab.pdfbase.pdfmetrics", nomi="""
        registra_carattere=registerFont larghezza_testo=stringWidth
        registra_famiglia=registerFontFamily
    """),
    "rapporti_pdf.caratteri_ttf": dict(orig="reportlab.pdfbase.ttfonts",
                                       nomi="CarattereTrueType=TTFont"),
}
