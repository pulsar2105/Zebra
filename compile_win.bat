@echo off
set "CurrentDir=%~dp0"

set "FullPath=%~1"
if "%FullPath%" == "" (
    echo None path
    exit /b 1
)

set "FullPath=%FullPath:"=%"

for %%I in ("%FullPath%") do (
    set "FileNameWithoutExtension=%%~nI"
    set "FileDirectory=%%~dpI"
)

:: active command display
@echo on

:: creat directory to store executable + objects files
mkdir %FileDirectory%\compiled
:: remove old files .obj + .exe
del %FileDirectory%\compiled\%FileNameWithoutExtension%.obj
del %FileDirectory%\compiled\%FileNameWithoutExtension%.exe

:: creat object file from asm file
nasm -i %FileDirectory% -f win64 %FullPath% -o %FileDirectory%\compiled\%FileNameWithoutExtension%.obj
:: compile object file to compiled file
%CurrentDir%\linker\windows\GoLink.exe %FileDirectory%\compiled\%FileNameWithoutExtension%.obj /entry main /console kernel32.dll
:: execut exe file
%FileDirectory%\compiled\%FileNameWithoutExtension%.exe