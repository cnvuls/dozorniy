@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

set REPO=cnvuls/dozorniy
set EXE_NAME=user_app.exe
set ZIP_NAME=user_app.zip
set ENV_FILE=.env

echo [LAUNCHER] Starting Dozorniy Agent...

:CHECK_UPDATE
if not exist %ENV_FILE% (
    echo VERSION=0.0.0 > %ENV_FILE%
    set LOCAL_VER=0.0.0
) else (
    for /f "tokens=2 delims==" %%a in ('findstr "VERSION=" %ENV_FILE%') do set LOCAL_VER=%%a
)

set REMOTE_VER=
for /f "delims=" %%v in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $p = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; if ($p.tag_name) { echo $p.tag_name } } catch {}"') do set REMOTE_VER=%%v

if "%REMOTE_VER%"=="" goto START_APP
echo %REMOTE_VER% | findstr /R "^v ^[0-9]" >nul
if errorlevel 1 goto START_APP

echo [SYSTEM] Local: %LOCAL_VER% / Remote: %REMOTE_VER%

if not "%LOCAL_VER%"=="%REMOTE_VER%" (
    echo [UPDATE] New version found. Downloading ZIP...
    
    set DOWNLOAD_URL=
    for /f "delims=" %%u in ('powershell -command "$ErrorActionPreference = 'SilentlyContinue'; try { $r = Invoke-RestMethod 'https://api.github.com/repos/%REPO%/releases/latest'; $u = $r.assets | Where-Object { $_.name -like '*%ZIP_NAME%*' } | Select-Object -ExpandProperty browser_download_url; if ($u) { echo $u } } catch {}"') do set DOWNLOAD_URL=%%u

    if not "!DOWNLOAD_URL!"=="" (
        curl -L -o update.zip "!DOWNLOAD_URL!"
        if exist update.zip (
            taskkill /f /im %EXE_NAME% >nul 2>&1
            timeout /t 2 >nul
            
            :: Распаковка архива во временную папку и замена файлов
            powershell -command "Expand-Archive -Path update.zip -DestinationPath . -Force"
            
            :: Обновляем версию в .env
            powershell -command "(Get-Content %ENV_FILE%) -replace 'VERSION=.*', 'VERSION=%REMOTE_VER%' | Set-Content %ENV_FILE%.tmp; Move-Item -Force %ENV_FILE%.tmp %ENV_FILE%"
            
            del /q update.zip
            echo [UPDATE] Done.
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
echo [CRASH] Application exited. Restarting in 5s...
timeout /t 5 >nul
goto CHECK_UPDATE
