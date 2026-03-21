@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

:: --- CONFIG ---
set REPO=cnvuls/dozorniy
set EXE_NAME=main_app.exe
set ZIP_NAME=main_app.zip
set VERSION_FILE=version.txt

echo [LAUNCHER] Starting Dozorniy Server...

:CHECK_UPDATE
:: 1. Читаем локальную версию
set LOCAL_VER=0.0.0
if exist %VERSION_FILE% (set /p LOCAL_VER=<%VERSION_FILE%)

:: 2. GitHub Check
set REMOTE_VER=
for /f "delims=" %%v in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; if ($p.tag_name) { echo $p.tag_name } } catch {}"') do set REMOTE_VER=%%v

if "%REMOTE_VER%"=="" goto START_APP
echo %REMOTE_VER% | findstr /R "^v ^[0-9]" >nul
if errorlevel 1 goto START_APP

echo [SYSTEM] Local: %LOCAL_VER% / Remote: %REMOTE_VER%

:: 3. Если версии не совпадают - качаем ZIP
if not "%LOCAL_VER%"=="%REMOTE_VER%" (
    echo [UPDATE] New server version found. Downloading ZIP...
    
    set DOWNLOAD_URL=
    for /f "delims=" %%u in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $u = $r.assets | Where-Object { $_.name -like '*%ZIP_NAME%*' } | Select-Object -ExpandProperty browser_download_url; if ($u) { echo $u } } catch {}"') do set DOWNLOAD_URL=%%u

    if not "!DOWNLOAD_URL!"=="" (
        curl -L -o update_server.zip "!DOWNLOAD_URL!"
        if exist update_server.zip (
            taskkill /f /im %EXE_NAME% >nul 2>&1
            timeout /t 2 >nul
            
            :: Распаковка архива поверх старых файлов
            powershell -command "Expand-Archive -Path update_server.zip -DestinationPath . -Force"
            
            :: Обновляем локальную версию
            echo %REMOTE_VER% > %VERSION_FILE%
            
            del /q update_server.zip
            echo [UPDATE] Server updated to %REMOTE_VER%
        )
    )
)

:START_APP
if not exist %EXE_NAME% (
    echo [CRITICAL] %EXE_NAME% not found!
    timeout /t 10
    goto CHECK_UPDATE
)

echo [SYSTEM] Running %EXE_NAME%...
start /wait %EXE_NAME%
timeout /t 5 >nul
goto CHECK_UPDATE
