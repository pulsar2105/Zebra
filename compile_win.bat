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

mkdir %FileDirectory%\exe
nasm -f win64 %FullPath% -o %FileDirectory%\exe\%FileNameWithoutExtension%.o
%CurrentDir%\linker\windows\GoLink.exe %FileDirectory%\exe\%FileNameWithoutExtension%.o /entry main /console kernel32.dll
%FileDirectory%\exe\%FileNameWithoutExtension%.exe