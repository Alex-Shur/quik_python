"""
Окно для отображения таблиц - порт FormOutputTable.cs на Python Qt6
"""

from typing import List, Any
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'quik_python'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class OutputTableWindow(QWidget):
    """
    Окно для отображения различных таблиц данных
    """

    def __init__(self, title: str = "Таблица данных", parent=None):
        super().__init__(parent)
        self.window_title = title
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle(self.window_title)
        self.setGeometry(200, 200, 800, 600)
        
        # Основной layout
        layout = QVBoxLayout(self)
        
        # Таблица данных
        self.data_grid_view = QTableWidget()
        self.setup_table()
        layout.addWidget(self.data_grid_view)

    def setup_table(self):
        """Настройка таблицы"""
        # Настройка внешнего вида
        font = QFont("Consolas", 9)
        self.data_grid_view.setFont(font)
        
        # Автоматическое изменение размера колонок
        header = self.data_grid_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # Запрет редактирования
        self.data_grid_view.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Выделение целой строки
        self.data_grid_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def set_data(self, data: List[Any], headers: List[str] = None):
        """
        Установить данные в таблицу
        
        Args:
            data: Список объектов для отображения
            headers: Список заголовков колонок (опционально)
        """
        if not data:
            self.data_grid_view.setRowCount(0)
            self.data_grid_view.setColumnCount(0)
            return
            
        # Если данные - это список словарей
        if isinstance(data[0], dict):
            self.set_data_from_dicts(data, headers)
        # Если данные - это объекты с атрибутами
        else:
            self.set_data_from_objects(data, headers)

    def set_data_from_dicts(self, data: List[dict], headers: List[str] = None):
        """Установить данные из списка словарей"""
        if not data:
            return
            
        # Получаем ключи из первого элемента если заголовки не заданы
        if headers is None:
            headers = list(data[0].keys())
        
        # Настраиваем таблицу
        self.data_grid_view.setRowCount(len(data))
        self.data_grid_view.setColumnCount(len(headers))
        self.data_grid_view.setHorizontalHeaderLabels(headers)
        
        # Заполняем данными
        for row, item in enumerate(data):
            for col, header in enumerate(headers):
                value = item.get(header, "")
                cell_item = QTableWidgetItem(str(value))
                
                # Выравнивание для числовых значений
                if isinstance(value, (int, float)):
                    cell_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    
                self.data_grid_view.setItem(row, col, cell_item)

    def set_data_from_objects(self, data: List[Any], headers: List[str] = None):
        """Установить данные из списка объектов"""
        if not data:
            return
            
        # Получаем атрибуты из первого объекта если заголовки не заданы
        first_obj = data[0]
        if headers is None:
            if hasattr(first_obj, '__dict__'):
                headers = [attr for attr in dir(first_obj) 
                          if not attr.startswith('_') and not callable(getattr(first_obj, attr))]
            else:
                headers = ["Value"]
        
        # Настраиваем таблицу
        self.data_grid_view.setRowCount(len(data))
        self.data_grid_view.setColumnCount(len(headers))
        self.data_grid_view.setHorizontalHeaderLabels(headers)
        
        # Заполняем данными
        for row, item in enumerate(data):
            for col, header in enumerate(headers):
                try:
                    if hasattr(item, header):
                        value = getattr(item, header)
                    else:
                        value = str(item)
                        
                    cell_item = QTableWidgetItem(str(value))
                    
                    # Выравнивание для числовых значений
                    if isinstance(value, (int, float)):
                        cell_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                        
                    self.data_grid_view.setItem(row, col, cell_item)
                except Exception:
                    # В случае ошибки просто ставим пустое значение
                    self.data_grid_view.setItem(row, col, QTableWidgetItem(""))

    def set_title(self, title: str):
        """Установить заголовок окна"""
        self.window_title = title
        self.setWindowTitle(title)

    def clear_data(self):
        """Очистить данные таблицы"""
        self.data_grid_view.setRowCount(0)
        self.data_grid_view.setColumnCount(0)
