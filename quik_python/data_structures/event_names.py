"""
EventNames enum - имена событий QUIK
"""

from enum import Enum


class EventNames(Enum):
    """
    Перечисление имен событий для системы обратных вызовов QUIK
    """
    
    # Изменение денежных позиций
    OnAccountBalance = "OnAccountBalance"
    
    # Изменение позиций по инструментам
    OnAccountPosition = "OnAccountPosition"
    
    # Новая обезличенная сделка
    OnAllTrade = "OnAllTrade"
    
    # Событие очистки
    OnCleanUp = "OnCleanUp"
    
    # Закрытие терминала
    OnClose = "OnClose"
    
    # Установка соединения с сервером
    OnConnected = "OnConnected"
    
    # Изменение лимита по бумагам
    OnDepoLimit = "OnDepoLimit"
    
    # Удаление лимита по бумагам
    OnDepoLimitDelete = "OnDepoLimitDelete"
    
    # Отключение от сервера
    OnDisconnected = "OnDisconnected"
    
    # Изменение справочника фирм
    OnFirm = "OnFirm"
    
    # Изменение позиции по фьючерсному контракту
    OnFuturesClientHolding = "OnFuturesClientHolding"
    
    # Изменение ограничений по фьючерсам
    OnFuturesLimitChange = "OnFuturesLimitChange"
    
    # Удаление ограничений по фьючерсам
    OnFuturesLimitDelete = "OnFuturesLimitDelete"
    
    # Инициализация
    OnInit = "OnInit"
    
    # Изменение денежного лимита
    OnMoneyLimit = "OnMoneyLimit"
    
    # Удаление денежного лимита
    OnMoneyLimitDelete = "OnMoneyLimitDelete"
    
    # Новая сделка для исполнения
    OnNegDeal = "OnNegDeal"
    
    # Новая сделка
    OnNegTrade = "OnNegTrade"
    
    # Изменение заявки
    OnOrder = "OnOrder"
    
    # Изменение параметра
    OnParam = "OnParam"
    
    # Изменение стакана котировок
    OnQuote = "OnQuote"
    
    # Остановка
    OnStop = "OnStop"
    
    # Изменение стоп-заявки
    OnStopOrder = "OnStopOrder"
    
    # Новая сделка
    OnTrade = "OnTrade"
    
    # Ответ на транзакцию
    OnTransReply = "OnTransReply"
    
    # Новая свеча
    NewCandle = "NewCandle"
    
    @classmethod
    def from_string(cls, event_name: str):
        """Преобразует строку в EventNames enum"""
        for event in cls:
            if event.value == event_name:
                return event
        raise ValueError(f"Неизвестное имя события: {event_name}")
    
    def get_description(self) -> str:
        """Возвращает описание события"""
        descriptions = {
            self.OnAccountBalance: "Изменение денежных позиций",
            self.OnAccountPosition: "Изменение позиций по инструментам",
            self.OnAllTrade: "Новая обезличенная сделка",
            self.OnCleanUp: "Событие очистки",
            self.OnClose: "Закрытие терминала",
            self.OnConnected: "Установка соединения с сервером",
            self.OnDepoLimit: "Изменение лимита по бумагам",
            self.OnDepoLimitDelete: "Удаление лимита по бумагам",
            self.OnDisconnected: "Отключение от сервера",
            self.OnFirm: "Изменение справочника фирм",
            self.OnFuturesClientHolding: "Изменение позиции по фьючерсному контракту",
            self.OnFuturesLimitChange: "Изменение ограничений по фьючерсам",
            self.OnFuturesLimitDelete: "Удаление ограничений по фьючерсам",
            self.OnInit: "Инициализация",
            self.OnMoneyLimit: "Изменение денежного лимита",
            self.OnMoneyLimitDelete: "Удаление денежного лимита",
            self.OnNegDeal: "Новая сделка для исполнения",
            self.OnNegTrade: "Новая сделка",
            self.OnOrder: "Изменение заявки",
            self.OnParam: "Изменение параметра",
            self.OnQuote: "Изменение стакана котировок",
            self.OnStop: "Остановка",
            self.OnStopOrder: "Изменение стоп-заявки",
            self.OnTrade: "Новая сделка",
            self.OnTransReply: "Ответ на транзакцию",
            self.NewCandle: "Новая свеча"
        }
        return descriptions.get(self, "Неизвестное событие")
