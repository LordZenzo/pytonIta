"""Priorita' 3: librerie esterne (numpy, pandas, scipy, matplotlib, tksheet, PIL)."""

OPZ_MPL = """
        etichetta=label colore=color spessore_linea=linewidth
        stile_linea=linestyle marcatore=marker trasparenza=alpha
        dimensione_figura=figsize risoluzione=dpi intervalli=bins
        dimensione_carattere=fontsize posizione=loc dimensione=s
        colore_punti=c mappa_colori=cmap colore_bordo=edgecolor
        colori=colors larghezza=width altezza=height
        righe=nrows colonne=ncols condividi_x=sharex condividi_y=sharey
        riempimento=fill
"""

MODULI = {
    # -------------------------------------------------------------- numpy
    "numerico": dict(orig="numpy", nomi="""
        matrice=array zeri=zeros uni=ones vuoto=empty pieno=full
        intervallo=arange spaziatura_lineare=linspace
        spaziatura_logaritmica=logspace identita=eye
        identita_quadrata=identity somma=sum media=mean mediana=median
        deviazione_standard=std varianza=var minimo=min massimo=max
        indice_minimo=argmin indice_massimo=argmax ordina=sort
        indici_ordinati=argsort unici=unique concatena=concatenate
        impila=stack impila_verticale=vstack impila_orizzontale=hstack
        prodotto_scalare=dot prodotto_matriciale=matmul trasponi=transpose
        dove=where assoluto=abs radice_quadrata=sqrt esponenziale=exp
        logaritmo=log seno=sin coseno=cos tangente=tan potenza=power
        arrotonda=round limita=clip somma_cumulativa=cumsum
        prodotto_cumulativo=cumprod prodotto=prod differenze=diff
        è_nan=isnan non_numero=nan infinito=inf pigreco=pi
        qualsiasi=any tutti=all quasi_uguali=allclose è_vicino=isclose
        Matrice=ndarray tipo_dati=dtype decimale64=float64
        decimale32=float32 intero64=int64 intero32=int32
        booleano=bool_ rimodella=reshape appiattisci=ravel
        copia=copy conta_diversi_da_zero=count_nonzero
        quadrato=square pavimento=floor soffitto=ceil
        media_pesata=average percentile=percentile
        correlazione=corrcoef covarianza=cov salva=save carica=load
        da_testo=loadtxt in_testo=savetxt matrice_vuota_come=empty_like
        zeri_come=zeros_like uni_come=ones_like
    """, tipi={
        "ndarray": """forma=shape dimensione=size dimensioni=ndim
            rimodella=reshape appiattisci=flatten appiattito=ravel
            trasponi=transpose somma=sum media=mean massimo=max minimo=min
            deviazione_standard=std varianza=var ordina=sort copia=copy
            tipo_dati=dtype come_tipo=astype lista=tolist
            indice_massimo=argmax indice_minimo=argmin tutti=all
            qualsiasi=any limita=clip arrotonda=round
            somma_cumulativa=cumsum prodotto=prod
            indici_ordinati=argsort riempi=fill byte_totali=nbytes
            scambia_assi=swapaxes comprimi=squeeze""",
    }),
    "numerico.casuale": dict(orig="numpy.random", nomi="""
        uniformi=rand normali=randn interi=randint seme=seed scelta=choice
        mescola=shuffle permutazione=permutation uniforme=uniform
        normale=normal generatore=default_rng campione=sample
    """, tipi={
        "Generator": """interi=integers uniforme=uniform normale=normal
            scelta=choice mescola=shuffle permutazione=permutation
            casuali=random"""}),
    "numerico.algebra_lineare": dict(orig="numpy.linalg", nomi="""
        inversa=inv determinante=det autovalori_e_vettori=eig
        autovalori=eigvals risolvi=solve norma=norm rango=matrix_rank
        decomposizione_svd=svd pseudo_inversa=pinv minimi_quadrati=lstsq
        potenza_matrice=matrix_power ErroreAlgebraLineare=LinAlgError
    """),
    # ------------------------------------------------------------- pandas
    "tabelle": dict(orig="pandas", nomi="""
        TabellaDati=DataFrame Serie=Series leggi_csv=read_csv
        leggi_excel=read_excel leggi_json=read_json leggi_sql=read_sql
        concatena=concat unisci=merge in_data_ora=to_datetime
        intervallo_date=date_range è_nullo=isna non_nullo=notna
        in_numerico=to_numeric tabella_pivot=pivot_table
        crea_dummy=get_dummies Indice=Index Timestamp=Timestamp
        Categoria=Categorical opzioni=options NA=NA
        Differenza_tempo=Timedelta ordina_valori_tabella=DataFrame
    """.replace("ordina_valori_tabella=DataFrame", ""), tipi={
        "DataFrame": """testa=head coda=tail descrivi=describe
            informazioni=info raggruppa_per=groupby ordina_valori=sort_values
            ordina_indice=sort_index rimuovi=drop elimina_nulli=dropna
            riempi_nulli=fillna rinomina=rename unisci=merge
            aggiungi_colonne=join applica=apply itera_righe=iterrows
            scrivi_csv=to_csv scrivi_excel=to_excel in_dizionario=to_dict
            scrivi_json=to_json in_matrice=to_numpy
            reimposta_indice=reset_index imposta_indice=set_index
            etichetta=loc posizione=iloc colonne=columns indice=index
            forma=shape valori=values tipi_dati=dtypes copia=copy
            interroga=query tabella_pivot=pivot_table è_nullo=isna
            conta=count somma=sum media=mean massimo=max minimo=min
            unici=nunique rimuovi_duplicati=drop_duplicates
            trasponi=transpose ruota=pivot sostituisci=replace
            in_stringa=to_string converti_tipi=astype""",
        "Series": """testa=head coda=tail unici=unique conta_valori=value_counts
            somma=sum media=mean massimo=max minimo=min conta=count
            applica=apply mappa=map ordina_valori=sort_values
            riempi_nulli=fillna elimina_nulli=dropna in_lista=tolist
            in_dizionario=to_dict valori=values indice=index
            tipo_dati=dtype converti_tipi=astype è_nullo=isna
            descrivi=describe""",
    }),
    # -------------------------------------------------------------- scipy
    "scienza": dict(orig="scipy", nomi=""),
    "scienza.ottimizzazione": dict(orig="scipy.optimize", nomi="""
        minimizza=minimize adatta_curva=curve_fit radice=root
        risolvi_sistema=fsolve programmazione_lineare=linprog
        minimizza_scalare=minimize_scalar trova_radice=brentq
        minimi_quadrati=least_squares
    """),
    "scienza.statistica": dict(orig="scipy.stats", nomi="""
        normale=norm test_t_indipendenti=ttest_ind test_t_appaiati=ttest_rel
        correlazione_pearson=pearsonr correlazione_spearman=spearmanr
        regressione_lineare=linregress descrivi=describe punteggio_z=zscore
        test_chi_quadro=chisquare moda=mode asimmetria=skew curtosi=kurtosis
        test_normalita=shapiro
    """),
    "scienza.interpolazione": dict(orig="scipy.interpolate", nomi="""
        interpola_1d=interp1d spline=UnivariateSpline
        interpola_griglia=griddata
    """),
    "scienza.integrazione": dict(orig="scipy.integrate", nomi="""
        integra=quad risolvi_ode=solve_ivp integra_trapezi=trapezoid
        integra_doppio=dblquad
    """),
    "scienza.algebra_lineare": dict(orig="scipy.linalg", nomi="""
        inversa=inv determinante=det risolvi=solve norma=norm
        autovalori=eigvals decomposizione_lu=lu
    """),
    # --------------------------------------------------------- matplotlib
    "grafici": dict(orig="matplotlib", nomi="usa=use"),
    "grafici.disegno": dict(orig="matplotlib.pyplot", opz=OPZ_MPL, nomi="""
        traccia=plot figura=figure sottografici=subplots mostra=show
        salva_figura=savefig titolo=title etichetta_x=xlabel
        etichetta_y=ylabel legenda=legend griglia=grid limiti_x=xlim
        limiti_y=ylim barre=bar barre_orizzontali=barh istogramma=hist
        dispersione=scatter torta=pie scatola_baffi=boxplot
        mostra_immagine=imshow testo=text annota=annotate
        layout_compatto=tight_layout chiudi=close
        linea_orizzontale=axhline linea_verticale=axvline
        riempi_tra=fill_between barre_errore=errorbar sottografico=subplot
        asse_corrente=gca figura_corrente=gcf barra_colori=colorbar
        tacche_x=xticks tacche_y=yticks stile=style
        modalita_interattiva=ion pausa=pause scala_x=xscale scala_y=yscale
        titolo_generale=suptitle
    """, kw=[], extra="""
from grafici import assi as _assi, figura as _figura
from _italiano import traduci_kw as _tr
for _n in ('traccia', 'figura', 'sottografici', 'salva_figura', 'titolo',
           'etichetta_x', 'etichetta_y', 'legenda', 'barre', 'barre_orizzontali',
           'istogramma', 'dispersione', 'torta', 'testo', 'annota',
           'riempi_tra', 'barre_errore', 'mostra_immagine', 'sottografico',
           'titolo_generale', 'scatola_baffi'):
    globals()[_n] = _tr(globals()[_n], _OPZ_GRAFICI)
"""),
    "grafici.assi": dict(orig="matplotlib.axes", nomi="", opz=OPZ_MPL, kw=[(["Axes"], [
        "plot", "scatter", "bar", "barh", "hist", "text", "annotate", "legend",
        "fill_between", "errorbar", "imshow", "pie", "set_title", "set_xlabel",
        "set_ylabel", "grid", "axhline", "axvline", "boxplot"])], tipi={
        "Axes": """traccia=plot imposta_titolo=set_title
            imposta_etichetta_x=set_xlabel imposta_etichetta_y=set_ylabel
            legenda=legend griglia=grid barre=bar barre_orizzontali=barh
            istogramma=hist dispersione=scatter imposta_limiti_x=set_xlim
            imposta_limiti_y=set_ylim testo=text annota=annotate
            mostra_immagine=imshow torta=pie riempi_tra=fill_between
            barre_errore=errorbar linea_orizzontale=axhline
            linea_verticale=axvline scatola_baffi=boxplot
            imposta_tacche_x=set_xticks imposta_tacche_y=set_yticks
            imposta_scala_x=set_xscale imposta_scala_y=set_yscale
            cancella=clear ottieni_limiti_x=get_xlim ottieni_limiti_y=get_ylim
            disattiva_assi=set_axis_off"""}),
    "grafici.figura": dict(orig="matplotlib.figure", nomi="Figura=Figure", opz=OPZ_MPL,
                           kw=[(["Figure"], ["savefig", "suptitle", "legend", "text"])], tipi={
        "Figure": """aggiungi_sottografico=add_subplot aggiungi_assi=add_axes
            salva_figura=savefig titolo_generale=suptitle
            layout_compatto=tight_layout imposta_dimensione=set_size_inches
            barra_colori=colorbar ottieni_assi=get_axes
            legenda=legend testo=text"""}),
    # ------------------------------------------------------------- tksheet
    "foglio_tk": dict(orig="tksheet", nomi="Foglio=Sheet", tipi={
        "Sheet": """imposta_dati=set_sheet_data ottieni_dati=get_sheet_data
            imposta_cella=set_cell_data ottieni_cella=get_cell_data
            abilita_associazioni=enable_bindings
            disabilita_associazioni=disable_bindings
            ridisegna=redraw intestazioni=headers""",
    }),
    # ---------------------------------------------------------------- PIL
    "immagini": dict(orig="PIL.Image", nomi="""
        apri=open nuova=new Immagine=Image da_matrice=fromarray
        ruota_immagine=Image ANTIALIAS=LANCZOS
    """.replace("ruota_immagine=Image", "").replace("ANTIALIAS=LANCZOS", ""), tipi={
        "Image": """ridimensiona=resize ritaglia=crop ruota=rotate
            salva=save converti=convert miniatura=thumbnail copia=copy
            mostra=show ottieni_pixel=getpixel metti_pixel=putpixel
            incolla=paste dimensione=size formato=format modo=mode
            larghezza=width altezza=height trasponi=transpose
            dividi_canali=split filtra=filter""",
    }),
}

# opzioni di matplotlib condivise (definite una volta nel codice generato)
MODULI["grafici.disegno"]["extra"] = ("_OPZ_GRAFICI = _OPZ\n"
                                      + MODULI["grafici.disegno"]["extra"])
