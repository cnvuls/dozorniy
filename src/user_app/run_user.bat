@echo off
setlocal enabledelayedexpansion

:: --- CONFIG ---
set REPO=cnvuls/dozorniy
set EXE_NAME=user_app.exe
set ENV_FILE=.env

echo [LAUNCHER] Starting Dozorniy Agent...

:CHECK_UPDATE
if not exist %ENV_FILE% (
    echo VERSION=1.0.0 > %ENV_FILE%
    set LOCAL_VER=1.0.0
) else (
    for /f "tokens=2 delims==" %%a in ('findstr "VERSION=" %ENV_FILE%') do set LOCAL_VER=%%a
)

for /f "delims=" %%v in ('powershell -command "$p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $p.tag_name"') do set REMOTE_VER=%%v

if "%REMOTE_VER%"=="" (
    echo [OFFLINE] Skipping update check...
    goto START_APP
)

echo [SYSTEM] Local: %LOCAL_VER% | Remote: %REMOTE_VER%

if not "%LOCAL_VER%"=="%REMOTE_VER%" (
    echo [UPDATE] New version %REMOTE_VER% found! Downloading...
    
    for /f "delims=" %%u in ('powershell -command "$r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $r.assets | Where-Object { $_.name -like '*%EXE_NAME%*' } | Select-Object -ExpandProperty browser_download_url"') do set DOWNLOAD_URL=%%u

    if not "!DOWNLOAD_URL!"=="" (
        curl -L -o new_version.exe !DOWNLOAD_URL!
        taskkill /f /im %EXE_NAME% >nul 2>&1
        timeout /t 2 >nul
        move /y new_version.exe %EXE_NAME%
        
        powershell -command "(Get-Content %ENV_FILE%) -replace 'VERSION=.*', 'VERSION=%REMOTE_VER%' | Set-Content %ENV_FILE%"
        
        echo [UPDATE] Successfully updated to %REMOTE_VER%
    )
)

:START_APP
echo [SYSTEM] Running %EXE_NAME%...
start /wait %EXE_NAME%
echo [CRASH] Application exited. Restarting in 5s...
timeout /t 5 >nul
goto CHECK_UPDATE
