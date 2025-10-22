"""
DepoLimit class - информация о бумажном лимите
"""

from dataclasses import dataclass
from typing import Optional
# from decimal import Decimal
from .base import BaseDataStructure


@dataclass
class DepoLimit(BaseDataStructure):
    """
    При обработке изменения бумажного лимита функция возвращает таблицу Lua с параметрами
    """
    
    # Стоимость ценных бумаг, заблокированных на покупку
    depo_limit_locked_buy_value: Optional[float] = None
    
    # Текущий остаток по бумагам
    depo_current_balance: Optional[float] = None
    
    # Количество лотов ценных бумаг, заблокированных на покупку
    depo_limit_locked_buy: Optional[float] = None
    
    # Заблокированное количество лотов ценных бумаг
    depo_limit_locked: Optional[float] = None
    
    # Доступное количество ценных бумаг
    depo_limit_available: Optional[float] = None
    
    # Текущий лимит по бумагам
    depo_current_limit: Optional[float] = None
    
    # Входящий остаток по бумагам
    depo_open_balance: Optional[float] = None
    
    # Входящий лимит по инструментам
    depo_open_limit: Optional[float] = None
    
