"""
Enum for QUIK information parameters
"""

from enum import Enum


class InfoParams(Enum):
    """
    Параметры информации QUIK
    """
    
    # Версия программы
    VERSION = "VERSION"
    
    # Дата торгов
    TRADEDATE = "TRADEDATE"
    
    # Время сервера
    SERVERTIME = "SERVERTIME"
    
    # Время последней записи
    LASTRECORDTIME = "LASTRECORDTIME"
    
    # Число записей
    NUMRECORDS = "NUMRECORDS"
    
    # Последняя запись
    LASTRECORD = "LASTRECORD",

    # Отставшая запись
    LATERECORD = "LATERECORD",

    # Соединение
    CONNECTION = "CONNECTION",

    # IP-адрес сервера
    IPADDRESS = "IPADDRESS",

    # Порт сервера
    IPPORT = "IPPORT",

    # Описание соединения
    IPCOMMENT = "IPCOMMENT",

    # Описание сервера
    SERVER = "SERVER",

    # Идентификатор сессии
    SESSIONID = "SESSIONID",

    # Пользователь
    USER = "USER",

    # ID пользователя
    USERID = "USERID",

    # Организация
    ORG = "ORG",

    # Занято памяти
    MEMORY = "MEMORY",

    # Текущее время
    LOCALTIME = "LOCALTIME",

    # Время на связи
    CONNECTIONTIME = "CONNECTIONTIME",

    # Передано сообщений
    MESSAGESSENT = "MESSAGESSENT",

    # Передано всего байт
    ALLSENT = "ALLSENT",

    # Передано полезных байт
    BYTESSENT = "BYTESSENT",

    # Передано за секунду
    BYTESPERSECSENT = "BYTESPERSECSENT",

    # Принято сообщений
    MESSAGESRECV = "MESSAGESRECV",

    # Принято полезных байт
    BYTESRECV = "BYTESRECV",

    # Принято всего байт
    ALLRECV = "ALLRECV",

    # Принято за секунду
    BYTESPERSECRECV = "BYTESPERSECRECV",

    # Средняя скорость передачи
    AVGSENT = "AVGSENT",

    # Средняя скорость приема
    AVGRECV = "AVGRECV",

    # Время последней проверки связи
    LASTPINGTIME = "LASTPINGTIME",

    # Задержка данных при обмене с сервером
    LASTPINGDURATION = "LASTPINGDURATION",

    # Средняя задержка данных
    AVGPINGDURATION = "AVGPINGDURATION",

    # Время максимальной задержки
    MAXPINGTIME = "MAXPINGTIME",

    # Максимальная задержка данных
    MAXPINGDURATION = "MAXPINGDURATION"


    def __str__(self) -> str:
        """Возвращает строковое представление enum'а для отправки в QUIK"""
        return self.value
