"""
Trading functions for QUIK interaction
"""

import logging
from typing import List, Optional


from .base_functions import BaseFunctions
from ..data_structures import DepoLimit, DepoLimitEx, MoneyLimit, MoneyLimitEx, Transaction, ParamTable, \
                        FuturesLimits, FuturesLimitType, FuturesClientHolding, OptionBoard, Trade, \
                        AllTrade, PortfolioInfo, PortfolioInfoEx, BuySellInfo, QuikDateTime, \
                        CalcBuySellResult, ParamNames, LimitKind

class TradingFunctions(BaseFunctions):
    """
    Функции взаимодействия скрипта Lua и Рабочего места QUIK
    """
    logger = logging.getLogger('TradingFunctions')

    async def get_depo(self, client_code: str = "", firm_id: str = "", sec_code: str = "", account: str = "") -> Optional[DepoLimit]:
        """
        Функция для получения информации по бумажным лимитам

        Args:
            client_code: Код клиента
            firm_id: Идентификатор фирмы
            sec_code: Код инструмента
            account: Торговый счет

        Returns:
            Информация по бумажным лимитам
        """
        result = await self.call_function("getDepo", client_code, firm_id, sec_code, account)
        if result and result.get('data'):
            return DepoLimit.from_dict(result['data'])
        return None


    async def get_depo_ex(self, firm_id: str = "", client_code: str = "", sec_code: str = "", acc_id: str = "", limit_kind: LimitKind = LimitKind.T0) -> Optional[DepoLimitEx]:
        """
        Функция для получения информации по бумажным лимитам указанного типа

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента
            sec_code: Код инструмента
            acc_id: Торговый счет
            limit_kind: Тип лимита

        Returns:
            Информация по бумажным лимитам
        """
        result = await self.call_function("getDepoEx", firm_id, client_code, sec_code, acc_id, limit_kind.value)
        if result and result.get('data'):
            return DepoLimitEx.from_dict(result['data'])
        return None


    async def get_depo_limits(self, sec_code: str = "") -> List[DepoLimitEx]:
        """
        Возвращает список всех записей из таблицы 'Лимиты по бумагам', отфильтрованных по коду инструмента.

        Returns:
            Список лимитов по бумагам
        """
        result = await self.call_function("get_depo_limits", sec_code)
        if result and isinstance(result.get('data'), list):
            return [DepoLimitEx.from_dict(item) for item in result['data']]
        return []


    async def get_money(self, client_code: str = "", firm_id: str = "", tag: str = "", curr_code: str = "") -> Optional[MoneyLimit]:
        """
        Функция для получения информации по денежным лимитам

        Args:
            client_code: Код клиента
            firm_id: Идентификатор фирмы
            tag: Тег расчетов
            curr_code: Код валюты

        Returns:
            Информация по денежным лимитам
        """
        result = await self.call_function("getMoney", client_code, firm_id, tag, curr_code)
        if result and result.get('data'):
            return MoneyLimit.from_dict(result['data'])
        return None

    async def get_money_ex(self, firm_id: str = "", client_code: str = "", tag: str = "", curr_code: str = "", limit_kind: LimitKind = LimitKind.T0) -> Optional[MoneyLimitEx]:
        """
        Функция для получения информации по денежным лимитам указанного типа

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента
            tag: Тег расчетов
            curr_code: Код валюты
            limit_kind: Тип лимита

        Returns:
            Информация по денежным лимитам указанного типа
        """
        result = await self.call_function("getMoneyEx", firm_id, client_code, tag, curr_code, limit_kind.value)
        if result and result.get('data'):
            return MoneyLimitEx.from_dict(result['data'])
        return None


    async def get_money_limits(self) -> List[MoneyLimitEx]:
        """
        Функция для получения информации по денежным лимитам всех торговых счетов (кроме фьючерсных) и валют.
        Лучшее место для получения связки clientCode + firmid

        Returns:
            Список денежных лимитов
        """
        result = await self.call_function("getMoneyLimits")
        if result and isinstance(result.get('data'), list):
            return [MoneyLimitEx.from_dict(item) for item in result['data']]
        return []


    async def param_request(self, class_code: str, sec_code: str = "", param_name: ParamNames = ParamNames.CODE) -> bool:
        """
        Функция заказывает получение параметров Таблицы текущих торгов

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента
            param_name: Имя параметра

        Returns:
            Результат заказа параметра
        """
        result = await self.call_function("paramRequest", class_code, sec_code, param_name.value)
        return result.get('data', False) if result else False


    async def cancel_param_request(self, class_code: str, sec_code: str = "", param_name: ParamNames = ParamNames.CODE) -> bool:
        """
        Функция отмены заказа на изменения параметра

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента
            param_name: Имя параметра

        Returns:
            Результат отмены заказа параметра
        """
        result = await self.call_function("cancelParamRequest", class_code, sec_code, param_name.value)
        return result.get('data', False) if result else False


    async def get_param_ex(self, class_code: str, sec_code: str = "", param_name: ParamNames = ParamNames.CODE) -> Optional[ParamTable]:
        """
        Функция для получения параметров таблицы «Текущие торги» с дополнительной информацией об изменении параметра

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента
            param_name: Имя параметра

        Returns:
            Информация о параметре
        """
        result = await self.call_function("getParamEx", class_code, sec_code, param_name.value)
        if result and result.get('data'):
            return ParamTable.from_dict(result['data'])
        return None


    async def get_param_ex2(self, class_code: str, sec_code: str = "", param_name: ParamNames = ParamNames.CODE) -> Optional[ParamTable]:
        """
        Функция для получения параметров таблицы «Текущие торги» с дополнительной информацией об изменении параметра (версия 2)

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента
            param_name: Имя параметра

        Returns:
            Информация о параметре
        """
        result = await self.call_function("getParamEx2", class_code, sec_code, param_name.value)
        if result and result.get('data'):
            return ParamTable.from_dict(result['data'])
        return None


    async def get_futures_limit(self, firm_id: str = "", acc_id: str = "", limit_type: FuturesLimitType = FuturesLimitType.MONEY, curr_code: str = "") -> Optional[FuturesLimits]:
        """
        Функция для получения информации по фьючерсным лимитам

        Args:
            firm_id: Идентификатор фирмы
            trd_acc_id: Торговый счет
            limit_type: Тип лимита
            curr_code: Код валюты

        Returns:
            Информация по фьючерсным лимитам
        """
        result = await self.call_function("getFuturesLimit", firm_id, acc_id, limit_type.value, curr_code)
        if result and result.get('data'):
            return FuturesLimits.from_dict(result['data'])
        return None


    async def get_futures_client_limits(self) -> List[FuturesLimits]:
        """
        Функция для получения информации по всем фьючерсным лимитам клиента

        Returns:
            Список фьючерсных лимитов клиента
        """
        result = await self.call_function("getFuturesClientLimits")
        if result and isinstance(result.get('data'), list):
            return [FuturesLimits.from_dict(item) for item in result['data']]
        return []


    async def get_futures_holding(self, firm_id: str, acc_id: str, sec_code: str, pos_type: int) -> Optional[FuturesClientHolding]:
        """
        Функция для получения информации по фьючерсным позициям

        Args:
            firm_id: Идентификатор фирмы
            acc_id: Торговый счет
            sec_code: Код инструмента
            pos_type: Тип позиции

        Returns:
            Информация по фьючерсным позициям
        """
        result = await self.call_function("getFuturesHolding", firm_id, acc_id, sec_code, pos_type)
        if result and result.get('data'):
            return FuturesClientHolding.from_dict(result['data'])
        return None


    async def get_futures_client_holdings(self) -> List[FuturesClientHolding]:
        """
        Функция для получения информации по всем фьючерсным позициям клиента

        Returns:
            Список фьючерсных позиций клиента
        """
        result = await self.call_function("getFuturesClientHoldings")
        if result and isinstance(result.get('data'), list):
            return [FuturesClientHolding.from_dict(item) for item in result['data']]
        return []


    async def get_option_board(self, class_code: str, sec_code: str) -> Optional[OptionBoard]:
        """
        Функция для получения опционного борда

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента

        Returns:
            Опционный борд
        """
        result = await self.call_function("getOptionBoard", class_code, sec_code)
        if result and result.get('data'):
            return OptionBoard.from_dict(result['data'])
        return None


    async def get_trades(self, class_code: str, sec_code: str) -> List[Trade]:
        """
        Функция для получения таблицы сделок

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента

        Returns:
            Список сделок
        """
        result = await self.call_function("get_trades", class_code, sec_code)
        if result and isinstance(result.get('data'), list):
            return [Trade.from_dict(item) for item in result['data']]
        return []


    async def get_trades_list(self) -> List[Trade]:
        """
        Функция для получения таблицы сделок

        Returns:
            Список сделок
        """
        result = await self.call_function("get_trades")
        if result and isinstance(result.get('data'), list):
            return [Trade.from_dict(item) for item in result['data']]
        return []


    async def get_trades_by_order_number(self, order_num: int) -> List[Trade]:
        """
        Функция для получения сделок по номеру заявки

        Args:
            order_num: Номер заявки

        Returns:
            Список сделок
        """
        result = await self.call_function("get_Trades_by_OrderNumber", order_num)
        if result and isinstance(result.get('data'), list):
            return [Trade.from_dict(item) for item in result['data']]
        return []


    async def get_trade_date(self) -> Optional[QuikDateTime]:
        """
        Функция для получения даты торговой сессии

        Returns:
            Дата торговой сессии
        """
        result = await self.call_function("getTradeDate")
        if result and result.get('data'):
            return QuikDateTime.from_dict(result['data'])
        return None


    async def get_portfolio_info(self, firm_id: str, client_code: str) -> Optional[PortfolioInfo]:
        """
        Функция для получения информации по денежным средствам

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента

        Returns:
            Информация по денежным средствам
        """
        result = await self.call_function("getPortfolioInfo", firm_id, client_code)
        if result and result.get('data'):
            return PortfolioInfo.from_dict(result['data'])
        return None


    async def get_portfolio_info_ex(self, firm_id: str, client_code: str, limit_kind: int = 0) -> Optional[PortfolioInfoEx]:
        """
        Функция для получения информации по денежным средствам с учетом вида лимита

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента
            limit_kind: Тип лимита

        Returns:
            Информация по денежным средствам
        """
        result = await self.call_function("getPortfolioInfoEx", firm_id, client_code, limit_kind)
        if result and result.get('data'):
            return PortfolioInfoEx.from_dict(result['data'])
        return None


    async def get_buy_sell_info(self, firm_id: str, client_code: str, class_code: str, sec_code: str, price: float) -> Optional[BuySellInfo]:
        """
        Функция для получения информации по покупательной способности

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента
            class_code: Код класса инструмента
            sec_code: Код инструмента
            price: Цена

        Returns:
            Информация по покупательной способности
        """
        result = await self.call_function("getBuySellInfo", firm_id, client_code, class_code, sec_code, price)
        if result and result.get('data'):
            return BuySellInfo.from_dict(result['data'])
        return None


    async def get_buy_sell_info_ex(self, firm_id: str, client_code: str, class_code: str, sec_code: str, price: float) -> Optional[BuySellInfo]:
        """
        Функция для получения информации по покупательной способности (расширенная версия)

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента
            class_code: Код класса инструмента
            sec_code: Код инструмента
            price: Цена

        Returns:
            Информация по покупательной способности
        """
        result = await self.call_function("getBuySellInfoEx", firm_id, client_code, class_code, sec_code, price)
        if result and result.get('data'):
            return BuySellInfo.from_dict(result['data'])
        return None


    async def get_trd_acc_by_client_code(self, firm_id: str, client_code: str) -> Optional[str]:
        """
        Функция возвращает торговый счет срочного рынка, соответствующий коду клиента фондового рынка с единой денежной позицией

        Args:
            firm_id: Идентификатор фирмы
            client_code: Код клиента

        Returns:
            Торговый счет
        """
        result = await self.call_function("GetTrdAccByClientCode", firm_id, client_code)
        return result.get('data') if result else None


    async def get_client_code_by_trd_acc(self, firm_id: str, trd_acc_id: str) -> Optional[str]:
        """
        Функция возвращает код клиента фондового рынка с единой денежной позицией, соответствующий торговому счету срочного рынка

        Args:
            firm_id: Идентификатор фирмы
            trd_acc_id: Торговый счет

        Returns:
            Код клиента
        """
        result = await self.call_function("GetClientCodeByTrdAcc", firm_id, trd_acc_id)
        return result.get('data') if result else None


    async def is_ucp_client(self, firm_id: str, client: str) -> bool:
        """
        Функция для проверки, является ли клиент единым клиентом

        Args:
            firm_id: Идентификатор фирмы
            client: Код клиента

        Returns:
            True, если клиент является единым клиентом
        """
        result = await self.call_function("isUcpClient", firm_id, client)
        return result.get('data', False) if result else False


    async def get_all_trades(self) -> List[AllTrade]:
        """
        Функция для получения таблицы всех сделок

        Returns:
            Список всех сделок
        """
        result = await self.call_function("get_all_trades")
        if result and isinstance(result.get('data'), list):
            return [AllTrade.from_dict(item) for item in result['data']]
        return []


    async def get_all_trades_by_security(self, class_code: str, sec_code: str) -> List[AllTrade]:
        """
        Функция для получения всех сделок по инструменту

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента

        Returns:
            Список сделок по инструменту
        """
        result = await self.call_function("get_all_trades", class_code, sec_code)
        if result and isinstance(result.get('data'), list):
            return [AllTrade.from_dict(item) for item in result['data']]
        return []


    async def send_transaction(self, transaction: Transaction) -> int:
        """
        Функция для отправки транзакции с автоматическим присвоением TRANS_ID

        Args:
            transaction: Данные транзакции

        Returns:
            TRANS_ID транзакции (положительный при успехе, отрицательный при ошибке)
        """
        import time
        trans_id = int(time.time() * 1000) % 100000000  # time in milliseconds

        if transaction.TRANS_ID is None:
            transaction.TRANS_ID = trans_id
        else:
            trans_id = transaction.TRANS_ID

        # Устанавливаем CLIENT_CODE если не задан
        if transaction.CLIENT_CODE is None:
            transaction.CLIENT_CODE = str(trans_id)

        try:
            trans_data = transaction.to_dict()
            result = await self.call_function("sendTransaction", trans_data)

            if result and result.get('data'):
                # Сохранить транзакцию в хранилище
                self.service.storage.save(transaction.CLIENT_CODE, transaction)
                return trans_id
            else:
                # Транзакция не была отправлена
                return -trans_id

        except Exception as e:
            # В случае ошибки возвращаем отрицательный ID
            self.logger.error(f"Error sending transaction: {e}")
            transaction.error_message = str(e)
            return -trans_id


    async def calc_buy_sell(self, class_code: str, sec_code: str, client_code: str,
                            trd_acc_id: str, price: float, is_buy: bool, is_market: bool) -> Optional[CalcBuySellResult]:
        """
        Функция для расчета максимально возможного количества лотов в заявке

        Args:
            class_code: Код класса инструмента
            sec_code: Код инструмента
            client_code: Код клиента
            trd_acc_id: Торговый счет
            price: Цена
            is_buy: True для покупки, False для продажи
            is_market: True для рыночной заявки

        Returns:
            Результат расчета или None при ошибке
        """
        # Форматируем цену с точкой в качестве десятичного разделителя
        quik_price = str(price).replace(',', '.')

        # Формируем параметры в формате, ожидаемом QUIK
        result = await self.call_function("calc_buy_sell", class_code, sec_code, client_code, trd_acc_id, quik_price, is_buy, is_market)
        if result:
            return CalcBuySellResult.from_dict(result['data'])
        return None
