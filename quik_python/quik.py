"""
Main Quik class - entry point for QUIK Python API
"""

import logging
from typing import Optional
from datetime import timezone

from .quik_service import QuikService
from .storage import IPersistentStorage, InMemoryStorage
from .functions import DebugFunctions, ServiceFunctions, ClassFunctions, OrderBookFunctions, \
                        TradingFunctions, StopOrderFunctions, OrderFunctions, CandleFunctions



class Quik:
    """
    Quik interface in Python
    """

    # Default port for QUIK communication
    DEFAULT_PORT = 34130

    # Default host
    DEFAULT_HOST = "127.0.0.1"

    logger = logging.getLogger('Quik')

    def __init__(self, port: int = DEFAULT_PORT, storage: Optional[IPersistentStorage] = None, host: str = DEFAULT_HOST):
        """
        Quik interface in Python constructor

        Args:
            port: Port number for communication with QUIK Lua script
            storage: Persistent storage implementation
            host: Host address for QUIK connection
        """
        self._initialized = False
        self.storage = storage if storage is not None else InMemoryStorage()
        self._quik_service = QuikService.create(port, host)

        # Configure service
        self._quik_service.storage = self.storage
        self.events = self._quik_service.events

        # Initialize function modules
        self._debug = DebugFunctions(port, host)
        self._service = ServiceFunctions(port, host)
        self._clazz = ClassFunctions(port, host)  # 'class' is reserved in Python
        self._order_book = OrderBookFunctions(port, host)
        self._trading = TradingFunctions(port, host)
        self._stop_orders = StopOrderFunctions(port, self, host)
        self._orders = OrderFunctions(port, self, host)
        self._candles = CandleFunctions(port, self, host)

        # Configure service dependencies
        self._quik_service.candles = self._candles
        self._quik_service.stop_orders = self._stop_orders

        # Working folder will be initialized on first use
        self._quik_service.working_folder = None

        # Timezone for converting QUIK local time to UTC
        self.timezone_info: Optional[timezone] = None

    @property
    def debug(self) -> DebugFunctions:
        """
        Access to debug functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._debug

    @property
    def service(self) -> ServiceFunctions:
        """
        Access to service functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._service

    @property
    def clazz(self) -> ClassFunctions:
        """
        Access to class functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._clazz

    @property
    def order_book(self) -> OrderBookFunctions:
        """
        Access to order book functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._order_book

    @property
    def trading(self) -> TradingFunctions:
        """
        Access to trading functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._trading

    @property
    def stop_orders(self) -> StopOrderFunctions:
        """
        Access to stop order functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._stop_orders

    @property
    def orders(self) -> OrderFunctions:
        """
        Access to order functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._orders

    @property
    def candles(self) -> CandleFunctions:
        """
        Access to candle functions
        """
        if not self._initialized:
            raise RuntimeError("QUIK service is not initialized")
        return self._candles


    async def initialize(self):
        """
        Initialize QUIK service asynchronously
        Call this method after creating Quik instance
        """
        # Start event listener
        await self._quik_service.start_event_listener()

        # Initialize working folder
        await self._initialize_working_folder()
        self._initialized = True

    async def _initialize_working_folder(self):
        """Initialize working folder asynchronously"""
        try:
            self._quik_service.working_folder = await self._service.get_working_folder()
        except Exception :
            # Will retry later if needed
            pass

    def stop_service(self):
        """
        Stop QUIK service gracefully
        """
        if self._initialized:
            self._quik_service.stop()
            self._initialized = False

    def __del__(self):
        """Destructor to ensure service is stopped"""
        try:
            if self._initialized:
                self.stop_service()
        except Exception:
            pass  # Игнорируем ошибки в деструкторе

    def is_service_alive(self) -> bool:
        """
        Check if service is connected to QUIK

        Returns:
            True if connected, False otherwise
        """
        return self._quik_service.is_service_connected()

    @property
    def default_send_timeout(self) -> float:
        """
        Default timeout to use for send operations if no specific timeout supplied.
        """
        return self._quik_service.default_send_timeout

    @default_send_timeout.setter
    def default_send_timeout(self, value: float):
        """
        Set default timeout for send operations
        """
        self._quik_service.default_send_timeout = value

    # Connection methods
    async def connect(self) -> bool:
        """Connect to QUIK terminal"""
        return await self.initialize()

    def disconnect(self):
        """Disconnect from QUIK terminal gracefully"""
        try:
            self.stop_service()
        except Exception as e:
            self.logger.error(f"Error during disconnect: {e}")

    # Trading function delegates
    async def send_transaction(self, transaction):
        """Delegate to trading.send_transaction"""
        return await self.trading.send_transaction(transaction)

    async def calc_buy_sell(self, class_code: str, sec_code: str, client_code: str,
                            trd_acc_id: str, price: float, is_buy: bool, is_market: bool):
        """Delegate to trading.calc_buy_sell"""
        return await self.trading.calc_buy_sell(class_code, sec_code, client_code, trd_acc_id, price, is_buy, is_market)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - ensure cleanup"""
        try:
            self.stop_service()
        except Exception as e:
            self.logger.error(f"Error during context exit: {e}")
        return False  # Don't suppress exceptions
