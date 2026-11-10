#!/bin/sh
# Installa pytonIta (l'interprete pitonit e PitStudio) su Linux e macOS, compilando dai sorgenti.
#
#   sh installa.sh                      installa in ~/.local/pytonita (compila pitonit: 5-15 minuti)
#   sh installa.sh --prefisso=/opt/pit  installa in un'altra cartella
#   sh installa.sh --scientifiche       aggiunge numpy, pandas, scipy, matplotlib, requests, reportlab, tksheet
#   sh installa.sh --solo-pitstudio     riscrive solo PitStudio e le librerie italiane (senza ricompilare: è l'aggiornamento)
#   sh installa.sh --disinstalla        toglie pytonIta (la cartella di installazione e la voce nel menu); non serve il repository
#   sh installa.sh --disinstalla --tutto  toglie anche le impostazioni (~/.rad); i tuoi progetti non si toccano mai
#
# Va lanciato dalla cartella del repository (scaricato con git clone o con «Source code» della Release).
set -eu

CPYTHON_COMMIT="42155a0feaca9ba6991942c323cbe9fb7278be3c"      # CPython 3.13.18 su cui si applica la patch di pitonit
QUI="$(cd "$(dirname "$0")" && pwd)"
RADICE="$(cd "$QUI/../.." && pwd)"
PREFISSO="${PREFISSO:-$HOME/.local/pytonita}"
SOLO_PITSTUDIO=0
SCIENTIFICHE=0
DISINSTALLA=0
TUTTO=0
SISTEMA="$(uname -s)"

uso() {
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
}

for a in "$@"; do
    case "$a" in
        --prefisso=*) PREFISSO="${a#*=}" ;;
        --solo-pitstudio) SOLO_PITSTUDIO=1 ;;
        --scientifiche) SCIENTIFICHE=1 ;;
        --disinstalla) DISINSTALLA=1 ;;
        --tutto) TUTTO=1 ;;
        -h|--aiuto|--help) uso; exit 0 ;;
        *) echo "Opzione sconosciuta: $a"; uso; exit 2 ;;
    esac
done

dica() { printf '\n==> %s\n' "$*"; }
errore() { printf '\nERRORE: %s\n' "$*" >&2; exit 1; }

# --------------------------------------------------------------------------- disinstallazione
disinstalla() {
    # sicurezza: si cancella solo una cartella che è davvero un'installazione di pytonIta
    [ -x "$PREFISSO/bin/pitstudio" ] || [ -d "$PREFISSO/PitStudio" ] || errore "in $PREFISSO non c'è un'installazione di pytonIta (usa --prefisso=CARTELLA se l'hai messa altrove)."
    case "$PREFISSO" in ""|"/"|"$HOME"|"$HOME/") errore "rifiuto di cancellare $PREFISSO." ;; esac
    voce="${XDG_DATA_HOME:-$HOME/.local/share}/applications/pitstudio.desktop"
    echo "Verrà tolto:"
    echo "  $PREFISSO"
    [ -f "$voce" ] && grep -q "^Exec=$PREFISSO/" "$voce" 2>/dev/null && echo "  $voce"
    [ "$TUTTO" = "1" ] && echo "  $HOME/.rad (impostazioni e librerie scaricate)"
    echo "I tuoi progetti non vengono toccati."
    if [ -t 0 ]; then
        printf 'Procedo? [s/N] '
        read risposta
        case "$risposta" in s|S|si|SI|sì|Sì) ;; *) echo "Annullato."; exit 0 ;; esac
    fi
    rm -rf "$PREFISSO"
    if [ -f "$voce" ] && grep -q "^Exec=$PREFISSO/" "$voce" 2>/dev/null; then rm -f "$voce"; fi
    [ "$TUTTO" = "1" ] && rm -rf "$HOME/.rad"
    dica "pytonIta è stato tolto"
    echo "Se avevi aggiunto $PREFISSO/bin al PATH in ~/.profile (o ~/.zshrc), puoi togliere quella riga."
    exit 0
}
[ "$DISINSTALLA" = "1" ] && disinstalla

# --------------------------------------------------------------------------- controlli
for f in "$RADICE/RAD/rad.pit" "$RADICE/pitonit/patch/pitonit.patch" "$RADICE/librerie/moduli"; do
    [ -e "$f" ] || errore "non trovo $f: lancia lo script dalla cartella del repository di pytonIta."
done

trova_python() { echo "$PREFISSO/bin/python3.13"; }

