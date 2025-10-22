"""
Order functions for QUIK interaction
"""

from typing import List, Optional, TYPE_CHECKING
import asyncio
from decimal import Decimal
from .base_functions import BaseFunctions
from ..data_structures import Order, TransactionReply, Operation, Transaction, TransactionAction, \
                        TransactionOperation, ExecutionCondition, TransactionType


if TYPE_CHECKING:
    from ..quik import Quik


class OrderFunctions(BaseFunctions):
    """
    Функции для работы с заявками
    """

    def __init__(self, port: int, quik_instance: 'Quik', host: str = "127.0.0.1"):
        """
        Initialize OrderFunctions

        Args:
            port: Port number for communication
            quik_instance: Reference to main Quik instance
            host: Host address
        """
        super().__init__(port, host)
        self._quik = quik_instance


    async def create_order(self, order: Order) -> int:
        """
        Создание новой заявки

        Args:
            order: Информация о новой заявке, на основе которой будет сформирована транзакция

        Returns:
            TRANS_ID транзакции (положительный при успехе, отрицательный при ошибке)
        """
        # Создаем новую транзакцию на основе заявки
        new_order_transaction = Transaction()
        new_order_transaction.ACTION = TransactionAction.NEW_ORDER
        new_order_transaction.ACCOUNT = order.account
        new_order_transaction.CLASSCODE = order.class_code
        new_order_transaction.SECCODE = order.sec_code
        new_order_transaction.QUANTITY = order.qty  # quantity в Order называется qty

        if order.operation == Operation.BUY or (isinstance(order.operation, str) and order.operation in ["Buy", "B"]):
            new_order_transaction.OPERATION = TransactionOperation.B
        else:
            new_order_transaction.OPERATION = TransactionOperation.S

        new_order_transaction.PRICE = Decimal(order.price) if order.price else Decimal("0")
        new_order_transaction.CLIENT_CODE = order.client_code

        if order.exec_type == 1:
            new_order_transaction.EXECUTION_CONDITION = ExecutionCondition.FILL_OR_KILL

        return await self._quik.trading.send_transaction(new_order_transaction)


    async def send_order(self, class_code: str, security_code: str, account_id: str,
                        operation: Operation, price: Decimal, qty: int, order_type: TransactionType,
                        execution_condition: ExecutionCondition = ExecutionCondition.PUT_IN_QUEUE,
                        client_code: Optional[str] = None) -> Order:
        """
        Создание заявки.

        Args:
            class_code: Код класса инструмента
            security_code: Код инструмента
            account_id: Счет клиента
            operation: Операция заявки (покупка/продажа)
            price: Цена заявки
            qty: Количество (в лотах)
            order_type: Тип заявки (L - лимитная, M - рыночная)
            execution_condition: Условие исполнения заявки (PUT_IN_QUEUE, FILL_OR_KILL, KILL_BALANCE)
            client_code: Код клиента

        Returns:
            Order: Созданная заявка с результатом операции
        """
        res = 0
        set_flag = False
        order_result = Order()

        # Переменная для хранения последнего ответа на транзакцию
        last_transaction_reply = TransactionReply()

        # Обработчик события ответа на транзакцию
        def on_trans_reply_handler(trans_reply: TransactionReply):
            nonlocal last_transaction_reply
            if trans_reply.trans_id == res:
                last_transaction_reply = trans_reply

        # Подписываемся на события ответов на транзакции
        self._quik.events.add_on_trans_reply(on_trans_reply_handler)

        try:
            # Создаем новую транзакцию заявки
            new_order_transaction = Transaction()
            new_order_transaction.ACTION = TransactionAction.NEW_ORDER
            new_order_transaction.ACCOUNT = account_id
            new_order_transaction.CLASSCODE = class_code
            new_order_transaction.SECCODE = security_code
            new_order_transaction.QUANTITY = qty
            new_order_transaction.OPERATION = TransactionOperation.B if operation == Operation.BUY else TransactionOperation.S
            new_order_transaction.PRICE = price
            new_order_transaction.TYPE = order_type
            new_order_transaction.EXECUTION_CONDITION = execution_condition
            new_order_transaction.CLIENT_CODE = client_code

            try:
                res = await self._quik.trading.send_transaction(new_order_transaction)
                await asyncio.sleep(0.5)  # Ждем 500ms как в оригинальном коде
                ##?? print(f"res: {res}")
            except Exception:
                # ignore - как в оригинальном коде
                pass

            # Ожидаем результата
            while not set_flag:
                if res > 0:
                    if (last_transaction_reply is None or
                        last_transaction_reply.result_msg is None or
                        last_transaction_reply.result_msg == "" or
                        last_transaction_reply.error_code == 0):
                        try:
                            order_result = await self.get_order_by_trans_id(class_code, security_code, res)
                        except Exception:
                            order_result = Order()
                            order_result.reject_reason = f"Неудачная попытка получения заявки по ID-транзакции №{res}"
                    else:
                        if order_result is not None:
                            order_result.reject_reason = last_transaction_reply.result_msg
                        else:
                            order_result = Order()
                            order_result.reject_reason = last_transaction_reply.result_msg
                else:
                    if order_result is not None:
                        order_result.reject_reason = new_order_transaction.error_message
                    else:
                        order_result = Order()
                        order_result.reject_reason = new_order_transaction.error_message

                if (order_result is not None and
                    (order_result.reject_reason != "" or order_result.order_num > 0)):
                    set_flag = True

        finally:
            self._quik.events.remove_on_trans_reply(on_trans_reply_handler)
            pass

        return order_result


    async def send_limit_order(self, class_code: str, security_code: str, account_id: str,
                            operation: Operation, price: Decimal, qty: int,
                            execution_condition: ExecutionCondition = ExecutionCondition.PUT_IN_QUEUE,
                            client_code: Optional[str] = None) -> Order:
        """
        Создание лимитированной заявки.

        Args:
            class_code: Код класса инструмента
            security_code: Код инструмента
            account_id: Счет клиента
            operation: Операция заявки (покупка/продажа)
            price: Цена заявки
            qty: Количество (в лотах)
            execution_condition: Условие исполнения заявки (PUT_IN_QUEUE, FILL_OR_KILL, KILL_BALANCE)
            client_code: Код клиента

        Returns:
            Order: Созданная лимитная заявка
        """
        return await self.send_order(
            class_code=class_code,
            security_code=security_code,
            account_id=account_id,
            operation=operation,
            price=price,
            qty=qty,
            order_type=TransactionType.L,  # L = лимитированная заявка
            execution_condition=execution_condition,
            client_code=client_code
        )


    async def send_market_order(self, class_code: str, security_code: str, account_id: str,
                            operation: Operation, qty: int,
                            execution_condition: ExecutionCondition = ExecutionCondition.PUT_IN_QUEUE,
                            client_code: Optional[str] = None) -> Order:
        """
        Создание рыночной заявки.

        Args:
            class_code: Код класса инструмента
            security_code: Код инструмента
            account_id: Счет клиента
            operation: Операция заявки (покупка/продажа)
            qty: Количество (в лотах)
            execution_condition: Условие исполнения заявки (PUT_IN_QUEUE, FILL_OR_KILL, KILL_BALANCE)
            client_code: Код клиента

        Returns:
            Order: Созданная рыночная заявка
        """
        return await self.send_order(
            class_code=class_code,
            security_code=security_code,
            account_id=account_id,
            operation=operation,
            price=0,  # Для рыночной заявки цена = 0
            qty=qty,
            order_type=TransactionType.M,  # M = рыночная заявка
            execution_condition=execution_condition,
            client_code=client_code
        )


    async def kill_order(self, order: Order) -> int:
        """
        Отмена заявки.

        Args:
            order: Информация по заявке, которую требуется отменить

        Returns:
            TRANS_ID транзакции (положительный при успехе, отрицательный при ошибке)
        """
        kill_order_transaction = Transaction()
        kill_order_transaction.ACTION = TransactionAction.KILL_ORDER
        kill_order_transaction.CLASSCODE = order.class_code
        kill_order_transaction.SECCODE = order.sec_code
        kill_order_transaction.ORDER_KEY = str(order.order_num)

        return await self._quik.trading.send_transaction(kill_order_transaction)


    async def get_order(self, class_code: str, order_id: int) -> Optional[Order]:
        """
        Возвращает заявку из хранилища терминала по её номеру.
        На основе: http://help.qlua.org/ch4_5_1_1.htm

        Args:
            class_code: Код класса
            order_id: Номер заявки

        Returns:
            Заявка
        """
        result = await self.call_function("get_order_by_number", class_code, order_id)
        if result and 'data' in result:
            return Order.from_dict(result['data'])
        return None  # Возвращаем пустую заявку при ошибке, как в C# коде


    async def get_orders(self, class_code: Optional[str] = None, security_code: Optional[str] = None) -> List[Order]:
        """
        Получить список всех заявок

        Args:
            class_code: Код класса инструмента
            security_code: Код инструмента

        Returns:
            Список заявок
        """
        if class_code and security_code:
            result = await self.call_function("get_orders", class_code, security_code)
        else:
            result = await self.call_function("get_orders")

        if result and isinstance(result['data'], list):
            return [Order.from_dict(order_data) for order_data in result['data']]
        return []


    async def get_order_by_trans_id(self, class_code: str, security_code: str, trans_id: int) -> Optional[Order]:
        """
        Возвращает заявку для заданного инструмента по ID транзакции.

        Args:
            class_code: Код класса инструмента
            security_code: Код инструмента
            trans_id: ID транзакции

        Returns:
            Order: Заявка, соответствующая транзакции
        """
        result = await self.call_function("getOrder_by_ID", class_code, security_code, trans_id)
        if result and 'data' in result:
            return Order.from_dict(result['data'])
        return None


    async def get_order_by_number(self, order_num: int) -> Optional[Order]:
        """
        Возвращает заявку по номеру.

        Args:
            order_num: Номер заявки

        Returns:
            Order: Заявка по указанному номеру
        """
        result = await self.call_function("getOrder_by_Number", order_num)
        if result and 'data' in result:
            return Order.from_dict(result['data'])
        return None

