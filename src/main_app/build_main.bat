@echo off
uv run pyinstaller --noconfirm --onefile --name "main_app" --add-data "features;features" --add-data "ui;ui" --add-data "core;core" --add-data "connection;connection" --collect-all "flet" --collect-all "websockets" main.py
