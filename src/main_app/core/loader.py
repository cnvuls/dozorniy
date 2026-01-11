import importlib
import os
import pkgutil
import sys

from main_app.features import feature


def autodiscover_features(package_path: str, package_name: str, filename: str):
    """
    Просто проходит по папке и импортирует модули.
    При импорте срабатывают декораторы @FeatureRegistry.register
    """
    if not os.path.exists(package_path):
        print(f"   ❌ ERROR: Path '{package_path}' does not exist on disk!")
        return

    try:
        files = os.listdir(package_path)
    except Exception as e:
        print(f"   ❌ ERROR listing directory: {e}")
        return

    for _, module_name, is_pkg in pkgutil.walk_packages(
        [package_path], prefix=f"{package_name}."
    ):
        try:
            if module_name.endswith(f".{filename}"):
                importlib.import_module(module_name)

        except Exception as e:
            print(f"         ❌ Error importing {module_name}: {e}")
