"""
PortfolioInfo class - параметры таблицы "Клиентский портфель"
"""

from dataclasses import dataclass
from typing import Optional
import json
from .base import BaseDataStructure


@dataclass
class PortfolioInfo(BaseDataStructure):
    """
    Параметры таблицы "Клиентский портфель"
    
    Соответствует идентификатору участника торгов «firmId» и коду клиента «clientCode»,
    возвращаемой функцией GetPortfolioInfo. Содержит подробную информацию о состоянии
    портфеля клиента, включая лимиты, активы, плечо и маржинальные показатели.
    """
    
    # Тип клиента
    is_leverage: Optional[str] = None
    
    # Вход. активы
    in_assets: Optional[str] = None
    
    # Плечо
    leverage: Optional[str] = None
    
    # Вход. лимит
    open_limit: Optional[str] = None
    
    # Шорты
    val_short: Optional[str] = None
    
    # Лонги
    val_long: Optional[str] = None
    
    # Лонги МО
    val_long_margin: Optional[str] = None
    
    # Лонги О
    val_long_asset: Optional[str] = None
    
    # Тек. активы
    assets: Optional[str] = None
    
    # Текущее плечо
    cur_leverage: Optional[str] = None
    
    # Ур. маржи
    margin: Optional[str] = None
    
    # Тек. лимит
    lim_all: Optional[str] = None
    
    # ДостТекЛимит
    av_lim_all: Optional[str] = None
    
    # Блок. покупка
    locked_buy: Optional[str] = None
    
    # Блок. пок. маржин.
    locked_buy_margin: Optional[str] = None
    
    # Блок.пок. обесп.
    locked_buy_asset: Optional[str] = None
    
    # Блок. продажа
    locked_sell: Optional[str] = None
    
    # Блок. пок. немарж.
    locked_value_coef: Optional[str] = None
    
    # ВходСредства
    in_all_assets: Optional[str] = None
    
    # ТекСредства
    all_assets: Optional[str] = None
    
    # Прибыль/убытки
    profit_loss: Optional[str] = None
    
    # ПроцИзмен
    rate_change: Optional[str] = None
    
    # На покупку
    lim_buy: Optional[str] = None
    
    # На продажу
    lim_sell: Optional[str] = None
    
    # НаПокупНеМаржин
    lim_non_margin: Optional[str] = None
    
    # НаПокупОбесп
    lim_buy_asset: Optional[str] = None
    
    # Шорты (нетто)
    val_short_net: Optional[str] = None
    
    # Сумма ден. остатков
    total_money_bal: Optional[str] = None
    
    # Суммарно заблок.
    total_locked_money: Optional[str] = None
    
    # Сумма дисконтов
    haircuts: Optional[str] = None
    
    # ТекАктБезДиск
    assets_without_hc: Optional[str] = None
    
    # Статус счета
    status_coef: Optional[str] = None
    
    # Вариац. маржа
    var_margin: Optional[str] = None
    
    # ГО поз.
    go_for_positions: Optional[str] = None
    
    # ГО заяв.
    go_for_orders: Optional[str] = None
    
    # Активы/ГО
    rate_futures: Optional[str] = None
    
    # ПовышУрРиска
    is_qual_client: Optional[str] = None
    
    # Сроч. счет
    is_futures: Optional[str] = None
    
    # Парам. расч.
    curr_tag: Optional[str] = None

    # Расчетные методы
    def get_total_position_value(self) -> Optional[float]:
        """Получить общую стоимость позиций"""
        val_long = self.get_numeric_value(self.val_long)
        val_short = self.get_numeric_value(self.val_short)
        
        if val_long is not None and val_short is not None:
            return val_long + val_short  # val_short отрицательное
        return None

    def get_available_margin(self) -> Optional[float]:
        """Получить доступную маржу"""
        lim_all = self.get_numeric_value(self.lim_all)
        av_lim_all = self.get_numeric_value(self.av_lim_all)
        
        if lim_all is not None and av_lim_all is not None:
            return av_lim_all
        return None

    def get_margin_ratio(self) -> Optional[float]:
        """Получить коэффициент маржи"""
        try:
            return float(self.margin) if self.margin else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def get_numeric_value(value: Optional[str]) -> Optional[float]:
        """Вспомогательный метод для преобразования строки в число"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'PortfolioInfo':
        """Создание объекта из словаря с маппингом полей"""
        return cls(
            is_leverage=data.get('is_leverage'),
            in_assets=data.get('in_assets'),
            leverage=data.get('leverage'),
            open_limit=data.get('open_limit'),
            val_short=data.get('val_short'),
            val_long=data.get('val_long'),
            val_long_margin=data.get('val_long_margin'),
            val_long_asset=data.get('val_long_asset'),
            assets=data.get('assets'),
            cur_leverage=data.get('cur_leverage'),
            margin=data.get('margin'),
            lim_all=data.get('lim_all'),
            av_lim_all=data.get('av_lim_all'),
            locked_buy=data.get('locked_buy'),
            locked_buy_margin=data.get('locked_buy_margin'),
            locked_buy_asset=data.get('locked_buy_asset'),
            locked_sell=data.get('locked_sell'),
            locked_value_coef=data.get('locked_value_coef'),
            in_all_assets=data.get('in_all_assets'),
            all_assets=data.get('all_assets'),
            profit_loss=data.get('profit_loss'),
            rate_change=data.get('rate_change'),
            lim_buy=data.get('lim_buy'),
            lim_sell=data.get('lim_sell'),
            lim_non_margin=data.get('lim_non_margin'),
            lim_buy_asset=data.get('lim_buy_asset'),
            val_short_net=data.get('val_short_net'),
            total_money_bal=data.get('total_money_bal'),
            total_locked_money=data.get('total_locked_money'),
            haircuts=data.get('haircuts'),
            assets_without_hc=data.get('assets_without_hc'),
            status_coef=data.get('status_coef'),
            var_margin=data.get('varmargin'),
            go_for_positions=data.get('go_for_positions'),
            go_for_orders=data.get('go_for_orders'),
            rate_futures=data.get('rate_futures'),
            is_qual_client=data.get('is_qual_client'),
            is_futures=data.get('is_futures'),
            curr_tag=data.get('curr_tag')  # Обратите внимание на разные имена
        )

    def to_dict(self) -> dict:
        """Преобразование в словарь с именами полей C#"""
        return {
            'is_leverage': self.is_leverage,
            'in_assets': self.in_assets,
            'leverage': self.leverage,
            'open_limit': self.open_limit,
            'val_short': self.val_short,
            'val_long': self.val_long,
            'val_long_margin': self.val_long_margin,
            'val_long_asset': self.val_long_asset,
            'assets': self.assets,
            'cur_leverage': self.cur_leverage,
            'margin': self.margin,
            'lim_all': self.lim_all,
            'av_lim_all': self.av_lim_all,
            'locked_buy': self.locked_buy,
            'locked_buy_margin': self.locked_buy_margin,
            'locked_buy_asset': self.locked_buy_asset,
            'locked_sell': self.locked_sell,
            'locked_value_coef': self.locked_value_coef,
            'in_all_assets': self.in_all_assets,
            'all_assets': self.all_assets,
            'profit_loss': self.profit_loss,
            'rate_change': self.rate_change,
            'lim_buy': self.lim_buy,
            'lim_sell': self.lim_sell,
            'lim_non_margin': self.lim_non_margin,
            'lim_buy_asset': self.lim_buy_asset,
            'val_short_net': self.val_short_net,
            'total_money_bal': self.total_money_bal,
            'total_locked_money': self.total_locked_money,
            'haircuts': self.haircuts,
            'assets_without_hc': self.assets_without_hc,
            'status_coef': self.status_coef,
            'varmargin': self.var_margin,
            'go_for_positions': self.go_for_positions,
            'go_for_orders': self.go_for_orders,
            'rate_futures': self.rate_futures,
            'is_qual_client': self.is_qual_client,
            'is_futures': self.is_futures,
            'curr_tag': self.curr_tag  # Обратите внимание на разные имена
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
