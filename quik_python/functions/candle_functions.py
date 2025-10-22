"""
Candle functions for QUIK interaction
"""

import logging
from typing import List, Optional, Callable, TYPE_CHECKING
from .base_functions import BaseFunctions
from ..data_structures import Candle, CandleInterval

if TYPE_CHECKING:
    from ..quik import Quik


# Типы для обработчиков событий (эквивалент C# делегатов)
CandleHandler = Callable[[Candle], None]


class CandleFunctions(BaseFunctions):
    """
    Функции для работы со свечами
    """

    logger = logging.getLogger('CandleFunctions')

    def __init__(self, port: int, quik_instance: 'Quik', host: str = "127.0.0.1"):
        """
        Initialize CandleFunctions

        Args:
            port: Port number for communication
            quik_instance: Reference to main Quik instance (equivalent to QuikService)
            host: Host address
        """
        super().__init__(port, host)
        self._quik = quik_instance  # Эквивалент QuikService в C#
        self._new_candle_handlers: List[CandleHandler] = []  # Эквивалент события NewCandle

    @property
    def quik_service(self) -> 'Quik':
        """
        Эквивалент свойства QuikService в C#
        
        Returns:
            Reference to main Quik instance
        """
        return self._quik

    def add_new_candle_handler(self, handler: CandleHandler) -> None:
        """
        Подписка на событие получения новой свечи (эквивалент event NewCandle)
        
        Args:
            handler: Обработчик события новой свечи
        """
        if handler not in self._new_candle_handlers:
            self._new_candle_handlers.append(handler)

    def remove_new_candle_handler(self, handler: CandleHandler) -> None:
        """
        Отписка от события получения новой свечи
        
        Args:
            handler: Обработчик события для удаления
        """
        if handler in self._new_candle_handlers:
            self._new_candle_handlers.remove(handler)

    def raise_new_candle_event(self, candle: Candle) -> None:
        """
        Эквивалент internal void RaiseNewCandleEvent(Candle candle) в C#
        Вызывает событие получения новой свечи
        
        Args:
            candle: Новая свеча
        """
        for handler in self._new_candle_handlers:
            try:
                handler(candle)
            except Exception as e:
                # Логируем ошибку, но не прерываем обработку других обработчиков
                self.logger.error(f"Ошибка в обработчике события новой свечи: {e}")

    async def get_num_candles_by_tag(self, graphic_tag: str) -> int:
        """
        Функция предназначена для получения количества свечей по тегу

        Args:
            graphic_tag: Строковый идентификатор графика или индикатора

        Returns:
            Количество свечей
        """
        result = await self.call_function("get_num_candles", graphic_tag)
        return int(result['data']) if result and 'data' in result else 0


    async def get_all_candles_by_tag(self, graphic_tag: str) -> List[Candle]:
        """
        Функция предназначена для получения информации о свечках по идентификатору.
        Возвращаются все доступные свечки.

        Args:
            graphic_tag: Строковый идентификатор графика или индикатора

        Returns:
            Список всех доступных свечей
        """
        return await self.get_candles_by_tag(graphic_tag, 0, 0, 0)


    async def get_candles_by_tag(self, graphic_tag: str, line: int, first: int, count: int) -> List[Candle]:
        """
        Функция предназначена для получения информации о свечках по идентификатору (заказ данных для построения графика плагин не осуществляет, поэтому для успешного доступа нужный график должен быть открыт).

        Args:
            graphic_tag: Строковый идентификатор графика или индикатора
            line:       Номер линии графика или индикатора. Первая линия имеет номер 0
            first:      Индекс первой свечки. Первая (самая левая) свечка имеет индекс 0
            count:      Количество запрашиваемых свечек</param>

        Returns:
            Список свечей
        """
        result = await self.call_function("get_candles", graphic_tag, line, first, count)
        candle_list = []
        if result and isinstance(result['data'], list):
            for candle_data in result['data']:
                candle_data['class_'] = candle_data.pop('class')
                candle_list.append(Candle.from_dict(candle_data))

        return candle_list


    async def get_all_candles(self, class_code: str, sec_code: str, 
                            interval: CandleInterval, param: str = "-") -> List[Candle]:
        """
        Функция возвращает список свечек указанного инструмента заданного интервала и параметра запрошенных данных.

        Args:
            class_code: Класс инструмента.
            sec_code: Код инструмента
            interval: Интервал свечей
            param: Параметр запрашиваемых свечей.

        Returns:
            Список свечей
        """
        return await self.get_last_candles(class_code, sec_code, interval, 0, param)


    async def get_last_candles(self, class_code: str, sec_code: str,
                            interval: CandleInterval, count: int, param: str = "-") -> List[Candle]:
        """
        Возвращает заданное количество свечек указанного инструмента и интервала с конца.

        Args:
            class_code: Код класса
            sec_code: Код инструмента
            interval: Интервал свечей
            count: Количество свечей
            param: Параметр запрашиваемых свечей.

        Returns:
            Список свечей
        """
        result = await self.call_function("get_candles_from_data_source", 
                                        class_code, sec_code, interval.value, param, count)
        candle_list = []
        if result and isinstance(result['data'], list):
            for candle_data in result['data']:
                candle_data['class_'] = candle_data.pop('class')
                candle_list.append(Candle.from_dict(candle_data))
        return candle_list


    async def subscribe(self, class_code: str, sec_code: str, interval: CandleInterval, param: str = "-", mode: str = "new") -> Optional[str]:
        """
        Осуществляет подписку на получение исторических данных (свечи)

        Args:
            class_code: Класс инструмента.
            sec_code: Код инструмента
            interval: Интервал свечей
            param: Параметр запрашиваемых свечей.

        Returns:
            Идентификатор источника данных
        """
        result = await self.call_function("subscribe_to_candles", class_code, sec_code, interval.value, param, mode)
        return result['data'] if result else None


    async def unsubscribe(self, class_code: str, sec_code: str, interval: CandleInterval, param: str = "-", mode: str = "new") -> Optional[str]:
        """
        Отписывается от получения исторических данных (свечей)

        Args:
            class_code: Класс инструмента.
            sec_code: Код инструмента
            interval: Интервал свечей
            param: Параметр запрашиваемых свечей.

        Returns:
            Идентификатор источника данных
        """
        result = await self.call_function("unsubscribe_from_candles", class_code, sec_code, interval.value, param, mode)
        return result['data'] if result else None


    async def is_subscribed(self, class_code: str, sec_code: str, interval: CandleInterval, param: str = "-", mode: str = "new") -> bool:
        """
        Проверка состояния подписки на исторические данные (свечи)

        Args:
            class_code: Класс инструмента.
            sec_code: Код инструмента
            interval: Интервал свечей
            param: Параметр запрашиваемых свечей.

        Returns:
            True если есть подписка
        """
        result = await self.call_function("is_subscribed", class_code, sec_code, interval.value, param, mode)
        return bool(result['data']) if result else False
