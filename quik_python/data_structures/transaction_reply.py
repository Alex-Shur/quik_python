"""
TransactionReply class - результат выполнения транзакции
"""

import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from .base import BaseDataStructure
from .quik_datetime import QuikDateTime


@dataclass
class TransactionReply(BaseDataStructure):
    """
    Результат OnTransReply
    """
    
    # Timestamp для Lua
    lua_timestamp: Optional[int] = None
    
    # Пользовательский идентификатор транзакции
    trans_id: Optional[int] = None
    
    # Статус транзакции
    # «0» - транзакция отправлена серверу,
    # «1» - транзакция получена на сервер QUIK от клиента,
    # «2» - ошибка при передаче транзакции в торговую систему, поскольку отсутствует подключение шлюза Московской Биржи, повторно транзакция не отправляется,
    # «3» - транзакция выполнена,
    # «4» - транзакция не выполнена торговой системой, код ошибки торговой системы будет указан в поле «DESCRIPTION»,
    # «5» - транзакция не прошла проверку сервера QUIK по каким-либо критериям. Например, проверку на наличие прав у пользователя на отправку транзакции данного типа,
    # «6» - транзакция не прошла проверку лимитов сервера QUIK,
    # «10» - транзакция не поддерживается торговой системой. К примеру, попытка отправить «ACTION = MOVE_ORDERS» на Московской Бирже,
    # «11» - транзакция не прошла проверку правильности электронной подписи. К примеру, если ключи, зарегистрированные на сервере, не соответствуют подписи отправленной транзакции.
    # «12» - не удалось дождаться ответа на транзакцию, т.к. истек таймаут ожидания. Может возникнуть при подаче транзакций из QPILE.
    # «13» - транзакция отвергнута, т.к. ее выполнение могло привести к кросс-сделке (т.е. сделке с тем же самым клиентским счетом).
    status: Optional[int] = None
    
    # Сообщение
    result_msg: Optional[str] = None
    
    # Время (в QLUA представлено как число)
    time: Optional[str] = None
    
    # Идентификатор пользователя у брокера
    uid: Optional[int] = None
    
    # Флаги транзакции (временно не используется)
    flags: Optional[int] = None
    
    # Идентификатор транзакции на сервере
    server_trans_id: Optional[int] = None
    
    # Номер заявки
    order_num: Optional[int] = None
    
    # Цена
    price: Optional[Decimal] = None
    
    # Количество
    quantity: Optional[Decimal] = None
    
    # Остаток
    balance: Optional[Decimal] = None
    
    # Идентификатор фирмы
    firm_id: Optional[str] = None
    
    # Торговый счет
    account: Optional[str] = None
    
    # Код клиента
    client_code: Optional[str] = None
    
    # Поручение/комментарий
    brokerref: Optional[str] = None
    
    # Код класса
    class_code: Optional[str] = None
    
    # Код бумаги
    sec_code: Optional[str] = None
    
    # Биржевой номер заявки
    exchange_code: Optional[str] = None
    
    # Числовой код ошибки
    error_code: Optional[int] = None
    
    # Источник сообщения
    # «1» – Торговая система; 
    # «2» – Сервер QUIK; 
    # «3» – Библиотека расчёта лимитов; 
    # «4» – Шлюз торговой системы
    error_source: Optional[int] = None
    
    # Номер первой заявки при автоматической замене кода клиента
    first_ordernum: Optional[int] = None
    
    # Дата и время получения шлюзом ответа на транзакцию
    gate_reply_time: Optional[QuikDateTime] = None
    
    @property
    def trans_reply_status(self) -> Optional[str]:
        """
        Возвращает описание статуса транзакции
        """
        status_descriptions = {
            0: "Транзакция отправлена серверу",
            1: "Транзакция получена на сервер QUIK от клиента",
            2: "Ошибка при передаче в торговую систему (отсутствует подключение шлюза)",
            3: "Транзакция выполнена",
            4: "Транзакция не выполнена торговой системой",
            5: "Транзакция не прошла проверку сервера QUIK",
            6: "Транзакция не прошла проверку лимитов сервера QUIK",
            10: "Транзакция не поддерживается торговой системой",
            11: "Транзакция не прошла проверку электронной подписи",
            12: "Истек таймаут ожидания ответа на транзакцию",
            13: "Транзакция отвергнута из-за возможной кросс-сделки"
        }
        return status_descriptions.get(self.status, f"Неизвестный статус: {self.status}")
    
    @property
    def error_source_description(self) -> Optional[str]:
        """
        Возвращает описание источника ошибки
        """
        if self.error_source is None:
            return None

        source_descriptions = {
            1: "Торговая система",
            2: "Сервер QUIK",
            3: "Библиотека расчёта лимитов",
            4: "Шлюз торговой системы"
        }
        return source_descriptions.get(self.error_source, f"Неизвестный источник: {self.error_source}")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TransactionReply':
        """
        Create TransactionReply from dictionary
        
        Args:
            data: Dictionary containing transaction reply data
            
        Returns:
            TransactionReply instance
        """
        return cls(
            lua_timestamp=data.get('lua_timestamp'),
            trans_id=data.get('trans_id'),
            status=data.get('status'),
            result_msg=data.get('result_msg'),
            time=data.get('time'),
            uid=data.get('uid'),
            flags=data.get('flags'),
            server_trans_id=data.get('server_trans_id'),
            order_num=data.get('order_num'),
            price=Decimal(str(data['price'])) if data.get('price') is not None else None,
            quantity=Decimal(str(data['quantity'])) if data.get('quantity') is not None else None,
            balance=Decimal(str(data['balance'])) if data.get('balance') is not None else None,
            firm_id=data.get('firm_id'),
            account=data.get('account'),
            client_code=data.get('client_code'),
            brokerref=data.get('brokerref'),
            class_code=data.get('class_code'),
            sec_code=data.get('sec_code'),
            exchange_code=data.get('exchange_code'),
            error_code=data.get('error_code'),
            error_source=data.get('error_source'),
            first_ordernum=data.get('first_ordernum'),
            gate_reply_time=QuikDateTime.from_dict(data['gate_reply_time']) if data.get('gate_reply_time') else None
        )
    
    def to_dict(self) -> dict:
        """
        Convert TransactionReply to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'lua_timestamp': self.lua_timestamp,
            'trans_id': self.trans_id,
            'status': self.status,
            'result_msg': self.result_msg,
            'time': self.time,
            'uid': self.uid,
            'flags': self.flags,
            'server_trans_id': self.server_trans_id,
            'order_num': self.order_num,
            'price': float(self.price) if self.price is not None else None,
            'quantity': float(self.quantity) if self.quantity is not None else None,
            'balance': float(self.balance) if self.balance is not None else None,
            'firm_id': self.firm_id,
            'account': self.account,
            'client_code': self.client_code,
            'brokerref': self.brokerref,
            'class_code': self.class_code,
            'sec_code': self.sec_code,
            'exchange_code': self.exchange_code,
            'error_code': self.error_code,
            'error_source': self.error_source,
            'first_ordernum': self.first_ordernum,
            'gate_reply_time': self.gate_reply_time.to_dict() if self.gate_reply_time else None
        }
    
    def to_json(self) -> str:
        """
        Convert TransactionReply to JSON string
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def __str__(self) -> str:
        """String representation"""
        return self.to_json()
