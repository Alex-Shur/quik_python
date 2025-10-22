"""
OrderBook class - стакан котировок
"""

from dataclasses import dataclass, field
from typing import Optional, List
import json
from .base import BaseDataStructure


@dataclass 
class PriceQuantity(BaseDataStructure):
    """
    Строка стакана - цена и количество
    """
    
    # Цена покупки / продажи
    price: Optional[float] = None
    
    # Количество в лотах
    quantity: Optional[float] = None


@dataclass
class OrderBook(BaseDataStructure):
    """
    Стакан котировок
    
    Представляет стакан заявок с котировками покупки и продажи,
    включая информацию о времени, коде инструмента и уровнях цен.
    """
    
    # Код класса
    class_code: Optional[str] = None
    
    # Код бумаги
    sec_code: Optional[str] = None
    
    # time in msec from lua epoch
    lua_timestamp: Optional[int] = None
    
    # Result of getInfoParam("SERVERTIME") right before getQuoteLevel2 call
    server_time: Optional[str] = None
    
    # Количество котировок покупки
    bid_count: Optional[float] = None
    
    # Количество котировок продажи
    offer_count: Optional[float] = None
    
    # Котировки спроса (покупки)
    bid: List[PriceQuantity] = field(default_factory=list)
    
    # Котировки предложений (продажи)
    offer: List[PriceQuantity] = field(default_factory=list)

    def get_bid_count(self) -> float:
        """Получить количество котировок покупки"""
        return self.bid_count if self.bid_count is not None else 0.0

    def get_offer_count(self) -> float:
        """Получить количество котировок продажи"""
        return self.offer_count if self.offer_count is not None else 0.0

    def get_bid(self) -> List[PriceQuantity]:
        """Получить котировки покупки"""
        return self.bid if self.bid is not None else []

    def get_offer(self) -> List[PriceQuantity]:
        """Получить котировки продажи"""
        return self.offer if self.offer is not None else []

    # Дополнительные методы для анализа стакана
    def get_best_bid(self) -> Optional[PriceQuantity]:
        """Получить лучшую цену покупки"""
        if not self.bid:
            return None
        return max(self.bid, key=lambda x: x.price)

    def get_best_offer(self) -> Optional[PriceQuantity]:
        """Получить лучшую цену продажи"""
        if not self.offer:
            return None
        return min(self.offer, key=lambda x: x.price)

    def get_spread(self) -> float:
        """Получить спред между лучшими ценами"""
        best_bid = self.get_best_bid()
        best_offer = self.get_best_offer()
        
        if best_bid and best_offer:
            return best_offer.price - best_bid.price
        return 0.0

    def get_mid_price(self) -> float:
        """Получить среднюю цену"""
        best_bid = self.get_best_bid()
        best_offer = self.get_best_offer()
        
        if best_bid and best_offer:
            return (best_bid.price + best_offer.price) / 2.0
        return 0.0

    def is_empty(self) -> bool:
        """Проверить, пустой ли стакан"""
        return len(self.bid) == 0 and len(self.offer) == 0

    def has_data(self) -> bool:
        """Проверить, есть ли данные в стакане"""
        return not self.is_empty()

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'OrderBook':
        """Создание объекта из словаря"""
        
        # Преобразование bid массива
        bid_data = data.get('bid', [])
        bid_list = []
        if bid_data:
            for item in bid_data:
                if isinstance(item, dict):
                    bid_list.append(PriceQuantity.from_dict(item))
                elif isinstance(item, PriceQuantity):
                    bid_list.append(item)
        
        # Преобразование offer массива
        offer_data = data.get('offer', [])
        offer_list = []
        if offer_data:
            for item in offer_data:
                if isinstance(item, dict):
                    offer_list.append(PriceQuantity.from_dict(item))
                elif isinstance(item, PriceQuantity):
                    offer_list.append(item)
        
        return cls(
            class_code=data.get('class_code'),
            sec_code=data.get('sec_code'),
            lua_timestamp=data.get('lua_timestamp'),
            server_time=data.get('server_time'),
            bid_count=data.get('bid_count'),
            offer_count=data.get('offer_count'),
            bid=bid_list,
            offer=offer_list
        )

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            'class_code': self.class_code,
            'sec_code': self.sec_code,
            'lua_timestamp': self.lua_timestamp,
            'server_time': self.server_time,
            'bid_count': self.bid_count,
            'offer_count': self.offer_count,
            'bid': [item.to_dict() for item in self.bid] if self.bid else [],
            'offer': [item.to_dict() for item in self.offer] if self.offer else []
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
