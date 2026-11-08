@echo off
rem Avvia PitStudio, l'ambiente di sviluppo per pytonIta (senza finestra di console).
rem Per vedere gli errori nella console usa invece:  ..\pitonit\installazione\pitonit.exe rad.pit
start "" "%~dp0..\pitonit\installazione\pitonitw.exe" "%~dp0rad.pit" %*
