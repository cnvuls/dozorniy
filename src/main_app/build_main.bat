@echo off
echo [1/4] Cleaning...
rmdir /s /q build dist 2>nul

echo [2/4] Getting library paths...
for /f "delims=" %%i in ('uv run python -c "import flet; import os; print(os.path.dirname(flet.__file__))"') do set FLET_DIR=%%i

echo [3/4] Running PyInstaller...
uv run python -m PyInstaller --noconfirm --onedir --name "main_app" ^
--add-data "features;features" ^
--add-data "ui;ui" ^
--add-data "core;core" ^
--add-data "connection;connection" ^
--add-data "%FLET_DIR%;flet" ^
--collect-all "flet" ^
--collect-all "websockets" ^
--collect-all "click" ^
--hidden-import="click" ^
main.py

echo [4/4] Final touch: Fix Flet Desktop path...
if exist dist\main_app\_internal\flet\flet_desktop (
    echo [OK] Flet Desktop found.
) else (
    xcopy /E /I /Y "%FLET_DIR%\flet_desktop" "dist\main_app\_internal\flet_desktop"
)

echo [DONE]
pause
