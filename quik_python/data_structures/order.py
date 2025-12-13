"""
Order data structure for QUIK
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from .base import BaseDataStructure
from .quik_datetime import QuikDateTime


class Operation(Enum):
    """
    Тип операции - Buy или Sell
    """

    BUY = 0

    SELL = 1


class State(Enum):
    """
    Состояние заявки
    """
    
    #"Active"
    ACTIVE = 0
 
    #"Canceled" 
    CANCELED = 1
   
    #"Completed"
    COMPLETED = 2


class OrderTradeFlags(Enum):
    """
    Набор битовых флагов для заявки
    http://help.qlua.org/ch9_1.htm
    """

    ACTIVE = 0x1

    CANCELED = 0x2

    IS_SELL = 0x4

    IS_LIMIT = 0x8

    ALLOW_DIFF_PRICE = 0x10

    FILL_OR_KILL = 0x20

    IS_MARKET_MAKER_OR_SENT = 0x40

    IS_RECEIVED = 0x80

    IS_KILL_BALANCE = 0x100

    ICEBERG = 0x200



@dataclass
class Order(BaseDataStructure):
    """
    Описание параметров Таблицы заявок
    """
    
    # Timestamp для Lua
    lua_timestamp: Optional[int] = None
    
    # Номер заявки в торговой системе
    order_num: Optional[int] = None
    
    # Поручение/комментарий, обычно: код клиента/номер поручения
    brokerref: Optional[str] = None
    
    # Идентификатор трейдера
    userid: Optional[str] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Торговый счет
    account: Optional[str] = None
    
    # Цена
    price: Optional[Decimal] = None
    
    # Количество в лотах
    qty: Optional[int] = None
    
    # Остаток
    balance: Optional[int] = None
    
    # Объем в денежных средствах
    value: Optional[Decimal] = None
    
    # Накопленный купонный доход
    accruedint: Optional[Decimal] = None
    
    # Доходность
    yield_: Optional[Decimal] = None  # yield is reserved keyword, using yield_
    
    # Идентификатор транзакции
    trans_id: Optional[int] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Цена выкупа
    price2: Optional[Decimal] = None
    
    # Код расчетов
    settlecode: Optional[str] = None
    
    # Идентификатор пользователя
    uid: Optional[int] = None
    
    # Идентификатор пользователя, снявшего заявку
    canceled_uid: Optional[int] = None
    
    # Код биржи в торговой системе
    exchange_code: Optional[str] = None
    
    # Время активации
    activation_time: Optional[int] = None
    
    # Номер заявки в торговой системе
    linked_order: Optional[int] = None
    
    # Дата окончания срока действия заявки
    expiry: Optional[Decimal] = None
    
    # Код бумаги заявки
    sec_code: Optional[str] = None
    
    # Код класса заявки
    class_code: Optional[str] = None
    
    # Дата и время
    datetime: Optional[QuikDateTime] = None
    
    # Дата и время снятия заявки
    withdraw_datetime: Optional[QuikDateTime] = None
    
    # Идентификатор расчетного счета/кода в клиринговой организации
    bank_acc_id: Optional[str] = None
    
    # Способ указания объема заявки. Возможные значения: «0» – по количеству, «1» – по объему
    value_entry_type: Optional[int] = None
    
    # Срок РЕПО, в календарных днях
    repoterm: Optional[Decimal] = None
    
    # Сумма РЕПО на текущую дату. Отображается с точностью 2 знака
    repovalue: Optional[Decimal] = None
    
    # Объём сделки выкупа РЕПО. Отображается с точностью 2 знака
    repo2value: Optional[Decimal] = None
    
    # Остаток суммы РЕПО за вычетом суммы привлеченных или предоставленных по сделке РЕПО денежных средств в неисполненной части заявки
    repo_value_balance: Optional[Decimal] = None
    
    # Начальный дисконт, в %
    start_discount: Optional[Decimal] = None
    
    # Причина отклонения заявки брокером
    reject_reason: Optional[str] = None
    
    # Битовое поле для получения специфических параметров с западных площадок
    ext_order_flags: Optional[int] = None
    
    # Минимально допустимое количество, которое можно указать в заявке по данному инструменту
    min_qty: Optional[int] = None
    
    # Тип исполнения заявки
    # Тип исполнения заявки. Возможные значения:
    # «0» – Значение не указано; 
    # «1» – Немедленно или отклонить; 
    # «2» – Поставить в очередь; 
    # «3» – Снять остаток; 
    # «4» – До снятия; 
    # «5» – До даты; 
    # «6» – В течение сессии; 
    # «7» – Открытие; 
    # «8» – Закрытие; 
    # «9» – Кросс; 
    # «11» – До следующей сессии; 
    # «13» – До отключения; 
    # «15» – До времени; 
    # «16» – Следующий аукцион; 
    exec_type: Optional[int] = None
    
    # Поле для получения параметров по западным площадкам
    side_qualifier: Optional[int] = None
    
    # Поле для получения параметров по западным площадкам
    acnt_type: Optional[int] = None
    
    # Роль в исполнении заявки
    # «0» – Не определено; 
    # «1» – Agent; 
    # «2» – Principal; 
    # «3» – Riskless principal; 
    # «4» – CFG give up; 
    # «5» – Cross as agent; 
    # «6» – Matched Principal; 
    # «7» – Proprietary; 
    # «8» – Individual; 
    # «9» – Agent for other member; 
    # «10» – Mixed; 
    # «11» – Market maker;
    capacity: Optional[int] = None
    
    # Поле для получения параметров по западным площадкам
    passive_only_order: Optional[int] = None
    
    # Видимое количество. Параметр айсберг-заявок
    visible: Optional[int] = None
    
    # Средняя цена приобретения. Актуально, когда заявка выполнилась частями
    awg_price: Optional[Decimal] = None
    
    # Время окончания срока действия заявки в формате "ЧЧММСС"
    expiry_time: Optional[int] = None
    
    # Номер ревизии заявки
    revision_number: Optional[int] = None
    
    # Валюта цены заявки
    price_currency: Optional[str] = None
    
    # Расширенный статус заявки
    # «0» (по умолчанию) – не определено; 
    # «1» – заявка активна; 
    # «2» – заявка частично исполнена; 
    # «3» – заявка исполнена; 
    # «4» – заявка отменена; 
    # «5» – заявка заменена; 
    # «6» – заявка в состоянии отмены; 
    # «7» – заявка отвергнута; 
    # «8» – приостановлено исполнение заявки; 
    # «9» – заявка в состоянии регистрации; 
    # «10» – заявка снята по времени действия; 
    # «11» – заявка в состоянии замены
    ext_order_status: Optional[int] = None
    
    # UID пользователя-менеджера, подтвердившего заявку
    accepted_uid: Optional[int] = None
    
    # Исполненный объем заявки в валюте цены
    filled_value: Optional[int] = None
    
    # Внешняя ссылка, используется для обратной связи с внешними системами
    extref: Optional[str] = None
    
    # Валюта расчетов по заявке
    settle_currency: Optional[str] = None
    
    # UID пользователя, от имени которого выставлена заявка
    on_behalf_of_uid: Optional[int] = None
    
    # Квалификатор клиента, от имени которого выставлена заявка
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «3» – Legal Entity
    client_qualifier: Optional[int] = None
    
    # Краткий идентификатор клиента
    client_short_code: Optional[int] = None
    
    # Квалификатор принявшего решение о выставлении заявки
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «2» – Algorithm
    investment_decision_maker_qualifier: Optional[int] = None
    
    # Краткий идентификатор принявшего решение о выставлении заявки
    investment_decision_maker_short_code: Optional[int] = None
    
    # Квалификатор трейдера, исполнившего заявку
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «2» – Algorithm
    executing_trader_qualifier: Optional[int] = None
    
    # Краткий идентификатор трейдера, исполнившего заявку
    executing_trader_short_code: Optional[int] = None
    
    # Набор битовых флагов
    _flags: int = 0

    @property
    def flags(self) -> Optional[int]:
        """Получить флаги"""
        return getattr(self, '_flags', 0)

    @flags.setter
    def flags(self, value: Optional[int]):
        """Установить флаги и обновить кэшированные поля"""
        self._flags = value

    @property
    def operation(self) -> Optional[Operation]:
        """Получить операцию (покупка/продажа) из флагов"""
        if self.flags is None:
            return None
        return Operation.SELL if (self.flags & OrderTradeFlags.IS_SELL.value) != 0 else Operation.BUY

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
            self.flags = self.flags | OrderTradeFlags.IS_SELL.value  # Устанавливаем бит SELL
        else:  # Operation.BUY
            self.flags = self.flags & ~OrderTradeFlags.IS_SELL.value  # Сбрасываем бит SELL


    @property
    def state(self) -> Optional[State]:
        """Получить состояние заявки из флагов"""
        if self.flags is None:
            return None

        if (self.flags & OrderTradeFlags.ACTIVE.value) != 0:
            return State.ACTIVE
        elif (self.flags & OrderTradeFlags.CANCELED.value) != 0:
            return State.CANCELED
        else:
            return State.COMPLETED

    @state.setter
    def state(self, value: State):
        """Установить состояние заявки через изменение флагов"""
        if self.flags is None:
            self.flags = 0

        # Сбрасываем биты состояния (0x1 и 0x2)
        self.flags = self.flags & ~(OrderTradeFlags.CANCELED.value|OrderTradeFlags.ACTIVE.value)

        # Устанавливаем новое состояние
        if value == State.ACTIVE:
            self.flags = self.flags | OrderTradeFlags.ACTIVE.value
        elif value == State.CANCELED:
            self.flags = self.flags | OrderTradeFlags.CANCELED.value
        # State.COMPLETED не требует установки битов (остается 0x0)

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Создание объекта из словаря с маппингом полей"""
        instance = cls(
            lua_timestamp=data.get('lua_timestamp'),
            order_num=data.get('order_num'),
            brokerref=data.get('brokerref'),
            userid=data.get('userid'),
            firm_id=data.get('firmid'),
            account=data.get('account'),
            price=Decimal(str(data.get('price'))) if data.get('price') is not None else None,
            qty=data.get('qty'),
            balance=data.get('balance'),
            value=Decimal(str(data.get('value'))) if data.get('value') is not None else None,
            accruedint=Decimal(str(data.get('accruedint'))) if data.get('accruedint') is not None else None,
            yield_=Decimal(str(data.get('yield'))) if data.get('yield') is not None else None,
            trans_id=data.get('trans_id'),
            client_code=data.get('client_code'),
            price2=Decimal(str(data.get('price2'))) if data.get('price2') is not None else None,
            settlecode=data.get('settlecode'),
            uid=data.get('uid'),
            canceled_uid=data.get('canceled_uid'),
            exchange_code=data.get('exchange_code'),
            activation_time=data.get('activation_time'),
            linked_order=data.get('linkedorder'),
            expiry=Decimal(str(data.get('expiry'))) if data.get('expiry') is not None else None,
            sec_code=data.get('sec_code'),
            class_code=data.get('class_code'),
            datetime=QuikDateTime.from_dict(data.get('datetime')) if data.get('datetime') else None,
            withdraw_datetime=QuikDateTime.from_dict(data.get('withdraw_datetime')) if data.get('withdraw_datetime') else None,
            bank_acc_id=data.get('bank_acc_id'),
            value_entry_type=data.get('value_entry_type'),
            repoterm=Decimal(str(data.get('repoterm'))) if data.get('repoterm') is not None else None,
            repovalue=Decimal(str(data.get('repovalue'))) if data.get('repovalue') is not None else None,
            repo2value=Decimal(str(data.get('repo2value'))) if data.get('repo2value') is not None else None,
            repo_value_balance=Decimal(str(data.get('repo_value_balance'))) if data.get('repo_value_balance') is not None else None,
            start_discount=Decimal(str(data.get('start_discount'))) if data.get('start_discount') is not None else None,
            reject_reason=data.get('reject_reason'),
            ext_order_flags=data.get('ext_order_flags'),
            min_qty=data.get('min_qty'),
            exec_type=data.get('exec_type'),
            side_qualifier=data.get('side_qualifier'),
            acnt_type=data.get('acnt_type'),
            capacity=data.get('capacity'),
            passive_only_order=data.get('passive_only_order'),
            visible=data.get('visible'),
            awg_price=Decimal(str(data.get('awg_price'))) if data.get('awg_price') is not None else None,
            expiry_time=data.get('expiry_time'),
            revision_number=data.get('revision_number'),
            price_currency=data.get('price_currency'),
            ext_order_status=data.get('ext_order_status'),
            accepted_uid=data.get('accepted_uid'),
            filled_value=data.get('filled_value'),
            extref=data.get('extref'),
            settle_currency=data.get('settle_currency'),
            on_behalf_of_uid=data.get('on_behalf_of_uid'),
            client_qualifier=data.get('client_qualifier'),
            client_short_code=data.get('client_short_code'),
            investment_decision_maker_qualifier=data.get('investment_decision_maker_qualifier'),
            investment_decision_maker_short_code=data.get('investment_decision_maker_short_code'),
            executing_trader_qualifier=data.get('executing_trader_qualifier'),
            executing_trader_short_code=data.get('executing_trader_short_code'),
        )
        # Устанавливаем flags после создания объекта
        instance.flags = data.get('flags')
        return instance

    def to_dict(self) -> dict:
        """Преобразование в словарь с именами полей C#"""
        return {
            'lua_timestamp': self.lua_timestamp,
            'order_num': self.order_num,
            'brokerref': self.brokerref,
            'userid': self.userid,
            'firmid': self.firm_id,
            'account': self.account,
            'price': Decimal(self.price) if self.price is not None else None,
            'qty': self.qty,
            'balance': self.balance,
            'value': Decimal(self.value) if self.value is not None else None,
            'accruedint': Decimal(self.accruedint) if self.accruedint is not None else None,
            'yield': Decimal(self.yield_) if self.yield_ is not None else None,
            'trans_id': self.trans_id,
            'client_code': self.client_code,
            'price2': Decimal(self.price2) if self.price2 is not None else None,
            'settlecode': self.settlecode,
            'uid': self.uid,
            'canceled_uid': self.canceled_uid,
            'exchange_code': self.exchange_code,
            'activation_time': self.activation_time,
            'linkedorder': self.linked_order,
            'expiry': float(self.expiry) if self.expiry is not None else None,
            'sec_code': self.sec_code,
            'class_code': self.class_code,
            'datetime': self.datetime.to_dict() if self.datetime else None,
            'withdraw_datetime': self.withdraw_datetime.to_dict() if self.withdraw_datetime else None,
            'bank_acc_id': self.bank_acc_id,
            'value_entry_type': self.value_entry_type,
            'repoterm': float(self.repoterm) if self.repoterm is not None else None,
            'repovalue': float(self.repovalue) if self.repovalue is not None else None,
            'repo2value': float(self.repo2value) if self.repo2value is not None else None,
            'repo_value_balance': float(self.repo_value_balance) if self.repo_value_balance is not None else None,
            'start_discount': float(self.start_discount) if self.start_discount is not None else None,
            'reject_reason': self.reject_reason,
            'ext_order_flags': self.ext_order_flags,
            'min_qty': self.min_qty,
            'exec_type': self.exec_type,
            'side_qualifier': self.side_qualifier,
            'acnt_type': self.acnt_type,
            'capacity': self.capacity,
            'passive_only_order': self.passive_only_order,
            'visible': self.visible,
            'awg_price': float(self.awg_price) if self.awg_price is not None else None,
            'expiry_time': self.expiry_time,
            'revision_number': self.revision_number,
            'price_currency': self.price_currency,
            'ext_order_status': self.ext_order_status,
            'accepted_uid': self.accepted_uid,
            'filled_value': self.filled_value,
            'extref': self.extref,
            'settle_currency': self.settle_currency,
            'on_behalf_of_uid': self.on_behalf_of_uid,
            'client_qualifier': self.client_qualifier,
            'client_short_code': self.client_short_code,
            'investment_decision_maker_qualifier': self.investment_decision_maker_qualifier,
            'investment_decision_maker_short_code': self.investment_decision_maker_short_code,
            'executing_trader_qualifier': self.executing_trader_qualifier,
            'executing_trader_short_code': self.executing_trader_short_code,
            'flags': self.flags,
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False)
