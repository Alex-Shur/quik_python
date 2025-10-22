"""
Главное окно приложения - порт FormMain.cs на Python Qt6
"""

import sys
import asyncio
import locale
import threading
from typing import Optional, List
from datetime import datetime
from decimal import Decimal, getcontext

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget,
    QCheckBox, QComboBox, QTabWidget, QGroupBox
)
from PyQt6.QtCore import QTimer, pyqtSignal, QObject, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from quik_python.data_structures.param_names import ParamNames


class AsyncRunner(QObject):
    """Helper class for running async operations and emitting signals"""
    finished = pyqtSignal(object)  # Результат выполнения
    error = pyqtSignal(str)        # Ошибка выполнения
    
    # Сигналы для управления таймером из других потоков
    start_timer = pyqtSignal()
    stop_timer = pyqtSignal()
    
    # Сигналы для обновления UI
    update_connection_status = pyqtSignal(bool)
    update_client_codes = pyqtSignal(list)
    update_accounts = pyqtSignal(list)
    update_instrument_info = pyqtSignal(dict)
    update_position = pyqtSignal(float)  # Новый сигнал для обновления позиции
    update_price = pyqtSignal(str)       # Сигнал для обновления цены
    show_security_info = pyqtSignal(object)  # Сигнал для отображения информации о бумаге
    show_depo_limits = pyqtSignal(list)  # Сигнал для отображения депо лимитов
    show_depo_limits_all = pyqtSignal(list)  # Сигнал для отображения депо лимитов по всем бумагам
    show_futures_limits = pyqtSignal(object)  # Сигнал для отображения фьючерсных лимитов
    show_futures_client_holdings = pyqtSignal(list)  # Сигнал для отображения фьючерсных позиций клиентов
    show_orders = pyqtSignal(list)  # Сигнал для отображения таблицы заявок
    show_trades = pyqtSignal(list)  # Сигнал для отображения таблицы сделок
    show_all_trades = pyqtSignal(list)  # Сигнал для отображения таблицы обезличенных сделок
    show_portfolio_info_ex = pyqtSignal(list)  # Сигнал для отображения таблицы клиентского портфеля
    show_money_limits = pyqtSignal(list)  # Сигнал для отображения таблицы денежных лимитов
    show_money_limits_ex = pyqtSignal(list)  # Сигнал для отображения таблицы расширенных денежных лимитов
    show_buy_sell_info = pyqtSignal(list)  # Сигнал для отображения таблицы Купить/Продать
    show_order_book_window = pyqtSignal(object)  # Сигнал для отображения окна стакана заявок

# Импорты для работы с quik_python
from quik_python import Quik, InMemoryStorage
from quik_python.data_structures.order_book import OrderBook
from quik_python.data_structures.stop_order import StopOrder, OffsetUnits, StopOrderType, Condition
from quik_python.data_structures.candle import Candle
from quik_python.data_structures.order import Order
from quik_python.data_structures.trade import Trade
from quik_python.data_structures.all_trade import AllTrade
from quik_python.data_structures.security_info import SecurityInfo
from quik_python.data_structures.depo_limit_ex import DepoLimitEx, LimitKind
from quik_python.data_structures.futures_limits import FuturesLimits, FuturesLimitType
from quik_python.data_structures.futures_client_holding import FuturesClientHolding
from quik_python.data_structures.portfolio_info_ex import PortfolioInfoEx
from quik_python.data_structures.money_limit import MoneyLimit
from quik_python.data_structures.money_limit_ex import MoneyLimitEx
from quik_python.data_structures.buy_sell_info import BuySellInfo
from quik_python.data_structures.param import Param
from quik_python.data_structures.stop_order import StopOrder
from quik_python.data_structures.transaction import Transaction
from quik_python.data_structures.transaction_types import (
    TransactionAction, TransactionType, TransactionOperation, ExecutionCondition
)
from quik_python.data_structures.order import Operation

from .order_book_window import OrderBookWindow
from .output_table_window import OutputTableWindow
from .request_value_window import RequestValueWindow
from .candles_window import CandlesWindow


