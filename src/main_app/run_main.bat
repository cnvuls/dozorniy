@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

if "%1"=="updated" (
    timeout /t 2 >nul
    echo [SYSTEM] Server scripts updated and restarted.
)

set "REPO=cnvuls/dozorniy"
set "EXE_NAME=main_app.exe"
set "ZIP_NAME=main_app.zip"
set "VERSION_FILE=version.txt"

echo [LAUNCHER] Starting Dozorniy Server...

:CHECK_CONFIG
set "LOCAL_VER=1.0.0"
if exist "%VERSION_FILE%" (
    set /p LOCAL_VER=<"%VERSION_FILE%"
)
echo [DEBUG] Local Server Version: !LOCAL_VER!

:GET_REMOTE_VER
set "REMOTE_VER="
for /f "delims=" %%v in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; if ($p.tag_name) { echo $p.tag_name } } catch {}"') do set "REMOTE_VER=%%v"

if "%REMOTE_VER%"=="" (
    echo [SKIP] Could not fetch remote version.
    goto START_APP
)
echo [DEBUG] Remote Server Version: %REMOTE_VER%

if "%LOCAL_VER%"=="%REMOTE_VER%" goto START_APP

:DOWNLOAD_UPDATE
echo [UPDATE] New server version found (%REMOTE_VER%). Downloading...
set "DOWNLOAD_URL="
for /f "delims=" %%u in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $u = $r.assets | Where-Object { $_.name -like '*%ZIP_NAME%*' } | Select-Object -ExpandProperty browser_download_url; if ($u) { echo $u } } catch {}"') do set "DOWNLOAD_URL=%%u"

if "%DOWNLOAD_URL%"=="" (
    echo [ERROR] Could not find download URL.
    goto START_APP
)

curl -L -o update_server.zip --connect-timeout 15 "%DOWNLOAD_URL%"
if not exist update_server.zip goto START_APP

set "size=0"
for %%I in (update_server.zip) do set "size=%%~zI"
if !size! LSS 1000 (
    echo [ERROR] Server update file too small.
    del /q update_server.zip
    goto START_APP
)

:APPLY_UPDATE
echo [UPDATE] Applying server update...
taskkill /f /im %EXE_NAME% >nul 2>&1
timeout /t 2 >nul
powershell -command "Expand-Archive -Path update_server.zip -DestinationPath . -Force"
echo %REMOTE_VER% > "%VERSION_FILE%"
del /q update_server.zip

echo [UPDATE] Server core updated. Restarting...
start "" "%~f0" updated
exit

:START_APP
if not exist "%EXE_NAME%" (
    echo [CRITICAL] Server EXE not found!
    timeout /t 10
    goto GET_REMOTE_VER
)
echo [SYSTEM] Running %EXE_NAME%...
start /wait %EXE_NAME%
echo [CRASH] Server exited. Restarting in 5s...
timeout /t 5 >nul
goto GET_REMOTE_VER
