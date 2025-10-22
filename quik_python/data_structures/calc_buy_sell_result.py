"""
CalcBuySellResult class - результат расчета покупки/продажи
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class CalcBuySellResult(BaseDataStructure):
    """
    Результат расчета максимального количества и комиссии для операции покупки/продажи
    """
    
    # Максимально возможное количество бумаги
    qty: Optional[int] = None
    
    # Сумма комиссии
    comission: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalcBuySellResult':
        """
        Create CalcBuySellResult from dictionary
        
        Args:
            data: Dictionary containing calc buy sell result data
            
        Returns:
            CalcBuySellResult instance
        """
        return cls(
            qty=data.get('qty'),
            comission=data.get('comission')
        )
    
    def to_dict(self) -> dict:
        """
        Convert CalcBuySellResult to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'qty': self.qty,
            'comission': self.comission
        }
    
    def to_json(self) -> str:
        """
        Convert CalcBuySellResult to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
    
