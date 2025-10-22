"""
Order book functions for QUIK interaction
"""


from typing import Optional
from .base_functions import BaseFunctions
from ..data_structures import OrderBook


class OrderBookFunctions(BaseFunctions):
    """
    Функции для работы со стаканом котировок
    """

    async def subscribe(self, class_code: str, sec_code: str) -> bool:
        """
        Функция заказывает на сервер получение стакана по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если подписка успешна
        """
        result = await self.call_function("Subscribe_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def unsubscribe(self, class_code: str, sec_code: str) -> bool:
        """
        Функция отменяет заказ на получение с сервера стакана по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если отписка успешна
        """
        result = await self.call_function("Unsubscribe_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def is_subscribed(self, class_code: str, sec_code: str) -> bool:
        """
        Функция позволяет узнать, заказан ли с сервера стакан по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если есть подписка
        """
        result = await self.call_function("IsSubscribed_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def get_quote_level2(self, class_code: str, sec_code: str) -> Optional[OrderBook]:
        """
        Функция предназначена для получения стакана по указанному классу и инструменту

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            Стакан котировок
        """
        result = await self.call_function("GetQuoteLevel2", class_code, sec_code)
        return OrderBook.from_dict(result['data']) if result['data'] else None

