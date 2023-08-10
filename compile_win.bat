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
mkdir %FileDirectory%\exe
:: remove old files .obj + .exe
del %FileDirectory%\exe\%FileNameWithoutExtension%.obj
del %FileDirectory%\exe\%FileNameWithoutExtension%.exe

:: creat object file from asm file
nasm -i %FileDirectory% -f win64 %FullPath% -o %FileDirectory%\exe\%FileNameWithoutExtension%.obj
:: compile object file to exe file
%CurrentDir%\linker\windows\GoLink.exe %FileDirectory%\exe\%FileNameWithoutExtension%.obj /entry main /console kernel32.dll
:: execut exe file
%FileDirectory%\exe\%FileNameWithoutExtension%.exe