@echo off
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

nasm -f win64 %FullPath% -o %FileDirectory%%FileNameWithoutExtension%.o
gcc %FileDirectory%%FileNameWithoutExtension%.o -e main -o %FileDirectory%%FileNameWithoutExtension%
%FileDirectory%%FileNameWithoutExtension%.exe