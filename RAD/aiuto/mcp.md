# Altri agenti con MCP

PitStudio può offrire i suoi strumenti ad altri agenti di programmazione (Claude Code, Cursor, Windsurf…) con il protocollo **MCP**. L'agente continua a fare il suo lavoro e usa gli strumenti di PitStudio dove servono:

- **leggere e scrivere i file del progetto** (`leggi_file`, `scrivi_file`, `modifica_file`) con gli stessi controlli dell'assistente interno: se il codice ha un errore di sintassi, o un errore grave (parola chiave usata come nome, funzione predefinita nascosta), il file **non viene scritto** e l'agente riceve il motivo;
- **ottenere e impostare le finestre** (`ottieni_form`, `imposta_form`), così i file `*_ui.pit` restano sempre generati dal progettista;
- **controllare la sintassi** (`controlla_sintassi`), **cercare** nel progetto (`cerca_nel_progetto`, `elenca_file`) ed **esplorare i moduli** italiani (`membri_modulo`).

Il server **non cancella file** e **non esegue programmi** (l'esecuzione si può accendere con `--consenti-esecuzione`). Non ha bisogno che PitStudio sia aperto.

## Come si collega

*Strumenti → Collega altri agenti (MCP)…* mostra i comandi già pronti per il tuo progetto, con i pulsanti per copiarli:

- **Claude Code**: un comando da lanciare nella cartella del progetto, del tipo `claude mcp add pitstudio -- <pitonit> <PitStudio>/rad/mcp_server.pit --progetto <cartella>`;
- **altri programmi**: la voce `mcpServers` da aggiungere al loro file di configurazione MCP.

Da riga di comando: `pitonit rad/mcp_server.pit --progetto C:/miei/programmi/negozio`. Il server parla JSON-RPC su standard input/output (un messaggio per riga).

## Cosa dire all'agente

Scrive in pytonIta (Python con le parole chiave italiane): il server lo ricorda nelle sue istruzioni. I nomi delle funzioni predefinite hanno il trattino basso (`tipo_testo`, `lunghezza_di`…) e `e`, `o`, `l`, `I` non sono nomi di variabile ammessi; se sbaglia, il file non viene scritto e l'errore spiega come correggere.

Il protocollo **ACP** (agenti nell'editor) non è supportato.
