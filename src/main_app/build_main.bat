@echo off
echo [CLEANING] Removing old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [INSTALLING] Ensuring flet is up to date...
uv add flet

echo [BUILDING] Starting Official Flet Build for Windows...
:: flet build windows сам упакует всё содержимое папки в правильный EXE.
:: Он автоматически подтянет все зависимости и движок.
uv run flet build windows --name "main_app" --product "Dozorniy Server" --company "Dozorniy"

echo [DONE] Look into build/windows/ folder for your app.
pause
