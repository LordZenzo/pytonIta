@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
cd /d %~dp0
set SRC=C:\AppPython\pitonit\src
rc /nologo rad.rc
cl /nologo /O2 /MT /W3 /DUNICODE /D_UNICODE /DPy_BUILD_CORE_MODULE=0 /I%SRC%\Include /I%SRC%\PCbuild\amd64 pitstudio.c rad.res user32.lib delayimp.lib %SRC%\PCbuild\amd64\python313.lib /link /SUBSYSTEM:WINDOWS /ENTRY:wWinMainCRTStartup /DELAYLOAD:python313.dll /OUT:PitStudio.exe
