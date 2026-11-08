/* PitStudio.exe - l'ambiente di sviluppo PitStudio come programma nativo.
 *
 * L'interprete pitonit (python313.dll) è incorporato nel processo: non si lancia nessun altro programma.
 * L'applicazione (rad.pit e il pacchetto rad) e il runtime (librerie standard, tcl/tk) stanno accanto all'exe.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <windows.h>
#include <wchar.h>

static int esiste(const wchar_t *p) { return GetFileAttributesW(p) != INVALID_FILE_ATTRIBUTES; }

static void errore(const wchar_t *testo)
{
    MessageBoxW(NULL, testo, L"PitStudio", MB_ICONERROR);
}

/* cerca la prima delle sottocartelle relative che contiene python313.dll */
static int trova_runtime(const wchar_t *dir, wchar_t *uscita)
{
    const wchar_t *candidati[] = { L"\\pitonit", L"\\runtime", L"\\..\\pitonit", L"\\..\\pitonit\\installazione" };
    wchar_t prova[MAX_PATH * 2];
    for (int i = 0; i < 4; i++) {
        swprintf(prova, MAX_PATH * 2, L"%ls%ls\\python313.dll", dir, candidati[i]);
        if (esiste(prova)) {
            swprintf(uscita, MAX_PATH, L"%ls%ls", dir, candidati[i]);
            return 1;
        }
    }
    return 0;
}

static int cerca_app(const wchar_t *dir, wchar_t *uscita)
{
    const wchar_t *candidati[] = { L"", L"\\PitStudio", L"\\RAD" };
    wchar_t prova[MAX_PATH * 2];
    for (int i = 0; i < 3; i++) {
        swprintf(prova, MAX_PATH * 2, L"%ls%ls\\rad.pit", dir, candidati[i]);
        if (esiste(prova)) {
            swprintf(uscita, MAX_PATH, L"%ls%ls", dir, candidati[i]);
            return 1;
        }
    }
    return 0;
}

static int avvia(int argc, wchar_t **argv)
{
    wchar_t exe[MAX_PATH], dir[MAX_PATH], runtime[MAX_PATH], app[MAX_PATH], script[MAX_PATH], percorso[MAX_PATH * 2];
    GetModuleFileNameW(NULL, exe, MAX_PATH);
    wcscpy_s(dir, MAX_PATH, exe);
    wchar_t *s = wcsrchr(dir, L'\\');
    if (s) *s = 0;
    if (!trova_runtime(dir, runtime) || !cerca_app(dir, app)) {
        errore(L"Non trovo il runtime di pitonit o i file di PitStudio.\nReinstalla pytonIta.");
        return 1;
    }
    swprintf(script, MAX_PATH, L"%ls\\rad.pit", app);

    /* il runtime può stare in un'altra cartella: serve per caricare python313.dll e i moduli compilati */
    SetDllDirectoryW(runtime);
    wchar_t tcl[MAX_PATH * 2];
    swprintf(tcl, MAX_PATH * 2, L"%ls\\tcl\\tcl8.6", runtime);
    SetEnvironmentVariableW(L"TCL_LIBRARY", tcl);
    swprintf(tcl, MAX_PATH * 2, L"%ls\\tcl\\tk8.6", runtime);
    SetEnvironmentVariableW(L"TK_LIBRARY", tcl);

    PyPreConfig pre;
    PyPreConfig_InitIsolatedConfig(&pre);
    pre.utf8_mode = 1;
    PyStatus st = Py_PreInitialize(&pre);
    if (PyStatus_Exception(st)) {
        errore(L"Impossibile avviare l'interprete incorporato.");
        return 1;
    }
    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    config.site_import = 1;
    config.buffered_stdio = 0;
    st = PyConfig_SetString(&config, &config.program_name, exe);
    if (PyStatus_Exception(st)) goto fallito;
    st = PyConfig_SetString(&config, &config.home, runtime);
    if (PyStatus_Exception(st)) goto fallito;
    st = PyConfig_SetString(&config, &config.run_filename, script);
    if (PyStatus_Exception(st)) goto fallito;

    config.module_search_paths_set = 1;
    const wchar_t *relativi[] = { L"\\python313.zip", L"", L"\\Lib", L"\\DLLs", L"\\Lib\\site-packages" };
    for (int i = 0; i < 5; i++) {
        swprintf(percorso, MAX_PATH * 2, L"%ls%ls", runtime, relativi[i]);
        st = PyWideStringList_Append(&config.module_search_paths, percorso);
        if (PyStatus_Exception(st)) goto fallito;
    }
    st = PyWideStringList_Append(&config.module_search_paths, app);
    if (PyStatus_Exception(st)) goto fallito;

    /* argv[0] = script, poi gli argomenti passati a PitStudio.exe */
    wchar_t **nuovi = (wchar_t **)calloc(argc + 1, sizeof(wchar_t *));
    nuovi[0] = script;
    for (int i = 1; i < argc; i++) nuovi[i] = argv[i];
    st = PyConfig_SetArgv(&config, argc, nuovi);
    free(nuovi);
    if (PyStatus_Exception(st)) goto fallito;

    st = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(st)) goto fallito_init;
    return Py_RunMain();

fallito:
    PyConfig_Clear(&config);
fallito_init:
    errore(L"Impossibile avviare l'interprete incorporato.");
    return 1;
}

int WINAPI wWinMain(HINSTANCE h, HINSTANCE hp, LPWSTR args, int show)
{
    return avvia(__argc, __wargv);
}
