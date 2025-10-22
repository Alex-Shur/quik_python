"""
OptionBoard class - опционная доска
"""

from dataclasses import dataclass
from typing import Optional
import json
from .base import BaseDataStructure


@dataclass
class OptionBoard(BaseDataStructure):
    """
    Опционная доска
    
    Представляет информацию об опционе на опционной доске,
    включая страйк, волатильность, цены бид/оффер и другие параметры.
    """
    
    # Страйк опциона
    strike: Optional[float] = None
    
    # Код инструмента
    code: Optional[str] = None
    
    # Волатильность
    volatility: Optional[float] = None
    
    # Базовый актив опциона
    optionbase: Optional[str] = None
    
    # Цена предложения (оффер)
    offer: Optional[float] = None
    
    # Полное наименование
    longname: Optional[str] = None
    
    # Наименование
    name: Optional[str] = None
    
    # Тип опциона
    optiontype: Optional[str] = None
    
    # Краткое наименование
    shortname: Optional[str] = None
    
    # Цена спроса (бид)
    bid: Optional[float] = None
    
    # Дни до экспирации
    days_to_mat_date: Optional[int] = None

    # Совместимость с C# API (свойства в стиле C#)
    @classmethod
    def from_dict(cls, data: dict) -> 'OptionBoard':
        """Создание объекта из словаря с маппингом полей"""
        return cls(
            strike=data.get('Strike'),
            code=data.get('code'),
            volatility=data.get('Volatility'),
            optionbase=data.get('OPTIONBASE'),
            offer=data.get('OFFER'),
            longname=data.get('Longname'),
            name=data.get('Name'),
            optiontype=data.get('OPTIONTYPE'),
            shortname=data.get('shortname'),
            bid=data.get('BID'),
            days_to_mat_date=data.get('DAYS_TO_MAT_DATE')
        )

    def to_dict(self) -> dict:
        """Преобразование в словарь с именами полей C#"""
        return {
            'Strike': self.strike,
            'code': self.code,
            'Volatility': self.volatility,
            'OPTIONBASE': self.optionbase,
            'OFFER': self.offer,
            'Longname': self.longname,
            'Name': self.name,
            'OPTIONTYPE': self.optiontype,
            'shortname': self.shortname,
            'BID': self.bid,
            'DAYS_TO_MAT_DATE': self.days_to_mat_date
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
