import importlib
import os
import pkgutil

def autodiscover_features(base_package: str = "features"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_app_root = os.path.dirname(current_dir)
    features_path = os.path.join(user_app_root, "features")

    if not os.path.exists(features_path):
        return

    for _, name, is_pkg in pkgutil.iter_modules([features_path]):
        if is_pkg:
            module_name = f"{base_package}.{name}.handler"
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                if "No module named" not in str(e) or "handler" not in str(e):
                    print(f"Error loading {module_name}: {e}")
