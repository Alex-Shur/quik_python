"""
Account position data structure
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class AccountPosition(BaseDataStructure):
    """
    При изменении денежной позиции по счету функция возвращает таблицу Lua с параметрами
    """
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Код валюты
    curr_code: Optional[str] = None
    
    # Тэг расчетов
    tag: Optional[str] = None
    
    # Описание
    description: Optional[str] = None
    
    # Входящий остаток
    open_bal: Optional[float] = None
    
    # Текущий остаток
    current_pos: Optional[float] = None
    
    # Плановый остаток
    planned_pos: Optional[float] = None
    
    # Внешнее ограничение по деньгам
    limit1: Optional[float] = None
    
    # Внутреннее ограничение по деньгам
    limit2: Optional[float] = None
    
    # В заявках на продажу
    order_buy: Optional[float] = None
    
    # В заявках на покупку
    order_sell: Optional[float] = None
    
    # Нетто-позиция
    netto: Optional[float] = None
    
    # Плановая позиция
    planned_bal: Optional[float] = None
    
    # Дебит
    debit: Optional[float] = None
    
    # Кредит
    credit: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountPosition':
        """
        Create AccountPosition from dictionary
        
        Args:
            data: Dictionary with account position data
            
        Returns:
            AccountPosition instance
        """
        return cls(
            firm_id=data.get('firmid'),
            curr_code=data.get('currcode'),
            tag=data.get('tag'),
            description=data.get('description'),
            open_bal=data.get('openbal'),
            current_pos=data.get('currentpos'),
            planned_pos=data.get('plannedpos'),
            limit1=data.get('limit1'),
            limit2=data.get('limit2'),
            order_buy=data.get('orderbuy'),
            order_sell=data.get('ordersell'),
            netto=data.get('netto'),
            planned_bal=data.get('plannedbal'),
            debit=data.get('debit'),
            credit=data.get('credit')
        )
    
    def to_dict(self) -> dict:
        """
        Convert AccountPosition to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'currcode': self.curr_code,
            'tag': self.tag,
            'description': self.description,
            'openbal': self.open_bal,
            'currentpos': self.current_pos,
            'plannedpos': self.planned_pos,
            'limit1': self.limit1,
            'limit2': self.limit2,
            'orderbuy': self.order_buy,
            'ordersell': self.order_sell,
            'netto': self.netto,
            'plannedbal': self.planned_bal,
            'debit': self.debit,
            'credit': self.credit
        }
    
    def to_json(self) -> str:
        """
        Convert AccountPosition to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
