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

@echo on

nasm -f win64 %FullPath% -o %FileDirectory%%FileNameWithoutExtension%.obj
%CurrentDir%\linker\windows\GoLink.exe %FileDirectory%%FileNameWithoutExtension%.obj /entry main /console kernel32.dll
%FileDirectory%%FileNameWithoutExtension%.exe