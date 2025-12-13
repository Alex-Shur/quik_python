"""
DepoLimitEx class - расширенная информация о лимитах по бумагам
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .base import BaseDataStructure


class LimitKind(Enum):
    """
    Тип лимита бумаги
    """
    # Тип лимита T0
    T0 = 0
    
    # Тип лимита Т1
    T1 = 1
    
    # Тип лимита Т2
    T2 = 2
    
    # Не учтенный в данной структуре тип лимита
    NOT_IMPLEMENTED = -1


@dataclass
class DepoLimitEx(BaseDataStructure):
    """
    На основе: http://help.qlua.org/ch4_6_11.htm
    Запись, которую можно получить из таблицы "Лимиты по бумагам" (depo_limits)
    """
    
    # Код бумаги
    sec_code: Optional[str] = None
    
    # Счет депо
    trd_acc_id: Optional[str] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Входящий остаток по бумагам
    open_bal: Optional[int] = None
    
    # Входящий лимит по бумагам
    open_limit: Optional[int] = None
    
    # Текущий остаток по бумагам
    current_bal: Optional[int] = None
    
    # Текущий лимит по бумагам
    current_limit: Optional[int] = None
    
    # Заблокировано на продажу количества лотов
    locked_sell: Optional[int] = None
    
    # Заблокированного на покупку количества лотов
    locked_buy: Optional[int] = None
    
    # Стоимость ценных бумаг, заблокированных под покупку
    locked_buy_value: Optional[float] = None
    
    # Стоимость ценных бумаг, заблокированных под продажу
    locked_sell_value: Optional[float] = None
    
    # Цена приобретения (старый параметр)
    awg_position_price: Optional[float] = None
    
    # Цена приобретения
    wa_position_price: Optional[float] = None
    
    # Валюта цены приобретения
    wa_price_currency: Optional[str] = None

    # Тип лимита (целое число)
    limit_kind: Optional[LimitKind] = None


    @classmethod
    def from_dict(cls, data: dict) -> 'DepoLimitEx':
        """
        Create DepoLimitEx from dictionary
        
        Args:
            data: Dictionary with depo limit extended data
            
        Returns:
            DepoLimitEx instance
        """
        limit_kind = LimitKind.T0
        limit = data.get('limit_kind')
        if limit:
            if limit in LimitKind._value2member_map_:
                limit_kind = LimitKind(limit)
            else:
                limit_kind = LimitKind.NOT_IMPLEMENTED

        rc = cls(
            sec_code=data.get('sec_code'),
            trd_acc_id=data.get('trdaccid'),
            firm_id=data.get('firmid'),
            client_code=data.get('client_code'),
            open_bal=data.get('openbal'),
            open_limit=data.get('openlimit'),
            current_bal=data.get('currentbal'),
            current_limit=data.get('currentlimit'),
            locked_sell=data.get('locked_sell'),
            locked_buy=data.get('locked_buy'),
            locked_buy_value=data.get('locked_buy_value'),
            locked_sell_value=data.get('locked_sell_value'),
            awg_position_price=data.get('awg_position_price'),
            wa_position_price=data.get('wa_position_price'),
            wa_price_currency=data.get('wa_price_currency'),
            limit_kind=limit_kind
        )
        return rc
    
    def to_dict(self) -> dict:
        """
        Convert DepoLimitEx to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'sec_code': self.sec_code,
            'trdaccid': self.trd_acc_id,
            'firmid': self.firm_id,
            'client_code': self.client_code,
            'openbal': self.open_bal,
            'openlimit': self.open_limit,
            'currentbal': self.current_bal,
            'currentlimit': self.current_limit,
            'locked_sell': self.locked_sell,
            'locked_buy': self.locked_buy,
            'locked_buy_value': self.locked_buy_value,
            'locked_sell_value': self.locked_sell_value,
            'awg_position_price': self.awg_position_price,
            'wa_position_price': self.wa_position_price,
            'wa_price_currency': self.wa_price_currency,
            'limit_kind': self.limit_kind.value if self.limit_kind is not None else 0
        }
    
    def to_json(self) -> str:
        """
        Convert DepoLimitEx to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
