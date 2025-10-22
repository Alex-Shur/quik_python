"""
Account balance data structure
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class AccountBalance(BaseDataStructure):
    """
    При изменении текущей позиции по счету функция возвращает таблицу Lua с параметрами
    """
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Код бумаги
    sec_code: Optional[str] = None
    
    # Торговый счет
    trd_acc_id: Optional[str] = None
    
    # Счет депо
    dep_acc_id: Optional[str] = None
    
    # Входящий остаток
    open_bal: Optional[float] = None
    
    # Текущий остаток
    current_pos: Optional[float] = None
    
    # Плановая продажа
    planned_pos_sell: Optional[float] = None
    
    # Плановая покупка
    planned_pos_buy: Optional[float] = None
    
    # Контрольный остаток простого клиринга
    plan_bal: Optional[float] = None
    
    # Куплено
    us_qty_b: Optional[float] = None
    
    # Продано
    us_qty_s: Optional[float] = None
    
    # Плановый остаток
    planned: Optional[float] = None
    
    # Плановая позиция после проведения расчетов
    settle_bal: Optional[float] = None
    
    # Идентификатор расчетного счета/кода в клиринговой организации
    bank_acc_id: Optional[str] = None
    
    # Признак счета обеспечения (0 - обычный, 1 - обеспечения)
    firm_use: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountBalance':
        """
        Create AccountBalance from dictionary
        
        Args:
            data: Dictionary with account balance data
            
        Returns:
            AccountBalance instance
        """
        return cls(
            firm_id=data.get('firmid'),
            sec_code=data.get('sec_code'),
            trd_acc_id=data.get('trdaccid'),
            dep_acc_id=data.get('depaccid'),
            open_bal=data.get('openbal'),
            current_pos=data.get('currentpos'),
            planned_pos_sell=data.get('plannedpossell'),
            planned_pos_buy=data.get('plannedposbuy'),
            plan_bal=data.get('planbal'),
            us_qty_b=data.get('usqtyb'),
            us_qty_s=data.get('usqtys'),
            planned=data.get('planned'),
            settle_bal=data.get('settlebal'),
            bank_acc_id=data.get('bank_acc_id'),
            firm_use=data.get('firmuse')
        )
    
    def to_dict(self) -> dict:
        """
        Convert AccountBalance to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'sec_code': self.sec_code,
            'trdaccid': self.trd_acc_id,
            'depaccid': self.dep_acc_id,
            'openbal': self.open_bal,
            'currentpos': self.current_pos,
            'plannedpossell': self.planned_pos_sell,
            'plannedposbuy': self.planned_pos_buy,
            'planbal': self.plan_bal,
            'usqtyb': self.us_qty_b,
            'usqtys': self.us_qty_s,
            'planned': self.planned,
            'settlebal': self.settle_bal,
            'bank_acc_id': self.bank_acc_id,
            'firmuse': self.firm_use
        }
    
    def to_json(self) -> str:
        """
        Convert AccountBalance to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
