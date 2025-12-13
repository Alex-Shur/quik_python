"""
MoneyLimitEx class - лимиты по денежным средствам
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

from quik_python.data_structures.depo_limit_ex import LimitKind
from .base import BaseDataStructure


@dataclass
class MoneyLimitEx(BaseDataStructure):
    """
    Лимиты по денежным средствам
    
    Представляет расширенную информацию о денежных лимитах клиента,
    включая остатки, текущие лимиты, заблокированные средства и обеспечение.
    """
    
    # Код валюты
    curr_code: Optional[str] = None
    
    # Тэг расчетов
    tag: Optional[str] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Входящий остаток по деньгам
    open_bal: Optional[float] = None
    
    # Входящий лимит по деньгам
    open_limit: Optional[float] = None
    
    # Текущий остаток по деньгам
    current_bal: Optional[float] = None
    
    # Текущий лимит по деньгам
    current_limit: Optional[float] = None
    
    # Заблокированное количество
    locked: Optional[float] = None
    
    # Стоимость активов в заявках на покупку немаржинальных бумаг
    locked_value_coef: Optional[float] = None
    
    # Стоимость активов в заявках на покупку маржинальных бумаг
    locked_margin_value: Optional[float] = None
    
    # Плечо
    leverage: Optional[float] = None
    
    # Тип лимита (0 - обычные, иначе - технологические)
    limit_kind: Optional[LimitKind] = None
    
    # Средневзвешенная цена приобретения позиции
    wa_position_price: Optional[float] = None
    
    # Гарантийное обеспечение заявок
    orders_collateral: Optional[float] = None
    
    # Гарантийное обеспечение позиций
    positions_collateral: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MoneyLimitEx':
        """
        Create MoneyLimitEx from dictionary
        
        Args:
            data: Dictionary with money limit extended data
            
        Returns:
            MoneyLimitEx instance
        """
        limit_kind = LimitKind.T0
        limit = data.get('limit_kind')
        if limit:
            if limit in LimitKind._value2member_map_:
                limit_kind = LimitKind(limit)
            else:
                limit_kind = LimitKind.NOT_IMPLEMENTED

        return cls(
            curr_code=data.get('currcode'),
            tag=data.get('tag'),
            firm_id=data.get('firmid'),
            client_code=data.get('client_code'),
            open_bal=data.get('openbal'),
            open_limit=data.get('openlimit'),
            current_bal=data.get('currentbal'),
            current_limit=data.get('currentlimit'),
            locked=data.get('locked'),
            locked_value_coef=data.get('locked_value_coef'),
            locked_margin_value=data.get('locked_margin_value'),
            leverage=data.get('leverage'),
            limit_kind=limit_kind,
            wa_position_price=data.get('wa_position_price'),
            orders_collateral=data.get('orders_collateral'),
            positions_collateral=data.get('positions_collateral')
        )
    
    def to_dict(self) -> dict:
        """
        Convert MoneyLimitEx to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'currcode': self.curr_code,
            'tag': self.tag,
            'firmid': self.firm_id,
            'client_code': self.client_code,
            'openbal': self.open_bal,
            'openlimit': self.open_limit,
            'currentbal': self.current_bal,
            'currentlimit': self.current_limit,
            'locked': self.locked,
            'locked_value_coef': self.locked_value_coef,
            'locked_margin_value': self.locked_margin_value,
            'leverage': self.leverage,
            'limit_kind': self.limit_kind.value if self.limit_kind is not None else 0,
            'wa_position_price': self.wa_position_price,
            'orders_collateral': self.orders_collateral,
            'positions_collateral': self.positions_collateral
        }
    
    def to_json(self) -> str:
        """
        Convert MoneyLimitEx to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()

