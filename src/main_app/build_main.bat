@echo off
echo [CLEANING] Removing old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [INSTALLING] Ensuring dependencies...
uv add flet click websockets

echo [BUILDING] Starting PyInstaller for Server...
:: Добавляем --collect-all "flet" и --collect-submodules "flet"
uv run pyinstaller --noconfirm --onedir --name "main_app" ^
--add-data "features;features" ^
--add-data "ui;ui" ^
--add-data "core;core" ^
--add-data "connection;connection" ^
--collect-all "flet" ^
--collect-all "websockets" ^
--collect-all "click" ^
--hidden-import="flet" ^
--hidden-import="click" ^
main.py
pause