consiglia_pacchetti() {
    echo
    echo "Servono un compilatore C, make, git, curl e le librerie di sviluppo di Tk, OpenSSL, SQLite, zlib e altre."
    if [ "$SISTEMA" = "Darwin" ]; then
        echo "Su macOS (con Homebrew):"
        echo "  xcode-select --install"
        echo "  brew install openssl@3 tcl-tk xz sqlite3 readline"
    elif command -v apt-get >/dev/null 2>&1; then
        echo "Su Debian/Ubuntu:"
        echo "  sudo apt install build-essential git curl python3-tk tk-dev libssl-dev libffi-dev zlib1g-dev libbz2-dev libsqlite3-dev liblzma-dev libreadline-dev uuid-dev"
    elif command -v dnf >/dev/null 2>&1; then
        echo "Su Fedora:"
        echo "  sudo dnf install gcc make git curl tk-devel openssl-devel libffi-devel zlib-devel bzip2-devel sqlite-devel xz-devel readline-devel libuuid-devel"
    elif command -v pacman >/dev/null 2>&1; then
        echo "Su Arch:"
        echo "  sudo pacman -S base-devel git curl tk openssl libffi zlib bzip2 sqlite xz readline"
    fi
}

# Su Debian/Ubuntu le dipendenze si installano da sole (chiede conferma e la password di amministratore)
PACCHETTI_APT="build-essential git curl python3-tk tk-dev libssl-dev libffi-dev zlib1g-dev libbz2-dev libsqlite3-dev liblzma-dev libreadline-dev uuid-dev"
if [ "$SOLO_PITSTUDIO" = "0" ] && [ "$SISTEMA" = "Linux" ] && command -v apt-get >/dev/null 2>&1 && command -v dpkg >/dev/null 2>&1; then
    da_installare=""
    for pacchetto in $PACCHETTI_APT; do
        dpkg -s "$pacchetto" >/dev/null 2>&1 || da_installare="$da_installare $pacchetto"
    done
    if [ -n "$da_installare" ]; then
        echo "Per compilare l'interprete mancano questi pacchetti:$da_installare"
        risposta=s
        if [ -t 0 ]; then
            printf 'Li installo adesso con sudo apt? Ti chiederà la password. [S/n] '
            read risposta
        fi
        case "$risposta" in
            n|N|no|NO) echo "Allora installali tu con:"; echo "  sudo apt install$da_installare"; exit 1 ;;
        esac
        command -v sudo >/dev/null 2>&1 || errore "manca sudo: installa a mano con (da amministratore) apt install$da_installare"
        sudo apt-get update && sudo apt-get install -y $da_installare || errore "l'installazione dei pacchetti non è riuscita."
    fi
fi

mancano=""
if [ "$SOLO_PITSTUDIO" = "0" ]; then
    for c in cc make git tar; do
        command -v "$c" >/dev/null 2>&1 || mancano="$mancano $c"
    done
    command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1 || mancano="$mancano curl"
    if [ -n "$mancano" ]; then
        echo "Mancano questi programmi:$mancano"
        consiglia_pacchetti
        exit 1
    fi
fi

# --------------------------------------------------------------------------- interprete
costruisci_pitonit() {
    lavoro="$(mktemp -d "${TMPDIR:-/tmp}/pytonita.XXXXXX")"
    trap 'rm -rf "$lavoro"' EXIT
    dica "Scarico CPython 3.13.18 (circa 25 MB)"
    indirizzo="https://github.com/python/cpython/archive/$CPYTHON_COMMIT.tar.gz"
    if command -v curl >/dev/null 2>&1; then
        curl -fL "$indirizzo" -o "$lavoro/cpython.tar.gz" || errore "download di CPython non riuscito."
    else
        wget -O "$lavoro/cpython.tar.gz" "$indirizzo" || errore "download di CPython non riuscito."
    fi
    mkdir "$lavoro/src"
    tar xzf "$lavoro/cpython.tar.gz" -C "$lavoro/src" --strip-components=1
    dica "Applico la patch di pitonit (parole chiave e librerie in italiano)"
    ( cd "$lavoro/src" && git apply --whitespace=nowarn "$RADICE/pitonit/patch/pitonit.patch" ) || errore "la patch non si applica."

    dica "Configuro in $PREFISSO"
    opzioni="--prefix=$PREFISSO --with-ensurepip=install"
    if [ "$SISTEMA" = "Darwin" ] && command -v brew >/dev/null 2>&1; then
        ssl="$(brew --prefix openssl@3 2>/dev/null || true)"
        tcl="$(brew --prefix tcl-tk 2>/dev/null || true)"
        [ -n "$ssl" ] && opzioni="$opzioni --with-openssl=$ssl"
        if [ -n "$tcl" ]; then
            export TCLTK_CFLAGS="-I$tcl/include"
            export TCLTK_LIBS="-L$tcl/lib -ltcl8.6 -ltk8.6"
        fi
    fi
    ( cd "$lavoro/src" && ./configure $opzioni > "$lavoro/configure.log" 2>&1 ) || { tail -20 "$lavoro/configure.log"; errore "configure non è riuscito."; }

    dica "Compilo (alcuni minuti)"
    if command -v nproc >/dev/null 2>&1; then n="$(nproc)"; else n="$(sysctl -n hw.ncpu 2>/dev/null || echo 2)"; fi
    ( cd "$lavoro/src" && make -j"$n" > "$lavoro/make.log" 2>&1 ) || { tail -30 "$lavoro/make.log"; errore "la compilazione non è riuscita."; }
    dica "Installo"
    ( cd "$lavoro/src" && make install > "$lavoro/install.log" 2>&1 ) || { tail -20 "$lavoro/install.log"; errore "make install non è riuscito."; }
    ln -sf python3.13 "$PREFISSO/bin/pitonit"

    py="$(trova_python)"
    "$py" -c "import tkinter" 2>/dev/null || echo "ATTENZIONE: tkinter non è stato compilato (mancano le librerie di sviluppo di Tk): PitStudio non si aprirà."
}

