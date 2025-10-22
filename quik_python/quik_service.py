"""
QUIK service for managing connection and communication
"""

import logging
import asyncio
import json
import socket
import select
import threading
import atexit
from typing import Optional, TYPE_CHECKING, Any
from .events import QuikEvents
from .storage import IPersistentStorage
from .exceptions import ConnectionException, TimeoutException

CRLF = "\r\n"
CR = "\n"


if TYPE_CHECKING:
    from .functions.candle_functions import CandleFunctions
    from .functions.stop_order_functions import StopOrderFunctions


class QuikService:
    """
    Service for managing QUIK connection and communication
    """
    logger = logging.getLogger('QuikService')
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # Создаём ключ по параметрам
        key = (args, frozenset(kwargs.items()))
        with cls._lock:
            if key not in cls._instances:
                # logger.debug(f"Creating new QuikService instance for params: {key}")
                instance = super().__new__(cls)
                instance._initialized = False
                cls._instances[key] = instance
            else:
                # logger.debug(f"Reusing existing QuikService instance for params: {key}")
                pass
        return cls._instances[key]


    def __init__(self, port: int, host: str = "127.0.0.1"):
        if not self._initialized:
            self.logger.info(f"Initializing with port = {port}, host = {host}")
            self.port = port
            self.host = host
            self._initialized = True

            self.default_send_timeout = 10.0
            self.storage: Optional[IPersistentStorage] = None
            self.events = QuikEvents(self)
            self.candles: Optional['CandleFunctions'] = None
            self.stop_orders: Optional['StopOrderFunctions'] = None
            self.working_folder: Optional[str] = None
            self._connected = False
            self._event_listener_task: Optional[asyncio.Task] = None
            # Переменные для переиспользования соединения
            self._reader: Optional[asyncio.StreamReader] = None
            self._writer: Optional[asyncio.StreamWriter] = None
            self._connection_lock = asyncio.Lock()
            # Мьютекс для сериализации запросов/ответов
            self._request_lock = asyncio.Lock()
            # Регистрируем cleanup при завершении программы
            atexit.register(self._cleanup_on_exit)
    
    def _cleanup_on_exit(self):
        """Cleanup when program exits"""
        try:
            if self._connected or self._writer is not None:
                self.logger.info(f"QuikService cleanup on exit (port {self.port})")
                # Синхронное закрытие при завершении программы
                if self._writer and not self._writer.is_closing():
                    self._writer.close()
                self._connected = False
        except Exception:
            pass  # Игнорируем ошибки при завершении
    
    @classmethod
    def create(cls, port: int, host: str = "127.0.0.1") -> 'QuikService':
        """
        Create new QuikService instance
        
        Args:
            port: Port for QUIK communication
            host: Host for QUIK communication
            
        Returns:
            New QuikService instance
        """
        service = cls(port, host)
        return service
    
    async def start_event_listener(self) -> None:
        """Start listening for events from QUIK"""
        if self._event_listener_task and not self._event_listener_task.done():
            return
            
        self._event_listener_task = asyncio.create_task(self._event_listener_loop())
    
    async def _event_listener_loop(self) -> None:
        """Main event listener loop with connection monitoring and recovery"""
        event_reader = None
        event_writer = None
        reconnect_delay = 5.0
        max_reconnect_delay = 60.0
        
        while True:
            try:
                # Listen for events on a separate port (port + 1)
                event_port = self.port + 1
                
                try:
                    self.logger.info(f"Attempting to connect to event port {event_port}...")
                    event_reader, event_writer = await asyncio.wait_for(
                        asyncio.open_connection(self.host, event_port),
                        timeout=10.0
                    )
                    
                    # Настройка TCP_NODELAY для event соединения
                    event_sock = event_writer.get_extra_info('socket')
                    if event_sock:
                        event_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        event_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    
                    self._connected = True
                    reconnect_delay = 5.0  # Сбрасываем задержку после успешного подключения
                    self.logger.info(f"Successfully connected to event listener on port {event_port}")
                    
                    try:
                        while True:
                            # Использование select для проверки готовности данных
                            sock_fd = event_sock.fileno() if event_sock else None
                            if sock_fd and hasattr(select, 'select'):
                                # Проверяем готовность данных с timeout
                                ready, _, _ = select.select([sock_fd], [], [], 0.5)
                                if not ready:
                                    # Нет данных, продолжаем цикл
                                    await asyncio.sleep(0.03)
                                    continue
                            
                            # Read event data with timeout для обнаружения разорванного соединения
                            event_data = await asyncio.wait_for(
                                event_reader.readline(),
                                timeout=30.0  # Heartbeat timeout
                            )
                            
                            if not event_data:
                                self.logger.warning("Event connection closed by server")
                                break
                            
                            # Parse event
                            try:
                                event_json = event_data.decode('cp1251').strip()
                                ## self.logger.debug(f"Received event JSON: {event_json}")
                                if event_json:  # Игнорируем пустые строки
                                    event = json.loads(event_json)

                                    
                                    if isinstance(event, dict) and 'cmd' in event and 'data' in event:
                                        # Запускаем обработку события в фоне, не ждём завершения
                                        # Это позволяет быстро читать следующие события из сокета
                                        asyncio.create_task(
                                            self.events.handle_event_data(event['cmd'], event['data'])
                                        )
                            
                            except json.JSONDecodeError as je:
                                self.logger.error(f"Failed to parse event JSON: {je}, data: {event_json}")
                                continue
                            except Exception as e:
                                self.logger.error(f"Error processing event: {e}")
                                continue
                    
                    except asyncio.TimeoutError:
                        self.logger.warning("Event listener timeout - connection may be dead")
                        break
                    
                    finally:
                        # Закрываем соединение
                        if event_writer and not event_writer.is_closing():
                            event_writer.close()
                            try:
                                await event_writer.wait_closed()
                            except Exception:
                                pass
                        self._connected = False
                        self.logger.info("Event listener connection closed")
                
                except (socket.error, OSError, ConnectionRefusedError, asyncio.TimeoutError) as e:
                    self._connected = False
                    self.logger.error(f"Event listener connection failed: {e}")

                    # Увеличиваем задержку при неудачных попытках подключения
                    await asyncio.sleep(reconnect_delay)
                    reconnect_delay = min(reconnect_delay * 1.5, max_reconnect_delay)
                    self.logger.info(f"Will retry event connection in {reconnect_delay:.1f} seconds")
                
            except asyncio.CancelledError:
                self.logger.info("Event listener cancelled")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in event listener: {e}")
                self._connected = False
                await asyncio.sleep(5)
    
    def stop(self) -> None:
        """Stop QUIK service gracefully"""
        if not self._connected and self._event_listener_task is None:
            return  # Already stopped

        self.logger.info("Stopping QUIK service...")

        # Устанавливаем флаг отключения
        self._connected = False
        
        # Отменяем задачу прослушивания событий
        if self._event_listener_task and not self._event_listener_task.done():
            try:
                self._event_listener_task.cancel()
                self.logger.info("Event listener task cancelled")
            except Exception as e:
                self.logger.error(f"Error cancelling event listener: {e}")

        # Закрыть соединение для отправки запросов
        if self._writer and not self._writer.is_closing():
            try:
                self._writer.close()
                self.logger.info("Request connection closed")
            except Exception as e:
                self.logger.error(f"Error closing writer: {e}")

        # Очищаем ссылки
        self._reader = None
        self._writer = None
        self._event_listener_task = None
        self.logger.info("QUIK service stopped")

    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            if self._connected or self._writer is not None:
                # Синхронное закрытие при уничтожении объекта
                if self._writer and not self._writer.is_closing():
                    self._writer.close()
                self._connected = False
        except Exception:
            pass  # Игнорируем ошибки в деструкторе
    
    async def _ensure_connection(self) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Ensure connection is established and return reader/writer"""
        async with self._connection_lock:
            # Проверяем, есть ли активное соединение
            if self._writer and not self._writer.is_closing():
                return self._reader, self._writer

            # Устанавливаем новое соединение
            try:
                self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

                # Настройка TCP_NODELAY для снижения латентности
                sock = self._writer.get_extra_info('socket')
                if sock:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                return self._reader, self._writer
            except Exception as e:
                raise ConnectionException(f"Failed to connect to QUIK: {e}")
    
    def is_service_connected(self) -> bool:
        """
        Check if service is connected to QUIK
        
        Returns:
            True if connected
        """
        return self._connected
    
    async def send_request(self, function_name: str, params: list[Any] = None, trans_id: int = 0, timeout: Optional[float] = None) -> Any:
        """
        Send request to QUIK Lua script
        
        Args:
            function_name: Name of Lua function to call
            params: Function parameters
            timeout: Request timeout in seconds
            
        Returns:
            Response from QUIK
            
        Raises:
            ConnectionException: If connection to QUIK fails
            TimeoutException: If request times out
        """
        # Сериализация всех запросов для избежания смешивания ответов
        async with self._request_lock:
            if params is None or len(params) == 0:
                data = '""'
            elif len(params) == 1 and isinstance(params[0], dict):
                data = json.dumps(params[0], ensure_ascii=False)
            else:
                data = '"' + '|'.join(map(str, params)) + '"'

            t = ''
            #t = '' if timeout is None else int(timeout)

            request_data = f'{{"data": {data}, "id": {trans_id}, "cmd": "{function_name}", "t": "{t}"}}{CRLF}'
            # self.logger.debug(f"Sending request: {request_data}")

            attempt = 0
            try:
                while attempt < 2:
                    # Используем переиспользуемое соединение
                    reader, writer = await self._ensure_connection()

                    # Send request
                    writer.write(request_data.encode('cp1251'))
                    await asyncio.wait_for(writer.drain(), timeout=timeout or self.default_send_timeout)

                    response_list = []
                    while(True):
                        # Read response
                        data = await asyncio.wait_for(
                            reader.read(8192),
                            timeout=timeout or self.default_send_timeout
                        )
                        if data:
                            s = data.decode('cp1251')
                            response_list.append(s)
                            if s.endswith(CR):
                                attempt=999
                                break
                        elif not data:
                            # Если данных нет, значит соединение разорвано
                            self._writer = None
                            self._reader = None
                            # Соединение могло быть закрыто, пробуем переподключиться
                            reader, writer = await self._ensure_connection()
                            attempt += 1

                # Done
                response_json = ''.join(response_list).strip()
                response = json.loads(response_json)

                # Check for errors
                if isinstance(response, dict) and 'lua_error' in response:
                    raise Exception(f"QUIK Lua error: {response['lua_error']}")
                return response

            except asyncio.TimeoutError as e:
                raise TimeoutException(f"Request to {function_name} timed out: {e}")
            except (socket.error, OSError) as e:
                # При ошибке соединения сбрасываем кэшированное соединение
                self._writer = None
                self._reader = None
                raise ConnectionException(f"Failed to connect to QUIK: {e}")
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON response from QUIK: {e}.")
            except Exception as e:
                raise Exception(f"Failed to receive response from QUIK: {e}.")


    async def call_function(self, function_name: str, *args, trans_id:int=0, timeout: Optional[float] = None) -> Any:
        """
        Call QUIK function with positional arguments
        
        Args:
            function_name: Name of Lua function to call
            *args: Function arguments
            timeout: Request timeout in seconds
            
        Returns:
            Response from QUIK
        """
        params = list(args) if args else {}
        return await self.send_request(function_name=function_name, params=params, trans_id=trans_id, timeout=timeout)