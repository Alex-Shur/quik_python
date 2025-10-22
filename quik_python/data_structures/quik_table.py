"""
QuikTable class - таблицы, используемые в функциях QUIK API
"""

from dataclasses import dataclass
from typing import Optional
import json
from .base import BaseDataStructure


@dataclass
class QuikTable(BaseDataStructure):
    """
    Таблицы, используемые в функциях «getItem», «getOrderByNumber», «getNumberOf» и «SearchItems»
    """
    
    # Фирмы
    firms: Optional[str] = None
    
    # Классы
    classes: Optional[str] = None
    
    # Инструменты
    securities: Optional[str] = None
    
    # Торговые счета
    trade_accounts: Optional[str] = None
    
    # Коды клиентов
    # - функция getNumberOf("client_codes") возвращает количество доступных кодов клиента в терминале, а функция getItem("client_codes", i) - строку содержащую клиентский код с индексом i, где i может принимать значения от 0 до getNumberOf("client_codes") -1
    client_codes: Optional[str] = None
    
    # Обезличенные сделки
    all_trades: Optional[str] = None
    
    # Денежные позиции
    account_positions: Optional[str] = None
    
    # Заявки
    orders: Optional[str] = None
    
    # Позиции по клиентским счетам (фьючерсы)
    futures_client_holding: Optional[str] = None
    
    # Лимиты по фьючерсам
    futures_client_limits: Optional[str] = None
    
    # Лимиты по денежным средствам
    money_limits: Optional[str] = None
    
    # Лимиты по бумагам
    depo_limits: Optional[str] = None
    
    # Сделки
    trades: Optional[str] = None
    
    # Стоп-заявки
    stop_orders: Optional[str] = None
    
    # Заявки на внебиржевые сделки
    neg_deals: Optional[str] = None
    
    # Сделки для исполнения
    neg_trades: Optional[str] = None
    
    # Отчеты по сделкам для исполнения
    neg_deal_reports: Optional[str] = None
    
    # Текущие позиции по бумагам
    firm_holding: Optional[str] = None
    
    # Текущие позиции клиентским счетам
    account_balance: Optional[str] = None
    
    # Обязательства и требования по деньгам
    ccp_positions: Optional[str] = None
    
    # Обязательства и требования по активам
    ccp_holdings: Optional[str] = None

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'QuikTable':
        """Создание объекта из словаря с маппингом полей"""
        return cls(
            firms=data.get('firms'),
            classes=data.get('classes'),
            securities=data.get('securities'),
            trade_accounts=data.get('trade_accounts'),
            client_codes=data.get('client_codes'),
            all_trades=data.get('all_trades'),
            account_positions=data.get('account_positions'),
            orders=data.get('orders'),
            futures_client_holding=data.get('futures_client_holding'),
            futures_client_limits=data.get('futures_client_limits'),
            money_limits=data.get('money_limits'),
            depo_limits=data.get('depo_limits'),
            trades=data.get('trades'),
            stop_orders=data.get('stop_orders'),
            neg_deals=data.get('neg_deals'),
            neg_trades=data.get('neg_trades'),
            neg_deal_reports=data.get('neg_deal_reports'),
            firm_holding=data.get('firm_holding'),
            account_balance=data.get('account_balance'),
            ccp_positions=data.get('ccp_positions'),
            ccp_holdings=data.get('ccp_holdings')
        )

    def to_dict(self) -> dict:
        """Преобразование в словарь с именами полей C#"""
        return {
            'firms': self.firms,
            'classes': self.classes,
            'securities': self.securities,
            'trade_accounts': self.trade_accounts,
            'client_codes': self.client_codes,
            'all_trades': self.all_trades,
            'account_positions': self.account_positions,
            'orders': self.orders,
            'futures_client_holding': self.futures_client_holding,
            'futures_client_limits': self.futures_client_limits,
            'money_limits': self.money_limits,
            'depo_limits': self.depo_limits,
            'trades': self.trades,
            'stop_orders': self.stop_orders,
            'neg_deals': self.neg_deals,
            'neg_trades': self.neg_trades,
            'neg_deal_reports': self.neg_deal_reports,
            'firm_holding': self.firm_holding,
            'account_balance': self.account_balance,
            'ccp_positions': self.ccp_positions,
            'ccp_holdings': self.ccp_holdings
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
