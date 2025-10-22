"""
Окно отображения исторических данных (свечей).
Аналог части функциональности из оригинального C# проекта.
"""

import asyncio
from typing import Optional, List
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox,
    QSpinBox, QGroupBox, QHeaderView, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from quik_python.data_structures.candle import Candle, CandleInterval
from quik_python import Quik


class CandleWorker(QThread):
    """Worker thread для получения исторических данных"""
    
    data_ready = pyqtSignal(list)  # Данные готовы
    error_occurred = pyqtSignal(str)  # Ошибка получения данных
    progress_updated = pyqtSignal(int, str)  # Прогресс загрузки
    
    def __init__(self, quik : Quik, class_code, sec_code, client_code, count, interval, tag, main_loop):
        super().__init__()
        self.quik = quik
        self.class_code = class_code
        self.sec_code = sec_code
        self.client_code = client_code
        self.count = count
        self.interval = interval
        self.tag = tag
        self.main_loop = main_loop  # Основной event loop приложения
        self._is_cancelled = False
    
    def cancel(self):
        """Отменить загрузку данных"""
        self._is_cancelled = True
    
    def run(self):
        """Получение исторических данных в отдельном потоке"""
        try:
            # Используем основной event loop приложения через run_coroutine_threadsafe
            future = asyncio.run_coroutine_threadsafe(self._get_candles_async(), self.main_loop)
            result = future.result(timeout=30)  # Ждем максимум 30 секунд
            
            if not self._is_cancelled and result:
                self.data_ready.emit(result)
                
        except asyncio.TimeoutError:
            if not self._is_cancelled:
                self.error_occurred.emit("Превышен таймаут ожидания данных (30 секунд)")
        except Exception as e:
            if not self._is_cancelled:
                self.error_occurred.emit(str(e))
    
    async def _get_candles_async(self):
        """Асинхронное получение свечей"""
        try:
            self.progress_updated.emit(10, "Подключение к QUIK...")
            
            if self._is_cancelled:
                return None
            
            self.progress_updated.emit(30, "Запрос исторических данных...")
            
            # Получаем исторические данные
            candles = await self.quik.candles.get_last_candles(
                class_code=self.class_code,
                sec_code=self.sec_code,
                interval=self.interval,
                count=self.count
            )
            
            if self._is_cancelled:
                return None
            
            self.progress_updated.emit(70, "Обработка данных...")
            
            if candles:
                self.progress_updated.emit(100, "Данные получены")
                return candles
            else:
                self.error_occurred.emit("Не удалось получить исторические данные")
                return []
                
        except Exception as e:
            self.error_occurred.emit(f"Ошибка получения данных: {str(e)}")
            return []


