"""tkinter e sottomoduli  ->  interfaccia, interfaccia.tema, ..."""

# opzioni dei widget (argomenti con nome)
OPZIONI = """
    testo=text comando=command larghezza=width altezza=height
    sfondo=background primo_piano=foreground carattere=font
    margine_x=padx margine_y=pady lato=side riempi=fill espandi=expand
    riga=row colonna=column span_colonne=columnspan span_righe=rowspan
    aggancia=sticky ancora=anchor stato=state variabile_testo=textvariable
    variabile=variable immagine=image rilievo=relief bordo=borderwidth
    orientamento=orient comando_scorrimento_y=yscrollcommand
    comando_scorrimento_x=xscrollcommand modalita_selezione=selectmode
    mostra=show larghezza_a_capo=wraplength allineamento=justify
    valore=value da_=from_ a=to risoluzione=resolution cursore=cursor
    margine_interno_x=ipadx margine_interno_y=ipady
    sfondo_attivo=activebackground primo_piano_attivo=activeforeground
    primo_piano_disabilitato=disabledforeground
    sfondo_selezione=selectbackground primo_piano_selezione=selectforeground
    variabile_elenco=listvariable a_capo=wrap annulla=undo
    imbottitura=padding stile=style colonne=columns valori=values
    peso=weight dimensione_minima=minsize strappabile=tearoff
    etichetta=label acceleratore=accelerator sottolinea=underline
    valore_attivo=onvalue valore_non_attivo=offvalue lunghezza=length
    modalita=mode massimo=maximum minimo=minimum
    colore_cursore=insertbackground evidenzia_spessore=highlightthickness
    esporta_selezione=exportselection genitore=master
    altezza_riga=rowheight composto=compound
"""

VALORI = {
    "side": "sinistra=left destra=right alto=top basso=bottom",
    "fill": "entrambi=both nessuno=none",
    "anchor": "nord=n sud=s est=e ovest=w centro=center",
    "state": "normale=normal disabilitato=disabled attivo=active sola_lettura=readonly",
    "relief": "piatto=flat rialzato=raised incavato=sunken scanalato=groove bordo=ridge solido=solid",
    "orient": "orizzontale=horizontal verticale=vertical",
    "justify": "sinistra=left centro=center destra=right",
    "wrap": "nessuno=none carattere=char parola=word",
    "selectmode": "singola=single multipla=multiple estesa=extended",
    "compound": "alto=top basso=bottom sinistra=left destra=right centro=center nessuno=none",
}

WIDGET = ["Toplevel", "Frame", "Label", "Button", "Entry", "Text", "Canvas",
          "Listbox", "Scrollbar", "Checkbutton", "Radiobutton", "Scale",
          "Spinbox", "Menu", "Menubutton", "LabelFrame", "PanedWindow", "Message"]

TK_METODI = [
    (WIDGET, ["__init__"]),
    (["Misc"], ["configure", "config", "grid_columnconfigure", "columnconfigure",
                "grid_rowconfigure", "rowconfigure"]),
    (["Pack"], ["pack_configure", "pack", "configure", "config"]),
    (["Grid"], ["grid_configure", "grid", "configure", "config"]),
    (["Place"], ["place_configure", "place", "configure", "config"]),
    (["Canvas"], ["create_line", "create_rectangle", "create_oval", "create_text",
                  "create_image", "create_window", "create_polygon", "create_arc",
                  "itemconfigure", "itemconfig"]),
    (["Menu"], ["add_command", "add_cascade", "add_checkbutton", "add_radiobutton",
                "add_separator", "entryconfigure", "entryconfig"]),
    (["Text"], ["tag_configure", "tag_config"]),
]

