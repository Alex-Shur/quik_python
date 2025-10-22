"""
Конфигурация тестов для pytest
"""

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Переменные для тестирования
TEST_QUIK_HOST = "127.0.0.1"
TEST_QUIK_PORT = 34130
TEST_CHART_TAG = "si"
TEST_LABEL_PATH = "C:\\ClassesC\\Labels\\buy.bmp"
