@echo off
uv run python -m nuitka --standalone --onefile --windows-console-mode=disable --include-package=websockets --include-package=pydantic --include-package=pydantic_settings --include-package=features --include-package=connection --include-package=core --include-package-data=flet --output-filename=user_app.exe main.py
