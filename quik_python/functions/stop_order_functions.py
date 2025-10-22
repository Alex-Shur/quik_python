"""
Stop order functions for QUIK interaction
"""


from typing import List, Optional, Callable, TYPE_CHECKING
from decimal import Decimal
from .base_functions import BaseFunctions
from ..data_structures import Transaction, TransactionAction, TransactionOperation, Operation, \
                        StopOrder, StopOrderKind, StopOrderType

if TYPE_CHECKING:
    from ..quik import Quik


class StopOrderFunctions(BaseFunctions):
    """
    Функции для работы со стоп-заявками
    """

    def __init__(self, port: int, quik_instance: 'Quik', host: str = "127.0.0.1"):
        super().__init__(port, host)
        self._quik = quik_instance
        self._new_stop_order_handlers: List[Callable[[StopOrder], None]] = []

    def add_stop_order_handler(self, handler: Callable[[StopOrder], None]):
        """
        Добавить обработчик новых стоп-заявок

        Args:
            handler: Функция-обработчик
        """
        self._new_stop_order_handlers.append(handler)

    def remove_stop_order_handler(self, handler: Callable[[StopOrder], None]):
        """
        Удалить обработчик новых стоп-заявок

        Args:
            handler: Функция-обработчик для удаления
        """
        if handler in self._new_stop_order_handlers:
            self._new_stop_order_handlers.remove(handler)

    def _raise_new_stop_order_event(self, stop_order: StopOrder):
        """
        Вызвать событие новой стоп-заявки

        Args:
            stop_order: Стоп-заявка
        """
        for handler in self._new_stop_order_handlers:
            try:
                handler(stop_order)
            except Exception:
                # Подавляем ошибки в пользовательских обработчиках
                pass

    async def get_stop_orders(self, class_code: Optional[str] = None, security_code: Optional[str] = None) -> List[StopOrder]:
        """
        Возвращает список всех стоп-заявок или стоп-заявок для заданного инструмента

        Args:
            class_code: Код класса (опционально)
            security_code: Код инструмента (опционально)

        Returns:
            Список стоп-заявок
        """
        if class_code and security_code:
            # Получить стоп-заявки для конкретного инструмента
            result = await self.call_function("get_stop_orders", class_code, security_code)
        else:
            # Получить все стоп-заявки
            result = await self.call_function("get_stop_orders")

        if result and isinstance(result.get('data'), list):
            return [StopOrder.from_dict(order_data) for order_data in result['data']]
        return []

    async def create_stop_order(self, stop_order: StopOrder) -> int:
        """
        Создать стоп-заявку

        Args:
            stop_order: Параметры стоп-заявки

        Returns:
            Номер транзакции
        """
        # Создаем базовую транзакцию для новой стоп-заявки
        transaction = Transaction()
        transaction.ACTION = TransactionAction.NEW_STOP_ORDER
        transaction.ACCOUNT=stop_order.account
        transaction.CLASSCODE=stop_order.class_code
        transaction.SECCODE=stop_order.sec_code
        transaction.EXPIRY_DATE= "GTC" # до отмены
        transaction.STOPPRICE=stop_order.condition_price
        transaction.PRICE=stop_order.price
        transaction.QUANTITY=stop_order.qty
        transaction.STOP_ORDER_KIND= self.convert_stop_order_type(stop_order.stop_order_type)
        transaction.OPERATION=TransactionOperation.B if stop_order.operation == Operation.BUY else TransactionOperation.S

        if stop_order.stop_order_type in (StopOrderType.TAKE_PROFIT, StopOrderType.TAKE_PROFIT_STOP_LIMIT):
            transaction.OFFSET = stop_order.offset
            transaction.SPREAD = stop_order.spread
            transaction.OFFSET_UNITS = stop_order.offset_unit
            transaction.SPREAD_UNITS = stop_order.spread_unit

        if stop_order.stop_order_type == StopOrderType.TAKE_PROFIT_STOP_LIMIT:
            transaction.STOPPRICE2 = stop_order.condition_price2

        # //todo: Not implemented
        # //["OFFSET"]=tostring(SysFunc.toPrice(SecCode,MaxOffset)),
        # //["OFFSET_UNITS"]="PRICE_UNITS",
        # //["SPREAD"]=tostring(SysFunc.toPrice(SecCode,DefSpread)),
        # //["SPREAD_UNITS"]="PRICE_UNITS",
        # //["MARKET_STOP_LIMIT"]="YES",
        # //["MARKET_TAKE_PROFIT"]="YES",
        # //["STOPPRICE2"]=tostring(SysFunc.toPrice(SecCode,StopLoss)),
        # //["EXECUTION_CONDITION"] = "FILL_OR_KILL",

        return await self._quik.trading.send_transaction(transaction)

    def convert_stop_order_type(self, stop_order_type: StopOrderType) -> StopOrderKind:
        match stop_order_type:
            case StopOrderType.STOP_LIMIT:
                return StopOrderKind.SIMPLE_STOP_ORDER
            case StopOrderType.TAKE_PROFIT:
                return StopOrderKind.TAKE_PROFIT_STOP_ORDER
            case StopOrderType.TAKE_PROFIT_STOP_LIMIT:
                return StopOrderKind.TAKE_PROFIT_AND_STOP_LIMIT_ORDER
            case _:
                raise Exception("Not implemented stop order type: " + str(stop_order_type))


    async def kill_stop_order(self, stop_order: StopOrder) -> int:
        """
        Снять стоп-заявку

        Args:
            stop_order: Стоп-заявка для снятия

        Returns:
            Номер транзакции
        """
        transaction = Transaction(
            ACTION=TransactionAction.KILL_STOP_ORDER,
            CLASSCODE=stop_order.class_code,
            SECCODE=stop_order.sec_code,
            STOP_ORDER_KEY=str(stop_order.order_num)
        )

        return await self._quik.trading.send_transaction(transaction)
