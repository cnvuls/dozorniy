import json
from pathlib import Path

from .settings import Config


def create_new_config(path: Path, config: Config):
    if not path.exists():
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config.model_dump(), f, indent=4)
            print(f"Default config created at {path}")
        except Exception as e:
            print(f"Error creating config file {path}: {e}")


def load_config(name: str = "default.json") -> Config:
    path = Path(name)
    default_config = Config()

    create_new_config(path, default_config)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return default_config.model_validate(data)
    except FileNotFoundError:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_config.model_dump(), f)
        print(f"Config file {path} not found, using default config")
        return default_config
    except json.JSONDecodeError:
        print(f"Invalid JSON in {path}")
        return default_config
