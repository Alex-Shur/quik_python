"""
Trade data structure for QUIK
"""

import json
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from .base import BaseDataStructure
from .quik_datetime import QuikDateTime


class TradeWaiverFlags(Enum):
    """
    Признак того, что транзакция совершена по правилам пре-трейда
    """
    RFPT = 0x1

    NLIQ = 0x2

    OILQ = 0x4

    PRC = 0x8

    SIZE = 0x10

    ILQD = 0x20


class TradeOTCPostTradeIndicatorFlags(Enum):
    """
    OTC post-trade индикатор
    """

    # Benchmark
    BENCHMARK = 0x1

    # Agency cross
    AGENCY_CROSS = 0x2

    # Large in scale
    LARGE_IN_SCALE = 0x4

    # Illiquid instrument
    ILLIQUID_INSTRUMENT = 0x8

    # Above specified size
    ABOVE_SPECIFIED_SIZE = 0x10

    # Cancellations
    CANCELLATIONS = 0x20

    # Amendments
    AMENDMENTS = 0x40

    # Special dividend
    SPECIAL_DIVIDEND = 0x80

    # Price improvement
    PRICE_IMPROVEMENT = 0x100

    # Duplicative
    DUPLICATIVE = 0x200

    # Not contributing to the price discovery process
    NOT_CONTRIBUTING_TO_PRICE_DISCOVERY = 0x400

    # Package
    PACKAGE = 0x800

    # Exchange for Physical
    EXCHANGE_FOR_PHYSICAL = 0x1000


