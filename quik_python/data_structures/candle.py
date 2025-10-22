"""
Candle data structures
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .base import BaseDataStructure
from .quik_datetime import QuikDateTime
#OK


class CandleInterval(Enum):
    """
    Интервал запрашиваемого графика
    """
    # Тиковые данные
    TICK = 0
    
    # Минуты
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4
    M5 = 5
    M6 = 6
    M10 = 10
    M15 = 15
    M20 = 20
    M30 = 30
    
    # Часы
    H1 = 60
    H2 = 120
    H4 = 240
    
    # Дни
    D1 = 1440
    
    # Недели
    W1 = 10080
    
    # Месяц
    MN = 23200


@dataclass
class Candle(BaseDataStructure):
    """
    Свеча
    """
    
    # Минимальная цена сделки
    low: Optional[float] = None
    
    # Цена закрытия
    close: Optional[float] = None
    
    # Максимальная цена сделки
    high: Optional[float] = None
    
    # Цена открытия
    open: Optional[float] = None
    
    # Объем последней сделки
    volume: Optional[float] = None
    
    # Дата и время
    datetime: Optional[QuikDateTime] = None
    
    # Информация о принадлежности свечки к одной из подписок
    
    # Код инструмента
    sec_code: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None  # class - зарезервированное слово в Python
    
    # Интервал подписки
    interval: Optional[CandleInterval] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Candle':
        """
        Create Candle from dictionary
        
        Args:
            data: Dictionary containing candle data
            
        Returns:
            Candle instance
        """
        return cls(
            low=data.get('low'),
            close=data.get('close'),
            high=data.get('high'),
            open=data.get('open'),
            volume=data.get('volume'),
            datetime=QuikDateTime.from_dict(data['datetime']) if data.get('datetime') else None,
            sec_code=data.get('sec'),
            class_code=data.get('class'),
            interval=CandleInterval(data['interval']) if data.get('interval') is not None else None
        )
    
    def to_dict(self) -> dict:
        """
        Convert Candle to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'low': self.low,
            'close': self.close,
            'high': self.high,
            'open': self.open,
            'volume': self.volume,
            'datetime': self.datetime.to_dict() if self.datetime else None,
            'sec': self.sec_code,
            'class': self.class_code,
            'interval': self.interval.value if self.interval is not None else None
        }
    
    def to_json(self) -> str:
        """
        Convert Candle to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        return f"Open: {self.open}, Close: {self.close}, High: {self.high}, Low: {self.low}, Volume: {self.volume}"
