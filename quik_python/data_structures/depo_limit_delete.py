"""
DepoLimitDelete class - параметры при удалении бумажного лимита
"""

import json
from dataclasses import dataclass
from typing import Optional

from quik_python.data_structures.depo_limit_ex import LimitKind
from .base import BaseDataStructure


@dataclass
class DepoLimitDelete(BaseDataStructure):
    """
    При обработке удаления бумажного лимита функция возвращает таблицу Lua с параметрами
    """
    
    # Код инструмента
    sec_code: Optional[str] = None
    
    # Код торгового счета
    trd_acc_id: Optional[str] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Тип лимита. Возможные значения:
    # «0» – обычные лимиты,
    # значение не равное «0» – технологические лимиты
    limit_kind: Optional[LimitKind] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DepoLimitDelete':
        """
        Create DepoLimitDelete from dictionary
        
        Args:
            data: Dictionary with depo limit delete data
            
        Returns:
            DepoLimitDelete instance
        """
        limit_kind = LimitKind.T0
        limit = data.get('limit_kind')
        if limit:
            if limit in LimitKind._value2member_map_:
                limit_kind = LimitKind(limit)
            else:
                limit_kind = LimitKind.NOT_IMPLEMENTED

        return cls(
            sec_code=data.get('sec_code'),
            trd_acc_id=data.get('trdaccid'),
            firm_id=data.get('firmid'),
            client_code=data.get('client_code'),
            limit_kind=limit_kind
        )
    
    def to_dict(self) -> dict:
        """
        Convert DepoLimitDelete to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'sec_code': self.sec_code,
            'trdaccid': self.trd_acc_id,
            'firmid': self.firm_id,
            'client_code': self.client_code,
            'limit_kind': self.limit_kind.value if self.limit_kind is not None else 0
        }
    
    def to_json(self) -> str:
        """
        Convert DepoLimitDelete to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
