"""
MoneyLimitDelete class - удаление денежного лимита
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

from quik_python.data_structures.depo_limit_ex import LimitKind
from .base import BaseDataStructure


@dataclass
class MoneyLimitDelete(BaseDataStructure):
    """
    При удалении клиентского лимита по бумагам функция возвращает таблицу Lua с параметрами
    
    Используется для получения информации об удалении денежных лимитов клиента.
    """
    
    # Код валюты
    curr_code: Optional[str] = None
    
    # Тэг расчетов
    tag: Optional[str] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Тип лимита (0 - обычные, иначе - технологические)
    limit_kind: Optional[LimitKind] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MoneyLimitDelete':
        """
        Create MoneyLimitDelete from dictionary
        
        Args:
            data: Dictionary with money limit delete data
            
        Returns:
            MoneyLimitDelete instance
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
            client_code=data.get('client_code'),
            firm_id=data.get('firmid'),
            limit_kind=limit_kind
        )
    
    def to_dict(self) -> dict:
        """
        Convert MoneyLimitDelete to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'currcode': self.curr_code,
            'tag': self.tag,
            'client_code': self.client_code,
            'firmid': self.firm_id,
            'limit_kind': self.limit_kind.value if self.limit_kind is not None else 0
        }
    
    def to_json(self) -> str:
        """
        Convert MoneyLimitDelete to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()

