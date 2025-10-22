"""
QuikPython Demo - Python порт демо-приложения QuikSharp с использованием PyQt6

Этот пакет содержит портированную версию QuikSharpDemo, 
демонстрирующую возможности работы с QUIK через Python.
"""

__version__ = "1.0.0"
__author__ = "QuikPython Team"
__email__ = "info@quikpython.demo"
__license__ = "Apache-2.0"

# Ленивый импорт main функции
def main():
    """Точка входа приложения"""
    from .main import main as _main
    return _main()

__all__ = ["main", "__version__"]
