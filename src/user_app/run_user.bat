@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

if "%1"=="updated" (
    timeout /t 2 >nul
    echo [SYSTEM] Script updated and restarted.
)

set "REPO=cnvuls/dozorniy"
set "EXE_NAME=user_app.exe"
set "ZIP_NAME=user_app.zip"
set "ENV_FILE=.env"

echo [LAUNCHER] Starting Dozorniy Agent...

:CHECK_CONFIG
if not exist "%ENV_FILE%" (
    echo VERSION=1.0.0 > "%ENV_FILE%"
    set "LOCAL_VER=1.0.0"
) else (
    set "LOCAL_VER=1.0.0"
    for /f "tokens=2 delims==" %%a in ('findstr /I "VERSION=" "%ENV_FILE%"') do (
        set "val=%%a"
        set "LOCAL_VER=!val: =!"
    )
)
echo [DEBUG] Local Version: !LOCAL_VER!

:GET_REMOTE_VER
set "REMOTE_VER="
for /f "delims=" %%v in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; if ($p.tag_name) { echo $p.tag_name } } catch {}"') do set "REMOTE_VER=%%v"

if "%REMOTE_VER%"=="" (
    echo [SKIP] Could not fetch remote version.
    goto START_APP
)
echo [DEBUG] Remote Version: %REMOTE_VER%

if "%LOCAL_VER%"=="%REMOTE_VER%" goto START_APP

:DOWNLOAD_UPDATE
echo [UPDATE] New version found (%REMOTE_VER%). Downloading...
set "DOWNLOAD_URL="
for /f "delims=" %%u in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $u = $r.assets | Where-Object { $_.name -like '*%ZIP_NAME%*' } | Select-Object -ExpandProperty browser_download_url; if ($u) { echo $u } } catch {}"') do set "DOWNLOAD_URL=%%u"

if "%DOWNLOAD_URL%"=="" (
    echo [ERROR] Could not find download URL.
    goto START_APP
)

curl -L -o update.zip --connect-timeout 15 "%DOWNLOAD_URL%"
if not exist update.zip goto START_APP

set "size=0"
for %%I in (update.zip) do set "size=%%~zI"
if !size! LSS 1000 (
    echo [ERROR] Update file too small.
    del /q update.zip
    goto START_APP
)

:APPLY_UPDATE
echo [UPDATE] Applying update...
taskkill /f /im %EXE_NAME% >nul 2>&1
timeout /t 2 >nul
powershell -command "Expand-Archive -Path update.zip -DestinationPath . -Force"
powershell -command "(Get-Content '%ENV_FILE%') -replace 'VERSION=.*', 'VERSION=%REMOTE_VER%' | Set-Content '%ENV_FILE%.tmp'; Move-Item -Force '%ENV_FILE%.tmp' '%ENV_FILE%'"
del /q update.zip

echo [UPDATE] Done. Restarting...
start "" "%~f0" updated
exit

:START_APP
if not exist "%EXE_NAME%" (
    echo [CRITICAL] %EXE_NAME% not found!
    timeout /t 10
    goto GET_REMOTE_VER
)
echo [SYSTEM] Running %EXE_NAME%...
start /wait %EXE_NAME%
echo [CRASH] Application exited. Restarting in 5s...
timeout /t 5 >nul
goto GET_REMOTE_VER
