@echo off
setlocal enabledelayedexpansion

:: --- CONFIG ---
set REPO=cnvuls/dozorniy
set EXE_NAME=main_app.exe
set VERSION_FILE=version.txt

echo [LAUNCHER] Starting Dozorniy Server...

:CHECK_UPDATE
set LOCAL_VER=1.0.0
if exist %VERSION_FILE% (set /p LOCAL_VER=<%VERSION_FILE%)

for /f "delims=" %%v in ('powershell -command "$p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $p.tag_name"') do set REMOTE_VER=%%v

if "%REMOTE_VER%"=="" goto START_APP

echo [SYSTEM] Local: %LOCAL_VER% | Remote: %REMOTE_VER%

if not "%LOCAL_VER%"=="%REMOTE_VER%" (
    echo [UPDATE] New server version %REMOTE_VER% found!
    
    for /f "delims=" %%u in ('powershell -command "$r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $r.assets | Where-Object { $_.name -like '*%EXE_NAME%*' } | Select-Object -ExpandProperty browser_download_url"') do set DOWNLOAD_URL=%%u

    if not "!DOWNLOAD_URL!"=="" (
        curl -L -o new_server.exe !DOWNLOAD_URL!
        taskkill /f /im %EXE_NAME% >nul 2>&1
        timeout /t 2 >nul
        move /y new_server.exe %EXE_NAME%
        echo %REMOTE_VER% > %VERSION_FILE%
        echo [UPDATE] Server updated to %REMOTE_VER%
    )
)

:START_APP
echo [SYSTEM] Running %EXE_NAME%...
start /wait %EXE_NAME%
timeout /t 5 >nul
goto CHECK_UPDATE
