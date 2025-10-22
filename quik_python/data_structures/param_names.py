"""
ParamNames enum - наименования параметров для функций GetParamEx и GetParamEx2
"""

from enum import Enum


class ParamNames(Enum):
    """
    Наименования параметров для функции GetParamEx и GetParamEx2
    
    Перечисление всех доступных параметров, которые можно запросить
    для получения информации о финансовых инструментах через QUIK API.
    """
    
    ### Основные параметры инструмента

    # Код бумаги
    CODE = "CODE"

    # Код класса
    CLASS_CODE = "CLASS_CODE"

    # Краткое название бумаги
    SHORTNAME = "SHORTNAME"

    # Полное название бумаги
    LONGNAME = "LONGNAME"

    # Кратность лота
    LOT = "LOT"

    # Тип инструмента
    SECTYPESTATIC = "SECTYPESTATIC"

    # Тип фьючерса
    FUTURETYPE = "FUTURETYPE"

    # Минимальный шаг цены
    SEC_PRICE_STEP = "SEC_PRICE_STEP"

    # Название класса
    CLASSNAME = "CLASSNAME"

    # Размер лота
    LOTSIZE = "LOTSIZE"
    


    # Стоимость шага цены
    STEPPRICET = "STEPPRICET"
    
    # Стоимость шага цены
    STEPPRICE = "STEPPRICE"
    
    # Стоимость шага цены для клиринга
    STEPPRICECL = "STEPPRICECL"
    
    # Стоимость шага цены для промклиринга
    STEPPRICEPRCL = "STEPPRICEPRCL"
    
    # Точность цены
    SEC_SCALE = "SEC_SCALE"
    

    ### Цены
    
    # Цена закрытия
    PREVPRICE = "PREVPRICE"
    
    # Цена первой сделки в текущей сессии
    FIRSTOPEN = "FIRSTOPEN"
    
    # Цена последней сделки
    LAST = "LAST"
    
    # Цена последней сделки в текущей сессии
    LASTCLOSE = "LASTCLOSE"
    
    # Время последней сделки
    TIME = "TIME"
    
    
    ### Опционы
    
    # Базовый актив
    OPTIONBASE = "OPTIONBASE"
    
    # Класс базового актива
    OPTIONBASECLASS = "OPTIONBASECLASS"
    
    # Валюты
    
    # Валюта номинала
    SEC_FACE_UNIT = "SEC_FACE_UNIT"
    
    # Валюта шага цены
    CURSTEPPRICE = "CURSTEPPRICE"
    
    
    ### Лучшие цены
    
    # Лучшая цена предложения
    OFFER = "OFFER"
    
    # Лучшая цена спроса
    BID = "BID"
    
    # Количество заявок на покупку
    NUMBIDS = "NUMBIDS"
    
    # Количество заявок на продажу
    NUMOFFERS = "NUMOFFERS"
    
    # Глубина стакана
    
    # Спрос по лучшей цене
    BIDDEPTH = "BIDDEPTH"
    
    # Предложение по лучшей цене
    OFFERDEPTH = "OFFERDEPTH"
    
    # Суммарный спрос
    BIDDEPTHT = "BIDDEPTHT"
    
    # Суммарное предложение
    OFFERDEPTHT = "OFFERDEPTHT"
    
    
    ### Экстремумы
    
    # Максимальная цена сделки
    HIGH = "HIGH"
    
    # Минимальная цена сделки
    LOW = "LOW"
    
    # Максимально возможная цена
    PRICEMAX = "PRICEMAX"
    
    # Минимально возможная цена
    PRICEMIN = "PRICEMIN"
    

    ### Позиции и депо
    
    # Количество открытых позиций
    NUMCONTRACTS = "NUMCONTRACTS"
    
    # Гарантийное обеспечение покупателя
    BUYDEPO = "BUYDEPO"
    
    # Гарантийное обеспечение продавца
    SELLDEPO = "SELLDEPO"
    
    
    ### Номинал и даты
    
    # Номинал бумаги
    SEC_FACE_VALUE = "SEC_FACE_VALUE"
    
    # Дата исполнения инструмента
    EXPDATE = "EXPDATE"
    
    # Дата погашения
    MAT_DATE = "MAT_DATE"
    
    # Число дней до погашения
    DAYS_TO_MAT_DATE = "DAYS_TO_MAT_DATE"
    
    
    ### Время торговых сессий
    
    # Начало утренней сессии
    MONSTARTTIME = "MONSTARTTIME"
    
    # Окончание утренней сессии
    MONENDTIME = "MONENDTIME"
    
    # Начало вечерней сессии
    EVNSTARTTIME = "EVNSTARTTIME"
    
    # Окончание вечерней сессии
    EVNENDTIME = "EVNENDTIME"
    

    ### Статусы
    
    # Состояние сессии
    TRADINGSTATUS = "TRADINGSTATUS"
    
    # Статус клиринга
    CLSTATE = "CLSTATE"
    
    # Статус торговли инструментом
    STATUS = "STATUS"
    
    # Дата торгов
    TRADE_DATE_CODE = "TRADE_DATE_CODE"
    

    ### Внешние идентификаторы
    
    # Bloomberg ID
    BSID = "BSID"
    
    # CFI
    CFI_CODE = "CFI_CODE"
    
    # CUSIP
    CUSIP = "CUSIP"
    
    # ISIN
    ISINCODE = "ISINCODE"
    
    # RIC
    RIC = "RIC"
    
    # SEDOL
    SEDOL = "SEDOL"
    
    # StockCode
    STOCKCODE = "STOCKCODE"
    
    # StockName
    STOCKNAME = "STOCKNAME"
    

    ### Дополнительные параметры
    
    # Агрегированная ставка
    PERCENTRATE = "PERCENTRATE"
    
    # Анонимная торговля
    ANONTRADE = "ANONTRADE"
    
    # Биржевой сбор
    EXCH_PAY = "EXCH_PAY"
    
    # Время начала аукциона
    STARTTIME = "STARTTIME"
    
    # Время окончания аукциона
    ENDTIME = "ENDTIME"
    
    # Время последнего изменения
    CHANGETIME = "CHANGETIME"
    

    ### Дисконты
    
    # Дисконт1
    DISCOUNT1 = "DISCOUNT1"
    
    # Дисконт2
    DISCOUNT2 = "DISCOUNT2"
    
    # Дисконт3
    DISCOUNT3 = "DISCOUNT3"
    

    ### Объемы и количества
    
    # Количество в последней сделке
    QTY = "QTY"
    
    # Количество во всех сделках
    VOLTODAY = "VOLTODAY"
    
    # Количество сделок за сегодня
    NUMTRADES = "NUMTRADES"
    
    # Комментарий
    SEC_COMMENT = "SEC_COMMENT"
    

    ### Клиринг и оценки
    
    # Котировка последнего клиринга
    CLPRICE = "CLPRICE"
    
    # Оборот в деньгах
    VALTODAY = "VALTODAY"
    
    # Оборот в деньгах последней сделки
    VALUE = "VALUE"
    
    # Предыдущая оценка
    PREVWAPRICE = "PREVWAPRICE"
    
    # Подтип инструмента
    SECSUBTYPESTATIC = "SECSUBTYPESTATIC"
    
    # Предыдущая расчетная цена
    PREVSETTLEPRICE = "PREVSETTLEPRICE"
    
    # Предыдущий расчетный объем
    PREVSETTLEVOL = "PREVSETTLEVOL"
    

    ### Изменения цен
    
    # Процент изменения от закрытия
    LASTCHANGE = "LASTCHANGE"
    
    # Разница цены последней к предыдущей сделке
    TRADECHANGE = "TRADECHANGE"
    
    # Разница цены последней к предыдущей сессии
    CHANGE = "CHANGE"
    
    # Расчетная цена
    SETTLEPRICE = "SETTLEPRICE"
    
    # Реальная расчетная цена
    R_SETTLEPRICE = "R_SETTLEPRICE"
    
    # Регистрационный номер
    REGNUMBER = "REGNUMBER"
    
    # Средневзвешенная цена
    WAPRICE = "WAPRICE"
    
    # Текущая рыночная котировка
    REALVMPRICE = "REALVMPRICE"
    

    ### Типы
    
    # Тип
    SECTYPE = "SECTYPE"
    
    # Тип цены фьючерса
    ISPERCENT = "ISPERCENT"
    
    # Issuer
    FIRM_SHORT_NAME = "FIRM_SHORT_NAME"
    

    ### Облигации
    
    # Duration (дюрация)
    DURATION = "DURATION"
    
    # YieldMaturity (Доходность к погашению)
    YIELD = "YIELD"
    
    # Купон (размер/стоимость)
    COUPONVALUE = "COUPONVALUE"
    
    # Периодичность выплаты купонов
    COUPONPERIOD = "COUPONPERIOD"
    
    # Дата ближайшей выплаты купона
    NEXTCOUPON = "NEXTCOUPON"
    

    ### Точности и масштабы
    
    # Точные кол-ва
    QTY_SCALE = "QTY_SCALE"
    
    # Агент по размещению
    AGENT_ID = "AGENT_ID"
    
    # Макс.акт.точ.кол
    MAX_ACT_QTYSCALE = "MAX_ACT_QTYSCALE"
    
    # Стоимость шага в валюте
    STEP_IN_CURRENCY = "STEP_IN_CURRENCY"
    

    ### Дополнительные цены
    
    # % изменения к открытию
    OPENPCTCHANGE = "OPENPCTCHANGE"
    
    # Огран.отриц.цен
    NEGATIVEPRC = "NEGATIVEPRC"
    
    # Открытие
    OPEN = "OPEN"
    
    # Лучший спрос
    HIGHBID = "HIGHBID"
    
    # Лучшее предложение
    LOWOFFER = "LOWOFFER"
    
    # Закрытие
    CLOSEPRICE = "CLOSEPRICE"
    
    # Вчерашняя рыночная цена
    MARKETPRICE = "MARKETPRICE"
    
    # Рыночная цена
    MARKETPRICETODAY = "MARKETPRICETODAY"
    
    # Объем обр.
    ISSUESIZE = "ISSUESIZE"
    
    # Официальная текущая цена
    LCURRENTPRICE = "LCURRENTPRICE"
    
    # Официальная цена закрытия
    LCLOSEPRICE = "LCLOSEPRICE"
    

    ### Котировки
    
    # Тип цены
    QUOTEBASIS = "QUOTEBASIS"
    
    # Призн.котир.
    ADMITTEDQUOTE = "ADMITTEDQUOTE"
    
    # Призн.кот.пред.
    PREVADMITTEDQUOT = "PREVADMITTEDQUOT"
    
    # Спрос сессии
    LASTBID = "LASTBID"
    
    # Предложение сессии
    LASTOFFER = "LASTOFFER"
    
    # Рыночная цена2
    MARKETPRICE2 = "MARKETPRICE2"
    
    # Предыдущая цена закрытия
    PREVLEGALCLOSEPR = "PREVLEGALCLOSEPR"
    
    # Цена предторг.
    OPENPERIODPRICE = "OPENPERIODPRICE"
    
    # Минимальная тек цена
    MIN_CURR_LAST = "MIN_CURR_LAST"
    

    ### Коды и даты расчетов
    
    # Код расчетов
    SETTLECODE = "SETTLECODE"
    
    # Вр. изм.м.т.ц.
    MIN_CURR_LAST_TI = "MIN_CURR_LAST_TI"
    
    # Объем в обращении
    ISSUESIZEPLACED = "ISSUESIZEPLACED"
    
    # Дата расчетов
    SETTLEDATE = "SETTLEDATE"
    
    # Сопр.валюта
    CURRENCYID = "CURRENCYID"
    

    ### Листинг и ограничения
    
    # Листинг
    LISTLEVEL = "LISTLEVEL"
    
    # Размещение IPO
    PRIMARYDIST = "PRIMARYDIST"
    
    # Квалифицированный инвестор
    QUALIFIED = "QUALIFIED"
    
    # Дополнительная сессия
    EV_SESS_ALLOWED = "EV_SESS_ALLOWED"
    
    # П.И.Р.
    HIGH_RISK = "HIGH_RISK"
    
    # Дата последних торгов
    PREVDATE = "PREVDATE"
    

    ### Аукционы
    
    # Цена контраг.
    COUNTERPRICE = "COUNTERPRICE"
    
    # Начало аукциона план
    PLANNEDTIME = "PLANNEDTIME"
    
    # Цена аукциона
    AUCTPRICE = "AUCTPRICE"
    
    # Объем аукциона
    AUCTVALUE = "AUCTVALUE"
    
    # Количество аукциона
    AUCTVOLUME = "AUCTVOLUME"
    
    # Количество сд.аукц.
    AUCTNUMTRADES = "AUCTNUMTRADES"
    
    # Дисбаланс ПА
    IMBALANCE = "IMBALANCE"
    
    # Рын.пок.
    MARKETVOLB = "MARKETVOLB"
    
    # Рын.прод.
    MARKETVOLS = "MARKETVOLS"
    

    ### Гарантийное обеспечение
    
    # БГОП
    BGOP = "BGOP"
    
    # БГОНП
    BGONP = "BGONP"
    

    ### Опционы
    
    # Страйк
    STRIKE = "STRIKE"
    
    # Тип опциона
    OPTIONTYPE = "OPTIONTYPE"
    
    # Волатильность
    VOLATILITY = "VOLATILITY"
    
    # Теоретическая цена
    THEORPRICE = "THEORPRICE"
    
    # Марж.
    MARG = "MARG"
    
    # Разн. опц.
    OPTIONKIND = "OPTIONKIND"
    
    # Суммарный объем премии
    TOTALPREMIUMVOL = "TOTALPREMIUMVOL"
    

    ### Валютные инструменты
    
    # Базовая валюта
    FIRST_CUR = "FIRST_CUR"
    
    # Котир.валюта
    SECOND_CUR = "SECOND_CUR"
    
    # Минимальное количество
    MINQTY = "MINQTY"
    
    # Максимальное количество
    MAXQTY = "MAXQTY"
    
    # Минимальный шаг объема
    STEPQTY = "STEPQTY"
    

    ### Дополнительные расчеты
    
    # Изменение к предыдущей оценке
    PRICEMINUSPREVWA = "PRICEMINUSPREVWA"
    
    # Базовый курс
    BASEPRICE = "BASEPRICE"
    
    # Дата расчетов 1
    SETTLEDATE1 = "SETTLEDATE1"
    
    # Биржевая Сессия
    TRADINGPHASE = "TRADINGPHASE"
    
    # Заявок покупателей АКП
    DPVALINDICATORBU = "DPVALINDICATORBU"
    
    # Заявок продавцов АКП
    DPVALINDICATORSE = "DPVALINDICATORSE"
    

    ### Курсы и значения
    
    # Курс
    CROSSRATE = "CROSSRATE"
    
    # Значение
    CURRENTVALUE = "CURRENTVALUE"
    
    # Значение закрытия
    LASTVALUE = "LASTVALUE"
    
    # Минимум
    MIN = "MIN"
    
    # Максимум
    MAX = "MAX"
    
    # Открытие
    OPENVALUE = "OPENVALUE"
    
    # % изменение
    PCHANGE = "PCHANGE"
    

    ### Индексы
    
    # Открытие
    IOPEN = "IOPEN"
    
    # Мин.
    LOWVAL = "LOWVAL"
    
    # Макс.
    HIGHVAL = "HIGHVAL"
    
    # Капитал. бумаг
    ICAPITAL = "ICAPITAL"
    
    # Объем инд.сдел.
    IVOLUME = "IVOLUME"
    

    ### НКД и доходности
    
    # НКД
    ACCRUEDINT = "ACCRUEDINT"
    
    # Доходность пред.оц.
    YIELDATPREVWAPRI = "YIELDATPREVWAPRI"
    
    # Доходность оц.
    YIELDATWAPRICE = "YIELDATWAPRICE"
    
    # Доходность закр.
    CLOSEYIELD = "CLOSEYIELD"
    
    # Оферта
    BUYBACKPRICE = "BUYBACKPRICE"
    
    # Дата расч.доход
    BUYBACKDATE = "BUYBACKDATE"
    

    ### Дополнительные параметры облигаций
    
    # Тип цены обл.
    OBLPERCENT = "OBLPERCENT"
    
    # Суборд инстр-т
    SUBORDINATEDINST = "SUBORDINATEDINST"
    
    # Неточ. параметры
    BONDSREMARKS = "BONDSREMARKS"

    def __str__(self) -> str:
        """Строковое представление"""
        return self.value
