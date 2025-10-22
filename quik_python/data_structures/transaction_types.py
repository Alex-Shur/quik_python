"""
Transaction classes
"""

from enum import Enum


class TransactionAction(Enum):
    """
    Вид транзакции
    На основе http://help.qlua.org/ch4_8_1.htm
    """
    
    # новая заявка
    NEW_ORDER = 1
    
    # новая заявка на внебиржевую сделку
    NEW_NEG_DEAL = 2
    
    # новая заявка на сделку РЕПО
    NEW_REPO_NEG_DEAL = 3
    
    # новая заявка на сделку модифицированного РЕПО (РЕПО-М)
    NEW_EXT_REPO_NEG_DEAL = 4
    
    # новая стоп-заявка
    NEW_STOP_ORDER = 5
    
    # снять заявку
    KILL_ORDER = 6
    
    # снять заявку на внебиржевую сделку или заявку на сделку РЕПО
    KILL_NEG_DEAL = 7
    
    # снять стоп-заявку
    KILL_STOP_ORDER = 8
    
    # снять все заявки из торговой системы
    KILL_ALL_ORDERS = 9
    
    # снять все стоп-заявки
    KILL_ALL_STOP_ORDERS = 10
    
    # снять все заявки на внебиржевые сделки и заявки на сделки РЕПО
    KILL_ALL_NEG_DEALS = 11
    
    # снять все заявки на рынке FORTS
    KILL_ALL_FUTURES_ORDERS = 12
    
    # удалить лимит открытых позиций на спот-рынке RTS Standard
    KILL_RTS_T4_LONG_LIMIT = 13
    
    # удалить лимит открытых позиций клиента по спот-активу на рынке RTS Standard
    KILL_RTS_T4_SHORT_LIMIT = 14
    
    # переставить заявки на рынке FORTS
    MOVE_ORDERS = 15
    
    # новая безадресная заявка
    NEW_QUOTE = 16
    
    # снять безадресную заявку
    KILL_QUOTE = 17
    
    # новая заявка-отчет о подтверждении транзакций в режимах РПС и РЕПО
    NEW_REPORT = 18
    
    # новое ограничение по фьючерсному счету
    SET_FUT_LIMIT = 19


class TransactionType(Enum):
    """
    Тип заявки, необязательный параметр
    """
    
    # лимитированная (по умолчанию)
    L = 0
    
    # рыночная
    M = 1


class YesOrNo(Enum):
    """
    YES or NO
    """
    
    # NO
    NO = 1
    
    # YES
    YES = 2


class YesOrNoDefault(Enum):
    """
    YES or NO with NO default
    """
    
    # NO (по умолчанию)
    NO = 0
    
    # YES
    YES = 1


class TransactionOperation(Enum):
    """
    Тип операции транзакции
    """
    
    # купить
    B = 1
    
    # продать
    S = 2


class ExecutionCondition(Enum):
    """
    Условие исполнения заявки, необязательный параметр
    """
    
    # поставить в очередь (по умолчанию)
    PUT_IN_QUEUE = 0
    
    # немедленно или отклонить
    FILL_OR_KILL = 1
    
    # снять остаток
    KILL_BALANCE = 2


class ForAccount(Enum):
    """
    Лицо, от имени которого и за чей счет регистрируется сделка
    (параметр внебиржевой сделки)
    """
    
    # от своего имени, за свой счет
    OWNOWN = 1
    
    # от своего имени, за счет клиента
    OWNCLI = 2
    
    # от своего имени, за счет доверительного управления
    OWNDUP = 3
    
    # от имени клиента, за счет клиента
    CLICLI = 4


class OffsetUnits(Enum):
    """
    Единицы измерения отступа. Используется при стоп-заявках
    """
    
    # в процентах (шаг изменения – одна сотая процента)
    PERCENTS = 1
    
    # в параметрах цены (шаг изменения равен шагу цены по данному инструменту)
    PRICE_UNITS = 2
