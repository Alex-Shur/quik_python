#!/usr/bin/env python3
"""
Главный файл приложения QuikPythonDemo - порт Program.cs на Python Qt6

Точка входа для приложения QuikPython Demo.
"""

import sys
import os
import locale
from pathlib import Path

# Импорты Qt6
try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print("Ошибка импорта PyQt6. Убедитесь, что PyQt6 установлен:")
    print("pip install PyQt6")
    print(f"Детали ошибки: {e}")
    sys.exit(1)

# Импорт главного окна
try:
    from quik_python_demo.ui.main_window import MainWindow
except ImportError as e:
    print(f"Ошибка импорта главного окна: {e}")
    sys.exit(1)


def setup_locale():
    """Настройка локали для корректной работы с десятичными разделителями"""
    try:
        # Пытаемся установить русскую локаль
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    except locale.Error:
        try:
            # Если русская не доступна, пытаемся системную
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            # В крайнем случае используем C локаль
            locale.setlocale(locale.LC_ALL, 'C')


def setup_qt_application():
    """Настройка Qt приложения"""
    # Включаем High DPI масштабирование
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Создаем приложение
    app = QApplication(sys.argv)
    
    # Настройки приложения
    app.setApplicationName("QuikPython Demo")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("QuikPython")
    app.setOrganizationDomain("quikpython.demo")
    
    # Установка иконки приложения (если есть)
    project_root = Path(__file__).parent.parent  # Поднимаемся на уровень выше из quik_python_demo/
    icon_path = project_root / "resources" / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    return app


def main():
    """
    Главная функция приложения
    """
    print("QuikPython Demo - запуск приложения...")
    
    # Настройка локали
    setup_locale()
    
    # Проверяем наличие необходимых модулей
    try:
        import asyncio
        print("asyncio доступен")
    except ImportError:
        QMessageBox.critical(None, "Ошибка", "Модуль asyncio недоступен. Требуется Python 3.7+")
        return 1
    
    # Создаем Qt приложение
    try:
        app = setup_qt_application()
    except Exception as e:
        print(f"Ошибка создания Qt приложения: {e}")
        return 1
    
    # Создаем и показываем главное окно
    try:
        main_window = MainWindow()
        main_window.show()
        
        print("QuikPython Demo успешно запущен")
        print("Главное окно создано и отображено")
        
        # Запускаем главный цикл приложения
        return app.exec()
        
    except Exception as e:
        error_msg = f"Ошибка создания главного окна: {e}"
        print(error_msg)
        
        # Показываем ошибку пользователю если Qt доступен
        try:
            QMessageBox.critical(None, "Критическая ошибка", error_msg)
        except:
            pass
            
        return 1


if __name__ == "__main__":
    """
    Точка входа при запуске файла напрямую
    """
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nПриложение прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
