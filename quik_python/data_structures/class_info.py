"""
Class information data structure for QUIK
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class ClassInfo(BaseDataStructure):
    """
    Описание класса
    """
    
    # Код фирмы
    firm_id: Optional[str] = None
    
    # Наименование класса
    name: Optional[str] = None
    
    # Код класса
    code: Optional[str] = None
    
    # Количество параметров в классе
    n_pars: Optional[int] = None
    
    # Количество бумаг в классе
    n_secs: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ClassInfo':
        """
        Create ClassInfo from dictionary
        
        Args:
            data: Dictionary with class info data
            
        Returns:
            ClassInfo instance
        """
        return cls(
            firm_id=data.get('firmid'),
            name=data.get('name'),
            code=data.get('code'),
            n_pars=data.get('npars'),
            n_secs=data.get('nsecs')
        )
    
    def to_dict(self) -> dict:
        """
        Convert ClassInfo to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'name': self.name,
            'code': self.code,
            'npars': self.n_pars,
            'nsecs': self.n_secs
        }
    
    def to_json(self) -> str:
        """
        Convert ClassInfo to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
