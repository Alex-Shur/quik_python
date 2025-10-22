"""
Окно стакана заявок - порт FormOrderBook.cs на Python Qt6
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..models.quote import Quote


# Заглушка для OrderBook
class OrderBook:
    def __init__(self):
        self.bid = []
        self.offer = []
        self.server_time = ""


class OrderBookWindow(QWidget):
    """
    Окно для отображения стакана заявок
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_quotes: List[Quote] = []
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Стакан заявок")
        self.setGeometry(200, 200, 400, 600)
        
        # Основной layout
        layout = QVBoxLayout(self)
        
        # Заголовок
        self.header_label = QLabel("Тестовое окно стакана заявок")
        layout.addWidget(self.header_label)
        
        # Таблица стакана
        self.data_grid_view_order_book = QTableWidget()
        self.setup_table()
        layout.addWidget(self.data_grid_view_order_book)

    def setup_table(self):
        """Настройка таблицы стакана"""
        # Устанавливаем заголовки колонок
        headers = ["Тип", "Индекс", "Количество", "Цена"]
        self.data_grid_view_order_book.setColumnCount(len(headers))
        self.data_grid_view_order_book.setHorizontalHeaderLabels(headers)
        
        # Настройка внешнего вида
        font = QFont("Consolas", 9)
        self.data_grid_view_order_book.setFont(font)
        
        # Автоматическое изменение размера колонок
        header = self.data_grid_view_order_book.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Запрет редактирования
        self.data_grid_view_order_book.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Выделение целой строки
        self.data_grid_view_order_book.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def renew(self, order_book):
        """
        Обновить данные стакана
        
        Args:
            order_book: Объект стакана заявок или None для тестирования
        """
        if order_book is None:
            # Создаем тестовые данные
            self.list_quotes = [
                Quote("offer", 0, 100, 150.50),
                Quote("offer", 1, 200, 150.25),
                Quote("bid", 0, 150, 150.00),
                Quote("bid", 1, 300, 149.75),
            ]
            server_time = "Test Data"
        else:
            self.list_quotes = []
            # Добавляем котировки продажи (offer) - в обратном порядке
            if hasattr(order_book, 'offer') and order_book.offer and len(order_book.offer) > 0:
                for y in range(len(order_book.offer) - 1, -1, -1):
                    quote = Quote(
                        quote_type="offer",
                        index=y,
                        qty=int(order_book.offer[y].quantity) if hasattr(order_book.offer[y], 'quantity') and order_book.offer[y].quantity else 0,
                        price=float(order_book.offer[y].price) if hasattr(order_book.offer[y], 'price') and order_book.offer[y].price else 0.0
                    )
                    self.list_quotes.append(quote)

            # Добавляем котировки покупки (bid) - в обратном порядке  
            if hasattr(order_book, 'bid') and order_book.bid and len(order_book.bid) > 0:
                for y in range(len(order_book.bid) - 1, -1, -1):
                    quote = Quote(
                        quote_type="bid",
                        index=y,
                        qty=int(order_book.bid[y].quantity) if hasattr(order_book.bid[y], 'quantity') and order_book.bid[y].quantity else 0,
                        price=float(order_book.bid[y].price) if hasattr(order_book.bid[y], 'price') and order_book.bid[y].price else 0.0
                    )
                    self.list_quotes.append(quote)

            server_time = order_book.server_time if hasattr(order_book, 'server_time') and order_book.server_time else "N/A"
        
        # Обновляем заголовок окна
        self.setWindowTitle(f"Стакан на: {server_time}")
        
        # Обновляем таблицу
        self.update_table()

    def update_table(self):
        """Обновить таблицу с данными котировок"""
        # Устанавливаем количество строк
        self.data_grid_view_order_book.setRowCount(len(self.list_quotes))
        
        # Заполняем таблицу данными
        for row, quote in enumerate(self.list_quotes):
            # Тип котировки
            type_item = QTableWidgetItem(quote.type)
            if quote.type == "offer":
                type_item.setBackground(Qt.GlobalColor.lightGray)
            else:
                type_item.setBackground(Qt.GlobalColor.white)
            self.data_grid_view_order_book.setItem(row, 0, type_item)
            
            # Индекс
            index_item = QTableWidgetItem(str(quote.index))
            self.data_grid_view_order_book.setItem(row, 1, index_item)
            
            # Количество
            qty_item = QTableWidgetItem(str(quote.qty))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.data_grid_view_order_book.setItem(row, 2, qty_item)
            
            # Цена
            price_item = QTableWidgetItem(f"{quote.price:.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.data_grid_view_order_book.setItem(row, 3, price_item)
            
            # Цветовое выделение для разных типов котировок
            if quote.type == "offer":
                for col in range(4):
                    item = self.data_grid_view_order_book.item(row, col)
                    if item:
                        item.setBackground(Qt.GlobalColor.lightGray)
