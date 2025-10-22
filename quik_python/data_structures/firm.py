"""
Firm class - информация о фирме
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class Firm(BaseDataStructure):
    """
    При получении описания новой фирмы от сервера функция возвращает таблицу Lua с параметрами
    """
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Название фирмы
    firm_name: Optional[str] = None
    
    # Статус
    status: Optional[float] = None
    
    # Торговая площадка
    exchange: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Firm':
        """
        Create Firm from dictionary
        
        Args:
            data: Dictionary with firm data
            
        Returns:
            Firm instance
        """
        return cls(
            firm_id=data.get('firmid'),
            firm_name=data.get('firm_name'),
            status=data.get('status'),
            exchange=data.get('exchange')
        )
    
    def to_dict(self) -> dict:
        """
        Convert Firm to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'firm_name': self.firm_name,
            'status': self.status,
            'exchange': self.exchange
        }
    
    def to_json(self) -> str:
        """
        Convert Firm to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
