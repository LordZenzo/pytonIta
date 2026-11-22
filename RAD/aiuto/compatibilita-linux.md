# Compatibilità Windows / Linux e «Prova su Linux»

Un programma scritto su Windows può non funzionare su Linux (e viceversa): basta un `os.startfile`, un percorso `C:\...` o un comando come `cls`. PitStudio ti aiuta in due modi: **legge il codice** e dice cosa non andrebbe, e **lo prova davvero su Linux** dentro Windows.

## Verifica di compatibilità

*Esegui → Verifica compatibilità Windows / Linux…* apre una finestra che controlla **tutti i file `.pit` e `.py` del progetto** (senza eseguirli).

1. Scegli il **sistema di arrivo**: *Linux* (per portare su Linux un programma nato su Windows) o *Windows* (il contrario). Da Windows la finestra propone *Linux*.
2. Premi **Controlla** (parte da sola all'apertura e quando cambi sistema).
3. Ogni riga dell'elenco è un problema, con tre livelli:
   - **Non funziona**: sul sistema scelto il programma si ferma o fa altro (per esempio `import winreg`, `os.startfile`, `ctypes.windll`, `os.fork`, il comando `cls` o `sudo`, un percorso `C:\Utenti\...` o `/home/...` scritto a mano, `state("zoomed")`).
   - **Può non funzionare**: dipende da come lo usi (per esempio `iconbitmap` con un file `.ico`, o un percorso con la barra rovesciata `dati\file.txt`).
   - **Da sapere**: non rompe niente ma cambia da un sistema all'altro (per esempio `open()` senza `encoding=`, o il carattere «Segoe UI» che su Linux Tk sostituisce da solo).
4. Scegli una voce per leggere **come rimediare**; il doppio clic apre il file **alla riga** del problema. «Mostra anche le note» nasconde o mostra il terzo livello.

La finestra non blocca PitStudio: la lasci aperta, correggi, e premi di nuovo **Controlla**.

### Cosa conta come «scritto apposta»

Il codice dentro un controllo del sistema **non viene segnalato**, perché è già pensato per quel sistema:

```
se sys.platform == "win32":
    os.startfile(percorso)          # solo Windows: va bene
altrimenti:
    subprocess.run(["xdg-open", percorso])
```

Valgono anche `se os.name == "nt":`, `se piattaforma.WINDOWS:`, le forme negate (`!=`, `non`) e il ritorno anticipato (`se sys.platform != "win32": ritorna`: da lì in poi il blocco è per Windows). Un `importa` o una funzione dentro **`prova … eccetto`** diventa una semplice nota: il programma ha già un ripiego.

### Limiti

La verifica legge il codice, non lo esegue: non vede i percorsi costruiti a pezzi, i comandi che arrivano da variabili o da file, né i controlli fatti con funzioni tue (`se ho_windows():`). Non guarda i file `.form.json` (i caratteri delle finestre). È un aiuto per trovare i casi comuni, non una garanzia: **la prova vera è eseguire il programma su Linux**.

## Prova su Linux (WSL)

Windows 10 e 11 possono avere dentro un vero Linux, il **Sottosistema Windows per Linux (WSL)**. *Esegui → Prova su Linux (WSL)* esegue il **file principale** (o il file corrente) lì dentro, con l'**interprete pitonit di Linux**, sulla stessa cartella del progetto (Linux la vede come `/mnt/c/...`). L'output compare nella **console** di PitStudio e gli errori hanno i link che aprono il file alla riga giusta, come sempre.

Le **finestre grafiche** compaiono sul desktop di Windows grazie a **WSLg**: serve WSL 2 aggiornato (`wsl --update`). Senza WSLg i programmi a console funzionano lo stesso e la finestra «Linux di Windows» te lo dice.

### La prima volta: *Esegui → Linux di Windows: stato e guida…*

Se Linux non è pronto, «Prova su Linux» apre da solo questa finestra. Controlla tre cose:

| Controllo | Se manca |
|---|---|
| **WSL** e una **distribuzione** (per esempio Ubuntu) | `wsl --install -d Ubuntu` da PowerShell come amministratore, poi riavvio |
| Gli **strumenti per compilare** pytonIta in Linux | il comando `sudo apt install ...` da incollare in Ubuntu |
| **pytonIta dentro Linux** (l'interprete `pitonit`) | `git clone ... && sh ~/pytonIta/installatore/linux/installa.sh` (compila l'interprete: da 5 a 15 minuti) |

Ogni comando ha il pulsante **Copia**. Quando hai finito premi **Controlla di nuovo**: con tutto a posto compare «Pronto» e il pulsante **Prova ora**. Se hai più distribuzioni, scegli quale usare dal menu *Distribuzione* (PitStudio se lo ricorda).

PitStudio **non installa niente da solo**: i comandi li lanci tu, nel terminale indicato.

### Come si ferma e cosa cambia

- **Ferma** (Maiusc+F5) interrompe il collegamento con Linux e, normalmente, anche il programma. Se un programma restasse in esecuzione dentro Linux, chiudilo da lì con `pkill pitonit`.
- Il programma gira con le regole di Linux: maiuscole e minuscole nei nomi dei file contano, i separatori dei percorsi sono `/`, i caratteri sono quelli di Linux.
- L'interprete di Linux è quello compilato **dentro la distribuzione**: se aggiorni pytonIta su Windows, per avere la stessa versione in Linux rilancia `installa.sh` lì.
- «Prova su Linux» vale solo su Windows; su Linux e macOS la voce ti dice che sei già lì.

## Verificare e provare: l'ordine che consiglio

1. **Verifica di compatibilità** verso Linux: correggi i «Non funziona».
2. **Prova su Linux**: guarda come si comporta davvero.
3. Per consegnare il programma a un altro, vedi anche [Creare un eseguibile](#crea-exe) e [pytonIta su Linux e macOS](#linux-mac).