class MainWindow(QMainWindow):
    """
    Главное окно приложения - порт FormMain на Python Qt6
    """

    def __init__(self):
        super().__init__()
        
        # Настройка десятичного разделителя
        self.separator = locale.localeconv()['decimal_point']
        getcontext().prec = 28  # Настройка точности для Decimal
        
        # Создаем общий event loop для асинхронных операций
        self._loop = None
        self._loop_thread = None
        self.setup_async_loop()
        
        # Создаем таймер ПЕРЕД созданием AsyncRunner
        self.timer_renew_form = QTimer()
        self.timer_renew_form.timeout.connect(self.timer_renew_form_tick)
        self.timer_renew_form.setInterval(2000)  # Увеличиваем до 2 секунд для уменьшения нагрузки
        
        # Создаем AsyncRunner для thread-safe операций
        self.async_runner = AsyncRunner()
        self.async_runner.finished.connect(self.on_async_finished)
        self.async_runner.error.connect(self.on_async_error)
        
        # Подключаем сигналы управления таймером
        self.async_runner.start_timer.connect(self.timer_renew_form.start)
        self.async_runner.stop_timer.connect(self.timer_renew_form.stop)
        
        # Подключаем сигналы обновления UI
        self.async_runner.update_connection_status.connect(self.on_connection_status_updated)
        self.async_runner.update_client_codes.connect(self.on_client_codes_updated)
        self.async_runner.update_accounts.connect(self.on_accounts_updated)
        self.async_runner.update_instrument_info.connect(self.on_instrument_info_updated)
        self.async_runner.update_position.connect(self.on_position_updated)
        self.async_runner.update_price.connect(self.on_price_updated)  # Подключаем сигнал цены
        self.async_runner.show_security_info.connect(self.on_show_security_info)  # Подключаем сигнал информации о бумаге
        self.async_runner.show_depo_limits.connect(self.on_show_depo_limits)  # Подключаем сигнал депо лимитов
        self.async_runner.show_depo_limits_all.connect(self.on_show_depo_limits_all)  # Подключаем сигнал депо лимитов по всем бумагам
        self.async_runner.show_futures_limits.connect(self.on_show_futures_limits)  # Подключаем сигнал фьючерсных лимитов
        self.async_runner.show_futures_client_holdings.connect(self.on_show_futures_client_holdings)  # Подключаем сигнал фьючерсных позиций клиентов
        self.async_runner.show_orders.connect(self.on_show_orders)  # Подключаем сигнал таблицы заявок
        self.async_runner.show_trades.connect(self.on_show_trades)  # Подключаем сигнал таблицы сделок
        self.async_runner.show_all_trades.connect(self.on_show_all_trades)  # Подключаем сигнал таблицы обезличенных сделок
        self.async_runner.show_portfolio_info_ex.connect(self.on_show_portfolio_info_ex)  # Подключаем сигнал таблицы клиентского портфеля
        self.async_runner.show_money_limits.connect(self.on_show_money_limits)  # Подключаем сигнал таблицы денежных лимитов
        self.async_runner.show_money_limits_ex.connect(self.on_show_money_limits_ex)  # Подключаем сигнал таблицы расширенных денежных лимитов
        self.async_runner.show_buy_sell_info.connect(self.on_show_buy_sell_info)  # Подключаем сигнал таблицы Купить/Продать
        self.async_runner.show_order_book_window.connect(self.on_show_order_book_window)  # Подключаем сигнал окна стакана заявок
        
        # Переменные состояния
        self.quik: Optional[Quik] = None
        self.is_server_connected = False
        self.is_subscribed_tool_order_book = False
        self.is_subscribed_tool_candles = False
        self.is_subscribed_param = False  # Флаг подписки на параметры
        
        # Параметры инструмента
        self.sec_code = "SBER"
        self.class_code = "QJSIM"
        # self.sec_code = "SiH6"
        # self.class_code = "SPBFUT"
        self.client_code = ""
        
        # Данные по инструменту
        self.bid: Optional[Decimal] = None
        self.offer: Optional[Decimal] = None
        self.tool = None
        self.tool_order_book: Optional[OrderBook] = None
        self.tool_candles: List[Candle] = []
        
        # Списки данных
        self.list_orders: List[Order] = []
        self.list_trades: List[Trade] = []
        self.list_all_trades: List[AllTrade] = []
        self.list_security_info: List[SecurityInfo] = []
        self.list_depo_limits: List[DepoLimitEx] = []
        self.list_futures_limits: List[FuturesLimits] = []
        self.list_futures_client_holdings: List[FuturesClientHolding] = []
        self.list_portfolio: List[PortfolioInfoEx] = []
        self.list_money_limits: List[MoneyLimit] = []
        self.list_money_limits_ex: List[MoneyLimitEx] = []
        self.list_buy_sell_info: List[BuySellInfo] = []
        
        # Дополнительные окна
        self.tool_candles_table: Optional[OutputTableWindow] = None
        self.tool_order_book_table: Optional[OrderBookWindow] = None
        self.tool_order_book_table1: Optional[OrderBookWindow] = None
        self.tool_security_info_table: Optional[OutputTableWindow] = None
        self.tool_depo_limits_table: Optional[OutputTableWindow] = None
        self.tool_depo_limits_all_table: Optional[OutputTableWindow] = None
        self.tool_futures_limits_table: Optional[OutputTableWindow] = None
        self.tool_futures_client_holdings_table: Optional[OutputTableWindow] = None
        self.tool_orders_table: Optional[OutputTableWindow] = None
        self.tool_trades_table: Optional[OutputTableWindow] = None
        self.tool_all_trades_table: Optional[OutputTableWindow] = None
        self.tool_portfolio_info_ex_table: Optional[OutputTableWindow] = None
        self.tool_money_limits_table: Optional[OutputTableWindow] = None
        self.tool_money_limits_ex_table: Optional[OutputTableWindow] = None
        self.tool_buy_sell_info_table: Optional[OutputTableWindow] = None
        self.request_value: Optional[RequestValueWindow] = None
        self.candles_window: Optional[CandlesWindow] = None
        
        # Данные заявок и позиций
        self.order: Optional[Order] = None
        self.fut_limit: Optional[FuturesLimits] = None
        self.futures_position: Optional[FuturesClientHolding] = None
        
        # Время обновления стакана
        self.renew_order_book_time: Optional[datetime] = None
        
        # Флаг для предотвращения одновременных запросов позиции
        self._updating_position = False
        
        # Флаг состояния приложения
        self._is_closing = False
        
        # Инициализация UI
        self.init_ui()
        self.init_controls()

    def setup_async_loop(self):
        """Настройка общего event loop для асинхронных операций"""
        def run_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        
        self._loop_thread = threading.Thread(target=run_loop, daemon=True)
        self._loop_thread.start()
        
        # Ждем пока loop будет готов
        while self._loop is None:
            threading.Event().wait(0.01)
    
    def run_async_task(self, coro):
        """Запустить корутину в общем event loop"""
        if self._loop and not self._loop.is_closed():
            future = asyncio.run_coroutine_threadsafe(coro, self._loop)
            return future
        else:
            self.append_text_to_logs("Ошибка: Event loop недоступен")
            return None
    
    def closeEvent(self, event):
        """Обработчик закрытия окна - закрываем event loop и все дочерние окна"""
        self._is_closing = True
        try:
            # Закрываем все дочерние окна
            self.close_all_windows()
            
            # Закрываем event loop
            if self._loop and not self._loop.is_closed():
                self._loop.call_soon_threadsafe(self._loop.stop)
        except Exception as e:
            print(f"Ошибка при закрытии приложения: {e}")
        finally:
            super().closeEvent(event)
    
    def close_all_windows(self):
        """Закрыть все дочерние окна"""
        try:
            windows_to_close = [
                self.tool_order_book_table,
                self.tool_order_book_table1,
                self.tool_candles_table,
                self.tool_security_info_table,
                self.tool_depo_limits_table,
                self.tool_depo_limits_all_table,
                self.tool_futures_limits_table,
                self.tool_futures_client_holdings_table,
                self.tool_orders_table,
                self.tool_trades_table,
                self.tool_all_trades_table,
                self.tool_portfolio_info_ex_table,
                self.tool_money_limits_table,
                self.tool_money_limits_ex_table,
                self.tool_buy_sell_info_table,
                self.request_value,
                self.candles_window
            ]
            
            for window in windows_to_close:
                if window is not None:
                    try:
                        window.close()
                    except:
                        pass  # Игнорируем ошибки при закрытии
        except Exception:
            pass  # Игнорируем ошибки
    
    def on_async_finished(self, result):
        """Обработчик успешного завершения асинхронной операции"""
        # Результат уже обработан в самой корутине
        pass
    
    def on_async_error(self, error_message):
        """Обработчик ошибки асинхронной операции"""
        self.append_text_to_logs(f"Асинхронная ошибка: {error_message}")
    
    def on_connection_status_updated(self, is_connected):
        """Thread-safe обновление статуса подключения"""
        if is_connected:
            self.button_run.setEnabled(True)
            self.button_start.setEnabled(False)
        else:
            self.button_run.setEnabled(False)
            self.button_start.setEnabled(True)
    
    def on_client_codes_updated(self, codes):
        """Thread-safe обновление кодов клиентов"""
        self.combo_box_client_code.clear()
        for code in codes:
            self.combo_box_client_code.addItem(code)
        if self.combo_box_client_code.count() > 0:
            self.combo_box_client_code.setCurrentIndex(0)
            self.client_code = self.combo_box_client_code.currentText()
    
    def on_accounts_updated(self, accounts):
        """Thread-safe обновление торговых аккаунтов"""
        for account in accounts:
            self.append_text_to_logs(f"Найден аккаунт: firmID-{account.firm_id}, TrdaccId-{account.trd_acc_id}, MainTrdaccid-{account.main_trd_acc_id}")
    
    def on_instrument_info_updated(self, tool_info):
        """Thread-safe обновление информации об инструменте"""
        self.tool = tool_info
        if self.tool:
            self.text_box_account_id.setText(self.tool.get('account_id', ''))
            self.text_box_firm_id.setText(self.tool.get('firm_id', ''))
            self.text_box_short_name.setText(self.tool.get('name', ''))
            self.text_box_lot.setText(str(self.tool.get('lot', '')))
            self.text_box_step.setText(str(self.tool.get('step', '')))
            self.text_box_guarantee_providing.setText(str(self.tool.get('guarantee_providing', '')))
            self.text_box_last_price.setText(str(self.tool.get('last_price', '')))

    def on_position_updated(self, position):
        """Thread-safe обновление позиции"""
        self.text_box_qty.setText(str(position))

    @pyqtSlot(str)
    def on_price_updated(self, price):
        """Thread-safe обновление цены"""
        self.text_box_last_price.setText(price)

    @pyqtSlot(object)
    def on_show_security_info(self, security_info):
        """Thread-safe отображение информации о бумаге"""
        if security_info:
            # Создаем список с одним элементом для совместимости с OutputTableWindow
            self.list_security_info = [security_info]
            
            self.append_text_to_logs("Выводим данные в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_security_info_table') or self.tool_security_info_table is None:
                self.tool_security_info_table = OutputTableWindow("Информация по бумаге")
                self.tool_security_info_table.set_data(self.list_security_info)
            else:
                self.tool_security_info_table.set_data(self.list_security_info)
                
            self.tool_security_info_table.show()
        else:
            tool_name = self.tool.get('name', self.sec_code) if self.tool else self.sec_code
            self.append_text_to_logs(f"Информация по бумаге '{tool_name}' отсутствует.")

    @pyqtSlot(list)
    def on_show_depo_limits(self, depo_limits):
        """Thread-safe отображение депо лимитов"""
        if depo_limits and len(depo_limits) > 0:
            # Сохраняем список лимитов
            self.list_depo_limits = depo_limits
            
            self.append_text_to_logs("Выводим данные лимитов в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_depo_limits_table') or self.tool_depo_limits_table is None:
                self.tool_depo_limits_table = OutputTableWindow("Таблица лимитов по бумаге")
                self.tool_depo_limits_table.set_data(self.list_depo_limits)
            else:
                self.tool_depo_limits_table.set_data(self.list_depo_limits)
                
            self.tool_depo_limits_table.show()
        else:
            tool_name = self.tool.get('name', self.sec_code) if self.tool else self.sec_code
            self.append_text_to_logs(f"Бумага '{tool_name}' в таблице лимитов отсутствует.")

    @pyqtSlot(list)
    def on_show_depo_limits_all(self, depo_limits):
        """Thread-safe отображение депо лимитов по всем бумагам"""
        if depo_limits and len(depo_limits) > 0:
            # Сохраняем список лимитов
            self.list_depo_limits = depo_limits
            
            self.append_text_to_logs("Выводим данные лимитов по всем бумагам в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_depo_limits_all_table') or self.tool_depo_limits_all_table is None:
                self.tool_depo_limits_all_table = OutputTableWindow("Таблица лимитов по всем бумагам")
                self.tool_depo_limits_all_table.set_data(self.list_depo_limits)
            else:
                self.tool_depo_limits_all_table.set_data(self.list_depo_limits)
                
            self.tool_depo_limits_all_table.show()
        else:
            self.append_text_to_logs("Таблица лимитов по всем бумагам пуста.")

    @pyqtSlot(object)
    def on_show_futures_limits(self, futures_limit):
        """Thread-safe отображение фьючерсных лимитов"""
        if futures_limit is not None:
            self.append_text_to_logs("Выводим данные фьючерсных лимитов в таблицу...")
            
            # Создаем список для отображения в таблице
            futures_limits_list = [futures_limit]
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_futures_limits_table') or self.tool_futures_limits_table is None:
                self.tool_futures_limits_table = OutputTableWindow("Таблица фьючерсных лимитов")
                self.tool_futures_limits_table.set_data(futures_limits_list)
            else:
                self.tool_futures_limits_table.set_data(futures_limits_list)
                
            self.tool_futures_limits_table.show()
        else:
            self.append_text_to_logs("Фьючерсный лимит отсутствует.")

    @pyqtSlot(list)
    def on_show_futures_client_holdings(self, futures_client_holdings):
        """Thread-safe отображение фьючерсных позиций клиентов"""
        if futures_client_holdings and len(futures_client_holdings) > 0:
            self.append_text_to_logs("Выводим данные по фьючерсным позициям в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_futures_client_holdings_table') or self.tool_futures_client_holdings_table is None:
                self.tool_futures_client_holdings_table = OutputTableWindow("Таблица позиций по клиентским счетам (фьючерсы)")
                self.tool_futures_client_holdings_table.set_data(futures_client_holdings)
            else:
                self.tool_futures_client_holdings_table.set_data(futures_client_holdings)
                
            self.tool_futures_client_holdings_table.show()
        else:
            self.append_text_to_logs("Таблица фьючерсных позиций пуста.")

    @pyqtSlot(list)
    def on_show_orders(self, orders):
        """Thread-safe отображение таблицы заявок"""
        if orders and len(orders) > 0:
            self.append_text_to_logs("Выводим данные о заявках в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_orders_table') or self.tool_orders_table is None:
                self.tool_orders_table = OutputTableWindow("Таблица заявок")
                self.tool_orders_table.set_data(orders)
            else:
                self.tool_orders_table.set_data(orders)
                
            self.tool_orders_table.show()
        else:
            self.append_text_to_logs("Таблица заявок пуста.")

    def on_show_trades(self, trades):
        """Thread-safe отображение таблицы сделок"""
        if trades and len(trades) > 0:
            self.append_text_to_logs("Выводим данные о сделках в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_trades_table') or self.tool_trades_table is None:
                self.tool_trades_table = OutputTableWindow("Таблица сделок")
                self.tool_trades_table.set_data(trades)
            else:
                self.tool_trades_table.set_data(trades)
                
            self.tool_trades_table.show()
        else:
            self.append_text_to_logs("Таблица сделок пуста.")

    def on_show_all_trades(self, all_trades):
        """Thread-safe отображение таблицы обезличенных сделок"""
        if all_trades and len(all_trades) > 0:
            self.append_text_to_logs("Выводим данные о обезличенных сделках в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_all_trades_table') or self.tool_all_trades_table is None:
                self.tool_all_trades_table = OutputTableWindow("Таблица обезличенных сделок")
                self.tool_all_trades_table.set_data(all_trades)
            else:
                self.tool_all_trades_table.set_data(all_trades)
                
            self.tool_all_trades_table.show()
        else:
            self.append_text_to_logs("Таблица обезличенных сделок пуста.")

    def on_show_portfolio_info_ex(self, portfolio_info):
        """Thread-safe отображение таблицы клиентского портфеля"""
        if portfolio_info and len(portfolio_info) > 0:
            self.append_text_to_logs("Выводим данные о портфеле в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_portfolio_info_ex_table') or self.tool_portfolio_info_ex_table is None:
                self.tool_portfolio_info_ex_table = OutputTableWindow("Таблица `Клиентский портфель`")
                self.tool_portfolio_info_ex_table.set_data(portfolio_info)
            else:
                self.tool_portfolio_info_ex_table.set_data(portfolio_info)
                
            self.tool_portfolio_info_ex_table.show()
        else:
            self.append_text_to_logs("В таблице `Клиентский портфель` отсутствуют записи.")

    def on_show_money_limits(self, money_limits):
        """Thread-safe отображение таблицы денежных лимитов"""
        if money_limits and len(money_limits) > 0:
            self.append_text_to_logs("Выводим данные о денежных лимитах в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_money_limits_table') or self.tool_money_limits_table is None:
                self.tool_money_limits_table = OutputTableWindow("Таблица денежных лимитов")
                self.tool_money_limits_table.set_data(money_limits)
            else:
                self.tool_money_limits_table.set_data(money_limits)
                
            self.tool_money_limits_table.show()
        else:
            self.append_text_to_logs("Таблица денежных лимитов пуста.")

    def on_show_money_limits_ex(self, money_limits_ex):
        """Thread-safe отображение таблицы расширенных денежных лимитов"""
        if money_limits_ex and len(money_limits_ex) > 0:
            self.append_text_to_logs("Выводим данные о денежных лимитах в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_money_limits_ex_table') or self.tool_money_limits_ex_table is None:
                self.tool_money_limits_ex_table = OutputTableWindow("Таблица расширенных денежных лимитов")
                self.tool_money_limits_ex_table.set_data(money_limits_ex)
            else:
                self.tool_money_limits_ex_table.set_data(money_limits_ex)
                
            self.tool_money_limits_ex_table.show()
        else:
            self.append_text_to_logs("Таблица расширенных денежных лимитов пуста.")

    def on_show_buy_sell_info(self, buy_sell_info):
        """Thread-safe отображение таблицы Купить/Продать"""
        if buy_sell_info and len(buy_sell_info) > 0:
            self.append_text_to_logs("Выводим данные о параметрах Купить/Продать в таблицу...")
            
            # Создаем окно для отображения таблицы в главном потоке
            if not hasattr(self, 'tool_buy_sell_info_table') or self.tool_buy_sell_info_table is None:
                self.tool_buy_sell_info_table = OutputTableWindow("Таблица `Купить/Продать`")
                self.tool_buy_sell_info_table.set_data(buy_sell_info)
            else:
                self.tool_buy_sell_info_table.set_data(buy_sell_info)
                
            self.tool_buy_sell_info_table.show()
        else:
            self.append_text_to_logs("В таблице `Купить/Продать` отсутствуют записи.")

    @pyqtSlot(object)
    def on_show_order_book_window(self, order_book):
        """Thread-safe отображение окна стакана заявок"""
        if self._is_closing:
            return
            
        try:
            # Используем существующее окно или создаем новое только если его нет
            if self.tool_order_book_table1 is None:
                self.tool_order_book_table1 = OrderBookWindow()
            
            if order_book:
                self.tool_order_book_table1.renew(order_book)
                self.tool_order_book_table1.show()
                self.append_text_to_logs("Окно стакана отображено")
            else:
                self.append_text_to_logs("Не удалось получить данные стакана")
        except Exception as e:
            self.append_text_to_logs(f"Ошибка при отображении окна стакана: {e}")

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("QuikPython Demo")
        self.setGeometry(100, 100, 1200, 800)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Правая панель
        right_panel = self.create_right_panel()  
        main_layout.addWidget(right_panel, 2)

    def create_left_panel(self) -> QWidget:
        """Создание левой панели с параметрами подключения и инструмента"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Группа подключения
        connection_group = QGroupBox("Подключение")
        connection_layout = QGridLayout(connection_group)
        
        # Удаленный хост
        self.checkbox_remote_host = QCheckBox("Удаленный хост")
        connection_layout.addWidget(self.checkbox_remote_host, 0, 0, 1, 2)
        
        connection_layout.addWidget(QLabel("Хост:"), 1, 0)
        self.text_box_host = QLineEdit("127.0.0.1")
        connection_layout.addWidget(self.text_box_host, 1, 1)
        
        # Кнопка подключения
        self.button_start = QPushButton("Старт")
        self.button_start.clicked.connect(self.button_start_click)
        connection_layout.addWidget(self.button_start, 2, 0, 1, 2)
        
        layout.addWidget(connection_group)
        
        # Группа инструмента
        instrument_group = QGroupBox("Параметры инструмента")
        instrument_layout = QGridLayout(instrument_group)
        
        instrument_layout.addWidget(QLabel("Код бумаги:"), 0, 0)
        self.text_box_sec_code = QLineEdit()
        instrument_layout.addWidget(self.text_box_sec_code, 0, 1)
        
        instrument_layout.addWidget(QLabel("Класс:"), 1, 0)
        self.text_box_class_code = QLineEdit()
        instrument_layout.addWidget(self.text_box_class_code, 1, 1)
        
        instrument_layout.addWidget(QLabel("Код клиента:"), 2, 0)
        self.combo_box_client_code = QComboBox()
        instrument_layout.addWidget(self.combo_box_client_code, 2, 1)
        
        # Кнопка запуска
        self.button_run = QPushButton("Запуск")
        self.button_run.clicked.connect(self.button_run_click)
        instrument_layout.addWidget(self.button_run, 3, 0, 1, 2)
        
        layout.addWidget(instrument_group)
        
        # Группа информации о бумаге
        info_group = QGroupBox("Информация о бумаге")
        info_layout = QGridLayout(info_group)
        
        # Поля информации
        info_fields = [
            ("Account ID:", "text_box_account_id"),
            ("Firm ID:", "text_box_firm_id"),
            ("Краткое название:", "text_box_short_name"),
            ("Размер лота:", "text_box_lot"),
            ("Шаг цены:", "text_box_step"),
            ("ГО:", "text_box_guarantee_providing"),
            ("Последняя цена:", "text_box_last_price"),
            ("Позиция:", "text_box_qty"),
            ("Вариационная маржа:", "text_box_var_margin")
        ]
        
        for i, (label_text, attr_name) in enumerate(info_fields):
            info_layout.addWidget(QLabel(label_text), i, 0)
            text_box = QLineEdit()
            text_box.setReadOnly(True)
            setattr(self, attr_name, text_box)
            info_layout.addWidget(text_box, i, 1)
            
        layout.addWidget(info_group)
        
        # Группа стакана
        quote_group = QGroupBox("Стакан")
        quote_layout = QGridLayout(quote_group)
        
        quote_layout.addWidget(QLabel("Время обновления:"), 0, 0)
        self.text_box_renew_time = QLineEdit()
        self.text_box_renew_time.setReadOnly(True)
        quote_layout.addWidget(self.text_box_renew_time, 0, 1)
        
        quote_layout.addWidget(QLabel("Лучшая продажа:"), 2, 0)
        self.text_box_best_offer = QLineEdit()
        self.text_box_best_offer.setReadOnly(True)
        quote_layout.addWidget(self.text_box_best_offer, 2, 1)
        
        quote_layout.addWidget(QLabel("Лучшая покупка:"), 1, 0)
        self.text_box_best_bid = QLineEdit()
        self.text_box_best_bid.setReadOnly(True)
        quote_layout.addWidget(self.text_box_best_bid, 1, 1)
        
        layout.addWidget(quote_group)
        
        # Группа активной заявки
        order_group = QGroupBox("Активная заявка")
        order_layout = QGridLayout(order_group)
        
        order_layout.addWidget(QLabel("Номер заявки:"), 0, 0)
        self.text_box_order_number = QLineEdit()
        self.text_box_order_number.setReadOnly(True)
        order_layout.addWidget(self.text_box_order_number, 0, 1)
        
        layout.addWidget(order_group)
        
        return panel

    def create_right_panel(self) -> QWidget:
        """Создание правой панели с командами и логами"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Группа команд
        commands_group = QGroupBox("Команды")
        commands_layout = QVBoxLayout(commands_group)
        
        # Список команд
        self.list_box_commands = QListWidget()
        self.list_box_commands.currentRowChanged.connect(self.list_box_commands_selection_changed)
        commands_layout.addWidget(self.list_box_commands)
        
        # Описание команды
        self.text_box_description = QTextEdit()
        self.text_box_description.setMaximumHeight(100)
        self.text_box_description.setReadOnly(True)
        commands_layout.addWidget(self.text_box_description)
        
        # Кнопка выполнения команды
        self.button_command_run = QPushButton("Выполнить команду")
        self.button_command_run.clicked.connect(self.button_command_run_click)
        commands_layout.addWidget(self.button_command_run)
        
        layout.addWidget(commands_group)
        
        # Окно логов
        logs_group = QGroupBox("Логи")
        logs_layout = QVBoxLayout(logs_group)
        
        self.text_box_logs_window = QTextEdit()
        self.text_box_logs_window.setReadOnly(True)
        font = QFont("Consolas", 9)
        self.text_box_logs_window.setFont(font)
        logs_layout.addWidget(self.text_box_logs_window)
        
        layout.addWidget(logs_group)
        
        return panel

    def init_controls(self):
        """Инициализация значений контролов"""
        self.text_box_sec_code.setText(self.sec_code)
        self.text_box_class_code.setText(self.class_code)
        
        # Изначально отключаем кнопки
        self.button_run.setEnabled(False)
        self.button_command_run.setEnabled(False)
        self.timer_renew_form.stop()
        self.list_box_commands.setEnabled(False)
        
        # Заполняем список команд
        commands = [
            "Получить исторические данные",
            "Получить исторические данные (с параметром `bid`)",
            "Выставить лимитрированную заявку (без сделки)",
            "Выставить лимитрированную заявку (c выполнением!!!)",
            "Выставить рыночную заявку (c выполнением!!!)",
            "Удалить активную заявку",
            "Получить заявку по номеру",
            "Получить заявку по ID транзакции",
            "Получить информацию по бумаге",
            "Получить таблицу лимитов по бумаге",
            "Получить таблицу лимитов по всем бумагам",
            "Получить таблицу по фьючерсным лимитам",
            "Получить таблицу позиций по клиентским счетам (фьючерсы)",
            "Получить таблицу заявок",
            "Получить таблицу сделок",
            "Получить таблицу обезличенных сделок",
            "Получить таблицу `Клиентский портфель`",
            "Получить таблицы денежных лимитов",
            "Получить таблицу Купить/Продать",
            "Получить стакан заявок",
            "Получить стакан заявок(без обновления)",
            "Связка ParamRequest + OnParam + GetParamEx2",
            "CancelParamRequest",
            "Отменить заказ на получение стакана",
            "Выставить стоп-заявку типа тейк-профит и стоп-лимит", 
            "Рассчитать максимальное количество лотов в заявке",
            "Получить дату торговой сессии",
        ]
        
        for command in commands:
            self.list_box_commands.addItem(command)

    def append_text_to_logs(self, text: str):
        """Добавить текст в окно логов"""
        self.text_box_logs_window.append(text.rstrip('\n'))
        
    def set_text_to_textbox(self, textbox: QLineEdit, text: str):
        """Установить текст в текстовое поле (thread-safe)"""
        textbox.setText(text)

    def button_start_click(self):
        """Обработчик нажатия кнопки Старт"""
        try:
            self.append_text_to_logs("Подключаемся к терминалу Quik...")
            
            if self.checkbox_remote_host.isChecked():
                host = self.text_box_host.text()
                self.quik = Quik(Quik.DEFAULT_PORT, InMemoryStorage(), host)
            else:
                self.quik = Quik(34130, InMemoryStorage())  # Отладочный порт как в C#
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка инициализации объекта Quik: {e}")
            return
            
        if self.quik is not None:
            self.append_text_to_logs("Экземпляр Quik создан.")
            
            try:
                self.append_text_to_logs("Получаем статус соединения с сервером....")
                
                # Используем общий event loop
                self.run_async_task(self.check_connection())
                
            except Exception as e:
                self.append_text_to_logs(f"Неудачная попытка получить статус соединения с сервером: {e}")

    async def check_connection(self):
        """Асинхронная проверка подключения"""
        try:
            # Инициализируем Quik
            await self.quik.initialize()
            
            # Проверяем подключение
            self.is_server_connected = await self.quik.service.is_connected()
            
            if self.is_server_connected:
                self.append_text_to_logs("Соединение с сервером установлено.")
                self.append_text_to_logs("Определяем код клиента...")
                
                # Получаем коды клиентов
                codes = await self.quik.clazz.get_client_codes()
                if codes:
                    # Используем сигнал для thread-safe обновления UI
                    self.async_runner.update_client_codes.emit(codes)

                self.append_text_to_logs("Определяем аккаунт...")
                
                # Получаем торговые аккаунты
                accounts = await self.quik.clazz.get_trade_accounts()
                if accounts:
                    # Используем сигнал для thread-safe обновления UI
                    self.async_runner.update_accounts.emit(accounts)

                # Используем сигнал для thread-safe обновления статуса
                self.async_runner.update_connection_status.emit(True)
            else:
                self.append_text_to_logs("Соединение с сервером НЕ установлено.")
                # Используем сигнал для thread-safe обновления статуса
                self.async_runner.update_connection_status.emit(False)
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка при проверке подключения: {e}")
            self.async_runner.update_connection_status.emit(False)

    def button_run_click(self):
        """Обработчик нажатия кнопки Запуск"""
        # Используем общий event loop
        self.run_async_task(self.run())

    async def run(self):
        """Основная логика запуска работы с инструментом"""
        try:
            self.sec_code = self.text_box_sec_code.text()
            self.client_code = self.combo_box_client_code.currentText()
            
            self.append_text_to_logs(f"Определяем код класса инструмента {self.sec_code}, по списку классов...")
            
            try:
                if not self.text_box_class_code.text():
                    self.class_code = await self.quik.clazz.get_security_class(
                        "SPBFUT,TQBR,TQBS,TQNL,TQLV,TQNE,TQOB,SPBXM", 
                        self.sec_code
                    )
                else:
                    self.class_code = self.text_box_class_code.text().upper()
            except Exception as e:
                self.append_text_to_logs(f"Ошибка определения класса инструмента. Убедитесь, что тикер указан правильно: {e}")
                return
                
            if self.class_code:
                self.text_box_class_code.setText(self.class_code)
                self.append_text_to_logs(f"Создаем экземпляр инструмента {self.sec_code}|{self.class_code}...")
                
                # Создаем инструмент (Tool) - упрощенная версия
                await self.create_tool()
                
                if self.tool:
                    self.append_text_to_logs(f"Инструмент {self.tool.get('name', '')} создан.")
                    
                    # Заполняем поля информации
                    self.text_box_account_id.setText(self.tool.get('account_id', ''))
                    self.text_box_firm_id.setText(self.tool.get('firm_id', ''))
                    self.text_box_short_name.setText(self.tool.get('name', ''))
                    self.text_box_lot.setText(str(self.tool.get('lot', '')))
                    self.text_box_step.setText(str(self.tool.get('step', '')))
                    self.text_box_guarantee_providing.setText(str(self.tool.get('guarantee_providing', '')))
                    self.text_box_last_price.setText(str(self.tool.get('last_price', '')))
                    
                    # Получаем позицию
                    position = await self.get_position_t2()
                    self.text_box_qty.setText(str(position))
                    
                    # Подписываемся на стакан
                    self.append_text_to_logs("Подписываемся на стакан...")
                    try:
                        rc = await self.quik.order_book.subscribe(self.class_code, self.sec_code)
                        self.is_subscribed_tool_order_book = await self.quik.order_book.is_subscribed(self.class_code, self.sec_code)
                        
                        if self.is_subscribed_tool_order_book:
                            self.tool_order_book = OrderBook()
                            self.append_text_to_logs("Подписка на стакан прошла успешно.")
                            
                            # Подписываемся на события
                            self.append_text_to_logs("Подписываемся на колбэк 'OnQuote'...")
                            self.quik.events.add_on_quote(self.on_quote_do)
                            
                            self.append_text_to_logs("Подписываемся на колбэк 'OnFuturesClientHolding'...")
                            self.quik.events.add_on_futures_client_holding(self.on_futures_client_holding_do)
                            
                            self.append_text_to_logs("Подписываемся на колбэк 'OnDepoLimit'...")
                            self.quik.events.add_on_depo_limit(self.on_depo_limit_do)
                            
                            # Используем сигнал для запуска таймера из другого потока
                            self.async_runner.start_timer.emit()
                            self.list_box_commands.setCurrentRow(0)
                            self.list_box_commands.setEnabled(True)
                            self.button_command_run.setEnabled(True)
                        else:
                            self.append_text_to_logs("Подписка на стакан не удалась.")
                            self.text_box_best_bid.setText("-")
                            self.text_box_best_offer.setText("-")
                            # Используем сигнал для остановки таймера из другого потока
                            self.async_runner.stop_timer.emit()
                            self.list_box_commands.setEnabled(False)
                            self.button_command_run.setEnabled(False)
                    except Exception as e:
                        self.append_text_to_logs(f"Ошибка подписки на стакан: {e}")
                        
                    self.button_run.setEnabled(False)
                    
        except Exception as e:
            self.append_text_to_logs(f"Ошибка получения данных по инструменту: {e}")

    async def create_tool(self):
        """Создание объекта инструмента"""
        try:
            # Получаем информацию о бумаге
            security_info = await self.quik.clazz.get_security_info(self.class_code, self.sec_code)
            last_price = (await self.quik.trading.get_param_ex(self.class_code, self.sec_code, ParamNames.LAST)).param_value
            account_id = await self.quik.clazz.get_trade_account(self.class_code)
            class_info = await self.quik.clazz.get_class_info(self.class_code)
            lot = security_info.lot_size if security_info else 0
            guaranteeProviding = 0
            if class_info == "SPBFUT":
                guaranteeProviding = (await self.quik.trading.get_param_ex(self.class_code, self.sec_code, ParamNames.BUYDEPO)).param_value
            else:
                lot = (await self.quik.trading.get_param_ex(self.class_code, self.sec_code, ParamNames.LOTSIZE)).param_value

            priceAccuracy = (await self.quik.trading.get_param_ex(self.class_code, self.sec_code, ParamNames.SEC_SCALE)).param_value

            if security_info:
                self.tool = {
                    'security_code': self.sec_code,
                    'class_code': self.class_code,
                    'name': security_info.short_name,
                    'lot': lot,
                    'step': security_info.min_price_step,
                    'guarantee_providing': guaranteeProviding,
                    'last_price': last_price,
                    'account_id': account_id,
                    'firm_id': class_info.firm_id,
                    'price_accuracy': priceAccuracy
                }
        except Exception as e:
            self.append_text_to_logs(f"Ошибка создания инструмента: {e}")
            self.tool = None

    async def get_position_t2(self) -> float:
        """Получить позицию T2 по инструменту"""
        try:
            qty = 0
            tool = self.tool
            if self.class_code == "SPBFUT":
                q1 = await self.quik.trading.get_futures_holding(firm_id=tool["firm_id"], acc_id=tool["account_id"],
                                                                                    sec_code=self.sec_code, pos_type=0)
                if q1:
                    qty = q1.total_net
            else:
                q1 = await self.quik.trading.get_depo_ex(firm_id=tool["firm_id"], client_code=self.client_code,
                                                                    sec_code=self.sec_code, acc_id=tool["account_id"],
                                                                    limit_kind=LimitKind.T0)
                if q1:
                    qty = q1.current_balance
            return qty
        except Exception as e:
            self.append_text_to_logs(f"Ошибка получения позиции: {e}")
            return 0.0

    async def update_position_async(self):
        """Асинхронное обновление позиции"""
        # Проверяем, не выполняется ли уже обновление, и подключены ли к серверу
        if self._updating_position or not self.is_server_connected:
            return  # Пропускаем, если уже выполняется или не подключены
            
        self._updating_position = True
        try:
            # Обновляем позицию
            position = await self.get_position_t2()
            
            # Обновляем текущую цену
            if self.class_code and self.sec_code:
                last_price_result = await self.quik.trading.get_param_ex(
                    self.class_code, self.sec_code, ParamNames.LAST
                )
                if last_price_result and hasattr(last_price_result, 'param_value'):
                    price_value = str(last_price_result.param_value)
                    if self.tool:
                        self.tool['last_price'] = last_price_result.param_value
                    # Отправляем сигнал обновления цены
                    self.async_runner.update_price.emit(price_value)
                    
            # Отправляем результат через сигнал для thread-safe обновления UI
            self.async_runner.update_position.emit(position)
        except Exception as e:
            self.append_text_to_logs(f"Ошибка обновления позиции: {e}")
        finally:
            self._updating_position = False

    def on_quote_do(self, quote: OrderBook):
        """Обработчик события получения котировок"""
        if quote.sec_code == self.sec_code and quote.class_code == self.class_code:
            self.renew_order_book_time = datetime.now()
            self.tool_order_book = quote
            
            if quote.bid and len(quote.bid) > 0:
                self.bid = Decimal(str(quote.bid[-1].price))
            if quote.offer and len(quote.offer) > 0:
                self.offer = Decimal(str(quote.offer[0].price))
        self.text_box_best_bid.setText(str(self.bid) if self.bid is not None else "-")
        self.text_box_best_offer.setText(str(self.offer) if self.offer is not None else "-")
        self.set_text_to_textbox(self.text_box_renew_time,
                                self.renew_order_book_time.strftime("%H:%M:%S") if self.renew_order_book_time else "-")

    def on_futures_client_holding_do(self, fut_pos: FuturesClientHolding):
        """Обработчик события изменения позиций по фьючерсам"""
        if fut_pos.sec_code == self.sec_code:
            self.futures_position = fut_pos
        self.text_box_var_margin.setText(str(fut_pos.var_margin) if fut_pos else "-")

    def on_depo_limit_do(self, dep_limit: DepoLimitEx):
        """Обработчик события изменения депо лимитов"""
        self.append_text_to_logs("Вызвано событие OnDepoLimit (изменение бумажного лимита)...")
        self.append_text_to_logs(f"Заблокировано на покупку количества лотов - {dep_limit.locked_buy}")

    def timer_renew_form_tick(self):
        """Обработчик таймера обновления формы"""
        if self.tool:
            # Обновляем последнюю цену
            if 'last_price' in self.tool:
                price_value = str(self.tool['last_price'])
                self.text_box_last_price.setText(price_value)
            
            # Запускаем асинхронное обновление позиции только если подключены к QUIK
            if self.is_server_connected and self.quik is not None:
                self.run_async_task(self.update_position_async())
            
            # Обновляем стакан
            if self.tool_order_book and self.tool_order_book.bid:
                if self.renew_order_book_time:
                    self.set_text_to_textbox(self.text_box_renew_time,
                                           self.renew_order_book_time.strftime("%H:%M:%S"))
                if self.bid is not None:
                    self.set_text_to_textbox(self.text_box_best_bid, str(self.bid))
                if self.offer is not None:
                    self.set_text_to_textbox(self.text_box_best_offer, str(self.offer))
                
                # Обновляем окно стакана если оно открыто
                if self.tool_order_book_table:
                    self.tool_order_book_table.renew(self.tool_order_book)
            
            # Обновляем вариационную маржу
            if self.futures_position:
                self.text_box_var_margin.setText(str(self.futures_position.var_margin))

    def list_box_commands_selection_changed(self, current_row: int):
        """Обработчик изменения выбранной команды"""
        if current_row < 0:
            return
            
        selected_command = self.list_box_commands.item(current_row).text()
        
        descriptions = {
            "Получить исторические данные": "Получить и отобразить исторические данные котировок по заданному инструменту. Тайм-фрейм = 15 Minute",
            "Получить исторические данные (с параметром `bid`)": "Получить и отобразить исторические данные котировок по заданному инструменту и параметру `bid`. Тайм-фрейм = 15 Minute",
            "Выставить лимитрированную заявку (без сделки)": "Будет выставлена заявку на покупку 1-го лота заданного инструмента, по цене на 5% ниже текущей цены (вероятность срабатывания такой заявки достаточно низкая, чтобы успеть ее отменить)",
            "Выставить лимитрированную заявку (c выполнением!!!)": "Будет выставлена заявку на покупку 1-го лота заданного инструмента, по цене на 5 шагов цены выше текущей цены (вероятность срабатывания такой заявки достаточно высокая!!!)",
            "Выставить рыночную заявку (c выполнением!!!)": "Будет выставлена заявку на покупку 1-го лота заданного инструмента, \"по рынку\" (Заявка будет автоматически исполнена по текущим доступным ценам!!!)",
            "Удалить активную заявку": "Если предварительно была выставлена заявка, заявка имеет статус 'Активна' и ее номер отображается в форме, то эта заявка будет удалена/отменена",
            "Получить заявку по номеру": "Попытаться получить заявку по номеру, который укажет пользователь",
            "Получить заявку по ID транзакции": "Попытаться получить заявку по ID транзакции, который укажет пользователь",
            "Получить информацию по бумаге": "Получить и отобразить таблицу c информацией по бумаге. quik.Class.GetSecurityInfo(classCode, securityCode)",
            "Получить таблицу лимитов по бумаге": "Получить и отобразить таблицу лимитов по бумагам. quik.Trading.GetDepoLimits(securityCode)",
            "Получить таблицу лимитов по всем бумагам": "Получить и отобразить таблицу лимитов по бумагам. quik.Trading.GetDepoLimits()",
            "Получить таблицу по фьючерсным лимитам": "Получить и отобразить таблицу лимитов по фьючерсам. quik.Trading.GetFuturesLimit(firmId, accId, limitType, currCode)",
            "Получить таблицу позиций по клиентским счетам (фьючерсы)": "Получить и отобразить таблицу \"Позиции по клиенским счетам (фьючерсы)\". quik.Trading.GetFuturesClientHoldings()",
            "Получить таблицу заявок": "Получить и отобразить таблицу всех клиентских заявок. quik.Orders.GetOrders()",
            "Получить таблицу сделок": "Получить и отобразить таблицу всех клиентских сделок. quik.Trading.GetTrades()",
            "Получить таблицу обезличенных сделок": "Получить и отобразить таблицу обезличенных сделок по инструменту. quik.Trading.GetAllTrades()",
            "Получить таблицу `Клиентский портфель`": "Получить и отобразить таблицу `Клиентский портфель`. quik.Trading.GetPortfolioInfoEx()",
            "Получить таблицы денежных лимитов": "Получить и отобразить таблицы денежных лимитов (стандартную и дополнительную Т2). Работает только на инструментах фондовой секции. quik.Trading.GetMoney() и quik.Trading.GetMoneyEx()",
            "Получить таблицу Купить/Продать": "Получить и отобразить таблицу с параметрами из таблицы QUIK «Купить/Продать», означающими возможность купить либо продать указанный инструмент \"sec_code\" класса \"class_code\", указанным клиентом \"client_code\" фирмы \"firmid\", по указанной цене \"price\". Если цена равна \"0\", то используются лучшие значения спроса/предложения. quik.Trading.GetBuySellInfo() и quik.Trading.GetBuySellInfoEx()",
            "Получить стакан заявок": "Получить и отобразить стакан заявок в виде таблицы (данные обновляются)",
            "Получить стакан заявок(без обновления)": "Получить и отобразить стакан заявок в виде таблицы (данные на момент вызова функции. Без обновления)",
            "Связка ParamRequest + OnParam + GetParamEx2": "Демонстрация работы связки ParamRequest + OnParam + GetParamEx2",
            "CancelParamRequest": "Отменяем подписку на обновление параметра и отключаем обработку события OnParam",
            "Отменить заказ на получение стакана": "Вызываем функцию отмены заказа стакана по инструменту",
            "Выставить стоп-заявку типа тейк-профит и стоп-лимит": "Выставляем стоп-заявку типа тейк-профит и стоп-лимит. Закрываем short. Тейк-профит по цене минус 50 шагов цены от последней сделки. Стоп-лимит - плюс 40 шагов цены. Для тейпрофита для отступа используем тип шаг цены, для спреда - процент.",
            "Рассчитать максимальное количество лотов в заявке": "Получить максимальное количество лото в заявке по текущему инструменту. (`покупка` по текущей цене, лимитированной заявкой)",
            "Получить дату торговой сессии": "Получить дату текущей торговой сессии"
        }
        
        description = descriptions.get(selected_command, "Описание команды не найдено")
        self.text_box_description.setPlainText(description)

    def button_command_run_click(self):
        """Обработчик выполнения команды"""
        current_row = self.list_box_commands.currentRow()
        if current_row < 0:
            return
            
        selected_command = self.list_box_commands.item(current_row).text()
        self.append_text_to_logs(f"Выполняется команда: {selected_command}")
        
        # Выполнение команд
        if selected_command == "Получить исторические данные":
            self.show_candles_window()
        elif selected_command == "Получить исторические данные (с параметром `bid`)":
            self.show_candles_window("bid")
        elif selected_command == "Выставить лимитрированную заявку (без сделки)":
            self.run_async_task(self.place_limit_order(market=False, exec=False))
        elif selected_command == "Выставить лимитрированную заявку (c выполнением!!!)":
            self.run_async_task(self.place_limit_order(market=True, exec=True))
        elif selected_command == "Выставить рыночную заявку (c выполнением!!!)":
            self.run_async_task(self.place_limit_order(market=True, exec=True))
        elif selected_command == "Удалить активную заявку":
            self.run_async_task(self.cancel_active_order())
        elif selected_command == "Получить информацию по бумаге":
            self.run_async_task(self.get_security_info())
        elif selected_command == "Получить таблицу лимитов по бумаге":
            self.run_async_task(self.get_depo_limits_by_security())
        elif selected_command == "Получить таблицу лимитов по всем бумагам":
            self.run_async_task(self.get_depo_limits_all())
        elif selected_command == "Получить таблицу по фьючерсным лимитам":
            self.run_async_task(self.get_futures_limits())
        elif selected_command == "Получить таблицу позиций по клиентским счетам (фьючерсы)":
            self.run_async_task(self.get_futures_client_holdings())
        elif selected_command == "Получить таблицу заявок":
            self.run_async_task(self.get_orders())
        elif selected_command == "Получить таблицу сделок":
            self.run_async_task(self.get_trades())
        elif selected_command == "Получить таблицу обезличенных сделок":
            self.run_async_task(self.get_all_trades())
        elif selected_command == "Получить таблицу `Клиентский портфель`":
            self.run_async_task(self.get_portfolio_info_ex())
        elif selected_command == "Получить таблицы денежных лимитов": ##??
            self.run_async_task(self.get_money_and_money_ex())
        elif selected_command == "Получить таблицу Купить/Продать": #??
            self.run_async_task(self.get_buy_sell_info_and_ex())
        elif selected_command == "Получить стакан заявок":
            self.show_order_book_window()
        elif selected_command == "Получить стакан заявок(без обновления)":
            self.run_async_task(self.show_order_book_window1())
        elif selected_command == "Связка ParamRequest + OnParam + GetParamEx2":
            self.run_async_task(self.param_request_demo())
        elif selected_command == "CancelParamRequest":
            self.run_async_task(self.cancel_param_request_demo())
        elif selected_command == "Отменить заказ на получение стакана":
            self.run_async_task(self.cancel_order_book_subscription())
        elif selected_command == "Выставить стоп-заявку типа тейк-профит и стоп-лимит":
            self.run_async_task(self.place_stop_order())
        elif selected_command == "Рассчитать максимальное количество лотов в заявке":
            self.run_async_task(self.calculate_max_lots())
        elif selected_command == "Получить дату торговой сессии":
            self.run_async_task(self.get_trading_day())
        else:
            self.append_text_to_logs("Команда еще не реализована в данной версии")

    def show_order_book_window(self):
        """Показать окно стакана заявок"""
        if self._is_closing:
            return
            
        try:
            # Создаем окно только если его еще нет
            if self.tool_order_book_table is None:
                self.tool_order_book_table = OrderBookWindow()
            
            # Обновляем данные если есть
            if self.tool_order_book:
                self.tool_order_book_table.renew(self.tool_order_book)
                self.tool_order_book_table.show()
                self.append_text_to_logs("Окно стакана отображено с кешированными данными")
            else:
                self.append_text_to_logs("Нет данных стакана для отображения")
        except Exception as e:
            self.append_text_to_logs(f"Ошибка при отображении окна стакана: {e}")

    async def show_order_book_window1(self):
        """Показать окно стакана заявок"""
        if self._is_closing:
            return
            
        if not self.quik or not self.is_server_connected:
            self.append_text_to_logs("Ошибка: не подключены к QUIK")
            return
            
        if not self.class_code or not self.sec_code:
            self.append_text_to_logs("Ошибка: не выбран инструмент")
            return

        try:
            self.append_text_to_logs("Получаем данные стакана с сервера...")
            book = await self.quik.order_book.get_quote_level2(self.class_code, self.sec_code)
            
            # Используем сигнал для thread-safe создания и отображения окна в главном потоке
            self.async_runner.show_order_book_window.emit(book)
            
        except Exception as e:
            self.append_text_to_logs(f"Ошибка при получении стакана: {e}")
            # Передаем None через сигнал в случае ошибки
            self.async_runner.show_order_book_window.emit(None)
        

    def show_candles_window(self, tag=""):
        """Показать окно исторических данных"""
        if self._is_closing:
            return
            
        if not self.quik or not self.is_server_connected:
            self.append_text_to_logs("Ошибка: не подключены к QUIK")
            return
            
        if not self.class_code or not self.sec_code:
            self.append_text_to_logs("Ошибка: не выбран инструмент")
            return
        
        try:
            # Закрываем предыдущее окно если оно существует
            if self.candles_window is not None:
                self.candles_window.close()
                
            # Создаем новое окно
            self.candles_window = CandlesWindow(
                self.quik, self.class_code, self.sec_code, self.client_code, self._loop, tag
            )
            self.candles_window.show()
            self.append_text_to_logs(f"Окно исторических данных открыто{'с параметром ' + tag if tag else ''}")
        except Exception as e:
            self.append_text_to_logs(f"Ошибка при открытии окна исторических данных: {e}")
        self.candles_window.show()
        

    async def place_limit_order(self, market=False, exec=False):
        """
        Выставить лимитрированную заявку
        Args:
            market: False - заявка без сделки (цена ниже рынка), True - заявка с исполнением
        """
        try:
            if not self.tool or not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: инструмент не инициализирован или нет подключения к QUIK")
                return
                
            # Рассчитываем цену заявки
            last_price = Decimal(self.tool.get('last_price', 0))
            if last_price == 0:
                self.append_text_to_logs("Ошибка: последняя цена инструмента равна нулю")
                return
            step_price = Decimal(self.tool.get('step', 0.01))

            if not market:
                if exec:
                    price_order = last_price + (step_price * 5)
                else:
                    # Заявка без сделки - на 5% ниже текущей цены
                    price_order = last_price - (last_price / 50)
            else:
                price_order = last_price + (step_price * 5)
            
            price_accuracy = int(float(self.tool.get('price_accuracy', 2)))

            # Округляем до нужной точности
            price_in_order = Decimal(str(price_order)).quantize(Decimal(f'1e-{price_accuracy}'))
            
            self.append_text_to_logs(f"Выставляем заявку на покупку, по цене: {price_in_order} ...")

            if not market:
                if not exec:
                    order = await self.quik.orders.send_limit_order(self.class_code, self.sec_code, 
                                                                    account_id=self.tool.get('account_id', ''),
                                                                    operation=Operation.BUY,
                                                                    price=price_in_order,
                                                                    qty=1,
                                                                    client_code=self.client_code)
                    if order.order_num > 0:
                        self.append_text_to_logs(f"Заявка выставлена. ID транзакции - {order.trans_id}")
                        self.append_text_to_logs(f"Заявка выставлена. Номер заявки - {order.order_num}")
                        self.append_text_to_logs(f"Заявка выставлена. Код клиента - {order.client_code}")
                        # Сохраняем order для возможной отмены и обновляем UI
                        self.order = order
                        self.text_box_order_number.setText(str(order.order_num))
                    else:
                        self.append_text_to_logs("Заявка не была выставлена. Error "+order.reject_reason)
                        self.text_box_order_number.setText("-")

                else:
                    order = await self.quik.orders.send_limit_order(self.class_code, self.sec_code, 
                                                                    account_id=self.tool.get('account_id', ''),
                                                                    operation=Operation.BUY,
                                                                    price=price_in_order,
                                                                    qty=1,
                                                                    execution_condition=ExecutionCondition.PUT_IN_QUEUE,
                                                                    client_code=self.client_code)
                    if order.order_num > 0:
                        self.append_text_to_logs(f"Заявка выставлена. ID транзакции - {order.trans_id}")
                        if order.trans_id > 0:
                            asyncio.sleep(0.5)  # Ждем немного для получения ответа
                        try:
                            order_fetched = await self.quik.orders.get_order_by_trans_id(self.class_code, self.sec_code, order.trans_id)
                            if order_fetched:
                                self.append_text_to_logs(f"Заявка выставлена. Номер заявки - {order_fetched.order_num}")
                                self.append_text_to_logs(f"Заявка выставлена. Код клиента - {order_fetched.client_code}")
                                # Сохраняем order для возможной отмены и обновляем UI
                                self.order = order_fetched
                                self.text_box_order_number.setText(str(order_fetched.order_num))
                        except Exception as e:
                            self.append_text_to_logs(f"Ошибка при получении заявки: {e}")
                    else:
                        self.append_text_to_logs("Заявка не была выставлена. Error "+order.reject_reason)
                        self.text_box_order_number.setText("-")

            else:
                # Выставляем рыночную заявку
                order = await self.quik.orders.send_market_order(self.class_code, self.sec_code, 
                                                                    account_id=self.tool.get('account_id', ''),
                                                                    operation=Operation.BUY,
                                                                    qty=1,
                                                                    client_code=self.client_code)
                if order.order_num > 0:
                    self.append_text_to_logs(f"Заявка выставлена. ID транзакции - {order.trans_id}")
                    if order.trans_id > 0:
                        asyncio.sleep(0.5)  # Ждем немного для получения ответа
                    try:
                        order_fetched = await self.quik.orders.get_order_by_trans_id(self.class_code, self.sec_code, order.trans_id)
                        if order_fetched:
                            self.append_text_to_logs(f"Заявка выставлена. Номер заявки - {order_fetched.order_num}")
                            self.append_text_to_logs(f"Заявка выставлена. Код клиента - {order_fetched.client_code}")
                            # Сохраняем order для возможной отмены и обновляем UI
                            self.order = order_fetched
                            self.text_box_order_number.setText(str(order_fetched.order_num))
                    except Exception as e:
                        self.append_text_to_logs(f"Ошибка при получении заявки: {e}")
                else:
                    self.append_text_to_logs("Заявка не была выставлена. Error "+order.reject_reason)
                    self.text_box_order_number.setText("-")

        except Exception as e:
            self.append_text_to_logs(f"Ошибка процедуры размещения заявки: {e}")

    async def cancel_active_order(self):
        """
        Удалить активную заявку
        """
        try:
            if self.order is not None and self.order.order_num > 0:
                self.append_text_to_logs(f"Удаляем заявку на покупку с номером - {self.order.order_num} ...")
                
                # Отменяем заявку через quik API
                result = await self.quik.orders.kill_order(self.order)
                
                self.append_text_to_logs(f"Результат - {result} ... Заявка снята.")
                
                # Очищаем поле номера заявки
                self.text_box_order_number.setText("")
                
                # Очищаем сохраненную заявку
                self.order = None
                
            else:
                self.append_text_to_logs("Нет активной заявки для удаления.")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка удаления заявки: {e}")

    async def get_security_info(self):
        """
        Получить информацию по бумаге
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
                
            self.append_text_to_logs("Получаем таблицу информации...")
            
            # Получаем информацию о бумаге
            security_info = await self.quik.clazz.get_security_info(self.class_code, self.sec_code)
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_security_info.emit(security_info)
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка получения информации по бумаге: {e}")

    async def get_depo_limits_by_security(self):
        """
        Получить таблицу лимитов по бумаге
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
                
            self.append_text_to_logs("Получаем таблицу лимитов...")
            
            # Получаем лимиты по бумаге
            depo_limits = await self.quik.trading.get_depo_limits(self.sec_code)
            if len(depo_limits) == 0:
                self.append_text_to_logs(f"Лимиты по {self.tool.name['name']} бумаге не найдены.")
            else:
                # Используем сигнал для thread-safe отображения окна
                self.async_runner.show_depo_limits.emit(depo_limits if depo_limits else [])
        except Exception as e:
            self.append_text_to_logs("Ошибка получения лимитов.")

    async def get_depo_limits_all(self):
        """
        Получить таблицу лимитов по всем бумагам
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            self.append_text_to_logs("Получаем таблицу лимитов...")
            
            # Получаем лимиты по всем бумагам (без параметра security_code)
            depo_limits = await self.quik.trading.get_depo_limits()
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_depo_limits_all.emit(depo_limits if depo_limits else [])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения лимитов.")

    async def get_futures_limits(self):
        """
        Получить таблицу фьючерсных лимитов
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            # Проверяем наличие инструмента и торгового счета
            if not self.tool or self.tool.get('firm_id') is None:
                self.append_text_to_logs("Ошибка: необходимо выбрать инструмент с информацией о firmId")
                return
            
            if not self.tool or self.tool.get("account_id") is None:
                self.append_text_to_logs("Ошибка: не выбран торговый счет")
                return
                
            self.append_text_to_logs("Получаем таблицу фьючерсных лимитов...")
            
            # Получаем фьючерсный лимит
            # Параметры: firm_id, account_id, limit_type (MONEY), currency_code ("SUR" - рубли)
            futures_limit = await self.quik.trading.get_futures_limit(
                self.tool["firm_id"],
                self.tool["account_id"], 
                FuturesLimitType.MONEY, 
                "SUR"
            )
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_futures_limits.emit(futures_limit)
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения фьючерсных лимитов.")

    async def get_futures_client_holdings(self):
        """
        Получить таблицу позиций по клиентским счетам (фьючерсы)
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            self.append_text_to_logs("Получаем таблицу фьючерсных позиций...")
            
            # Получаем фьючерсные позиции клиентов (без параметров)
            futures_client_holdings = await self.quik.trading.get_futures_client_holdings()
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_futures_client_holdings.emit(futures_client_holdings if futures_client_holdings else [])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения фьючерсных позиций.")

    async def get_orders(self):
        """
        Получить таблицу заявок
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            self.append_text_to_logs("Получаем таблицу заявок...")
            
            # Получаем все заявки (без параметров)
            orders = await self.quik.orders.get_orders()
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_orders.emit(orders if orders else [])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения заявок.")

    async def get_trades(self):
        """
        Получить таблицу сделок
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            self.append_text_to_logs("Получаем таблицу сделок...")
            
            # Получаем все сделки (без параметров)
            trades = await self.quik.trading.get_trades_list()
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_trades.emit(trades if trades else [])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения сделок.")

    async def get_all_trades(self):
        """
        Получить таблицу обезличенных сделок
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не указан код класса или код бумаги")
                return
                
            self.append_text_to_logs("Получаем таблицу обезличенных сделок...")
            
            # Получаем обезличенные сделки по конкретной бумаге (class_code, sec_code)
            all_trades = await self.quik.trading.get_all_trades_by_security(self.class_code, self.sec_code)
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_all_trades.emit(all_trades if all_trades else [])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения обезличенных сделок.")

    async def get_portfolio_info_ex(self):
        """
        Получить таблицу `Клиентский портфель`
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return

            if not self.tool or self.tool.get("firm_id") is None:
                self.append_text_to_logs("Ошибка: не указан firm_id")
                return
                
            self.append_text_to_logs("Получаем таблицу `Клиентский портфель`...")
            
            portfolio_list = []
            
            # Проверяем тип класса для определения логики получения портфеля
            if self.class_code == "SPBFUT":
                # Для фьючерсов используем account_id
                if self.trade_account_id:
                    portfolio_info = await self.quik.trading.get_portfolio_info_ex(
                        self.tool["firm_id"],
                        self.tool["account_id"],
                        0
                    )
                    if portfolio_info:
                        portfolio_list.append(portfolio_info)
                else:
                    self.append_text_to_logs("Ошибка: не указан торговый счет для фьючерсов")
                    return
            else:
                # Для остальных инструментов используем client_code
                if self.client_code:
                    # Получаем портфель с разными типами лимитов (0, 1, 2)
                    for limit_kind in [0, 1, 2]:
                        portfolio_info = await self.quik.trading.get_portfolio_info_ex(
                            self.tool["firm_id"],
                            self.client_code,
                            limit_kind
                        )
                        if portfolio_info:
                            portfolio_list.append(portfolio_info)
                else:
                    self.append_text_to_logs("Ошибка: не указан код клиента")
                    return
            
            # Используем сигнал для thread-safe отображения окна
            self.async_runner.show_portfolio_info_ex.emit(portfolio_list)
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения клиентского портфеля.")

    async def get_money_and_money_ex(self):
        """
        Получить таблицы денежных лимитов
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.tool or self.tool.get("firm_id") is None:
                self.append_text_to_logs("Ошибка: не указан firm_id")
                return
                
            if not self.client_code:
                self.append_text_to_logs("Ошибка: не указан код клиента")
                return
            
            # Получаем обычные денежные лимиты
            self.append_text_to_logs("Получаем таблицу денежных лимитов...")
            
            money_limit = await self.quik.trading.get_money(
                self.client_code,
                self.tool["firm_id"],
                "EQTV",
                "SUR"
            )
            
            # Отправляем данные через сигнал для отображения
            if money_limit:
                self.async_runner.show_money_limits.emit([money_limit])
            
            # Получаем расширенные денежные лимиты
            self.append_text_to_logs("Получаем расширение таблицы денежных лимитов...")
            
            # Импортируем LimitKind здесь чтобы использовать его значение
            from quik_python.data_structures.depo_limit_ex import LimitKind
            
            money_limit_ex = await self.quik.trading.get_money_ex(
                self.tool["firm_id"],
                self.client_code,
                "EQTV", 
                "SUR",
                LimitKind.T2  # limit_kind = 2 в C# коде
            )
            
            # Отправляем данные через сигнал для отображения
            if money_limit_ex:
                self.async_runner.show_money_limits_ex.emit([money_limit_ex])
                
        except Exception as e:
            self.append_text_to_logs("Ошибка получения денежных лимитов.")

    async def get_buy_sell_info_and_ex(self):
        """
        Получить таблицу `Купить/Продать`
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.tool or self.tool.get("firm_id") is None:
                self.append_text_to_logs("Ошибка: не указан firm_id")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
            
            self.append_text_to_logs("Получаем таблицу `Купить/Продать`...")
            
            # Определяем client_code в зависимости от класса
            # Для фьючерсов (SPBFUT) используем account_id, для остальных - client_code
            client_or_account = ""
            if self.class_code == "SPBFUT":
                if self.tool.get("account_id") and self.tool["account_id"]:
                    client_or_account = self.tool["account_id"]
                else:
                    self.append_text_to_logs("Ошибка: не указан account_id для фьючерсов")
                    return
            else:
                if self.client_code:
                    client_or_account = self.client_code
                else:
                    self.append_text_to_logs("Ошибка: не указан код клиента")
                    return
            
            # Получаем информацию по покупке/продаже с ценой 0 (используются лучшие значения)
            buy_sell_info = await self.quik.trading.get_buy_sell_info_ex(
                self.tool["firm_id"],
                client_or_account,
                self.class_code,
                self.sec_code,
                0  # price = 0 как в C# коде
            )
            
            # Отправляем данные через сигнал для отображения
            if buy_sell_info:
                self.async_runner.show_buy_sell_info.emit([buy_sell_info])
            else:
                self.append_text_to_logs("В таблице `Купить/Продать` отсутствуют записи.")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка получения таблицы Купить/Продать: {e}")

    async def param_request_demo(self):
        """
        Связка ParamRequest + OnParam + GetParamEx2
        Подписка на получение обновляемого параметра 'BID', через ParamRequest
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
                
            self.append_text_to_logs("Подписываемся на получение обновляемого параметра 'BID', через ParamRequest...")
            
            # Подписка на параметр BID
            p_req = await self.quik.trading.param_request(
                self.class_code,
                self.sec_code,
                ParamNames.BID
            )
            
            if p_req:
                self.append_text_to_logs("Подписываемся на колбэк 'OnParam'...")
                # Добавляем обработчик события OnParam
                self.quik.events.add_on_param(self.on_param_do)
                self.is_subscribed_param = True
            else:
                self.append_text_to_logs("Неудачная попытка подписки на обновление параметра...")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка работы в связке ParamRequest + OnParam + GetParamEx2: {e}")

    def on_param_do(self,  param: Param):
        """
        Обработчик события OnParam - обновление параметра инструмента
        """
        try:
            if param.class_code == self.class_code and param.sec_code == self.sec_code:
                # Получаем значение параметра через GetParamEx2 асинхронно
                self.run_async_task(self.get_param_value_async(param.class_code, param.sec_code))
        except Exception as e:
            self.append_text_to_logs(f"Ошибка в обработчике OnParam: {e}")
            
    async def get_param_value_async(self, class_code: str, sec_code: str):
        """
        Асинхронное получение значения параметра через GetParamEx2
        """
        try:
            param_result = await self.quik.trading.get_param_ex(class_code, sec_code, ParamNames.BID)
            if param_result:
                self.append_text_to_logs(
                    f"OnParam -> GetParamEx2: {class_code}|{sec_code}|{ParamNames.BID} = {param_result.param_value}"
                )
        except Exception as e:
            self.append_text_to_logs(f"Ошибка получения параметра через GetParamEx2: {e}")

    async def cancel_param_request_demo(self):
        """
        CancelParamRequest - отмена подписки на обновление параметра и отключение обработки события OnParam
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
                
            self.append_text_to_logs("Отменяем подписку на обновление параметра...")
            
            # Отменяем подписку на параметр BID
            cancel_result = await self.quik.trading.cancel_param_request(
                self.class_code,
                self.sec_code,
                ParamNames.BID
            )
            
            if cancel_result:
                self.append_text_to_logs("Подписка на параметр отменена успешно")
                # Удаляем обработчик события OnParam
                if hasattr(self, 'is_subscribed_param') and self.is_subscribed_param:
                    self.quik.events.remove_on_param(self.on_param_do)
                    self.is_subscribed_param = False
                    self.append_text_to_logs("Обработчик OnParam отключен")
            else:
                self.append_text_to_logs("Ошибка отмены подписки на параметр")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка отмены подписки на параметр: {e}")

    async def cancel_order_book_subscription(self):
        """
        Отменить заказ на получение стакана
        Отменяем заказ на получение с сервера стакана по указанному классу и инструменту
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.class_code or not self.sec_code:
                self.append_text_to_logs("Ошибка: не выбран инструмент")
                return
                
            self.append_text_to_logs("Отменяем заказ на получение с сервера стакана по указанному классу и инструменту...")
            
            # Пытаемся отписаться от стакана с повторными попытками
            result_unsub = await self.quik.order_book.unsubscribe(self.class_code, self.sec_code)
            count = 0
            
            # Повторяем попытки отписки до 10 раз с интервалом 0.5 секунды
            while not result_unsub and count < 10:
                await asyncio.sleep(0.5)  # Ждем 500 мс
                result_unsub = await self.quik.order_book.unsubscribe(self.class_code, self.sec_code)
                count += 1
            
            # Проверяем статус подписки с повторными попытками
            i = 0
            while self.is_subscribed_tool_order_book and i < 10:
                await asyncio.sleep(0.5)  # Ждем 500 мс
                self.is_subscribed_tool_order_book = await self.quik.order_book.is_subscribed(self.class_code, self.sec_code)
                i += 1
            
            # Обрабатываем результат
            if self.is_subscribed_tool_order_book:
                # Отмена подписки не удалась
                self.tool_order_book = OrderBook()  # Создаем пустой стакан
                self.append_text_to_logs("Отмена подписки на стакан не удалась.")
            else:
                # Отмена подписки прошла успешно
                self.tool_order_book = None
                self.append_text_to_logs("Отмена подписки на стакан прошла успешно.")
                
                # Сбрасываем значения bid и offer
                self.bid = None
                self.offer = None
                
                # Обновляем поля в UI
                self.text_box_best_bid.setText("-")
                self.text_box_best_offer.setText("-")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка в функции отмены заказа стакана: {e}")

    async def place_stop_order(self):
        """
        Выставить стоп-заявку типа тейк-профит и стоп-лимит
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.tool:
                self.append_text_to_logs("Ошибка: инструмент не инициализирован")
                return
                
            self.append_text_to_logs("Подписываемся на событие OnStopOrder...")
            
            # В Python используем событийную систему QUIK API
            # Подписка на события стоп-заявок (если поддерживается API)
            
            # Получаем текущую цену и параметры инструмента
            last_price = Decimal(self.tool.get('last_price', 0))
            if last_price == 0:
                self.append_text_to_logs("Ошибка: последняя цена инструмента равна нулю")
                return
                
            step_price = Decimal(self.tool.get('step', 0.01))
            price_accuracy = int(float(self.tool.get('price_accuracy', 2)))
            
            # Рассчитываем цены для стоп-заявки
            price_in_order = last_price.quantize(Decimal(f'1e-{price_accuracy}'))
            condition_price = (last_price - 50 * step_price).quantize(Decimal(f'1e-{price_accuracy}'))
            condition_price2 = (last_price + 40 * step_price).quantize(Decimal(f'1e-{price_accuracy}'))
            order_price = (last_price + 45 * step_price).quantize(Decimal(f'1e-{price_accuracy}'))
            
            # self.append_text_to_logs(f"Выставляем стоп-заявку на покупку, по цене: {price_in_order}...")
            self.append_text_to_logs(f"Выставляем стоп-заявку на покупку, по цене: {order_price}...") #{price_in_order}")
            
            # Создаем стоп-заявку
            # Примечание: В зависимости от API QUIK Python, параметры могут отличаться
            try:
                # Пример структуры стоп-заявки (адаптировано под Python API)
                ord = StopOrder()
                ord.account = self.tool.get('account_id', '')
                ord.class_code = self.class_code
                ord.client_code = self.client_code
                ord.sec_code = self.sec_code
                ord.offset = 5
                ord.offset_unit = OffsetUnits.PRICE_UNITS  # Тип отступа - шаги цены
                ord.spread = Decimal('0.1')
                ord.spread_unit = OffsetUnits.PERCENTS  # Тип спреда - проценты
                ord.stop_order_type = StopOrderType.TAKE_PROFIT_STOP_LIMIT
                ord.condition = Condition.LESS_OR_EQUAL
                ord.condition_price = condition_price
                ord.condition_price2 = condition_price2
                ord.price = order_price
                ord.operation = 'Buy'
                ord.qty = 1
                
                # Выставляем стоп-заявку через API
                # Примечание: Конкретный метод зависит от используемого Python API для QUIK
                trans_id = await self.quik.stop_orders.create_stop_order(ord)

                if trans_id > 0:
                    self.append_text_to_logs(f"Заявка выставлена. ID транзакции - {trans_id}")
                    
                    # Ждем немного для обработки заявки
                    await asyncio.sleep(0.5)
                    
                    try:
                        # Получаем список стоп-заявок для проверки
                        stop_orders = await self.quik.stop_orders.get_stop_orders()
                        
                        # Ищем нашу стоп-заявку по ID транзакции
                        for stop_order in stop_orders:
                            if (hasattr(stop_order, 'trans_id') and stop_order.trans_id == trans_id and 
                                stop_order.class_code == self.class_code and 
                                stop_order.sec_code == self.sec_code):
                                self.append_text_to_logs(f"Стоп-заявка выставлена. Номер стоп-заявки - {stop_order.order_num}")
                                break
                                
                    except Exception as e:
                        self.append_text_to_logs("Ошибка получения номера стоп-заявки.")
                else:
                    self.append_text_to_logs("Неудачная попытка выставления стоп-заявки.")
                    
            except AttributeError:
                # Если API не поддерживает стоп-заявки или методы отличаются
                self.append_text_to_logs("Стоп-заявки не поддерживаются данной версией API или требуют другой реализации.")
                self.append_text_to_logs(f"Параметры стоп-заявки:")
                self.append_text_to_logs(f"  Цена условия (тейк-профит): {condition_price}")
                self.append_text_to_logs(f"  Цена условия 2 (стоп-лимит): {condition_price2}")
                self.append_text_to_logs(f"  Цена заявки: {order_price}")
                self.append_text_to_logs(f"  Количество: 1 лот")
                self.append_text_to_logs(f"  Операция: Покупка")
                
        except Exception as e:
            self.append_text_to_logs(f"Ошибка выставления стоп-заявки: {e}")

    async def calculate_max_lots(self):
        """
        Рассчитать максимальное количество лотов в заявке
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            if not self.tool:
                self.append_text_to_logs("Ошибка: инструмент не инициализирован")
                return
                
            if not self.client_code:
                self.append_text_to_logs("Ошибка: код клиента не определен")
                return
                
            self.append_text_to_logs("Получаем максимальное количество лотов в заявке для текущей цены...")
            
            # Получаем текущую цену инструмента
            last_price = self.tool.get('last_price', 0)
            if last_price == 0:
                self.append_text_to_logs("Ошибка: последняя цена инструмента равна нулю")
                return
            
            # Вызываем функцию расчета покупки/продажи
            # Параметры: class_code, sec_code, client_code, account_id, price, is_buy, is_market
            calc_result = await self.quik.trading.calc_buy_sell(
                class_code=self.class_code,
                sec_code=self.sec_code,
                client_code=self.client_code,
                trd_acc_id=self.tool.get('account_id', ''),
                price=float(last_price),
                is_buy=True,     # Покупка
                is_market=False  # Лимитированная заявка
            )
            
            if calc_result is not None:
                # Выводим результат расчета
                qty = getattr(calc_result, 'qty', 0)
                commission = getattr(calc_result, 'comission', 0)  # Возможна опечатка в API как в C#
                if not commission:
                    commission = getattr(calc_result, 'commission', 0)  # Пробуем правильное написание
                
                self.append_text_to_logs(f"Количество лотов = {qty}, Комиссия = {commission}")
                
                # Пауза как в C# версии
                await asyncio.sleep(0.5)
                
            else:
                self.append_text_to_logs("Неудачная получения данных о максимальном количество лотов в заявке.")
                
        except AttributeError as e:
            # Если метод calc_buy_sell не существует в API
            self.append_text_to_logs("Функция CalcBuySell не поддерживается данной версией API.")
            self.append_text_to_logs(f"Параметры расчета:")
            self.append_text_to_logs(f"  Класс: {self.class_code}")
            self.append_text_to_logs(f"  Код бумаги: {self.sec_code}")
            self.append_text_to_logs(f"  Клиент: {self.client_code}")
            self.append_text_to_logs(f"  Счет: {self.tool.get('account_id', '') if self.tool else 'N/A'}")
            self.append_text_to_logs(f"  Цена: {self.tool.get('last_price', 0) if self.tool else 'N/A'}")
            self.append_text_to_logs(f"  Операция: Покупка (лимитированная заявка)")
            
        except Exception as e:
            self.append_text_to_logs(f"Ошибка выполнения функции CalcBuySell: {e}")

    async def get_trading_day(self):
        """
        Получить дату торговой сессии
        """
        try:
            if not self.quik or not self.is_server_connected:
                self.append_text_to_logs("Ошибка: не подключены к QUIK")
                return
                
            self.append_text_to_logs("Получаем дату торговой сессии...")
            
            # Получаем дату торговой сессии
            trading_date = await self.quik.trading.get_trade_date()
            
            if trading_date is not None:
                # Форматируем дату в строку
                if hasattr(trading_date, 'strftime'):
                    # Если это объект datetime
                    formatted_date = trading_date.strftime("%d.%m.%Y")
                elif hasattr(trading_date, 'date'):
                    # Если это объект с атрибутом date
                    formatted_date = trading_date.date().strftime("%d.%m.%Y")
                else:
                    # Если это строка или другой тип
                    formatted_date = str(trading_date)
                
                self.append_text_to_logs(f"Дата торговой сессии = {formatted_date}")
                
                # Пауза как в C# версии
                await asyncio.sleep(0.5)
                
            else:
                self.append_text_to_logs("Неудачная получения даты торговой сессии.")
                
        except AttributeError as e:
            # Если метод get_trade_date не существует в API
            self.append_text_to_logs("Функция GetTradeDate не поддерживается данной версией API.")
            self.append_text_to_logs("Возможные альтернативы:")
            self.append_text_to_logs("  - Использовать текущую дату системы")
            self.append_text_to_logs("  - Получить дату из параметров инструмента")
            
            # Показываем текущую дату как альтернативу
            from datetime import datetime
            current_date = datetime.now().strftime("%d.%m.%Y")
            self.append_text_to_logs(f"Текущая дата системы = {current_date}")
            
        except Exception as e:
            self.append_text_to_logs(f"Ошибка выполнения функции GetTradeDate: {e}")