@dataclass
class Trade(BaseDataStructure):
    """
    Описание параметров Таблицы сделок
    """
    
    # Timestamp для Lua
    lua_timestamp: Optional[int] = None
    
    # Номер сделки в торговой системе
    trade_num: Optional[int] = None
    
    # Номер заявки в торговой системе
    order_num: Optional[int] = None
    
    # Поручение/комментарий, обычно: код клиента/номер поручения
    broker_ref: Optional[str] = None
    
    # Идентификатор трейдера
    userid: Optional[str] = None
    
    # Идентификатор дилера
    firmid: Optional[str] = None
    
    # Торговый счет
    account: Optional[str] = None
    
    # Цена
    price: Optional[Decimal] = None
    
    # Количество бумаг в последней сделке в лотах
    qty: Optional[int] = None
    
    # Объем в денежных средствах
    value: Optional[Decimal] = None
    
    # Накопленный купонный доход
    accruedint: Optional[Decimal] = None
    
    # Доходность
    yield_: Optional[Decimal] = None  # yield is reserved keyword
    
    # Код расчетов
    settlecode: Optional[str] = None
    
    # Код фирмы партнера
    cpfirmid: Optional[str] = None
    
    # Набор битовых флагов
    flags: Optional[int] = None
    
    # Цена выкупа
    price2: Optional[Decimal] = None
    
    # Ставка РЕПО (%)
    reporate: Optional[Decimal] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Доход (%) на дату выкупа
    accrued2: Optional[Decimal] = None
    
    # Сумма РЕПО
    repovalue: Optional[Decimal] = None
    
    # Объем выкупа РЕПО
    repo2value: Optional[Decimal] = None
    
    # Начальный дисконт (%)
    start_discount: Optional[Decimal] = None
    
    # Нижний дисконт (%)
    lower_discount: Optional[Decimal] = None
    
    # Верхний дисконт (%)
    upper_discount: Optional[Decimal] = None
    
    # Блокировка обеспечения («Да»/«Нет»)
    block_securities: Optional[Decimal] = None
    
    # Клиринговая комиссия (ММВБ)
    clearing_comission: Optional[Decimal] = None
    
    # Комиссия Фондовой биржи (ММВБ)
    exchange_comission: Optional[Decimal] = None
    
    # Комиссия Технического центра (ММВБ)
    tech_center_comission: Optional[Decimal] = None
    
    # Дата расчетов
    settle_date: Optional[Decimal] = None
    
    # Валюта расчетов
    settle_currency: Optional[str] = None
    
    # Валюта
    trade_currency: Optional[str] = None
    
    # Код биржи в торговой системе
    exchange_code: Optional[str] = None
    
    # Идентификатор рабочей станции
    station_id: Optional[str] = None
    
    # Код бумаги заявки
    sec_code: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None
    
    # Дата и время
    datetime: Optional[QuikDateTime] = None
    
    # Идентификатор расчетного счета/кода в клиринговой организации
    bank_acc_id: Optional[str] = None
    
    # Комиссия брокера
    broker_comission: Optional[Decimal] = None
    
    # Номер витринной сделки в Торговой Системе для сделок РЕПО с ЦК и SWAP
    linked_trade: Optional[int] = None
    
    # Период торговой сессии
    period: Optional[int] = None
    
    # Идентификатор транзакции
    trans_id: Optional[int] = None
    
    # Тип сделки
    # «1» – Обычная; 
    # «2» – Адресная; 
    # «3» – Первичное размещение; 
    # «4» – Перевод денег/бумаг; 
    # «5» – Адресная сделка первой части РЕПО; 
    # «6» – Расчетная по операции своп; 
    # «7» – Расчетная по внебиржевой операции своп; 
    # «8» – Расчетная сделка бивалютной корзины; 
    # «9» – Расчетная внебиржевая сделка бивалютной корзины; 
    # «10» – Сделка по операции РЕПО с ЦК; 
    # «11» – Первая часть сделки по операции РЕПО с ЦК; 
    # «12» – Вторая часть сделки по операции РЕПО с ЦК; 
    # «13» – Адресная сделка по операции РЕПО с ЦК; 
    # «14» – Первая часть адресной сделки по операции РЕПО с ЦК; 
    # «15» – Вторая часть адресной сделки по операции РЕПО с ЦК; 
    # «16» – Техническая сделка по возврату активов РЕПО с ЦК; 
    # «17» – Сделка по спреду между фьючерсами разных сроков на один актив; 
    # «18» – Техническая сделка первой части от спреда между фьючерсами; 
    # «19» – Техническая сделка второй части от спреда между фьючерсами; 
    # «20» – Адресная сделка первой части РЕПО с корзиной; 
    # «21» – Адресная сделка второй части РЕПО с корзиной; 
    # «22» – Перенос позиций срочного рынка
    kind: Optional[int] = None
    
    # Идентификатор счета в НКЦ (расчетный код)
    clearing_bank_accid: Optional[str] = None
    
    # Дата и время снятия сделки
    canceled_datetime: Optional[QuikDateTime] = None
    
    # Идентификатор фирмы - участника клиринга
    clearing_firmid: Optional[str] = None
    
    # Дополнительная информация по сделке
    system_ref: Optional[str] = None
    
    # Идентификатор пользователя на сервере QUIK
    uid: Optional[int] = None
    
    # Приоритетное обеспечение
    lseccode: Optional[str] = None
    
    # Номер ревизии заявки
    # Номер ревизии заявки, по которой была совершена сделка (параметр используется только для сделок, совершенных по заявкам, к которым применена транзакция замены заявки с сохранением номера)
    order_revision_number: Optional[int] = None
    
    # Количество в заявке на момент совершения сделки
    # Количество в заявке на момент совершения сделки, в лотах (параметр используется только для сделок, совершенных по заявкам, к которым применена транзакция замены заявки с сохранением номера)
    order_qty: Optional[int] = None
    
    # Цена в заявке на момент совершения сделки
    # Цена в заявке на момент совершения сделки (параметр используется только для сделок, совершенных по заявкам, к которым применена транзакция замены заявки с сохранением номера)
    order_price: Optional[Decimal] = None
    
    # Биржевой номер заявки
    order_exchange_code: Optional[str] = None
    
    # Площадка исполнения
    exec_market: Optional[str] = None
    
    # Индикатор ликвидности
    # «0» – не определено; 
    # «1» – по заявке мейкера; 
    # «2» – по заявке тейкера; 
    # «3» – вывод ликвидности; 
    # «4» – по заявке в период аукциона
    liquidity_indicator: Optional[int] = None
    
    # Внешняя ссылка
    # Внешняя ссылка, используется для обратной связи с внешними системами
    extref: Optional[str] = None
    
    # Расширенные флаги
    # Расширенные флаги, полученные от шлюза напрямую, без вмешательства сервера QUIK. Поле не заполняется
    ext_trade_flags: Optional[int] = None
    
    # UID пользователя, от имени которого совершена сделка
    on_behalf_of_uid: Optional[int] = None
    
    # Квалификатор клиента
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «3» – Legal Entity
    client_qualifier: Optional[int] = None
    
    # Краткий идентификатор клиента
    client_short_code: Optional[int] = None
    
    # Квалификатор принявшего решение о совершении сделки
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «3» – Algorithm
    investment_decision_maker_qualifier: Optional[int] = None
    
    # Краткий идентификатор принявшего решение о совершении сделки
    investment_decision_maker_short_code: Optional[int] = None
    
    # Квалификатор трейдера, исполнившего заявку
    # «0» – не определено; 
    # «1» – Natural Person; 
    # «3» – Algorithm
    executing_trader_qualifier: Optional[int] = None
    
    # Краткий идентификатор трейдера, исполнившего заявку
    executing_trader_short_code: Optional[int] = None
    
    # Признак того, что транзакция совершена по правилам пре-трейда. Возможные значения битовых флагов: 
    # бит 0 (0x1) – RFPT; 
    # бит 1 (0x2) – NLIQ; 
    # бит 2 (0x4) – OILQ; 
    # бит 3 (0x8) – PRC; 
    # бит 4 (0x10)– SIZE; 
    # бит 5 (0x20) – ILQD
    waiver_flag: Optional[int] = None
    
    # Идентификатор базового инструмента для multileg-инструментов
    mleg_base_sid: Optional[int] = None
    
    # Квалификатор операции. Возможные значения: 
    # «0» – не определено; 
    # «1» – Buy; 
    # «2» – Sell; 
    # «3» – Sell short; 
    # «4» – Sell short exempt; 
    # «5» – Sell undiclosed
    side_qualifier: Optional[int] = None
    
    # OTC post-trade индикатор. Возможные значения битовых флагов: 
    # бит 0 (0x1) – Benchmark; 
    # бит 1 (0x2) – Agency cross;
    # бит 2 (0x4) – Large in scale; 
    # бит 3 (0x8) – Illiquid instrument;
    # бит 4 (0x10) – Above specified size; 
    # бит 5 (0x20) – Cancellations; 
    # бит 6 (0x40) – Amendments; 
    # бит 7 (0x80) – Special dividend;
    # бит 8 (0x100) – Price improvement;
    # бит 9 (0x200) – Duplicative; 
    # бит 10 (0x400) – Not contributing to the price discovery process; 
    # бит 11 (0x800) – Package; 
    # бит 12 (0x1000) – Exchange for Physical
    otc_post_trade_indicator: Optional[int] = None
    
    # Роль в исполнении заявки. Возможные значения: 
    # «0» – не определено; 
    # «1» – Agent; 
    # «2» – Principal; 
    # «3» – Riskless principal; 
    # «4» – CFG give up; 
    # «5» – Cross as agent; 
    # «6» – Matched principal; 
    # «7» – Proprietary; 
    # «8» – Individual; 
    # «9» – Agent for other member; 
    # «10» – Mixed; 
    # «11» – Market maker
    capacity: Optional[int] = None
    
    # Кросс-курс валюты цены сделки к валюте расчетов
    cross_rate: Optional[Decimal] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Trade':
        """
        Create Trade from dictionary
        
        Args:
            data: Dictionary with trade data
            
        Returns:
            Trade instance
        """
        return cls(
            lua_timestamp=data.get('lua_timestamp'),
            trade_num=data.get('trade_num'),
            order_num=data.get('order_num'),
            broker_ref=data.get('brokerref'),
            userid=data.get('userid'),
            firmid=data.get('firmid'),
            account=data.get('account'),
            price=Decimal(str(data['price'])) if data.get('price') is not None else None,
            qty=data.get('qty'),
            value=Decimal(str(data['value'])) if data.get('value') is not None else None,
            accruedint=Decimal(str(data['accruedint'])) if data.get('accruedint') is not None else None,
            yield_=Decimal(str(data['yield'])) if data.get('yield') is not None else None,
            settlecode=data.get('settlecode'),
            cpfirmid=data.get('cpfirmid'),
            flags=data.get('flags'),
            price2=Decimal(str(data['price2'])) if data.get('price2') is not None else None,
            reporate=Decimal(str(data['reporate'])) if data.get('reporate') is not None else None,
            client_code=data.get('client_code'),
            accrued2=Decimal(str(data['accrued2'])) if data.get('accrued2') is not None else None,
            repovalue=Decimal(str(data['repovalue'])) if data.get('repovalue') is not None else None,
            repo2value=Decimal(str(data['repo2value'])) if data.get('repo2value') is not None else None,
            start_discount=Decimal(str(data['start_discount'])) if data.get('start_discount') is not None else None,
            lower_discount=Decimal(str(data['lower_discount'])) if data.get('lower_discount') is not None else None,
            upper_discount=Decimal(str(data['upper_discount'])) if data.get('upper_discount') is not None else None,
            block_securities=Decimal(str(data['block_securities'])) if data.get('block_securities') is not None else None,
            clearing_comission=Decimal(str(data['clearing_comission'])) if data.get('clearing_comission') is not None else None,
            exchange_comission=Decimal(str(data['exchange_comission'])) if data.get('exchange_comission') is not None else None,
            tech_center_comission=Decimal(str(data['tech_center_comission'])) if data.get('tech_center_comission') is not None else None,
            settle_date=Decimal(str(data['settle_date'])) if data.get('settle_date') is not None else None,
            settle_currency=data.get('settle_currency'),
            trade_currency=data.get('trade_currency'),
            exchange_code=data.get('exchange_code'),
            station_id=data.get('station_id'),
            sec_code=data.get('sec_code'),
            class_code=data.get('class_code'),
            datetime=QuikDateTime.from_dict(data['datetime']) if data.get('datetime') else None,
            bank_acc_id=data.get('bank_acc_id'),
            broker_comission=Decimal(str(data['broker_comission'])) if data.get('broker_comission') is not None else None,
            linked_trade=data.get('linked_trade'),
            period=data.get('period'),
            trans_id=data.get('trans_id'),
            kind=data.get('kind'),
            clearing_bank_accid=data.get('clearing_bank_accid'),
            canceled_datetime=QuikDateTime.from_dict(data['canceled_datetime']) if data.get('canceled_datetime') else None,
            clearing_firmid=data.get('clearing_firmid'),
            system_ref=data.get('system_ref'),
            uid=data.get('uid'),
            lseccode=data.get('lseccode'),
            order_revision_number=data.get('order_revision_number'),
            order_qty=data.get('order_qty'),
            order_price=Decimal(str(data['order_price'])) if data.get('order_price') is not None else None,
            order_exchange_code=data.get('order_exchange_code'),
            exec_market=data.get('exec_market'),
            liquidity_indicator=data.get('liquidity_indicator'),
            extref=data.get('extref'),
            ext_trade_flags=data.get('ext_trade_flags'),
            on_behalf_of_uid=data.get('on_behalf_of_uid'),
            client_qualifier=data.get('client_qualifier'),
            client_short_code=data.get('client_short_code'),
            investment_decision_maker_qualifier=data.get('investment_decision_maker_qualifier'),
            investment_decision_maker_short_code=data.get('investment_decision_maker_short_code'),
            executing_trader_qualifier=data.get('executing_trader_qualifier'),
            executing_trader_short_code=data.get('executing_trader_short_code'),
            waiver_flag=data.get('waiver_flag'),
            mleg_base_sid=data.get('mleg_base_sid'),
            side_qualifier=data.get('side_qualifier'),
            otc_post_trade_indicator=data.get('otc_post_trade_indicator'),
            capacity=data.get('capacity'),
            cross_rate=Decimal(str(data['cross_rate'])) if data.get('cross_rate') is not None else None
        )
    
    def to_dict(self) -> dict:
        """
        Convert Trade to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'lua_timestamp': self.lua_timestamp,
            'trade_num': self.trade_num,
            'order_num': self.order_num,
            'brokerref': self.broker_ref,
            'userid': self.userid,
            'firmid': self.firmid,
            'account': self.account,
            'price': float(self.price) if self.price is not None else None,
            'qty': self.qty,
            'value': float(self.value) if self.value is not None else None,
            'accruedint': float(self.accruedint) if self.accruedint is not None else None,
            'yield': float(self.yield_) if self.yield_ is not None else None,
            'settlecode': self.settlecode,
            'cpfirmid': self.cpfirmid,
            'flags': self.flags,
            'price2': float(self.price2) if self.price2 is not None else None,
            'reporate': float(self.reporate) if self.reporate is not None else None,
            'client_code': self.client_code,
            'accrued2': float(self.accrued2) if self.accrued2 is not None else None,
            'repovalue': float(self.repovalue) if self.repovalue is not None else None,
            'repo2value': float(self.repo2value) if self.repo2value is not None else None,
            'start_discount': float(self.start_discount) if self.start_discount is not None else None,
            'lower_discount': float(self.lower_discount) if self.lower_discount is not None else None,
            'upper_discount': float(self.upper_discount) if self.upper_discount is not None else None,
            'block_securities': float(self.block_securities) if self.block_securities is not None else None,
            'clearing_comission': float(self.clearing_comission) if self.clearing_comission is not None else None,
            'exchange_comission': float(self.exchange_comission) if self.exchange_comission is not None else None,
            'tech_center_comission': float(self.tech_center_comission) if self.tech_center_comission is not None else None,
            'settle_date': float(self.settle_date) if self.settle_date is not None else None,
            'settle_currency': self.settle_currency,
            'trade_currency': self.trade_currency,
            'exchange_code': self.exchange_code,
            'station_id': self.station_id,
            'sec_code': self.sec_code,
            'class_code': self.class_code,
            'datetime': self.datetime.to_dict() if self.datetime else None,
            'bank_acc_id': self.bank_acc_id,
            'broker_comission': float(self.broker_comission) if self.broker_comission is not None else None,
            'linked_trade': self.linked_trade,
            'period': self.period,
            'trans_id': self.trans_id,
            'kind': self.kind,
            'clearing_bank_accid': self.clearing_bank_accid,
            'canceled_datetime': self.canceled_datetime.to_dict() if self.canceled_datetime else None,
            'clearing_firmid': self.clearing_firmid,
            'system_ref': self.system_ref,
            'uid': self.uid,
            'lseccode': self.lseccode,
            'order_revision_number': self.order_revision_number,
            'order_qty': self.order_qty,
            'order_price': float(self.order_price) if self.order_price is not None else None,
            'order_exchange_code': self.order_exchange_code,
            'exec_market': self.exec_market,
            'liquidity_indicator': self.liquidity_indicator,
            'extref': self.extref,
            'ext_trade_flags': self.ext_trade_flags,
            'on_behalf_of_uid': self.on_behalf_of_uid,
            'client_qualifier': self.client_qualifier,
            'client_short_code': self.client_short_code,
            'investment_decision_maker_qualifier': self.investment_decision_maker_qualifier,
            'investment_decision_maker_short_code': self.investment_decision_maker_short_code,
            'executing_trader_qualifier': self.executing_trader_qualifier,
            'executing_trader_short_code': self.executing_trader_short_code,
            'waiver_flag': self.waiver_flag,
            'mleg_base_sid': self.mleg_base_sid,
            'side_qualifier': self.side_qualifier,
            'otc_post_trade_indicator': self.otc_post_trade_indicator,
            'capacity': self.capacity,
            'cross_rate': float(self.cross_rate) if self.cross_rate is not None else None
        }
    
    def to_json(self) -> str:
        """
        Convert Trade to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
    