class CandlesWindow(QMainWindow):
    """Окно для отображения исторических данных (свечей)"""
    
    def __init__(self, quik, class_code, sec_code, client_code, main_loop, tag=""):
        super().__init__()
        self.quik = quik
        self.class_code = class_code
        self.sec_code = sec_code
        self.client_code = client_code
        self.tag = tag
        self.main_loop = main_loop  # Основной event loop приложения
        self.candles_data: List[Candle] = []
        self.worker: Optional[CandleWorker] = None
        
        self.init_ui()
        
    def init_ui(self):
        """Инициализация интерфейса"""
        title = f"Исторические данные: {self.sec_code} ({self.class_code})"
        if self.tag:
            title += f" [{self.tag}]"
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 1000, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        
        # Панель управления
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Таблица данных
        self.table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.table)
        
        # Панель информации
        info_panel = self.create_info_panel()
        main_layout.addWidget(info_panel)
    
    def create_control_panel(self) -> QWidget:
        """Создание панели управления"""
        panel = QGroupBox("Параметры запроса")
        layout = QGridLayout(panel)
        
        # Количество свечей
        layout.addWidget(QLabel("Количество свечей:"), 0, 0)
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setRange(1, 10000)
        self.count_spinbox.setValue(100)
        layout.addWidget(self.count_spinbox, 0, 1)
        
        # Интервал
        layout.addWidget(QLabel("Интервал:"), 0, 2)
        self.interval_combo = QComboBox()
        intervals = [
            ("1 минута", CandleInterval.M1),
            ("5 минут", CandleInterval.M5), 
            ("15 минут", CandleInterval.M15),
            ("30 минут", CandleInterval.M30),
            ("1 час", CandleInterval.H1),
            ("4 часа", CandleInterval.H4),
            ("1 день", CandleInterval.D1),
            ("1 неделя", CandleInterval.W1),
            ("1 месяц", CandleInterval.MN)
        ]
        
        for name, value in intervals:
            self.interval_combo.addItem(name, value)
        
        # По умолчанию 15 минут
        self.interval_combo.setCurrentIndex(2)
        layout.addWidget(self.interval_combo, 0, 3)
        
        # Кнопка загрузки
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button, 0, 4)
        
        # Кнопка отмены
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.cancel_loading)
        self.cancel_button.setEnabled(False)
        layout.addWidget(self.cancel_button, 0, 5)
        
        # Кнопка обновления
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.refresh_data)
        self.refresh_button.setEnabled(False)
        layout.addWidget(self.refresh_button, 1, 4)
        
        # Кнопка экспорта
        self.export_button = QPushButton("Экспорт в CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.export_button.setEnabled(False)
        layout.addWidget(self.export_button, 1, 5)
        
        return panel
    
    def create_info_panel(self) -> QWidget:
        """Создание информационной панели"""
        panel = QGroupBox("Информация")
        layout = QHBoxLayout(panel)
        
        self.info_label = QLabel("Данные не загружены")
        layout.addWidget(self.info_label)
        
        # Растягиваем
        layout.addStretch()
        
        return panel
    
    def setup_table(self):
        """Настройка таблицы"""
        headers = [
            "DateTime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Настройка заголовков
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Дата
        for i in range(1, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        # Стиль таблицы
        font = QFont("Consolas", 9)
        self.table.setFont(font)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def load_data(self):
        """Загрузка исторических данных"""
        if self.worker and self.worker.isRunning():
            return
        
        count = self.count_spinbox.value()
        interval_data = self.interval_combo.currentData()
        
        # Создаем worker для загрузки данных
        self.worker = CandleWorker(
            self.quik, self.class_code, self.sec_code, 
            self.client_code, count, interval_data, self.tag, self.main_loop
        )
        
        # Подключаем сигналы
        self.worker.data_ready.connect(self.on_data_ready)
        self.worker.error_occurred.connect(self.on_error_occurred)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.finished.connect(self.on_loading_finished)
        
        # Обновляем UI
        self.load_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Запускаем загрузку
        self.worker.start()
    
    def cancel_loading(self):
        """Отмена загрузки данных"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.quit()
            self.worker.wait(3000)  # Ждем до 3 секунд
    
    def refresh_data(self):
        """Обновление данных"""
        self.load_data()
    
    def on_data_ready(self, candles_data):
        """Обработчик получения данных"""
        self.candles_data = candles_data
        self.populate_table()
        self.update_info()
        
        # Включаем кнопки
        self.refresh_button.setEnabled(True)
        self.export_button.setEnabled(True)
    
    def on_error_occurred(self, error_message):
        """Обработчик ошибки"""
        QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных:\n{error_message}")
        self.info_label.setText(f"Ошибка: {error_message}")
    
    def on_progress_updated(self, value, message):
        """Обработчик обновления прогресса"""
        self.progress_bar.setValue(value)
        self.info_label.setText(message)
    
    def on_loading_finished(self):
        """Обработчик завершения загрузки"""
        self.load_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def populate_table(self):
        """Заполнение таблицы данными"""
        if not self.candles_data:
            return
        
        self.table.setRowCount(len(self.candles_data))
        
        for row, candle in enumerate(self.candles_data):
            # Дата/время
            dt_item = QTableWidgetItem(candle.datetime.to_datetime().strftime("%Y-%m-%d %H:%M:%S"))
            dt_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, dt_item)
            
            # Цены
            for col, key in enumerate(['open', 'high', 'low', 'close'], 1):
                price_item = QTableWidgetItem(f"{getattr(candle, key):.4f}")
                price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, price_item)
            
            # Объем
            volume_item = QTableWidgetItem(str(getattr(candle, 'volume', 0)))
            volume_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, volume_item)
            
    
    def update_info(self):
        """Обновление информационной панели"""
        if not self.candles_data:
            self.info_label.setText("Данные не загружены")
            return
        
        count = len(self.candles_data)
        if count > 0:
            first_candle = self.candles_data[0]
            last_candle = self.candles_data[-1]
            
            info_text = (f"Загружено {count} свечей. "
                        f"Период: {first_candle.datetime.to_datetime().strftime('%Y-%m-%d %H:%M')} - "
                        f"{last_candle.datetime.to_datetime().strftime('%Y-%m-%d %H:%M')}")
            self.info_label.setText(info_text)
    
    def export_to_csv(self):
        """Экспорт данных в CSV файл"""
        if not self.candles_data:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для экспорта")
            return
        
        try:
            from PyQt6.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Сохранить как CSV", 
                f"{self.sec_code}_{self.class_code}_candles.csv",
                "CSV files (*.csv)"
            )
            
            if filename:
                import csv
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    
                    # Заголовки
                    writer.writerow([
                        'DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'
                    ])
                    
                    # Данные
                    for candle in self.candles_data:
                        writer.writerow([
                            candle.datetime.to_datetime().strftime('%Y-%m-%d %H:%M:%S'),
                            candle.open,
                            candle.high,
                            candle.low,
                            candle.close,
                            candle.volume
                        ])
                
                QMessageBox.information(self, "Экспорт", f"Данные сохранены в файл:\n{filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка экспорта:\n{str(e)}")
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.quit()
            self.worker.wait(3000)
        event.accept()
