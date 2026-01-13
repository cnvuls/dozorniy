import importlib
import os
import pkgutil


def autodiscover_features(base_package: str = "user_app.features"):
    """
    Ищет и импортирует модули в папке features.

    :param base_package: Путь импорта для Python (например, "user_app.features")
    """
    # 1. Определяем, где лежит этот файл (loader.py) -> .../src/user_app/core/
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Поднимаемся на уровень выше -> .../src/user_app/
    user_app_root = os.path.dirname(current_dir)

    # 3. Формируем путь к физической папке "features"
    # ВАЖНО: На диске папка называется просто "features"
    features_path = os.path.join(user_app_root, "features")

    # Для отладки (можешь убрать потом)
    # print(f"[Loader] Looking for features in: {features_path}")

    if not os.path.exists(features_path):
        print(f"⚠️  Feature folder not found at: {features_path}")
        return

    # Проходим по всем подпапкам в features
    for _, name, is_pkg in pkgutil.iter_modules([features_path]):
        print(is_pkg)
        if is_pkg:
            # Формируем Python-путь для импорта: user_app.features.shell.handler
            module_name = f"{base_package}.{name}.handler"
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                # Часто бывает, что папка есть, а handler.py в ней нет — это нормально
                # Но если ошибка внутри handler.py, её полезно видеть
                if "No module named" not in str(e) or "handler" not in str(e):
                    print(f"❌ Error loading {module_name}: {e}")
