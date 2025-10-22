"""
Модель котировки - порт класса Quote из C#
"""

from dataclasses import dataclass


@dataclass
class Quote:
    """
    Котировка для стакана заявок
    """
    
    # Тип котировки (offer/bid)
    type: str
    
    # Индекс записи в таблице
    index: int
    
    # Количество
    qty: int
    
    # Цена
    price: float

    def __init__(self, quote_type: str = "", index: int = 0, qty: int = 0, price: float = 0.0):
        """
        Инициализация котировки
        
        Args:
            quote_type: Тип котировки (offer/bid)
            index: Индекс записи в таблице
            qty: Количество
            price: Цена
        """
        self.type = quote_type
        self.index = index
        self.qty = qty
        self.price = price
