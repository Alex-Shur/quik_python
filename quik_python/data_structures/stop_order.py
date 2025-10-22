"""
Stop Order data structure for QUIK
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from .base import BaseDataStructure
from .order import Operation, State
from .transaction_types import OffsetUnits


class StopOrderType(Enum):
    """
    Тип стоп-заявки
    """
    NOT_IMPLEMENTED = 0

    # «1» – стоп-лимит
    STOP_LIMIT = 1

    # «2» – условие по другому инструменту,
    # «3» – со связанной заявкой,

    # «6» – тейк-профит
    TAKE_PROFIT = 6

    # «7» – стоп-лимит по исполнению активной заявки,
    # «8» –  тейк-профит по исполнению активной заявки,

    # «9» - тэйк-профит и стоп-лимит
    TAKE_PROFIT_STOP_LIMIT = 9


class StopOrderKind(Enum):
    """
    Вид стоп-заявки для транзакций
    Если параметр пропущен, то считается, что заявка имеет тип «стоп-лимит»
    """
    # стоп-лимит,
    # Если параметр пропущен, то считается, что заявка имеет тип «стоп-лимит»
    SIMPLE_STOP_ORDER = 0

    # с условием по другой бумаге,
    CONDITION_PRICE_BY_OTHER_SEC = 1

    # со связанной заявкой,
    WITH_LINKED_LIMIT_ORDER = 2

    # тэйк-профит,
    TAKE_PROFIT_STOP_ORDER = 3

    # тэйк-профит и стоп-лимит,
    TAKE_PROFIT_AND_STOP_LIMIT_ORDER = 4

    # стоп-лимит по исполнению заявки,
    ACTIVATED_BY_ORDER_SIMPLE_STOP_ORDER = 5

    # тэйк-профит по исполнению заявки,
    ACTIVATED_BY_ORDER_TAKE_PROFIT_STOP_ORDER = 6

    # тэйк-профит и стоп-лимит по исполнению заявки.
    ACTIVATED_BY_ORDER_TAKE_PROFIT_AND_STOP_LIMIT_ORDER = 7


class Condition(Enum):
    """
    Направленность стоп-цены
    """

    # меньше или равно
    LESS_OR_EQUAL = 4

    # больше или равно
    MORE_OR_EQUAL = 5


@dataclass
class StopOrder(BaseDataStructure):
    """
    Описание параметров стоп-заявки
    На основе http://help.qlua.org/ch4_6_6.htm
    """

    # Timestamp для Lua
    lua_timestamp: Optional[int] = None

    # Регистрационный номер стоп-заявки на сервере QUIK
    order_num: Optional[int] = None

    # Поручение/комментарий, обычно: код клиента/номер поручения
    broker_ref: Optional[str] = None

    # Идентификатор транзакции
    trans_id: Optional[int] = None

    # Торговый счет
    account: Optional[str] = None

    # Код клиента
    client_code: Optional[str] = None

    # Код бумаги заявки
    sec_code: Optional[str] = None

    # Код класса заявки
    class_code: Optional[str] = None

    # Отступ от min/max
    offset: Optional[Decimal] = None

    # Единицы измерения отступа
    offset_unit: Optional[OffsetUnits] = None

    # Защитный спред
    spread: Optional[Decimal] = None

    # Единицы измерения защитного спреда
    spread_unit: Optional[OffsetUnits] = None

    # Вид стоп заявки (целое число)
    stop_order_type: Optional[StopOrderType] = None

    # Направленность стоп-цены (целое число)
    condition: Optional[Condition] = None

    # Стоп-цена
    condition_price: Optional[Decimal] = None

    # Цена
    price: Optional[Decimal] = None

    # Количество в лотах
    qty: Optional[int] = None

    # Исполненное количество
    filled_qty: Optional[int] = None

    # Стоп-лимит цена (для заявок типа «Тэйк-профит и стоп-лимит»)
    condition_price2: Optional[Decimal] = None

    # Номер заявки в торговой системе, зарегистрированной по наступлению условия стоп-цены
    linked_order: Optional[int] = None

    _flags: int = 0

    @property
    def flags(self) -> Optional[int]:
        """Получить флаги"""
        return getattr(self, '_flags', 0)

    @flags.setter
    def flags(self, value: Optional[int]):
        """Установить флаги и обновить кэшированные поля"""
        self._flags = value

    # # Методы для работы с типами стоп-заявок
    # @property
    # def stop_order_type(self) -> Optional[StopOrderType]:
    #     """Получить тип стоп-заявки как enum"""
    #     if self.stop_order_type is None:
    #         return StopOrderType.NOT_IMPLEMENTED

    #     return self._stop_order_type

    # @property.setter
    # def stop_order_type(self, value: StopOrderType):
    #     """Установить тип стоп-заявки через enum"""
    #     self._stop_order_type = value

    # @property
    # def condition(self) -> Optional[Condition]:
    #     """Получить направленность стоп-цены как enum"""
    #     if self.condition is None:
    #         return None

    #     condition_mapping = {
    #         4: Condition.LESS_OR_EQUAL,
    #         5: Condition.MORE_OR_EQUAL
    #     }
    #     return condition_mapping.get(self.condition)

    @property
    def operation(self) -> Optional[Operation]:
        """Получить операцию (покупка/продажа) из флагов"""
        if self.flags is None:
            return None
        return Operation.SELL if (self.flags & 0x4) != 0 else Operation.BUY

    @operation.setter
    def operation(self, operation: Operation):
        """
        Установить операцию (покупка/продажа) через изменение флагов

        Args:
            operation: Operation.BUY или Operation.SELL
        """
        if self.flags is None:
            self.flags = 0

        # Сбрасываем бит операции и устанавливаем новый
        if operation == Operation.SELL:
            self.flags = self.flags | 0x4  # Устанавливаем бит SELL
        else:  # Operation.BUY
            self.flags = self.flags & ~0x4  # Сбрасываем бит SELL

    @property
    def state(self) -> Optional[State]:
        """Получить состояние стоп-заявки из флагов"""
        if self.flags is None:
            return None

        if (self.flags & 0x1) != 0:
            return State.ACTIVE
        elif (self.flags & 0x2) != 0:
            return State.CANCELED
        else:
            return State.COMPLETED

    @state.setter
    def state(self, state: State):
        """
        Установить состояние стоп-заявки через изменение флагов

        Args:
            state: State.ACTIVE, State.CANCELED или State.COMPLETED
        """
        if self.flags is None:
            self.flags = 0

        # Сбрасываем биты состояния (0x1 и 0x2)
        self.flags = self.flags & ~0x3

        # Устанавливаем новое состояние
        if state == State.ACTIVE:
            self.flags = self.flags | 0x1
        elif state == State.CANCELED:
            self.flags = self.flags | 0x2
        # State.COMPLETED не требует установки битов (остается 0x0)

    @property
    def is_waiting_activation(self) -> bool:
        """Проверить, ожидает ли стоп-заявка активации"""
        if self.flags is None:
            return False
        return (self.flags & 0x20) != 0

    @is_waiting_activation.setter
    def is_waiting_activation(self, waiting: bool):
        """
        Установить флаг ожидания активации через изменение флагов

        Args:
            waiting: True для установки флага, False для сброса
        """
        if self.flags is None:
            self.flags = 0

        if waiting:
            self.flags = self.flags | 0x20  # Устанавливаем бит
        else:
            self.flags = self.flags & ~0x20  # Сбрасываем бит

    @staticmethod
    def get_numeric_value(value: Optional[str]) -> Optional[float]:
        """Вспомогательный метод для преобразования строки в число"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    # Алиасы для совместимости с C# API
    # @property
    # def comment(self) -> Optional[str]:
    #     """Алиас для brokerref для совместимости"""
    #     return self.brokerref

    # @comment.setter
    # def comment(self, value: Optional[str]):
    #     """Сеттер для comment"""
    #     self.brokerref = value

    # @property
    # def quantity(self) -> Optional[int]:
    #     """Алиас для qty для совместимости"""
    #     return self.qty

    # @quantity.setter
    # def quantity(self, value: Optional[int]):
    #     """Сеттер для quantity"""
    #     self.qty = value

    # @property
    # def filled_quantity(self) -> Optional[int]:
    #     """Алиас для filled_qty для совместимости"""
    #     return self.filled_qty

    # @filled_quantity.setter
    # def filled_quantity(self, value: Optional[int]):
    #     """Сеттер для filled_quantity"""
    #     self.filled_qty = value

    # @property
    # def linked_order(self) -> Optional[int]:
    #     """Алиас для linkedorder для совместимости"""
    #     return self.linkedorder

    # @linked_order.setter
    # def linked_order(self, value: Optional[int]):
    #     """Сеттер для linked_order"""
    #    self.linkedorder = value

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'StopOrder':
        """Создание объекта из словаря с маппингом полей"""
        instance = cls(
            lua_timestamp=data.get('lua_timestamp'),
            order_num=data.get('order_num'),
            broker_ref=data.get('brokerref'),
            trans_id=data.get('trans_id'),
            account=data.get('account'),
            client_code=data.get('client_code'),
            sec_code=data.get('sec_code'),
            class_code=data.get('class_code'),
            offset=Decimal(str(data.get('offset'))) if data.get('offset') is not None else None,
            offset_unit=OffsetUnits(data.get('offset_unit')) if data.get('offset_unit') else None,
            spread=Decimal(str(data.get('spread'))) if data.get('spread') is not None else None,
            spread_unit=OffsetUnits(data.get('spread_unit')) if data.get('spread_unit') else None,
            stop_order_type=StopOrderType(data.get('stop_order_type')) if data.get('stop_order_type') else None,
            condition=Condition(data.get('condition')) if data.get('condition') else None,
            condition_price=Decimal(str(data.get('condition_price'))) if data.get('condition_price') is not None else None,
            price=Decimal(str(data.get('price'))) if data.get('price') is not None else None,
            qty=data.get('qty'),
            filled_qty=data.get('filled_qty'),
            condition_price2=Decimal(str(data.get('condition_price2'))) if data.get('condition_price2') is not None else None,
            linked_order=data.get('linkedorder')
        )
        # Устанавливаем flags после создания объекта
        instance.flags = data.get('flags')
        return instance

    def to_dict(self) -> dict:
        """Преобразование в словарь с именами полей C#"""
        return {
            'lua_timestamp': self.lua_timestamp,
            'order_num': self.order_num,
            'brokerref': self.broker_ref,
            'flags': self.flags,
            'trans_id': self.trans_id,
            'account': self.account,
            'client_code': self.client_code,
            'sec_code': self.sec_code,
            'class_code': self.class_code,
            'offset': Decimal(self.offset) if self.offset is not None else None,
            'offset_unit': self.offset_unit.value if self.offset_unit else None,
            'spread': Decimal(self.spread) if self.spread is not None else None,
            'spread_unit': self.spread_unit.value if self.spread_unit else None,
            'stop_order_type': self.stop_order_type.value,
            'condition': self.condition.value if self.condition else None,
            'condition_price': Decimal(self.condition_price) if self.condition_price is not None else None,
            'price': Decimal(self.price) if self.price is not None else None,
            'qty': self.qty,
            'filled_qty': self.filled_qty,
            'condition_price2': Decimal(self.condition_price2) if self.condition_price2 is not None else None,
            'linkedorder': self.linked_order
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False)
