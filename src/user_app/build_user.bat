@echo off
echo [CLEANING] Removing old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [INSTALLING] Ensuring click is present...
uv add click

echo [BUILDING] Starting PyInstaller...
uv run pyinstaller --noconfirm --onedir --windowed --name "user_app" ^
--add-data "features;features" ^
--add-data "core;core" ^
--add-data "connection;connection" ^
--collect-all "websockets" ^
--collect-all "pydantic" ^
--collect-all "pydantic_settings" ^
--collect-all "click" ^
--hidden-import="click" ^
main.py
pause
