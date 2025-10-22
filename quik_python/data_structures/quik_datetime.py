"""
DateTime data structure for QUIK
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .base import BaseDataStructure


@dataclass
class QuikDateTime(BaseDataStructure):
    """
    Формат даты и времени, используемый таблицах.
    Для корректного отображения даты и времени все параметры должны быть заданы.
    """
    
    # Микросекунды игнорируются в текущей версии
    mcs: Optional[int] = None
    
    # Миллисекунды
    ms: Optional[int] = None
    
    # Секунды
    sec: Optional[int] = None
    
    # Минуты
    min: Optional[int] = None
    
    # Час
    hour: Optional[int] = None
    
    # День
    day: Optional[int] = None
    
    # День недели (понедельник = 1, воскресенье = 7)
    week_day: Optional[int] = None
    
    # Месяц
    month: Optional[int] = None
    
    # Год
    year: Optional[int] = None
    
    def to_datetime(self) -> Optional[datetime]:
        """
        Конвертирует в Python datetime объект
        """
        if not all([self.year, self.month, self.day]):
            return None
            
        dt = datetime(
            year=self.year or 1900,
            month=self.month or 1,
            day=self.day or 1,
            hour=self.hour or 0,
            minute=self.min or 0,
            second=self.sec or 0,
            microsecond=(self.mcs or self.ms * 1000 or 0) if self.mcs or self.ms else 0
        )
        return dt
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> 'QuikDateTime':
        """
        Создает QuikDateTime из Python datetime объекта
        """
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            min=dt.minute,
            sec=dt.second,
            ms=dt.microsecond // 1000,
            mcs=dt.microsecond,
            week_day=7 if dt.weekday() == 6 else dt.weekday() + 1  # Python: 0=Monday, QUIK: 1=Monday, 7=Sunday
        )

    def __str__(self) -> str:
        """String representation"""
        return str(self.to_datetime())
