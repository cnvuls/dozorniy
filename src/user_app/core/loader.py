import importlib
import pkgutil

def autodiscover_features(base_package: str = "features"):
    try:
        package = importlib.import_module(base_package)
        if not hasattr(package, "__path__"):
            return
    except ImportError:
        return

    for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
        if is_pkg:
            module_name = f"{base_package}.{name}.handler"
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                if "No module named" not in str(e) or "handler" not in str(e):
                    print(f"Error loading {module_name}: {e}")