# --------------------------------------------------------------------------- PitStudio e librerie
installa_pitstudio() {
    py="$(trova_python)"
    [ -x "$py" ] || errore "non trovo l'interprete in $py: installa prima senza --solo-pitstudio."
    lib="$("$py" -c "import os; print(os.path.dirname(os.__file__))")"

    dica "Librerie italiane (108) in $lib"
    cp -R "$RADICE/librerie/moduli/." "$lib/"

    dica "PitStudio in $PREFISSO/PitStudio"
    rm -rf "$PREFISSO/PitStudio" "$PREFISSO/pitonit"
    mkdir -p "$PREFISSO/PitStudio" "$PREFISSO/pitonit"
    for voce in rad rad.pit aiuto esempi esercizi modelli modelli_codice LEGGIMI.md; do
        [ -e "$RADICE/RAD/$voce" ] && cp -R "$RADICE/RAD/$voce" "$PREFISSO/PitStudio/"
    done
    find "$PREFISSO/PitStudio" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
    cp -R "$RADICE/pitonit/tools" "$PREFISSO/pitonit/tools"
    find "$PREFISSO/pitonit" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true

    if [ "$SOLO_PITSTUDIO" = "0" ]; then
        dica "Pillow (serve a PitStudio per le immagini)"
        "$py" -m pip install --quiet pillow || echo "ATTENZIONE: pillow non installato: alcune immagini non si vedranno."
        if [ "$SCIENTIFICHE" = "1" ]; then
            dica "Librerie scientifiche (può richiedere qualche minuto)"
            "$py" -m pip install --quiet numpy pandas scipy matplotlib requests reportlab tksheet || echo "ATTENZIONE: alcune librerie scientifiche non si sono installate."
        fi
    fi

    mkdir -p "$PREFISSO/bin"
    cat > "$PREFISSO/bin/pitstudio" <<LANCIATORE
#!/bin/sh
# Avvia PitStudio. Accetta una cartella di progetto: pitstudio ~/miei-programmi/gioco
exec "$PREFISSO/bin/python3.13" "$PREFISSO/PitStudio/rad.pit" "\$@"
LANCIATORE
    chmod +x "$PREFISSO/bin/pitstudio"
}

# --------------------------------------------------------------------------- collegamenti nel menu (solo Linux)
installa_menu() {
    [ "$SISTEMA" = "Linux" ] || return 0
    cartella="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
    mkdir -p "$cartella"
    icona="$PREFISSO/PitStudio/rad/risorse/rad.png"
    cat > "$cartella/pitstudio.desktop" <<VOCE
[Desktop Entry]
Type=Application
Name=PitStudio
Comment=Ambiente di sviluppo per pytonIta (Python in italiano)
Exec=$PREFISSO/bin/pitstudio
Icon=$icona
Terminal=false
Categories=Development;IDE;Education;
StartupWMClass=tk
VOCE
}

if [ "$SOLO_PITSTUDIO" = "0" ]; then
    costruisci_pitonit
fi
installa_pitstudio
installa_menu

dica "Fatto"
echo "Per avviare PitStudio:   $PREFISSO/bin/pitstudio"
echo "Per usare l'interprete:  $PREFISSO/bin/pitonit programma.pit"
case ":$PATH:" in
    *":$PREFISSO/bin:"*) ;;
    *) echo
       echo "Per averli sempre a portata di mano aggiungi questa riga a ~/.profile (o ~/.zshrc):"
       echo "  export PATH=\"$PREFISSO/bin:\$PATH\"" ;;
esac
