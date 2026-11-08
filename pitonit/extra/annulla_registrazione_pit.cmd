@echo off
reg delete "HKCU\Software\Classes\.pit" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Pitonit.Programma" /f >nul 2>&1
echo Associazione .pit rimossa.
