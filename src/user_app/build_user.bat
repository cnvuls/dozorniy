@echo off
uv run pyinstaller --noconfirm --onefile --windowed --name "user_app" --add-data "features;features" --add-data "core;core" --add-data "connection;connection" --collect-all "websockets" --collect-all "pydantic" --collect-all "pydantic_settings" main.py
