"""
All trades data structure
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import IntFlag
from .base import BaseDataStructure
from .quik_datetime import QuikDateTime


class AllTradeFlags(IntFlag):
    """
    Набор битовых флагов для сделок
    бит 0 (0x1) Сделка на продажу
    бит 1 (0x2) Сделка на покупку
    """
    # Сделка на продажу
    SELL = 0x1

    # Сделка на покупку
    BUY = 0x2


@dataclass
class AllTrade(BaseDataStructure):
    """
    Таблица с параметрами обезличенной сделки
    """
    
    # Номер сделки в торговой системе
    trade_num: Optional[int] = None
    
    # Набор битовых флагов:
    # бит 0 (0x1) Сделка на продажу
    # бит 1 (0x2) Сделка на покупку
    flags: Optional[AllTradeFlags] = None
    
    # Цена
    price: Optional[float] = None
    
    # Количество бумаг в последней сделке в лотах
    qty: Optional[int] = None
    
    # Объем в денежных средствах
    value: Optional[float] = None
    
    # Накопленный купонный доход
    accruedint: Optional[float] = None
    
    # Доходность
    yield_: Optional[float] = None  # yield - зарезервированное слово в Python
    
    # Код расчетов
    settlecode: Optional[str] = None
    
    # Ставка РЕПО (%)
    reporate: Optional[float] = None
    
    # Сумма РЕПО
    repovalue: Optional[float] = None
    
    # Объем выкупа РЕПО
    repo2value: Optional[float] = None
    
    # Срок РЕПО в днях
    repoterm: Optional[float] = None
    
    # Код бумаги заявки
    sec_code: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None
    
    # Дата и время
    datetime: Optional[QuikDateTime] = None
    
    # Период торговой сессии. Возможные значения:
    # «0» – Открытие;
    # «1» – Нормальный;
    # «2» – Закрытие
    period: Optional[int] = None
    
    # Открытый интерес
    open_interest: Optional[float] = None
    
    # Код биржи в торговой системе
    exchange_code: Optional[str] = None
    
    # Площадка исполнения
    exec_market: Optional[str] = None
    
    # Timestamp from Lua
    lua_timestamp: Optional[int] = None
    
    def get_yield(self) -> Optional[float]:
        """
        Получить доходность (альтернатива для yield_)
        """
        return self.yield_
    
    def set_yield(self, value: Optional[float]):
        """
        Установить доходность
        """
        self.yield_ = value
    
    @property
    def repo2_value(self) -> Optional[float]:
        """
        Алиас для repo2value с подчеркиванием для лучшей читаемости
        """
        return self.repo2value
    
    @repo2_value.setter
    def repo2_value(self, value: Optional[float]):
        """
        Сеттер для repo2_value
        """
        self.repo2value = value
    
    # def is_buy(self) -> bool:
    #     """
    #     Проверка, является ли сделка покупкой
    #     """
    #     return bool(self.flags and (self.flags & AllTradeFlags.BUY))
    
    # def is_sell(self) -> bool:
    #     """
    #     Проверка, является ли сделка продажей
    #     """
    #     return bool(self.flags and (self.flags & AllTradeFlags.SELL))
    
    def get_period_description(self) -> str:
        """
        Возвращает описание периода торговой сессии
        """
        period_descriptions = {
            0: "Открытие",
            1: "Нормальный",
            2: "Закрытие"
        }
        return period_descriptions.get(self.period, f"Неизвестный период: {self.period}")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AllTrade':
        """
        Create AllTrade from dictionary
        
        Args:
            data: Dictionary containing all trade data
            
        Returns:
            AllTrade instance
        """
        return cls(
            trade_num=data.get('trade_num'),
            flags=AllTradeFlags(data['flags']) if data.get('flags') is not None else None,
            price=data.get('price'),
            qty=data.get('qty'),
            value=data.get('value'),
            accruedint=data.get('accruedint'),
            yield_=data.get('yield_'),
            settlecode=data.get('settlecode'),
            reporate=data.get('reporate'),
            repovalue=data.get('repovalue'),
            repo2value=data.get('repo2value'),
            repoterm=data.get('repoterm'),
            sec_code=data.get('sec_code'),
            class_code=data.get('class_code'),
            datetime=QuikDateTime.from_dict(data['datetime']) if data.get('datetime') else None,
            period=data.get('period'),
            open_interest=data.get('open_interest'),
            exchange_code=data.get('exchange_code'),
            exec_market=data.get('exec_market'),
            lua_timestamp=data.get('lua_timestamp')
        )
    
    def to_dict(self) -> dict:
        """
        Convert AllTrade to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'trade_num': self.trade_num,
            'flags': int(self.flags) if self.flags is not None else None,
            'price': self.price,
            'qty': self.qty,
            'value': self.value,
            'accruedint': self.accruedint,
            'yield_': self.yield_,
            'settlecode': self.settlecode,
            'reporate': self.reporate,
            'repovalue': self.repovalue,
            'repo2value': self.repo2value,
            'repoterm': self.repoterm,
            'sec_code': self.sec_code,
            'class_code': self.class_code,
            'datetime': self.datetime.to_dict() if self.datetime else None,
            'period': self.period,
            'open_interest': self.open_interest,
            'exchange_code': self.exchange_code,
            'exec_market': self.exec_market,
            'lua_timestamp': self.lua_timestamp
        }
    
    def to_json(self) -> str:
        """
        Convert AllTrade to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
    
