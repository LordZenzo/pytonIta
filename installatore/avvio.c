/* PitStudio.exe - avvia l'ambiente PitStudio con l'interprete pitonitw (senza finestra di console). */
#include <windows.h>
#include <wchar.h>

static int esiste(const wchar_t *p) { return GetFileAttributesW(p) != INVALID_FILE_ATTRIBUTES; }

int WINAPI wWinMain(HINSTANCE h, HINSTANCE hp, LPWSTR args, int show)
{
    wchar_t exe[MAX_PATH], dir[MAX_PATH], interprete[MAX_PATH], script[MAX_PATH], cmd[32768];
    GetModuleFileNameW(NULL, exe, MAX_PATH);
    wcscpy(dir, exe);
    wchar_t *s = wcsrchr(dir, L'\\');
    if (s) *s = 0;
    const wchar_t *relativi[] = { L"\\..\\pitonit\\pitonitw.exe", L"\\..\\pitonit\\installazione\\pitonitw.exe", L"\\pitonit\\pitonitw.exe" };
    interprete[0] = 0;
    for (int i = 0; i < 3; i++) {
        swprintf(interprete, MAX_PATH, L"%ls%ls", dir, relativi[i]);
        if (esiste(interprete)) break;
        interprete[0] = 0;
    }
    swprintf(script, MAX_PATH, L"%ls\\rad.pit", dir);
    if (!interprete[0] || !esiste(script)) {
        MessageBoxW(NULL, L"Non trovo l'interprete pitonit o il file rad.pit.\nReinstalla pytonIta.", L"PitStudio", MB_ICONERROR);
        return 1;
    }
    swprintf(cmd, 32768, L"\"%ls\" \"%ls\" %ls", interprete, script, args ? args : L"");
    STARTUPINFOW si = { sizeof si };
    PROCESS_INFORMATION pi;
    if (!CreateProcessW(NULL, cmd, NULL, NULL, FALSE, 0, NULL, dir, &si, &pi)) {
        MessageBoxW(NULL, L"Impossibile avviare pitonit.", L"PitStudio", MB_ICONERROR);
        return 1;
    }
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return 0;
}
