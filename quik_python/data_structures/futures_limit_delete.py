"""
FuturesLimitDelete class - удаление лимита по срочному рынку
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class FuturesLimitDelete(BaseDataStructure):
    """
    При удалении лимита по срочному рынку функция возвращает таблицу Lua с параметрами
    
    Используется для получения информации о результате удаления лимита
    """
    
    # Код торгового счета
    trd_acc_id: Optional[str] = None
    
    # Тип лимита
    limit_type: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FuturesLimitDelete':
        """
        Create FuturesLimitDelete from dictionary
        
        Args:
            data: Dictionary with futures limit delete data
            
        Returns:
            FuturesLimitDelete instance
        """
        return cls(
            trd_acc_id=data.get('trdaccid'),
            limit_type=data.get('limit_type')
        )
    
    def to_dict(self) -> dict:
        """
        Convert FuturesLimitDelete to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'trdaccid': self.trd_acc_id,
            'limit_type': self.limit_type
        }
    
    def to_json(self) -> str:
        """
        Convert FuturesLimitDelete to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
