"""
FuturesLimits class - ограничения по срочному рынку
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum
from .base import BaseDataStructure


class FuturesLimitType(IntEnum):
    """Типы лимитов по срочному рынку"""
    
    # Денежные средства
    MONEY = 0
    
    # Залоговые денежные средства
    PLEDGE_MONEY = 1
    
    # Всего
    TOTAL = 2
    
    # Клиринговые рубли
    CLEARING_RUBLES = 3
    
    # Клиринговые залоговые рубли
    CLEARING_PLEDGE_RUBLES = 4
    
    # Лимит открытых позиций на спот-рынке
    SPOT_OPEN_POSITIONS_LIMIT = 5


class FuturesRiskLevel(IntEnum):
    """Уровни риска клиента"""
    
    # Не указан (по умолчанию)
    NOT_SPECIFIED = 0
    
    # КНУР (клиент с начальным уровнем риска)
    INITIAL = 1
    
    # КСУР (клиент со стандартным уровнем риска)
    STANDARD = 2
    
    # КПУР (клиент с повышенным уровнем риска)
    INCREASED = 3
    
    # КОУР (клиент с особым уровнем риска)
    SPECIAL = 4


@dataclass
class FuturesLimits(BaseDataStructure):
    """
    При получении изменений ограничений по срочному рынку функция возвращает таблицу Lua с параметрами
    
    Используется для получения информации об ограничениях по срочному рынку
    """
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Торговый счет
    trd_acc_id: Optional[str] = None
    
    # Тип лимита
    limit_type: Optional[FuturesLimitType] = None
    
    # Коэффициент ликвидности
    liquidity_coef: Optional[float] = None
    
    # Предыдущий лимит открытых позиций на спот-рынке
    cbp_prev_limit: Optional[float] = None
    
    # Лимит открытых позиций
    cbp_limit: Optional[float] = None
    
    # Текущие чистые позиции
    cbp_l_used: Optional[float] = None
    
    # Плановые чистые позиции
    cbp_l_planned: Optional[float] = None
    
    # Вариационная маржа
    var_margin: Optional[float] = None
    
    # Накопленный купонный доход
    accruedint: Optional[float] = None
    
    # Текущие чистые позиции (под заявки)
    cbp_l_used_for_orders: Optional[float] = None
    
    # Текущие чистые позиции (под открытые позиции)
    cbp_l_used_for_positions: Optional[float] = None
    
    # Премия по опционам
    options_premium: Optional[float] = None
    
    # Биржевые сборы
    ts_comission: Optional[float] = None
    
    # Коэффициент клиентского гарантийного обеспечения
    kgo: Optional[float] = None
    
    # Валюта, в которой транслируется ограничение
    curr_code: Optional[str] = None
    
    # Реально начисленная в ходе клиринга вариационная маржа
    real_var_margin: Optional[float] = None
    
    # Уровень риска клиента
    risk_level: Optional[FuturesRiskLevel] = None
    
    # Методы для работы с типами лимитов
    def get_limit_type_description(self) -> str:
        """Получить описание типа лимита"""
        if self.limit_type is None:
            return "Не указан"

        limit_type_map = {
            FuturesLimitType.MONEY: "Денежные средства",
            FuturesLimitType.PLEDGE_MONEY: "Залоговые денежные средства",
            FuturesLimitType.TOTAL: "Всего",
            FuturesLimitType.CLEARING_RUBLES: "Клиринговые рубли",
            FuturesLimitType.CLEARING_PLEDGE_RUBLES: "Клиринговые залоговые рубли",
            FuturesLimitType.SPOT_OPEN_POSITIONS_LIMIT: "Лимит открытых позиций на спот-рынке"
        }
        return limit_type_map.get(self.limit_type, f"Неизвестный тип ({self.limit_type})")

    # Методы для работы с уровнем риска
    def get_risk_level_description(self) -> str:
        """Получить описание уровня риска"""
        if self.risk_level is None:
            return "Не указан"

        risk_level_map = {
            FuturesRiskLevel.NOT_SPECIFIED: "Не указан",
            FuturesRiskLevel.INITIAL: "КНУР (начальный уровень риска)",
            FuturesRiskLevel.STANDARD: "КСУР (стандартный уровень риска)",
            FuturesRiskLevel.INCREASED: "КПУР (повышенный уровень риска)",
            FuturesRiskLevel.SPECIAL: "КОУР (особый уровень риска)"
        }
        return risk_level_map.get(self.risk_level, f"Неизвестный уровень ({self.risk_level})")

    @classmethod
    def from_dict(cls, data: dict) -> 'FuturesLimits':
        """
        Create FuturesLimits from dictionary

        Args:
            data: Dictionary with futures limits data

        Returns:
            FuturesLimits instance
        """

        return cls(
            firm_id=data.get('firmid'),
            trd_acc_id=data.get('trdaccid'),
            limit_type=FuturesLimitType(data.get('limit_type')) if data.get('limit_type') is not None else None,
            liquidity_coef=data.get('liquidity_coef'),
            cbp_prev_limit=data.get('cbp_prev_limit'),
            cbp_limit=data.get('cbplimit'),
            cbp_l_used=data.get('cbplused'),
            cbp_l_planned=data.get('cbplplanned'),
            var_margin=data.get('varmargin'),
            accruedint=data.get('accruedint'),
            cbp_l_used_for_orders=data.get('cbplused_for_orders'),
            cbp_l_used_for_positions=data.get('cbplused_for_positions'),
            options_premium=data.get('options_premium'),
            ts_comission=data.get('ts_comission'),
            kgo=data.get('kgo'),
            curr_code=data.get('currcode'),
            real_var_margin=data.get('real_varmargin'),
            risk_level=FuturesRiskLevel(data.get('risk_level')) if data.get('risk_level') is not None else None
        )

    def to_dict(self) -> dict:
        """
        Convert FuturesLimits to dictionary

        Returns:
            Dictionary representation
        """
        return {
            'firmid': self.firm_id,
            'trdaccid': self.trd_acc_id,
            'limit_type': self.limit_type.value if self.limit_type is not None else None,
            'liquidity_coef': self.liquidity_coef,
            'cbp_prev_limit': self.cbp_prev_limit,
            'cbplimit': self.cbp_limit,
            'cbplused': self.cbp_l_used,
            'cbplplanned': self.cbp_l_planned,
            'varmargin': self.var_margin,
            'accruedint': self.accruedint,
            'cbplused_for_orders': self.cbp_l_used_for_orders,
            'cbplused_for_positions': self.cbp_l_used_for_positions,
            'options_premium': self.options_premium,
            'ts_comission': self.ts_comission,
            'kgo': self.kgo,
            'currcode': self.curr_code,
            'real_varmargin': self.real_var_margin,
            'risk_level': self.risk_level.value if self.risk_level is not None else None
        }

    def to_json(self) -> str:
        """
        Convert FuturesLimits to JSON string

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __str__(self) -> str:
        """String representation"""
        return self.to_json()

