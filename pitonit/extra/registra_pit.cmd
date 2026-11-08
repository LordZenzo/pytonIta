@echo off
rem Associa i file .pit a pitonit per l'utente corrente (HKCU, non serve l'amministratore).
rem Per annullare: annulla_registrazione_pit.cmd
set "BASE=%~dp0"
reg add "HKCU\Software\Classes\.pit" /ve /d "Pitonit.Programma" /f >nul
reg add "HKCU\Software\Classes\Pitonit.Programma" /ve /d "Programma pitonit" /f >nul
reg add "HKCU\Software\Classes\Pitonit.Programma\shell\open\command" /ve /d "\"%BASE%pitonit.exe\" \"%%1\" %%*" /f >nul
echo File .pit associati a %BASE%pitonit.exe
echo Per usare "pitonit" da qualsiasi cartella aggiungi %BASE% al PATH.
