"""
Trade accounts data structure for QUIK
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure
#OK+


@dataclass
class TradeAccounts(BaseDataStructure):
    """
    Торговые счета - результат getTradeAccounts
    """
    
    # Описание
    description: Optional[str] = None
    
    # Список кодов классов, разделенных символом «|»
    class_codes: Optional[str] = None
    
    # Запрет необеспеченных продаж
    # «0» – Нет;
    # «1» – Да
    fullcovered_sell: Optional[int] = None
    
    # Номер основного торгового счета
    main_trd_acc_id: Optional[str] = None
    
    # Расчетная организация по «Т+»
    bankid_tplus: Optional[str] = None
    
    # Тип депозитарного счета
    trd_acc_type: Optional[int] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Раздел счета Депо
    dep_unit_id: Optional[str] = None
    
    # Расчетная организация по «Т0»
    bankid_t0: Optional[str] = None
    
    # Тип раздела 
    # «0» – раздел обеспечения;
    # иначе – для торговых разделов
    firm_use: Optional[int] = None
    
    # Статус торгового счета
    # «0» – операции разрешены;
    # «1» – операции запрещены
    status: Optional[int] = None
    
    # Номер счета депо в депозитарии
    dep_acc_id: Optional[str] = None
    
    # Код торгового счета
    trd_acc_id: Optional[str] = None
    
    # Код дополнительной позиции по денежным средствам
    bank_acc_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TradeAccounts':
        """
        Create TradeAccounts from dictionary
        
        Args:
            data: Dictionary with trade accounts data from QUIK
            
        Returns:
            TradeAccounts instance
        """
        return cls(
            description=data.get('description'),
            class_codes=data.get('class_codes'),
            fullcovered_sell=data.get('fullcoveredsell'),
            main_trd_acc_id=data.get('main_trdaccid'),
            bankid_tplus=data.get('bankid_tplus'),
            trd_acc_type=data.get('trdacc_type'),
            firm_id=data.get('firmid'),
            dep_unit_id=data.get('depunitid'),
            bankid_t0=data.get('bankid_t0'),
            firm_use=data.get('firmuse'),
            status=data.get('status'),
            dep_acc_id=data.get('depaccid'),
            trd_acc_id=data.get('trdaccid'),
            bank_acc_id=data.get('bank_acc_id')
        )
    
    def to_dict(self) -> dict:
        """
        Convert TradeAccounts to dictionary
        
        Returns:
            Dictionary representation with original JSON keys
        """
        return {
            'description': self.description,
            'class_codes': self.class_codes,
            'fullcoveredsell': self.fullcovered_sell,
            'main_trdaccid': self.main_trd_acc_id,
            'bankid_tplus': self.bankid_tplus,
            'trdacc_type': self.trd_acc_type,
            'firmid': self.firm_id,
            'depunitid': self.dep_unit_id,
            'bankid_t0': self.bankid_t0,
            'firmuse': self.firm_use,
            'status': self.status,
            'depaccid': self.dep_acc_id,
            'trdaccid': self.trd_acc_id,
            'bank_acc_id': self.bank_acc_id
        }
    
    def to_json(self) -> str:
        """
        Convert TradeAccounts to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
    
    @property
    def is_operations_allowed(self) -> bool:
        """
        Проверить, разрешены ли операции по торговому счету
        
        Returns:
            True если операции разрешены, False иначе
        """
        return self.status == 0
    
    @property
    def is_short_selling_prohibited(self) -> bool:
        """
        Проверить, запрещены ли необеспеченные продажи
        
        Returns:
            True если необеспеченные продажи запрещены, False иначе
        """
        return self.fullcovered_sell == 1
    
    @property
    def is_guarantee_section(self) -> bool:
        """
        Проверить, является ли раздел разделом обеспечения
        
        Returns:
            True если раздел обеспечения, False если торговый раздел
        """
        return self.firm_use == 0
    
    def get_class_codes_list(self) -> list[str]:
        """
        Получить список кодов классов как список строк
        
        Returns:
            Список кодов классов
        """
        if not self.class_codes:
            return []
        return [code.strip() for code in self.class_codes.split('|') if code.strip()]
