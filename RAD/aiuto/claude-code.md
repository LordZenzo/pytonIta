# Claude Code con il tuo abbonamento

Se hai un abbonamento a Claude (Pro, Max…) e non vuoi comprare crediti per l'API, puoi lavorare con **Claude Code**, l'app ufficiale di Anthropic, direttamente nella cartella del tuo progetto. È la seconda strada, accanto all'[assistente integrato](#assistente) che usa una chiave API.

| | Assistente integrato | Claude Code |
|---|---|---|
| Si paga | a consumo, con una **chiave API** e crediti | con il tuo **abbonamento** (nei suoi limiti) |
| Dove | la chat di PitStudio | una finestra di console con Claude Code |
| Prima/dopo, limiti di memoria, statistiche dei token | sì | no (le conferme le chiede Claude Code, nel suo terminale) |
| Annulla di PitStudio | sì | **sì** |
| Controllo della sintassi dopo ogni scrittura | sì | **sì** |

## Come si usa

1. Installa Claude Code dal sito ufficiale di Anthropic ([code.claude.com](https://code.claude.com)) e, una volta, scrivi `claude` in un terminale per accedere con il tuo account. Il login lo fai **tu, nel programma di Anthropic**: PitStudio non vede e non conserva nessuna credenziale.
2. In PitStudio apri il progetto, poi **Strumenti → Apri Claude Code nel progetto…** (oppure il pulsante **⌨ Claude Code** nella chat).
3. La prima volta in un progetto PitStudio chiede il permesso di **prepararlo** (vedi sotto). Poi si apre una finestra di console con Claude Code, già nella cartella del progetto.
4. Parla con Claude Code come al solito. Quando cambia un file, l'editor di PitStudio lo ricarica da solo e il pulsante **↶ Annulla** (nella chat) si attiva.

## Cosa fa la preparazione del progetto

- **`CLAUDE.md`**: un blocco di istruzioni (tra due commenti `pitstudio:inizio` / `pitstudio:fine`) che spiega a Claude che i file `.pit` usano le parole chiave italiane, come si eseguono con `pitonit` e quali sono le regole principali. Il resto del tuo `CLAUDE.md`, se c'è, resta com'è.
- **`.claude/settings.local.json`**: tre piccoli controlli locali (i cosiddetti *hook*), che girano solo sul tuo computer:
  - a ogni richiesta **fotografano i file** del progetto (le copie stanno in `.rad/storia`), così *Annulla* funziona come con l'assistente integrato;
  - dopo ogni scrittura di un `.pit` o `.py` **controllano la sintassi** e, se è sbagliata, lo dicono a Claude perché corregga;
  - alla fine della richiesta **chiudono il gruppo di modifiche** e aggiornano il registro delle statistiche.
  Se il progetto è un repository git, `settings.local.json` viene aggiunto a `.gitignore`.

I controlli non inviano nulla in rete. Se preferisci, scegli «No» quando PitStudio lo chiede: Claude Code si apre lo stesso, senza preparazione.

## Annullare le modifiche

Dopo una richiesta a Claude Code che ha cambiato dei file, il pulsante **↶ Annulla** (o *Strumenti → Annulla l'ultima modifica dell'assistente*) riporta il progetto com'era prima: i file modificati tornano come erano, quelli creati vengono tolti, quelli eliminati ricompaiono. È lo stesso meccanismo dell'assistente integrato: vedi [Vedi cosa cambia, e puoi annullare](#assistente).

## Limiti da conoscere

- Le **statistiche** registrano le richieste e i file scritti di Claude Code, ma non i token (con l'abbonamento non si pagano a token).
- Claude Code gira in una **sua finestra**: non è incorporato in PitStudio.
- I **limiti di memoria** dei programmi non si applicano ai comandi che lancia Claude Code.
- Le copie per *Annulla* riguardano i **file di testo** fino a 512 KB (come nell'assistente integrato).
- Se Claude Code non viene trovato, indica il percorso di `claude.exe` in `config.json` (`claude_code.percorso`).
- L'uso di Claude Code con il tuo abbonamento segue le **condizioni di Anthropic**: PitStudio si limita ad aprire il programma ufficiale non modificato, dove accedi tu con il tuo account.
