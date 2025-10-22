"""
ParamTable class - таблица с параметрами для функции getParamEx
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import json
from .base import BaseDataStructure


class ParamType(Enum):
    """
    Тип данных параметра в Таблице текущих значений параметров
    """

    DOUBLE = "1"

    LONG = "2"

    CHAR = "3"

    ENUM = "4"

    TIME = "5"

    DATE = "6"


class ParamResult(Enum):
    """
    Результат выполнения операции getParamEx
    """

    # ошибка
    ERROR = "0"

    # параметр найден
    FOUND = "1"


@dataclass
class ParamTable(BaseDataStructure):
    """
    Таблица с параметрами для функции getParamEx
    
    Представляет результат запроса параметра инструмента через QUIK API,
    включая тип данных, значение и строковое представление параметра.
    """
    
    # Тип данных параметра
    param_type: Optional[str] = None
    
    # Значение параметра
    param_value: Optional[str] = None
    
    # Строковое значение параметра
    param_image: Optional[str] = None
    
    # Результат выполнения операции
    result: Optional[str] = None
    
    # time in msec from lua epoch
    lua_timestamp: Optional[int] = None

    # Методы проверки типа данных
    def is_double(self) -> bool:
        """Проверить, является ли параметр типом DOUBLE"""
        return self.param_type == ParamType.DOUBLE.value

    def is_long(self) -> bool:
        """Проверить, является ли параметр типом LONG"""
        return self.param_type == ParamType.LONG.value

    def is_char(self) -> bool:
        """Проверить, является ли параметр типом CHAR"""
        return self.param_type == ParamType.CHAR.value

    def is_enum(self) -> bool:
        """Проверить, является ли параметр перечислимым типом"""
        return self.param_type == ParamType.ENUM.value

    def is_time(self) -> bool:
        """Проверить, является ли параметр типом TIME"""
        return self.param_type == ParamType.TIME.value

    def is_date(self) -> bool:
        """Проверить, является ли параметр типом DATE"""
        return self.param_type == ParamType.DATE.value

    # Методы преобразования значений
    def get_numeric_value(self) -> Optional[float]:
        """Получить числовое значение параметра"""
        if not self.param_value:
            return None
        
        try:
            if self.is_double() or self.is_long():
                return float(self.param_value)
            elif self.is_enum():
                return float(self.param_value)  # порядковое значение
            else:
                return None
        except (ValueError, TypeError):
            return None

    def get_integer_value(self) -> Optional[int]:
        """Получить целочисленное значение параметра"""
        numeric = self.get_numeric_value()
        if numeric is not None:
            try:
                return int(numeric)
            except (ValueError, TypeError):
                return None
        return None

    def get_string_value(self) -> str:
        """Получить строковое значение (param_image или param_value)"""
        return self.param_image or self.param_value or ""

