"""
PortfolioInfoEx class - расширенные параметры таблицы "Клиентский портфель"
"""

from dataclasses import dataclass
from typing import Optional
import json
from .base import BaseDataStructure


@dataclass
class PortfolioInfoEx(BaseDataStructure):
    """
    Расширенные параметры таблицы "Клиентский портфель"
    
    Возвращаемой функцией GetPortfolioInfoEx. Содержит полную детализированную 
    информацию о состоянии портфеля клиента, включая специфические параметры
    для различных типов счетов и схем кредитования.
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
    
    # Нач.маржа
    init_margin: Optional[str] = None
    
    # Мин.маржа
    min_margin: Optional[str] = None
    
    # Скор.маржа
    corrected_margin: Optional[str] = None
    
    # Тип клиента
    client_type: Optional[str] = None
    
    # Стоимость портфеля
    portfolio_value: Optional[str] = None
    
    # ЛимОткрПозНачДня
    start_limit_open_pos: Optional[str] = None
    
    # ЛимОткрПоз
    total_limit_open_pos: Optional[str] = None
    
    # ПланЧистПоз
    limit_open_pos: Optional[str] = None
    
    # ТекЧистПоз
    used_lim_open_pos: Optional[str] = None
    
    # НакопВарМаржа
    acc_var_margin: Optional[str] = None
    
    # ВарМаржаПромклир
    cl_var_margin: Optional[str] = None
    
    # ЛиквСтоимОпционов
    opt_liquid_cost: Optional[str] = None
    
    # СумАктивовНаСрчРынке
    fut_asset: Optional[str] = None
    
    # ПолнСтоимостьПортфеля
    fut_total_asset: Optional[str] = None
    
    # ТекЗадолжНаСрчРынке
    fut_debt: Optional[str] = None
    
    # Дост. Средств
    fut_rate_asset: Optional[str] = None
    
    # Дост. Средств (ОткрПоз)
    fut_rate_asset_open: Optional[str] = None
    
    # КоэффЛикв ГО
    fut_rate_go: Optional[str] = None
    
    # Ожид. КоэффЛикв ГО
    planed_rate_go: Optional[str] = None
    
    # Cash Leverage
    cash_leverage: Optional[str] = None
    
    # ТипПозНаСрчРынке
    fut_position_type: Optional[str] = None
    
    # НакопДоход
    fut_accured_int: Optional[str] = None

    # Расчетные методы
    def get_total_assets_value(self) -> Optional[float]:
        """Получить общую стоимость активов"""
        if self.fut_total_asset:
            return self.get_numeric_value(self.fut_total_asset)
        return self.get_numeric_value(self.assets)

    def get_available_margin_amount(self) -> Optional[float]:
        """Получить доступную сумму маржи"""
        return self.get_numeric_value(self.av_lim_all)

    def get_total_locked_amount(self) -> Optional[float]:
        """Получить общую сумму заблокированных средств"""
        return self.get_numeric_value(self.total_locked_money)

    def get_haircuts_amount(self) -> Optional[float]:
        """Получить сумму дисконтов"""
        return self.get_numeric_value(self.haircuts)

    def get_var_margin_total(self) -> Optional[float]:
        """Получить общую вариационную маржу"""
        vm = self.get_numeric_value(self.var_margin)
        acc_vm = self.get_numeric_value(self.acc_var_margin)
        
        if vm is not None and acc_vm is not None:
            return vm + acc_vm
        return vm or acc_vm

    def calculate_leverage_ratio(self) -> Optional[float]:
        """Рассчитать фактическое плечо"""
        assets = self.get_numeric_value(self.assets)
        limit_all = self.get_numeric_value(self.lim_all)
        
        if assets and limit_all and assets > 0:
            return limit_all / assets
        return None

    def calculate_margin_adequacy(self) -> Optional[float]:
        """Рассчитать достаточность маржи"""
        if self.is_leverage == "МД":
            corrected = self.get_numeric_value(self.corrected_margin)
            minimum = self.get_numeric_value(self.min_margin)
            
            if corrected is not None and minimum is not None and minimum > 0:
                return corrected / minimum
        
        # Для других типов клиентов
        margin = self.get_numeric_value(self.margin)
        return margin

    @staticmethod
    def get_numeric_value(value: Optional[str]) -> Optional[float]:
        """Вспомогательный метод для преобразования строки в число"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    # Методы проверки статуса
    def is_leverage_client(self) -> bool:
        """Проверить, использует ли клиент плечо"""
        leverage_types = ["МЛ", "МП", "МОП", "МД"]
        return self.is_leverage in leverage_types

    def is_discount_client(self) -> bool:
        """Проверить, является ли клиент МД (по дисконтам)"""
        return self.is_leverage == "МД"

    def is_qualified_client(self) -> bool:
        """Проверить, является ли клиент квалифицированным"""
        return self.is_qual_client == "ПовышУрРиска"

    def has_futures_account(self) -> bool:
        """Проверить, есть ли срочный счет"""
        return bool(self.is_futures and self.is_futures.strip())

    def has_futures_positions(self) -> bool:
        """Проверить, есть ли позиции на срочном рынке"""
        return self.fut_position_type not in [None, "", "0"]

    def has_options_positions(self) -> bool:
        """Проверить, есть ли опционные позиции"""
        return self.fut_position_type in ["2", "3"]

    def has_futures_only_positions(self) -> bool:
        """Проверить, есть ли только фьючерсные позиции"""
        return self.fut_position_type == "1"

    def is_profitable(self) -> bool:
        """Проверить, прибыльный ли портфель"""
        profit = self.get_numeric_value(self.profit_loss)
        return profit is not None and profit > 0

    def get_client_type_description(self) -> str:
        """Получить описание типа клиента"""
        leverage_types = {
            "МЛ": "схема ведения позиции «по плечу», «плечо» рассчитано по значению Входящего лимита",
            "МП": "схема ведения позиции «по плечу», «плечо» указано явным образом",
            "МОП": "схема ведения позиции «лимит на открытую позицию»",
            "МД": "схема ведения позиции «по дисконтам»",
            "": "схема ведения позиции «по лимитам»"
        }
        return leverage_types.get(self.is_leverage or "", "Неизвестный тип")

    def get_futures_position_type_description(self) -> str:
        """Получить описание типа позиции на срочном рынке"""
        position_types = {
            "0": "нет позиции",
            "1": "фьючерсы",
            "2": "опционы",
            "3": "фьючерсы и опционы"
        }
        return position_types.get(self.fut_position_type or "", "Неизвестный тип")

    # JSON Serialization methods
    @classmethod
    def from_dict(cls, data: dict) -> 'PortfolioInfoEx':
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
            curr_tag=data.get('curr_tag'),
            init_margin=data.get('init_margin'),
            min_margin=data.get('min_margin'),
            corrected_margin=data.get('corrected_margin'),
            client_type=data.get('client_type'),
            portfolio_value=data.get('portfolio_value'),
            start_limit_open_pos=data.get('start_limit_open_pos'),
            total_limit_open_pos=data.get('total_limit_open_pos'),
            limit_open_pos=data.get('limit_open_pos'),
            used_lim_open_pos=data.get('used_lim_open_pos'),
            acc_var_margin=data.get('acc_var_margin'),
            cl_var_margin=data.get('cl_var_margin'),
            opt_liquid_cost=data.get('opt_liquid_cost'),
            fut_asset=data.get('fut_asset'),
            fut_total_asset=data.get('fut_total_asset'),
            fut_debt=data.get('fut_debt'),
            fut_rate_asset=data.get('fut_rate_asset'),
            fut_rate_asset_open=data.get('fut_rate_asset_open'),
            fut_rate_go=data.get('fut_rate_go'),
            planed_rate_go=data.get('planed_rate_go'),
            cash_leverage=data.get('cash_leverage'),
            fut_position_type=data.get('fut_position_type'),
            fut_accured_int=data.get('fut_accured_int')
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
            'curr_tag': self.curr_tag,
            'init_margin': self.init_margin,
            'min_margin': self.min_margin,
            'corrected_margin': self.corrected_margin,
            'client_type': self.client_type,
            'portfolio_value': self.portfolio_value,
            'start_limit_open_pos': self.start_limit_open_pos,
            'total_limit_open_pos': self.total_limit_open_pos,
            'limit_open_pos': self.limit_open_pos,
            'used_lim_open_pos': self.used_lim_open_pos,
            'acc_var_margin': self.acc_var_margin,
            'cl_var_margin': self.cl_var_margin,
            'opt_liquid_cost': self.opt_liquid_cost,
            'fut_asset': self.fut_asset,
            'fut_total_asset': self.fut_total_asset,
            'fut_debt': self.fut_debt,
            'fut_rate_asset': self.fut_rate_asset,
            'fut_rate_asset_open': self.fut_rate_asset_open,
            'fut_rate_go': self.fut_rate_go,
            'planed_rate_go': self.planed_rate_go,
            'cash_leverage': self.cash_leverage,
            'fut_position_type': self.fut_position_type,
            'fut_accured_int': self.fut_accured_int
        }

    def to_json(self) -> str:
        """Преобразование в JSON строку"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