MODULI = {
    "interfaccia": dict(orig="tkinter", opz=OPZIONI, val=VALORI, kw=TK_METODI, nomi="""
        Finestra=Tk FinestraSecondaria=Toplevel Riquadro=Frame
        Etichetta=Label Pulsante=Button CampoTesto=Entry AreaTesto=Text
        Tela=Canvas Elenco=Listbox BarraScorrimento=Scrollbar
        CasellaSelezione=Checkbutton PulsanteOpzione=Radiobutton
        Cursore=Scale CampoNumerico=Spinbox PulsanteMenu=Menubutton
        RiquadroEtichettato=LabelFrame PannelloDiviso=PanedWindow
        Messaggio=Message VariabileTesto=StringVar VariabileIntera=IntVar
        VariabileDecimale=DoubleVar VariabileBooleana=BooleanVar
        Immagine=PhotoImage ImmagineBit=BitmapImage ErroreTcl=TclError
        Evento=Event
        SINISTRA=LEFT DESTRA=RIGHT ALTO=TOP BASSO=BOTTOM ENTRAMBI=BOTH
        NESSUNO=NONE FINE=END INSERISCI=INSERT SELEZIONE=SEL
        NORMALE=NORMAL DISABILITATO=DISABLED ATTIVO=ACTIVE
        ORIZZONTALE=HORIZONTAL VERTICALE=VERTICAL CENTRO=CENTER
        PAROLA=WORD CARATTERE=CHAR NORD=N SUD=S EST=E OVEST=W
        NORD_EST=NE NORD_OVEST=NW SUD_EST=SE SUD_OVEST=SW
        RIALZATO=RAISED INCAVATO=SUNKEN PIATTO=FLAT SOLIDO=SOLID
        SCANALATO=GROOVE SINGOLA=SINGLE MULTIPLA=MULTIPLE ESTESA=EXTENDED
    """, tipi={
        "Misc": """
            ciclo_principale=mainloop aggiorna=update
            aggiorna_inattivi=update_idletasks dopo=after
            dopo_inattivo=after_idle annulla_dopo=after_cancel
            associa=bind dissocia=unbind associa_a_tutti=bind_all
            imposta_focus=focus_set forza_focus=focus_force
            ottieni_focus=focus_get distruggi=destroy esci=quit
            configura=configure ottieni_opzione=cget chiavi_opzioni=keys
            larghezza_finestra=winfo_width altezza_finestra=winfo_height
            larghezza_richiesta=winfo_reqwidth altezza_richiesta=winfo_reqheight
            larghezza_schermo=winfo_screenwidth altezza_schermo=winfo_screenheight
            posizione_x=winfo_x posizione_y=winfo_y
            posizione_x_radice=winfo_rootx posizione_y_radice=winfo_rooty
            puntatore_x=winfo_pointerx puntatore_y=winfo_pointery
            esiste=winfo_exists figli=winfo_children
            finestra_principale=winfo_toplevel è_mappata=winfo_ismapped
            configura_colonna=grid_columnconfigure
            configura_riga=grid_rowconfigure
            appunti_svuota=clipboard_clear appunti_aggiungi=clipboard_append
            appunti_ottieni=clipboard_get genera_evento=event_generate
            attendi_finestra=wait_window attendi_variabile=wait_variable
            cattura_input=grab_set rilascia_input=grab_release
            suono=bell aggiungi_opzione=option_add
            porta_in_primo_piano=lift porta_sotto=lower
            dimensione_griglia=grid_size elementi_griglia=grid_slaves
            elementi_impacchettati=pack_slaves
            ottieni_variabile_tcl=getvar imposta_variabile_tcl=setvar
            registra=register
        """,
        "Wm": """
            titolo=wm_title geometria=wm_geometry
            ridimensionabile=wm_resizable nascondi=wm_withdraw
            mostra=wm_deiconify riduci_a_icona=wm_iconify
            protocollo=wm_protocol attributi=wm_attributes
            dimensione_minima=wm_minsize dimensione_massima=wm_maxsize
            stato=wm_state transitoria=wm_transient
            imposta_icona=wm_iconbitmap sovrascrivi_reindirizza=wm_overrideredirect
            foto_icona=wm_iconphoto
        """,
        "Pack": """
            impacchetta=pack_configure rimuovi_impacchettato=pack_forget
            informazioni_impacchettato=pack_info
        """,
        "Grid": """
            griglia=grid_configure rimuovi_griglia=grid_forget
            nascondi_griglia=grid_remove informazioni_griglia=grid_info
        """,
        "Place": """
            posiziona=place_configure rimuovi_posizione=place_forget
            informazioni_posizione=place_info
        """,
        "Entry": """
            ottieni=get inserisci=insert cancella=delete
            posizione_cursore=icursor indice=index
            seleziona_intervallo=select_range seleziona_nulla=select_clear
            seleziona_tutto=selection_range
        """,
        "Text": """
            ottieni=get inserisci=insert cancella=delete mostra=see
            aggiungi_tag=tag_add rimuovi_tag=tag_remove
            configura_tag=tag_configure intervalli_tag=tag_ranges
            nomi_tag=tag_names imposta_segno=mark_set
            annulla_modifica=edit_undo ripeti_modifica=edit_redo
            cerca=search indice=index conta=count
            scorri_y=yview scorri_x=xview
            modificato=edit_modified azzera_modifiche=edit_reset
            crea_finestra=window_create crea_immagine=image_create
            associa_tag=tag_bind
        """,
        "Listbox": """
            inserisci=insert cancella=delete ottieni=get
            selezione_corrente=curselection imposta_selezione=selection_set
            azzera_selezione=selection_clear dimensione=size mostra=see
            attiva=activate vicino=nearest indice=index
            scorri_y=yview scorri_x=xview
            elemento_configura=itemconfigure
        """,
        "Canvas": """
            crea_linea=create_line crea_rettangolo=create_rectangle
            crea_ovale=create_oval crea_testo=create_text
            crea_immagine=create_image crea_finestra=create_window
            crea_poligono=create_polygon crea_arco=create_arc
            cancella=delete sposta=move coordinate=coords
            configura_elemento=itemconfigure ottieni_opzione_elemento=itemcget
            associa_tag=tag_bind rettangolo_contenitore=bbox
            trova_con_tag=find_withtag trova_tutti=find_all
            trova_sovrapposti=find_overlapping trova_vicino=find_closest
            porta_sopra=tag_raise porta_sotto=tag_lower
            scorri_y=yview scorri_x=xview
            tipo_elemento=type scala=scale
        """,
        "Menu": """
            aggiungi_comando=add_command aggiungi_sottomenu=add_cascade
            aggiungi_separatore=add_separator
            aggiungi_casella=add_checkbutton aggiungi_opzione=add_radiobutton
            inserisci_comando=insert_command cancella=delete
            mostra_popup=tk_popup configura_voce=entryconfigure
            indice=index invoca=invoke
        """,
        "Scrollbar": "imposta=set ottieni=get attiva=activate",
        "Scale": "ottieni=get imposta=set",
        "Spinbox": "ottieni=get inserisci=insert cancella=delete",
        "Button": "invoca=invoke lampeggia=flash",
        "Checkbutton": "seleziona=select deseleziona=deselect inverti=toggle invoca=invoke lampeggia=flash",
        "Radiobutton": "seleziona=select deseleziona=deselect invoca=invoke",
        "Variable": "ottieni=get imposta=set traccia=trace_add rimuovi_traccia=trace_remove",
        "PhotoImage": """
            larghezza=width altezza=height ottieni_pixel=get
            imposta_pixel=put copia=copy salva=write
            sottocampiona=subsample ingrandisci=zoom
        """,
        "Event": "",
    }),
    "interfaccia.tema": dict(orig="tkinter.ttk", opz=OPZIONI, val=VALORI, nomi="""
        Pulsante=Button Etichetta=Label Riquadro=Frame CampoTesto=Entry
        CasellaSelezione=Checkbutton PulsanteOpzione=Radiobutton
        CasellaCombinata=Combobox Albero=Treeview Schede=Notebook
        BarraProgresso=Progressbar BarraScorrimento=Scrollbar Cursore=Scale
        CampoNumerico=Spinbox Separatore=Separator RiquadroEtichettato=LabelFrame
        PannelloDiviso=PanedWindow PulsanteMenu=Menubutton Stile=Style
        Elemento=Widget MenuOpzioni=OptionMenu
    """, kw=[
        (["Button", "Label", "Frame", "Entry", "Checkbutton", "Radiobutton",
          "Combobox", "Treeview", "Notebook", "Progressbar", "Scrollbar",
          "Scale", "Spinbox", "Separator", "LabelFrame", "PanedWindow",
          "Menubutton"], ["__init__"]),
        (["Widget"], ["configure", "config"]),
    ], tipi={
        "Widget": "stato=state in_stato=instate identifica=identify",
        "Treeview": """
            intestazione=heading colonna=column inserisci=insert
            cancella=delete ottieni_figli=get_children elemento=item
            selezione=selection imposta=set sposta=move mostra=see
            identifica_riga=identify_row identifica_colonna=identify_column
            genitore=parent esiste=exists configura_tag=tag_configure
            stacca=detach successivo=next precedente=prev indice=index
            rettangolo_contenitore=bbox ricollega=reattach
            seleziona=selection_set aggiungi_selezione=selection_add
            rimuovi_selezione=selection_remove
        """,
        "Combobox": "corrente=current imposta=set ottieni=get",
        "Notebook": """
            aggiungi=add scheda=tab seleziona=select schede=tabs
            indice=index dimentica=forget nascondi=hide inserisci=insert
        """,
        "Progressbar": "avvia=start ferma=stop passo=step",
        "Style": """
            configura=configure mappa=map usa_tema=theme_use
            nomi_temi=theme_names cerca=lookup disposizione=layout
            crea_tema=theme_create
        """,
    }),
    "interfaccia.messaggi": dict(orig="tkinter.messagebox", opz="""
        titolo=title messaggio=message genitore=parent icona=icon
        dettaglio=detail predefinito=default
    """, val={}, kw=[], nomi="""
        mostra_info=showinfo mostra_avviso=showwarning mostra_errore=showerror
        chiedi_domanda=askquestion chiedi_ok_annulla=askokcancel
        chiedi_si_no=askyesno chiedi_si_no_annulla=askyesnocancel
        chiedi_riprova_annulla=askretrycancel
    """, extra="""
from _italiano import traduci_kw as _tr
_O = {'titolo': 'title', 'messaggio': 'message', 'genitore': 'parent',
      'icona': 'icon', 'dettaglio': 'detail', 'predefinito': 'default'}
for _n in ('mostra_info', 'mostra_avviso', 'mostra_errore', 'chiedi_domanda',
           'chiedi_ok_annulla', 'chiedi_si_no', 'chiedi_si_no_annulla',
           'chiedi_riprova_annulla'):
    globals()[_n] = _tr(globals()[_n], _O)
"""),
    "interfaccia.dialoghi_file": dict(orig="tkinter.filedialog", nomi="""
        chiedi_file_da_aprire=askopenfilename
        chiedi_file_da_salvare=asksaveasfilename
        chiedi_cartella=askdirectory chiedi_file_multipli=askopenfilenames
        apri_file=askopenfile salva_file=asksaveasfile
    """, extra="""
from _italiano import traduci_kw as _tr
_O = {'titolo': 'title', 'cartella_iniziale': 'initialdir',
      'tipi_file': 'filetypes', 'estensione_predefinita': 'defaultextension',
      'file_iniziale': 'initialfile', 'genitore': 'parent', 'modo': 'mode'}
for _n in ('chiedi_file_da_aprire', 'chiedi_file_da_salvare', 'chiedi_cartella',
           'chiedi_file_multipli', 'apri_file', 'salva_file'):
    globals()[_n] = _tr(globals()[_n], _O)
"""),
    "interfaccia.dialoghi_semplici": dict(orig="tkinter.simpledialog", nomi="""
        chiedi_testo=askstring chiedi_intero=askinteger
        chiedi_decimale=askfloat
    """, extra="""
from _italiano import traduci_kw as _tr
_O = {'titolo': 'title', 'messaggio': 'prompt', 'genitore': 'parent',
      'valore_iniziale': 'initialvalue', 'valore_minimo': 'minvalue',
      'valore_massimo': 'maxvalue'}
for _n in ('chiedi_testo', 'chiedi_intero', 'chiedi_decimale'):
    globals()[_n] = _tr(globals()[_n], _O)
"""),
    "interfaccia.caratteri": dict(orig="tkinter.font", nomi="""
        Carattere=Font famiglie=families nomi_caratteri=names
        GRASSETTO=BOLD NORMALE=NORMAL CORSIVO=ITALIC
    """, tipi={"Font": "misura_testo=measure metriche=metrics configura=configure copia=copy"}),
    "interfaccia.testo_scorrevole": dict(orig="tkinter.scrolledtext",
                                         nomi="TestoScorrevole=ScrolledText"),
    "interfaccia.selettore_colori": dict(orig="tkinter.colorchooser",
                                         nomi="chiedi_colore=askcolor"),
}
