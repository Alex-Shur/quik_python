"""
MoneyLimit class - денежный лимит
"""

from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class MoneyLimit(BaseDataStructure):
    """
    При обработке изменения денежного лимита функция getMoney возвращает таблицу Lua с параметрами
    
    Используется для получения информации о денежных лимитах и остатках клиента.
    """
    
    # Входящий лимит по денежным средствам
    money_open_limit: Optional[float] = None
    
    # Стоимость немаржинальных бумаг в заявках на покупку
    money_limit_locked_nonmarginal_value: Optional[float] = None
    
    # Заблокированное в заявках на покупку количество денежных средств
    money_limit_locked: Optional[float] = None
    
    # Входящий остаток по денежным средствам
    money_open_balance: Optional[float] = None
    
    # Текущий лимит по денежным средствам
    money_current_limit: Optional[float] = None
    
    # Текущий остаток по денежным средствам
    money_current_balance: Optional[float] = None
    
    # Доступное количество денежных средств
    money_limit_available: Optional[float] = None

