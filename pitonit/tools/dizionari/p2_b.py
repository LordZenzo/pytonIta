"""Priorita' 2 (parte B): rete, posta, html."""

MODULI = {
    "rete": dict(orig="socket", nomi="""
        Presa=socket FAMIGLIA_INET=AF_INET FAMIGLIA_INET6=AF_INET6
        TIPO_FLUSSO=SOCK_STREAM TIPO_DATAGRAMMA=SOCK_DGRAM
        nome_host=gethostname indirizzo_da_nome=gethostbyname
        info_indirizzo=getaddrinfo crea_connessione=create_connection
        ErroreRete=error ErroreTimeout=timeout ErroreNomeHost=gaierror
        SPEGNI_LETTURA=SHUT_RD SPEGNI_SCRITTURA=SHUT_WR SPEGNI_TUTTO=SHUT_RDWR
        LIVELLO_PRESA=SOL_SOCKET RIUSA_INDIRIZZO=SO_REUSEADDR
    """, tipi={
        "socket": """connetti=connect associa=bind ascolta=listen
            accetta=accept invia=send invia_tutto=sendall ricevi=recv
            invia_a=sendto ricevi_da=recvfrom chiudi=close
            imposta_timeout=settimeout imposta_opzione=setsockopt
            spegni=shutdown ottieni_nome_peer=getpeername
            ottieni_nome_presa=getsockname imposta_bloccante=setblocking
            crea_file=makefile"""}),
    "rete_http": dict(orig="http", nomi="StatoHttp=HTTPStatus"),
    "rete_http.client": dict(orig="http.client", nomi="""
        ConnessioneHttp=HTTPConnection ConnessioneHttps=HTTPSConnection
        RispostaHttp=HTTPResponse
    """, tipi={
        "HTTPConnection": """richiesta=request ottieni_risposta=getresponse
            chiudi=close connetti=connect imposta_livello_debug=set_debuglevel""",
        "HTTPResponse": """leggi=read ottieni_intestazione=getheader
            ottieni_intestazioni=getheaders chiudi=close
            stato=@status motivo=@reason intestazioni=@headers""",
    }),
    "rete_http.server": dict(orig="http.server", nomi="""
        ServerHttp=HTTPServer ServerHttpMultiplo=ThreadingHTTPServer
        GestoreRichiesteHttp=BaseHTTPRequestHandler
        GestoreFileHttp=SimpleHTTPRequestHandler
    """, tipi={
        "HTTPServer": """servi_per_sempre=serve_forever spegni=shutdown
            chiudi_server=server_close gestisci_richiesta=handle_request""",
        "BaseHTTPRequestHandler": """invia_risposta=send_response
            invia_intestazione=send_header termina_intestazioni=end_headers
            invia_errore=send_error percorso=@path comando=@command
            intestazioni=@headers flusso_uscita=@wfile flusso_ingresso=@rfile
            indirizzo_client=@client_address""",
    }, extra="""
def _ponte_metodi():
    for _m in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS'):
        def _crea(m):
            def _gestore(self):
                f = getattr(self, 'gestisci_' + m, None)
                if f is None:
                    return self.send_error(501, "Unsupported method (%r)" % m)
                return f()
            return _gestore
        if not hasattr(_orig.BaseHTTPRequestHandler, 'do_' + _m):
            setattr(_orig.BaseHTTPRequestHandler, 'do_' + _m, _crea(_m))


_ponte_metodi()
"""),
    "posta": dict(orig="email", nomi=""),
    "posta.messaggio": dict(orig="email.message", nomi="MessaggioEmail=EmailMessage Messaggio=Message", tipi={
        "Message": """ottieni_payload=get_payload imposta_payload=set_payload
            ottieni_tipo_contenuto=get_content_type
            ottieni_tipo_principale=get_content_maintype
            è_multiparte=is_multipart cammina=walk
            aggiungi_intestazione=add_header ottieni_nome_file=get_filename
            ottieni_parametro=get_param come_testo=as_string
            come_byte=as_bytes ottieni_tutti=get_all
            imposta_set_caratteri=set_charset""",
        "EmailMessage": """imposta_contenuto=set_content
            aggiungi_allegato=add_attachment aggiungi_alternativa=add_alternative
            ottieni_contenuto=get_content ottieni_tipo_contenuto=get_content_type
            è_multiparte=is_multipart cammina=walk"""}),
    "posta.smtp": dict(orig="smtplib", nomi="Smtp=SMTP SmtpSsl=SMTP_SSL ErroreSmtp=SMTPException", tipi={
        "SMTP": """avvia_tls=starttls accedi=login invia_messaggio=send_message
            invia_posta=sendmail esci=quit connetti=connect
            saluta=ehlo imposta_livello_debug=set_debuglevel"""}),
    "html_testo": dict(orig="html", nomi="proteggi=escape ripristina=unescape"),
    "html_testo.analizzatore": dict(orig="html.parser", nomi="AnalizzatoreHtml=HTMLParser", tipi={
        "HTMLParser": "alimenta=feed chiudi=close svuota=reset"}, extra="""
from _italiano import ponte as _ponte
_ponte(_orig.HTMLParser, {
    'handle_starttag': 'gestisci_tag_iniziale',
    'handle_endtag': 'gestisci_tag_finale',
    'handle_startendtag': 'gestisci_tag_vuoto',
    'handle_data': 'gestisci_dati',
    'handle_comment': 'gestisci_commento',
    'handle_entityref': 'gestisci_entita',
    'handle_charref': 'gestisci_carattere'})
"""),
}
