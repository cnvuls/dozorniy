@echo off
uv run python -m nuitka --standalone --windows-company-name="Dozorniy" --windows-product-name="DozorniyServer" --include-package=flet --include-package=websockets --include-package=features --include-package=ui --include-package=core --include-package=connection --include-package-data=flet --include-data-dir=ui/gui/assets=ui/gui/assets --output-filename=main_app.exe main.py
