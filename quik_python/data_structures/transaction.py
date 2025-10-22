"""
Transaction class for QUIK
Адаптированный под QLua формат .tri-файла с параметрами транзакций
"""

import json
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Callable
from .base import BaseDataStructure
from .transaction_reply import TransactionReply
from .transaction_types import (
    TransactionAction, TransactionType, TransactionOperation, ExecutionCondition,
    YesOrNo, ForAccount, OffsetUnits)
from .stop_order import StopOrderKind



@dataclass
class Transaction(BaseDataStructure):
    """
    Формат .tri-файла с параметрами транзакций
    Адоптированный под QLua
    """
    
    # Event handlers (будут реализованы как callback функции)
    on_trans_reply: Optional[Callable[['TransactionReply'], None]] = field(default=None, init=False)
    on_order: Optional[Callable] = field(default=None, init=False)  # Order будет импортирован позже
    on_stop_order: Optional[Callable] = field(default=None, init=False)  # StopOrder будет импортирован позже
    on_trade: Optional[Callable] = field(default=None, init=False)  # Trade будет импортирован позже
    
    # Response data
    transaction_reply: Optional['TransactionReply'] = field(default=None, init=False)
    orders: Optional[List] = field(default=None, init=False)  # List[Order]
    stop_orders: Optional[List] = field(default=None, init=False)  # List[StopOrder]
    trades: Optional[List] = field(default=None, init=False)  # List[Trade]
    
    # Error handling
    error_message: Optional[str] = field(default=None, init=False)
    
    # ===== TRANSACTION SPECIFICATION PROPERTIES =====
    
    # Код класса, по которому выполняется транзакция, например TQBR. Обязательный параметр
    CLASSCODE: Optional[str] = None
    
    # Код инструмента, по которому выполняется транзакция, например SBER
    SECCODE: Optional[str] = None
    
    # Вид транзакции
    ACTION: Optional[TransactionAction] = None
    
    # Идентификатор участника торгов (код фирмы)
    FIRM_ID: Optional[str] = None
    
    # Номер счета Трейдера
    ACCOUNT: Optional[str] = None
    
    # 20-ти символьное составное поле
    CLIENT_CODE: Optional[str] = None
    
    # Количество лотов в заявке, обязательный параметр
    QUANTITY: Optional[int] = None
    
    # Цена заявки, за единицу инструмента. Обязательный параметр
    PRICE: Optional[Decimal] = None
    
    # Направление заявки, обязательный параметр. Значения: «S» – продать, «B» – купить
    OPERATION: Optional[TransactionOperation] = None
    
    # Уникальный идентификационный номер заявки, значение от 1 до 2 294 967 294
    TRANS_ID: Optional[int] = None
    
    # Тип заявки, необязательный параметр. Значения: «L» – лимитированная (по умолчанию), «M» – рыночная
    TYPE: Optional[TransactionType] = None
    
    # Признак того, является ли заявка заявкой Маркет-Мейкера
    MARKET_MAKER_ORDER: Optional[YesOrNo] = None
    
    # Условие исполнения заявки, необязательный параметр
    EXECUTION_CONDITION: Optional[ExecutionCondition] = None
    
    # Объем сделки РЕПО-М в рублях
    REPOVALUE: Optional[Decimal] = None
    
    # Начальное значение дисконта в заявке на сделку РЕПО-М
    START_DISCOUNT: Optional[Decimal] = None
    
    # Нижнее предельное значение дисконта в заявке на сделку РЕПО-М
    LOWER_DISCOUNT: Optional[Decimal] = None
    
    # Верхнее предельное значение дисконта в заявке на сделку РЕПО-М
    UPPER_DISCOUNT: Optional[Decimal] = None
    
    # Стоп-цена, за единицу инструмента. Используется только при «ACTION» = «NEW_STOP_ORDER»
    STOPPRICE: Optional[Decimal] = None
    
    # Тип стоп-заявки
    STOP_ORDER_KIND: Optional[StopOrderKind] = None
    
    # Класс инструмента условия
    STOPPRICE_CLASSCODE: Optional[str] = None
    
    # Код инструмента условия
    STOPPRICE_SECCODE: Optional[str] = None
    
    # Направление предельного изменения стоп-цены
    STOPPRICE_CONDITION: Optional[str] = None
    
    # Цена связанной лимитированной заявки
    LINKED_ORDER_PRICE: Optional[Decimal] = None
    
    # Срок действия стоп-заявки
    EXPIRY_DATE: Optional[str] = None
    
    # Цена условия «стоп-лимит» для заявки типа «Тэйк-профит и стоп-лимит»
    STOPPRICE2: Optional[Decimal] = None
    
    # Признак исполнения заявки по рыночной цене при наступлении условия «стоп-лимит»
    MARKET_STOP_LIMIT: Optional[YesOrNo] = None
    
    # Признак исполнения заявки по рыночной цене при наступлении условия «тэйк-профит»
    MARKET_TAKE_PROFIT: Optional[YesOrNo] = None
    
    # Признак действия заявки типа «Тэйк-профит и стоп-лимит» в течение определенного интервала времени
    IS_ACTIVE_IN_TIME: Optional[YesOrNo] = None
    
    # Время начала действия заявки типа «Тэйк-профит и стоп-лимит» в формате «ЧЧММСС»
    ACTIVE_FROM_TIME: Optional[datetime] = None
    
    # Время окончания действия заявки типа «Тэйк-профит и стоп-лимит» в формате «ЧЧММСС»
    ACTIVE_TO_TIME: Optional[datetime] = None
    
    # Код организации – партнера по внебиржевой сделке
    PARTNER: Optional[str] = None
    
    # Номер заявки, снимаемой из торговой системы
    ORDER_KEY: Optional[str] = None
    
    # Номер стоп-заявки, снимаемой из торговой системы
    STOP_ORDER_KEY: Optional[str] = None
    
    # Код расчетов при исполнении внебиржевых заявок
    SETTLE_CODE: Optional[str] = None
    
    # Цена второй части РЕПО
    PRICE2: Optional[Decimal] = None
    
    # Срок РЕПО. Параметр сделок РЕПО-М
    REPOTERM: Optional[str] = None
    
    # Ставка РЕПО, в процентах
    REPORATE: Optional[str] = None
    
    # Признак блокировки бумаг на время операции РЕПО
    BLOCK_SECURITIES: Optional[YesOrNo] = None
    
    # Ставка фиксированного возмещения
    REFUNDRATE: Optional[Decimal] = None
    
    # Текстовый комментарий, указанный в заявке - поручение (brokerref in Trades/Orders)
    brokerref: Optional[str] = None
    
    # Признак крупной сделки (YES/NO). Параметр внебиржевой сделки
    LARGE_TRADE: Optional[YesOrNo] = None
    
    # Код валюты расчетов по внебиржевой сделки
    CURR_CODE: Optional[str] = None
    
    # Лицо, от имени которого и за чей счет регистрируется сделка
    FOR_ACCOUNT: Optional[ForAccount] = None
    
    # Дата исполнения внебиржевой сделки
    SETTLE_DATE: Optional[str] = None
    
    # Признак снятия стоп-заявки при частичном исполнении связанной лимитированной заявки
    KILL_IF_LINKED_ORDER_PARTLY_FILLED: Optional[YesOrNo] = None
    
    # Величина отступа от максимума (минимума) цены последней сделки
    OFFSET: Optional[Decimal] = None
    
    # Единицы измерения отступа
    OFFSET_UNITS: Optional[OffsetUnits] = None
    
    # Величина защитного спрэда
    SPREAD: Optional[Decimal] = None
    
    # Единицы измерения защитного спрэда
    SPREAD_UNITS: Optional[OffsetUnits] = None
    
    # Регистрационный номер заявки-условия
    BASE_ORDER_KEY: Optional[str] = None
    
    # Признак использования в качестве объема заявки «по исполнению» исполненного количества бумаг заявки-условия
    USE_BASE_ORDER_BALANCE: Optional[YesOrNo] = None
    
    # Признак активации заявки «по исполнению» при частичном исполнении заявки-условия
    ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED: Optional[YesOrNo] = None
    
    # Идентификатор базового контракта для фьючерсов или опционов
    BASE_CONTRACT: Optional[str] = None
    
    # Режим перестановки заявок на рынке FORTS
    MODE: Optional[str] = None
    
    # Номер первой заявки
    FIRST_ORDER_NUMBER: Optional[int] = None
    
    # Количество в первой заявке
    FIRST_ORDER_NEW_QUANTITY: Optional[int] = None
    
    # Цена в первой заявке
    FIRST_ORDER_NEW_PRICE: Optional[Decimal] = None
    
    # Номер второй заявки
    SECOND_ORDER_NUMBER: Optional[int] = None
    
    # Количество во второй заявке
    SECOND_ORDER_NEW_QUANTITY: Optional[int] = None
    
    # Цена во второй заявке
    SECOND_ORDER_NEW_PRICE: Optional[Decimal] = None
    
    # Признак снятия активных заявок по данному инструменту
    KILL_ACTIVE_ORDERS: Optional[YesOrNo] = None
    
    # Направление операции в сделке, подтверждаемой отчетом
    NEG_TRADE_OPERATION: Optional[str] = None
    
    # Номер подтверждаемой отчетом сделки для исполнения
    NEG_TRADE_NUMBER: Optional[int] = None
    
    # Лимит открытых позиций, при «Тип лимита» = «Ден.средства» или «Всего»
    VOLUMEMN: Optional[str] = None
    
    # Лимит открытых позиций, при «Тип лимита» = «Залоговые ден.средства»
    VOLUMEPL: Optional[str] = None
    
    # Коэффициент ликвидности
    KFL: Optional[str] = None
    
    # Коэффициент клиентского гарантийного обеспечения
    KGO: Optional[str] = None
    
    # Параметр, который определяет, будет ли загружаться величина КГО при загрузке лимитов из файла
    USE_KGO: Optional[str] = None
    
    # Признак проверки попадания цены заявки в диапазон допустимых цен
    CHECK_LIMITS: Optional[YesOrNo] = None
    
    # Ссылка, которая связывает две сделки РЕПО или РПС
    MATCHREF: Optional[str] = None
    
    # Режим корректировки ограничения по фьючерсным счетам
    CORRECTION: Optional[str] = None
    
    # Флаг ручного ввода (не передается в QUIK)
    is_manual: bool = field(default=False, init=False)
    
    def is_completed(self) -> bool:
        """
        Транзакция исполнена
        """
        if not self.orders or len(self.orders) == 0:
            return False
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from .order import OrderTradeFlags
        
        last_order = self.orders[-1]
        return (not (last_order.flags & OrderTradeFlags.ACTIVE.value) and
                not (last_order.flags & OrderTradeFlags.CANCELED.value))
    
    def on_trans_reply_call(self, reply: TransactionReply) -> None:
        """
        Функция вызывается терминалом QUIK при получении ответа на транзакцию пользователя
        """
        if self.on_trans_reply:
            self.on_trans_reply(reply)
        
        # This should happen only once per transaction id
        assert self.transaction_reply is None, "TransactionReply already exists for this transaction"
        self.transaction_reply = reply
    
    def on_order_call(self, order) -> None:  # order: Order
        """
        Функция вызывается терминалом QUIK при получении новой заявки или при изменении параметров существующей заявки
        """
        if self.on_order:
            self.on_order(order)
        
        if self.orders is None:
            self.orders = []
        self.orders.append(order)
    
    def on_stop_order_call(self, stop_order) -> None:  # stop_order: StopOrder
        """
        Функция вызывается терминалом QUIK при получении новой стоп-заявки или при изменении параметров существующей стоп-заявки
        """
        if self.on_stop_order:
            self.on_stop_order(stop_order)
        
        if self.stop_orders is None:
            self.stop_orders = []
        self.stop_orders.append(stop_order)
    
    def on_trade_call(self, trade) -> None:  # trade: Trade
        """
        Функция вызывается терминалом QUIK при получении сделки
        """
        if self.on_trade:
            self.on_trade(trade)
        
        if self.trades is None:
            self.trades = []
        self.trades.append(trade)
    
    def to_dict(self) -> dict:
        """
        Convert Transaction to dictionary
        
        Returns:
            Dictionary representation
        """
        rc = {
            'CLASSCODE': self.CLASSCODE,
            'SECCODE': self.SECCODE,
            'ACCOUNT': self.ACCOUNT,
            'CLIENT_CODE': self.CLIENT_CODE,
            'QUANTITY': str(self.QUANTITY),
            'PRICE': str(self.PRICE) if self.PRICE else "0",
        }
        if self.FIRM_ID:
            rc['FIRM_ID'] = self.FIRM_ID
        if self.ACTION:
            rc['ACTION'] = self.ACTION.name
        if self.OPERATION:
            rc['OPERATION'] = self.OPERATION.name
        if self.TRANS_ID:
            rc['TRANS_ID'] = str(self.TRANS_ID)
        if self.TYPE:
            rc['TYPE'] = self.TYPE.name
        if self.MARKET_MAKER_ORDER:
            rc['MARKET_MAKER_ORDER'] = self.MARKET_MAKER_ORDER.name
        if self.EXECUTION_CONDITION:
            rc['EXECUTION_CONDITION'] = self.EXECUTION_CONDITION.name
        if self.REPOVALUE:
            rc['REPOVALUE'] = str(self.REPOVALUE)
        if self.START_DISCOUNT:
            rc['START_DISCOUNT'] = str(self.START_DISCOUNT)
        if self.LOWER_DISCOUNT:
            rc['LOWER_DISCOUNT'] = str(self.LOWER_DISCOUNT)
        if self.UPPER_DISCOUNT:
            rc['UPPER_DISCOUNT'] = str(self.UPPER_DISCOUNT)
        if self.STOPPRICE:
            rc['STOPPRICE'] = str(self.STOPPRICE)
        if self.STOP_ORDER_KIND:
            rc['STOP_ORDER_KIND'] = self.STOP_ORDER_KIND.name
        if self.STOPPRICE_CLASSCODE:
            rc['STOPPRICE_CLASSCODE'] = self.STOPPRICE_CLASSCODE
        if self.STOPPRICE_SECCODE:
            rc['STOPPRICE_SECCODE'] = self.STOPPRICE_SECCODE
        if self.STOPPRICE_CONDITION:
            rc['STOPPRICE_CONDITION'] = self.STOPPRICE_CONDITION
        if self.LINKED_ORDER_PRICE:
            rc['LINKED_ORDER_PRICE'] = str(self.LINKED_ORDER_PRICE)
        if self.EXPIRY_DATE:
            rc['EXPIRY_DATE'] = self.EXPIRY_DATE
        if self.STOPPRICE2:
            rc['STOPPRICE2'] = str(self.STOPPRICE2)
        if self.MARKET_STOP_LIMIT:
            rc['MARKET_STOP_LIMIT'] = self.MARKET_STOP_LIMIT.name
        if self.MARKET_TAKE_PROFIT:
            rc['MARKET_TAKE_PROFIT'] = self.MARKET_TAKE_PROFIT.name
        if self.IS_ACTIVE_IN_TIME:
            rc['IS_ACTIVE_IN_TIME'] = self.IS_ACTIVE_IN_TIME.name
        if self.ACTIVE_FROM_TIME:
            rc['ACTIVE_FROM_TIME'] = self.ACTIVE_FROM_TIME.strftime('%H%M%S')
        if self.ACTIVE_TO_TIME:
            rc['ACTIVE_TO_TIME'] = self.ACTIVE_TO_TIME.strftime('%H%M%S')
        if self.PARTNER:
            rc['PARTNER'] = self.PARTNER
        if self.ORDER_KEY:
            rc['ORDER_KEY'] = self.ORDER_KEY
        if self.STOP_ORDER_KEY:
            rc['STOP_ORDER_KEY'] = self.STOP_ORDER_KEY
        if self.SETTLE_CODE:
            rc['SETTLE_CODE'] = self.SETTLE_CODE
        if self.PRICE2:
            rc['PRICE2'] = str(self.PRICE2)
        if self.REPOTERM:
            rc['REPOTERM'] = self.REPOTERM
        if self.REPORATE:
            rc['REPORATE'] = self.REPORATE
        if self.BLOCK_SECURITIES:
            rc['BLOCK_SECURITIES'] = self.BLOCK_SECURITIES.name
        if self.REFUNDRATE:
            rc['REFUNDRATE'] = str(self.REFUNDRATE)
        if self.brokerref:
            rc['brokerref'] = self.brokerref
        if self.LARGE_TRADE:
            rc['LARGE_TRADE'] = self.LARGE_TRADE.name
        if self.CURR_CODE:
            rc['CURR_CODE'] = self.CURR_CODE
        if self.FOR_ACCOUNT:
            rc['FOR_ACCOUNT'] = self.FOR_ACCOUNT.name
        if self.SETTLE_DATE:
            rc['SETTLE_DATE'] = self.SETTLE_DATE
        if self.KILL_IF_LINKED_ORDER_PARTLY_FILLED:
            rc['KILL_IF_LINKED_ORDER_PARTLY_FILLED'] = self.KILL_IF_LINKED_ORDER_PARTLY_FILLED.name
        if self.OFFSET:
            rc['OFFSET'] = str(self.OFFSET)
        if self.OFFSET_UNITS:
            rc['OFFSET_UNITS'] = self.OFFSET_UNITS.name
        if self.SPREAD:
            rc['SPREAD'] = str(self.SPREAD)
        if self.SPREAD_UNITS:
            rc['SPREAD_UNITS'] = self.SPREAD_UNITS.name
        if self.BASE_ORDER_KEY:
            rc['BASE_ORDER_KEY'] = self.BASE_ORDER_KEY
        if self.USE_BASE_ORDER_BALANCE:
            rc['USE_BASE_ORDER_BALANCE'] = self.USE_BASE_ORDER_BALANCE.name
        if self.ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED:
            rc['ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED'] = self.ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED.name
        if self.BASE_CONTRACT:
            rc['BASE_CONTRACT'] = self.BASE_CONTRACT
        if self.MODE:
            rc['MODE'] = self.MODE
        if self.FIRST_ORDER_NUMBER:
            rc['FIRST_ORDER_NUMBER'] = str(self.FIRST_ORDER_NUMBER)
        if self.FIRST_ORDER_NEW_QUANTITY:
            rc['FIRST_ORDER_NEW_QUANTITY'] = str(self.FIRST_ORDER_NEW_QUANTITY)
        if self.FIRST_ORDER_NEW_PRICE:
            rc['FIRST_ORDER_NEW_PRICE'] = str(self.FIRST_ORDER_NEW_PRICE)
        if self.SECOND_ORDER_NUMBER:
            rc['SECOND_ORDER_NUMBER'] = str(self.SECOND_ORDER_NUMBER)
        if self.SECOND_ORDER_NEW_QUANTITY:
            rc['SECOND_ORDER_NEW_QUANTITY'] = str(self.SECOND_ORDER_NEW_QUANTITY)
        if self.SECOND_ORDER_NEW_PRICE:
            rc['SECOND_ORDER_NEW_PRICE'] = str(self.SECOND_ORDER_NEW_PRICE)
        if self.KILL_ACTIVE_ORDERS:
            rc['KILL_ACTIVE_ORDERS'] = self.KILL_ACTIVE_ORDERS.name
        if self.NEG_TRADE_OPERATION:
            rc['NEG_TRADE_OPERATION'] = self.NEG_TRADE_OPERATION
        if self.NEG_TRADE_NUMBER:
            rc['NEG_TRADE_NUMBER'] = str(self.NEG_TRADE_NUMBER)
        if self.VOLUMEMN:
            rc['VOLUMEMN'] = self.VOLUMEMN
        if self.VOLUMEPL:
            rc['VOLUMEPL'] = self.VOLUMEPL
        if self.KFL:
            rc['KFL'] = self.KFL
        if self.KGO:
            rc['KGO'] = self.KGO
        if self.USE_KGO:
            rc['USE_KGO'] = self.USE_KGO
        if self.CHECK_LIMITS:
            rc['CHECK_LIMITS'] = self.CHECK_LIMITS.name
        if self.MATCHREF:
            rc['MATCHREF'] = self.MATCHREF
        if self.CORRECTION:
            rc['CORRECTION'] = self.CORRECTION
        return rc

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """
        Create Transaction from dictionary

        Args:
            data: Dictionary representation

        Returns:
            Transaction instance
        """
        return cls(
            CLASSCODE=data.get('CLASSCODE'),
            SECCODE=data.get('SECCODE'),
            ACTION=TransactionAction(data['ACTION']) if data.get('ACTION') else None,
            FIRM_ID=data.get('FIRM_ID'),
            ACCOUNT=data.get('ACCOUNT'),
            CLIENT_CODE=data.get('CLIENT_CODE'),
            QUANTITY=data.get('QUANTITY'),
            PRICE=Decimal(str(data['PRICE'])) if data.get('PRICE') else None,
            OPERATION=TransactionOperation(data['OPERATION']) if data.get('OPERATION') else None,
            TRANS_ID=data.get('TRANS_ID'),
            TYPE=TransactionType(data['TYPE']) if data.get('TYPE') else None,
            MARKET_MAKER_ORDER=YesOrNo(data['MARKET_MAKER_ORDER']) if data.get('MARKET_MAKER_ORDER') else None,
            EXECUTION_CONDITION=ExecutionCondition(data['EXECUTION_CONDITION']) if data.get('EXECUTION_CONDITION') else None,
            REPOVALUE=Decimal(str(data['REPOVALUE'])) if data.get('REPOVALUE') else None,
            START_DISCOUNT=Decimal(str(data['START_DISCOUNT'])) if data.get('START_DISCOUNT') else None,
            LOWER_DISCOUNT=Decimal(str(data['LOWER_DISCOUNT'])) if data.get('LOWER_DISCOUNT') else None,
            UPPER_DISCOUNT=Decimal(str(data['UPPER_DISCOUNT'])) if data.get('UPPER_DISCOUNT') else None,
            STOPPRICE=Decimal(str(data['STOPPRICE'])) if data.get('STOPPRICE') else None,
            STOP_ORDER_KIND=StopOrderKind(data['STOP_ORDER_KIND']) if data.get('STOP_ORDER_KIND') else None,
            STOPPRICE_CLASSCODE=data.get('STOPPRICE_CLASSCODE'),
            STOPPRICE_SECCODE=data.get('STOPPRICE_SECCODE'),
            STOPPRICE_CONDITION=data.get('STOPPRICE_CONDITION'),
            LINKED_ORDER_PRICE=Decimal(str(data['LINKED_ORDER_PRICE'])) if data.get('LINKED_ORDER_PRICE') else None,
            EXPIRY_DATE=data.get('EXPIRY_DATE'),
            STOPPRICE2=Decimal(str(data['STOPPRICE2'])) if data.get('STOPPRICE2') else None,
            MARKET_STOP_LIMIT=YesOrNo(data['MARKET_STOP_LIMIT']) if data.get('MARKET_STOP_LIMIT') else None,
            MARKET_TAKE_PROFIT=YesOrNo(data['MARKET_TAKE_PROFIT']) if data.get('MARKET_TAKE_PROFIT') else None,
            IS_ACTIVE_IN_TIME=YesOrNo(data['IS_ACTIVE_IN_TIME']) if data.get('IS_ACTIVE_IN_TIME') else None,
            ACTIVE_FROM_TIME=datetime.strptime(data['ACTIVE_FROM_TIME'], '%H%M%S') if data.get('ACTIVE_FROM_TIME') else None,
            ACTIVE_TO_TIME=datetime.strptime(data['ACTIVE_TO_TIME'], '%H%M%S') if data.get('ACTIVE_TO_TIME') else None,
            PARTNER=data.get('PARTNER'),
            ORDER_KEY=data.get('ORDER_KEY'),
            STOP_ORDER_KEY=data.get('STOP_ORDER_KEY'),
            SETTLE_CODE=data.get('SETTLE_CODE'),
            PRICE2=Decimal(str(data['PRICE2'])) if data.get('PRICE2') else None,
            REPOTERM=data.get('REPOTERM'),
            REPORATE=data.get('REPORATE'),
            BLOCK_SECURITIES=YesOrNo(data['BLOCK_SECURITIES']) if data.get('BLOCK_SECURITIES') else None,
            REFUNDRATE=Decimal(str(data['REFUNDRATE'])) if data.get('REFUNDRATE') else None,
            brokerref=data.get('brokerref'),
            LARGE_TRADE=YesOrNo(data['LARGE_TRADE']) if data.get('LARGE_TRADE') else None,
            CURR_CODE=data.get('CURR_CODE'),
            FOR_ACCOUNT=ForAccount(data['FOR_ACCOUNT']) if data.get('FOR_ACCOUNT') else None,
            SETTLE_DATE=data.get('SETTLE_DATE'),
            KILL_IF_LINKED_ORDER_PARTLY_FILLED=YesOrNo(data['KILL_IF_LINKED_ORDER_PARTLY_FILLED']) if data.get('KILL_IF_LINKED_ORDER_PARTLY_FILLED') else None,
            OFFSET=Decimal(str(data['OFFSET'])) if data.get('OFFSET') else None,
            OFFSET_UNITS=OffsetUnits(data['OFFSET_UNITS']) if data.get('OFFSET_UNITS') else None,
            SPREAD=Decimal(str(data['SPREAD'])) if data.get('SPREAD') else None,
            SPREAD_UNITS=OffsetUnits(data['SPREAD_UNITS']) if data.get('SPREAD_UNITS') else None,
            BASE_ORDER_KEY=data.get('BASE_ORDER_KEY'),
            USE_BASE_ORDER_BALANCE=YesOrNo(data['USE_BASE_ORDER_BALANCE']) if data.get('USE_BASE_ORDER_BALANCE') else None,
            ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED=YesOrNo(data['ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED']) if data.get('ACTIVATE_IF_BASE_ORDER_PARTLY_FILLED') else None,
            BASE_CONTRACT=data.get('BASE_CONTRACT'),
            MODE=data.get('MODE'),
            FIRST_ORDER_NUMBER=data.get('FIRST_ORDER_NUMBER'),
            FIRST_ORDER_NEW_QUANTITY=data.get('FIRST_ORDER_NEW_QUANTITY'),
            FIRST_ORDER_NEW_PRICE=Decimal(str(data['FIRST_ORDER_NEW_PRICE'])) if data.get('FIRST_ORDER_NEW_PRICE') else None,
            SECOND_ORDER_NUMBER=data.get('SECOND_ORDER_NUMBER'),
            SECOND_ORDER_NEW_QUANTITY=data.get('SECOND_ORDER_NEW_QUANTITY'),
            SECOND_ORDER_NEW_PRICE=Decimal(str(data['SECOND_ORDER_NEW_PRICE'])) if data.get('SECOND_ORDER_NEW_PRICE') else None,
            KILL_ACTIVE_ORDERS=YesOrNo(data['KILL_ACTIVE_ORDERS']) if data.get('KILL_ACTIVE_ORDERS') else None,
            NEG_TRADE_OPERATION=data.get('NEG_TRADE_OPERATION'),
            NEG_TRADE_NUMBER=data.get('NEG_TRADE_NUMBER'),
            VOLUMEMN=data.get('VOLUMEMN'),
            VOLUMEPL=data.get('VOLUMEPL'),
            KFL=data.get('KFL'),
            KGO=data.get('KGO'),
            USE_KGO=data.get('USE_KGO'),
            CHECK_LIMITS=YesOrNo(data['CHECK_LIMITS']) if data.get('CHECK_LIMITS') else None,
            MATCHREF=data.get('MATCHREF'),
            CORRECTION=data.get('CORRECTION')
        )
    
    def to_json(self) -> str:
        """
        Convert Transaction to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
