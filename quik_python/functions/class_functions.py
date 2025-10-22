"""
Class functions for QUIK interaction
"""
#OK+
from typing import List, Optional
from .base_functions import BaseFunctions
from ..data_structures import ClassInfo, SecurityInfo, TradeAccounts



class ClassFunctions(BaseFunctions):
    """
    Функции для обращения к спискам доступных параметров
    """

    async def get_classes_list(self) -> List[str]:
        """
        Функция предназначена для получения списка кодов классов, переданных с сервера в ходе сеанса связи.

        Returns:
            Список кодов классов
        """
        result = await self.call_function("getClassesList")
        return result['data'].split(',') if result else []


    async def get_class_info(self, class_code: str) -> Optional[ClassInfo]:
        """
        Функция предназначена для получения информации о классе.

        Args:
            class_code: Код класса

        Returns:
            Информация о классе
        """
        result = await self.call_function("getClassInfo", class_code)
        return ClassInfo.from_dict(result['data']) if result else None


    async def get_security_info(self, class_code: str, sec_code: str) -> Optional[SecurityInfo]:
        """
        Функция предназначена для получения информации по бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            Информация об инструменте
        """
        result = await self.call_function("getSecurityInfo", class_code, sec_code)
        return SecurityInfo.from_dict(result['data']) if result else None


    async def get_class_securities(self, class_code: str) -> List[str]:
        """
        Функция предназначена для получения списка кодов бумаг для списка классов, заданного списком кодов.

        Args:
            class_code: Код класса

        Returns:
            Список кодов инструментов
        """
        result = await self.call_function("getClassSecurities", class_code)
        return result['data'].split(',') if result else []


    async def get_security_class(self, classes_list: str, sec_code: str) -> str:
        """
        Функция предназначена для определения класса по коду инструмента из заданного списка классов.

        Args:
            classes_list: Список кодов классов через запятую
            sec_code: Код инструмента

        Returns:
            Код класса инструмента или пустая строка
        """
        result = await self.call_function("getSecurityClass", classes_list, sec_code)
        return result['data'] or ""


    async def get_client_code(self) -> str:
        """
        Функция возвращает код клиента.

        Returns:
            Код клиента
        """
        result = await self.call_function("getClientCode")
        return result['data'] or ""


    async def get_client_codes(self) -> List[str]:
        """
        Функция возвращает список всех кодов клиента.

        Returns:
            Список кодов клиента
        """
        result = await self.call_function("getClientCodes")
        return result['data'] if result else []


    async def get_trade_account(self, class_code: str) -> str:
        """
        Функция возвращает таблицу с описанием торгового счета для запрашиваемого кода класса.

        Args:
            class_code: Код класса

        Returns:
            str: Описание торгового счета
        """
        result = await self.call_function("getTradeAccount", class_code)
        return result['data'] or ""


    async def get_trade_accounts(self) -> List[TradeAccounts]:
        """
        Функция возвращает таблицу всех счетов в торговой системе.

        Returns:
            Список всех торговых счетов
        """
        result = await self.call_function("getTradeAccounts")
        return [TradeAccounts.from_dict(item) for item in result['data']] if result else []
