"""
Security information data structure
"""

from dataclasses import dataclass
from typing import Optional
from .base import BaseDataStructure


@dataclass
class SecurityInfo(BaseDataStructure):
    """
    Результат getSecurityInfo
    """
    
    # Код инструмента (устаревший параметр?)
    sec_code: Optional[str] = None
    
    # Код инструмента
    code: Optional[str] = None
    
    # Наименование инструмента
    name: Optional[str] = None
    
    # Краткое наименование
    short_name: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None
    
    # Наименование класса
    class_name: Optional[str] = None
    
    # Номинал
    face_value: Optional[str] = None
    
    # Код валюты номинала
    face_unit: Optional[str] = None
    
    # Количество значащих цифр после запятой
    scale: Optional[int] = None
    
    # Дата погашения (YYYYMMDD)
    mat_date: Optional[str] = None
    
    # Размер лота
    lot_size: Optional[int] = None
    
    # ISIN-код
    isin_code: Optional[str] = None
    
    # Минимальный шаг цены
    min_price_step: Optional[float] = None
    
    # Bloomberg ID
    bsid: Optional[str] = None
    
    # CUSIP
    cusip_code: Optional[str] = None
    
    # StockCode
    stock_code: Optional[str] = None
    
    # Размер купона
    couponvalue: Optional[float] = None
    
    # Код котируемой валюты в паре
    first_currcode: Optional[str] = None
    
    # Код базовой валюты в паре
    second_currcode: Optional[str] = None
    
    # Код класса базового актива
    base_active_classcode: Optional[str] = None
    
    # Базовый актив
    base_active_seccode: Optional[str] = None
    
    # Страйк опциона
    option_strike: Optional[float] = None
    
    # Кратность при вводе количества
    qty_multiplier: Optional[float] = None
    
    # Валюта шага цены
    step_price_currency: Optional[str] = None
    
    # SEDOL
    sedol_code: Optional[str] = None
    
    # CFI
    cfi_code: Optional[str] = None
    
    # RIC
    ric_code: Optional[str] = None
    
    # Дата оферты (YYYYMMDD)
    buybackdate: Optional[int] = None
    
    # Цена оферты
    buybackprice: Optional[float] = None
    
    # Уровень листинга
    list_level: Optional[int] = None
    
    # Точность количества
    qty_scale: Optional[int] = None
    
    # Доходность по предыдущей оценке
    yieldatprevwaprice: Optional[float] = None
    
    # Регистрационный номер
    regnumber: Optional[str] = None
    
    # Валюта торгов
    trade_currency: Optional[str] = None
    
    # Точность количества котируемой валюты
    second_curr_qty_scale: Optional[int] = None
    
    # Точность количества базовой валюты
    first_curr_qty_scale: Optional[int] = None
    
    # Накопленный купонный доход
    accruedint: Optional[float] = None
    
    # Код деривативного контракта в формате QUIK
    stock_name: Optional[str] = None
    
    # Дата выплаты купона (YYYYMMDD)
    nextcoupon: Optional[int] = None
    
    # Длительность купона
    couponperiod: Optional[int] = None
    
    # Текущий код расчетов для инструмента
    settlecode: Optional[str] = None
    
    # Дата экспирации (YYYYMMDD)
    exp_date: Optional[int] = None
    
    # Дата расчетов (YYYYMMDD)
    settle_date: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SecurityInfo':
        """
        Create SecurityInfo from dictionary
        
        Args:
            data: Dictionary with security info data from QUIK
            
        Returns:
            SecurityInfo instance
        """
        return cls(
            sec_code=data.get('sec_code'),
            code=data.get('code'),
            name=data.get('name'),
            short_name=data.get('short_name'),
            class_code=data.get('class_code'),
            class_name=data.get('class_name'),
            face_value=data.get('face_value'),
            face_unit=data.get('face_unit'),
            scale=data.get('scale'),
            mat_date=data.get('mat_date'),
            lot_size=data.get('lot_size'),
            isin_code=data.get('isin_code'),
            min_price_step=data.get('min_price_step'),
            bsid=data.get('bsid'),
            cusip_code=data.get('cusip_code'),
            stock_code=data.get('stock_code'),
            couponvalue=data.get('couponvalue'),
            first_currcode=data.get('first_currcode'),
            second_currcode=data.get('second_currcode'),
            base_active_classcode=data.get('base_active_classcode'),
            base_active_seccode=data.get('base_active_seccode'),
            option_strike=data.get('option_strike'),
            qty_multiplier=data.get('qty_multiplier'),
            step_price_currency=data.get('step_price_currency'),
            sedol_code=data.get('sedol_code'),
            cfi_code=data.get('cfi_code'),
            ric_code=data.get('ric_code'),
            buybackdate=data.get('buybackdate'),
            buybackprice=data.get('buybackprice'),
            list_level=data.get('list_level'),
            qty_scale=data.get('qty_scale'),
            yieldatprevwaprice=data.get('yieldatprevwaprice'),
            regnumber=data.get('regnumber'),
            trade_currency=data.get('trade_currency'),
            second_curr_qty_scale=data.get('second_curr_qty_scale'),
            first_curr_qty_scale=data.get('first_curr_qty_scale'),
            accruedint=data.get('accruedint'),
            stock_name=data.get('stock_name'),
            nextcoupon=data.get('nextcoupon'),
            couponperiod=data.get('couponperiod'),
            settlecode=data.get('settlecode'),
            exp_date=data.get('exp_date'),
            settle_date=data.get('settle_date')
        )
    
    def to_dict(self) -> dict:
        """
        Convert SecurityInfo to dictionary
        
        Returns:
            Dictionary representation with original JSON keys
        """
        return {
            'sec_code': self.sec_code,
            'code': self.code,
            'name': self.name,
            'short_name': self.short_name,
            'class_code': self.class_code,
            'class_name': self.class_name,
            'face_value': self.face_value,
            'face_unit': self.face_unit,
            'scale': self.scale,
            'mat_date': self.mat_date,
            'lot_size': self.lot_size,
            'isin_code': self.isin_code,
            'min_price_step': self.min_price_step,
            'bsid': self.bsid,
            'cusip_code': self.cusip_code,
            'stock_code': self.stock_code,
            'couponvalue': self.couponvalue,
            'first_currcode': self.first_currcode,
            'second_currcode': self.second_currcode,
            'base_active_classcode': self.base_active_classcode,
            'base_active_seccode': self.base_active_seccode,
            'option_strike': self.option_strike,
            'qty_multiplier': self.qty_multiplier,
            'step_price_currency': self.step_price_currency,
            'sedol_code': self.sedol_code,
            'cfi_code': self.cfi_code,
            'ric_code': self.ric_code,
            'buybackdate': self.buybackdate,
            'buybackprice': self.buybackprice,
            'list_level': self.list_level,
            'qty_scale': self.qty_scale,
            'yieldatprevwaprice': self.yieldatprevwaprice,
            'regnumber': self.regnumber,
            'trade_currency': self.trade_currency,
            'second_curr_qty_scale': self.second_curr_qty_scale,
            'first_curr_qty_scale': self.first_curr_qty_scale,
            'accruedint': self.accruedint,
            'stock_name': self.stock_name,
            'nextcoupon': self.nextcoupon,
            'couponperiod': self.couponperiod,
            'settlecode': self.settlecode,
            'exp_date': self.exp_date,
            'settle_date': self.settle_date
        }
    
    def to_json(self) -> str:
        """
        Convert SecurityInfo to JSON string
        
        Returns:
            JSON string representation
        """
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
