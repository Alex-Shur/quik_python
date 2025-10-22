"""
FuturesClientHolding class - позиции по клиентским счетам (фьючерсы)
"""

import json
from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class FuturesClientHolding(BaseDataStructure):
    """
    Описание параметров Таблицы позиций по клиентским счетам (фьючерсы)
    
    Используется для получения информации о позициях клиентов по фьючерсным контрактам
    """
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Торговый счет
    trd_acc_id: Optional[str] = None
    
    # Код фьючерсного контракта
    sec_code: Optional[str] = None
    
    # Тип лимита
    # Возможные значения:
    # «Основной счет»;
    # «Клиентские и дополнительные счета»;
    # «Все счета торг. членов»;
    type: Optional[str] = None
    
    # Входящие длинные позиции
    start_buy: Optional[float] = None
    
    # Входящие короткие позиции
    start_sell: Optional[float] = None
    
    # Входящие чистые позиции
    start_net: Optional[float] = None
    
    # Текущие длинные позиции
    today_buy: Optional[float] = None
    
    # Текущие короткие позиции
    today_sell: Optional[float] = None
    
    # Текущие чистые позиции
    total_net: Optional[float] = None
    
    # Активные на покупку
    open_buys: Optional[float] = None
    
    # Активные на продажу
    open_sells: Optional[float] = None
    
    # Оценка текущих чистых позиций
    cbp_l_used: Optional[float] = None
    
    # Плановые чистые позиции
    cbp_l_planned: Optional[float] = None
    
    # Вариационная маржа
    var_margin: Optional[float] = None
    
    # Эффективная цена позиций
    avr_pos_nprice: Optional[float] = None
    
    # Стоимость позиций
    position_value: Optional[float] = None
    
    # Реально начисленная в ходе клиринга вариационная маржа
    # Отображается с точностью до 2 двух знаков.
    # При этом, в поле «var_margin» транслируется вариационная маржа, 
    # рассчитанная с учетом установленных границ изменения цены
    real_var_margin: Optional[float] = None
    
    # Суммарная вариационная маржа по итогам основного клиринга 
    # начисленная по всем позициям.
    # Отображается с точностью до 2 двух знаков
    total_var_margin: Optional[float] = None
    
    # Актуальный статус торговой сессии
    # Возможные значения: 
    # «0» – не определено; 
    # «1» – основная сессия; 
    # «2» – начался промклиринг; 
    # «3» – завершился промклиринг; 
    # «4» – начался основной клиринг; 
    # «5» – основной клиринг: новая сессия назначена; 
    # «6» – завершился основной клиринг; 
    # «7» – завершилась вечерняя сессия
    session_status: Optional[int] = None
    
    # Временная метка Lua
    lua_timestamp: Optional[int] = None
    
    
    def get_session_status(self) -> int:
        """Получить статус торговой сессии"""
        return self.session_status or 0
    
    def get_session_status_description(self) -> str:
        """Получить описание статуса сессии"""
        status_map = {
            0: "Не определено",
            1: "Основная сессия",
            2: "Начался промклиринг",
            3: "Завершился промклиринг",
            4: "Начался основной клиринг",
            5: "Основной клиринг: новая сессия назначена",
            6: "Завершился основной клиринг",
            7: "Завершилась вечерняя сессия"
        }
        return status_map.get(self.get_session_status(), f"Неизвестный статус ({self.get_session_status()})")
    
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FuturesClientHolding':
        """
        Create FuturesClientHolding from dictionary
        
        Args:
            data: Dictionary with futures client holding data
            
        Returns:
            FuturesClientHolding instance
        """
        return cls(
            firm_id=data.get('firmid'),
            trd_acc_id=data.get('trdaccid'),
            sec_code=data.get('sec_code'),
            type=data.get('type'),
            start_buy=data.get('startbuy'),
            start_sell=data.get('startsell'),
            start_net=data.get('startnet'),
            today_buy=data.get('todaybuy'),
            today_sell=data.get('todaysell'),
            total_net=data.get('totalnet'),
            open_buys=data.get('openbuys'),
            open_sells=data.get('opensells'),
            cbp_l_used=data.get('cbplused'),
            cbp_l_planned=data.get('cbplplanned'),
            var_margin=data.get('varmargin'),
            avr_pos_nprice=data.get('avrposnprice'),
            position_value=data.get('positionvalue'),
            real_var_margin=data.get('real_varmargin'),
            total_var_margin=data.get('total_varmargin'),
            session_status=data.get('session_status'),
            lua_timestamp=data.get('lua_timestamp')
        )
    
    def to_dict(self) -> dict:
        """
        Convert FuturesClientHolding to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'trdaccid': self.trd_acc_id,
            'sec_code': self.sec_code,
            'type': self.type,
            'startbuy': self.start_buy,
            'startsell': self.start_sell,
            'startnet': self.start_net,
            'todaybuy': self.today_buy,
            'todaysell': self.today_sell,
            'totalnet': self.total_net,
            'openbuys': self.open_buys,
            'opensells': self.open_sells,
            'cbplused': self.cbp_l_used,
            'cbplplanned': self.cbp_l_planned,
            'varmargin': self.var_margin,
            'avrposnprice': self.avr_pos_nprice,
            'positionvalue': self.position_value,
            'real_varmargin': self.real_var_margin,
            'total_varmargin': self.total_var_margin,
            'session_status': self.session_status,
            'lua_timestamp': self.lua_timestamp
        }
    
    def to_json(self) -> str:
        """
        Convert FuturesClientHolding to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
