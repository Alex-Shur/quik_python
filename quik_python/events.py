"""
Event handling for QUIK Python API
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Dict, List, Optional, Any

from .data_structures import AccountBalance, AccountPosition, DepoLimitDelete, DepoLimitEx, Firm, \
    FuturesClientHolding, FuturesLimitDelete, FuturesLimits, MoneyLimitDelete, MoneyLimitEx, Param, \
    AllTrade, OrderBook, Candle, Order, Trade, StopOrder, TransactionReply, Transaction


class IQuikEvents(ABC):
    """
    Interface for QUIK event handling
    """

    @abstractmethod
    def add_on_account_balance(self, handler: Callable[[AccountBalance], None]) -> None:
        """Subscribe to account balance events"""
        pass

    @abstractmethod
    def add_on_account_position(self, handler: Callable[[AccountPosition], None]) -> None:
        """Subscribe to account position events"""
        pass

    @abstractmethod
    def add_on_all_trade(self, handler: Callable[[AllTrade], None]) -> None:
        """Subscribe to all trade events"""
        pass

    @abstractmethod
    def add_on_clean_up(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to clean up events"""
        pass

    @abstractmethod
    def add_on_close(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to close events"""
        pass

    @abstractmethod
    def add_on_connected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to connected events"""
        pass

    @abstractmethod
    def add_on_depo_limit(self, handler: Callable[[DepoLimitEx], None]) -> None:
        """Subscribe to depo limit events"""
        pass

    @abstractmethod
    def add_on_depo_limit_delete(self, handler: Callable[[DepoLimitDelete], None]) -> None:
        """Subscribe to depo limit delete events"""
        pass

    @abstractmethod
    def add_on_disconnected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to disconnected events"""
        pass

    @abstractmethod
    def add_on_firm(self, handler: Callable[[Firm], None]) -> None:
        """Subscribe to firm events"""
        pass

    @abstractmethod
    def add_on_futures_client_holding(self, handler: Callable[[FuturesClientHolding], None]) -> None:
        """Subscribe to futures client holding events"""
        pass

    @abstractmethod
    def add_on_futures_limit_change(self, handler: Callable[[FuturesLimits], None]) -> None:
        """Subscribe to futures limit events"""
        pass

    @abstractmethod
    def add_on_futures_limit_delete(self, handler: Callable[[FuturesLimitDelete], None]) -> None:
        """Subscribe to futures limit delete events"""
        pass

    @abstractmethod
    def add_on_money_limit(self, handler: Callable[[MoneyLimitEx], None]) -> None:
        """Subscribe to money limit events"""
        pass

    @abstractmethod
    def add_on_money_limit_delete(self, handler: Callable[[MoneyLimitDelete], None]) -> None:
        """Subscribe to money limit delete events"""
        pass

    @abstractmethod
    def add_on_order(self, handler: Callable[[Order], None]) -> None:
        """Subscribe to order events"""
        pass

    @abstractmethod
    def add_on_param(self, handler: Callable[[Param], None]) -> None:
        """Subscribe to param events"""
        pass

    @abstractmethod
    def add_on_quote(self, handler: Callable[[OrderBook], None]) -> None:
        """Subscribe to quote events"""
        pass

    @abstractmethod
    def add_on_stop(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to stop events"""
        pass

    @abstractmethod
    def add_on_stop_order(self, handler: Callable[[StopOrder], None]) -> None:
        """Subscribe to stop order events"""
        pass

    @abstractmethod
    def add_on_trade(self, handler: Callable[[Trade], None]) -> None:
        """Subscribe to trade events"""
        pass

    @abstractmethod
    def add_on_trans_reply(self, handler: Callable[[TransactionReply], None]) -> None:
        """Subscribe to transaction reply events"""
        pass


    @abstractmethod
    def remove_on_account_balance(self, handler: Callable[[AccountBalance], None]) -> None:
        """Unsubscribe to account balance events"""
        pass

    @abstractmethod
    def remove_on_account_position(self, handler: Callable[[AccountPosition], None]) -> None:
        """Unsubscribe to account position events"""
        pass

    @abstractmethod
    def remove_on_all_trade(self, handler: Callable[[AllTrade], None]) -> None:
        """Unsubscribe to all trade events"""
        pass

    @abstractmethod
    def remove_on_clean_up(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe to clean up events"""
        pass

    @abstractmethod
    def remove_on_close(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe to close events"""
        pass

    @abstractmethod
    def remove_on_connected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe to connected events"""
        pass

    @abstractmethod
    def remove_on_depo_limit(self, handler: Callable[[DepoLimitEx], None]) -> None:
        """Unsubscribe to depo limit events"""
        pass

    @abstractmethod
    def remove_on_depo_limit_delete(self, handler: Callable[[DepoLimitDelete], None]) -> None:
        """Unsubscribe to depo limit delete events"""
        pass

    @abstractmethod
    def remove_on_disconnected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe to disconnected events"""
        pass

    @abstractmethod
    def remove_on_firm(self, handler: Callable[[Firm], None]) -> None:
        """Unsubscribe to firm depo limit delete events"""
        pass

    @abstractmethod
    def remove_on_futures_client_holding(self, handler: Callable[[FuturesClientHolding], None]) -> None:
        """Unsubscribe to firm futures client holding events"""
        pass

    @abstractmethod
    def remove_on_futures_limit_change(self, handler: Callable[[FuturesLimits], None]) -> None:
        """Unsubscribe to firm futures limit change events"""
        pass

    @abstractmethod
    def remove_on_futures_limit_delete(self, handler: Callable[[FuturesLimitDelete], None]) -> None:
        """Unsubscribe to firm futures limit delete events"""
        pass

    @abstractmethod
    def remove_on_money_limit(self, handler: Callable[[MoneyLimitEx], None]) -> None:
        """Unsubscribe to firm money limit events"""
        pass

    @abstractmethod
    def remove_on_money_limit_delete(self, handler: Callable[[MoneyLimitDelete], None]) -> None:
        """Unsubscribe to firm money limit delete events"""
        pass

    @abstractmethod
    def remove_on_order(self, handler: Callable[[Order], None]) -> None:
        """Unsubscribe to order events"""
        pass

    @abstractmethod
    def remove_on_param(self, handler: Callable[[Param], None]) -> None:
        """Unsubscribe to param events"""
        pass

    @abstractmethod
    def remove_on_quote(self, handler: Callable[[OrderBook], None]) -> None:
        """Unsubscribe to quote events"""
        pass

    @abstractmethod
    def remove_on_stop(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Unsubscribe to stop events"""
        pass

    @abstractmethod
    def remove_on_stop_order(self, handler: Callable[[StopOrder], None]) -> None:
        """Unsubscribe to stop order events"""
        pass

    @abstractmethod
    def remove_on_trade(self, handler: Callable[[Trade], None]) -> None:
        """Unsubscribe to trade events"""
        pass

    @abstractmethod
    def remove_on_trans_reply(self, handler: Callable[[TransactionReply], None]) -> None:
        """Unsubscribe to transaction reply events"""
        pass



class QuikEvents(IQuikEvents):
    """
    Implementation of QUIK event handling
    """

    def __init__(self, service: 'QuikService'):
        self.service = service
        self.EPOCH = datetime(1970, 1, 1, 3, 0, 0)
        self._handlers: Dict[str, List[Callable]] = {
            'OnAccountBalance': [],
            'OnAccountPosition': [],

            'OnAllTrade': [],

            'OnCleanUp': [],
            'OnClose': [],
            'OnConnected': [],
            'OnDepoLimit': [],
            'OnDepoLimitDelete': [],
            'OnDisconnected': [],
            'OnFirm': [],
            'OnFuturesClientHolding': [],
            'OnFuturesLimitChange': [],
            'OnFuturesLimitDelete': [],
            'OnInit': [],
            'OnMoneyLimit': [],
            'OnMoneyLimitDelete': [],
            # 'OnNegDeal': [],
            # 'OnNegTrade': [],

            'OnOrder': [],
            'OnParam': [],
            'OnQuote': [],
            'OnStop': [],
            'OnStopOrder': [],
            'OnTrade': [],
            'OnTransReply': [],
            'NewCandle': []
        }


    def add_on_account_balance(self, handler: Callable[[AccountBalance], None]) -> None:
        """Subscribe to account balance events"""
        self._handlers['OnAccountBalance'].append(handler)

    def add_on_account_position(self, handler: Callable[[AccountPosition], None]) -> None:
        """Subscribe to account position events"""
        self._handlers['OnAccountPosition'].append(handler)

    def add_on_all_trade(self, handler: Callable[[AllTrade], None]) -> None:
        """Subscribe to all trade events"""
        self._handlers['OnAllTrade'].append(handler)

    def add_on_clean_up(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to clean up events"""
        self._handlers['OnCleanUp'].append(handler)

    def add_on_close(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to close events"""
        self._handlers['OnClose'].append(handler)

    def add_on_connected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to connected events"""
        self._handlers['OnConnected'].append(handler)

    def add_on_depo_limit(self, handler: Callable[[DepoLimitEx], None]) -> None:
        """Subscribe to depo limit events"""
        self._handlers['OnDepoLimit'].append(handler)

    def add_on_depo_limit_delete(self, handler: Callable[[DepoLimitDelete], None]) -> None:
        """Subscribe to depo limit delete events"""
        self._handlers['OnDepoLimitDelete'].append(handler)

    def add_on_disconnected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to disconnected events"""
        self._handlers['OnDisconnected'].append(handler)

    def add_on_firm(self, handler: Callable[[Firm], None]) -> None:
        """Subscribe to firm events"""
        self._handlers['OnFirm'].append(handler)

    def add_on_futures_client_holding(self, handler: Callable[[FuturesClientHolding], None]) -> None:
        """Subscribe to futures client holding events"""
        self._handlers['OnFuturesClientHolding'].append(handler)

    def add_on_futures_limit_change(self, handler: Callable[[FuturesLimits], None]) -> None:
        """Subscribe to futures limit events"""
        self._handlers['OnFuturesLimitChange'].append(handler)

    def add_on_futures_limit_delete(self, handler: Callable[[FuturesLimitDelete], None]) -> None:
        """Subscribe to futures limit delete events"""
        self._handlers['OnFuturesLimitDelete'].append(handler)

    def add_on_money_limit(self, handler: Callable[[MoneyLimitEx], None]) -> None:
        """Subscribe to money limit events"""
        self._handlers['OnMoneyLimit'].append(handler)

    def add_on_money_limit_delete(self, handler: Callable[[MoneyLimitDelete], None]) -> None:
        """Subscribe to money limit delete events"""
        self._handlers['OnMoneyLimitDelete'].append(handler)

    def add_on_order(self, handler: Callable[[Order], None]) -> None:
        """Subscribe to order events"""
        self._handlers['OnOrder'].append(handler)

    def add_on_param(self, handler: Callable[[Param], None]) -> None:
        """Subscribe to param events"""
        self._handlers['OnParam'].append(handler)

    def add_on_quote(self, handler: Callable[[OrderBook], None]) -> None:
        """Subscribe to quote events"""
        self._handlers['OnQuote'].append(handler)

    def add_on_stop(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to stop events"""
        self._handlers['OnStop'].append(handler)

    def add_on_stop_order(self, handler: Callable[[StopOrder], None]) -> None:
        """Subscribe to stop order events"""
        self._handlers['OnStopOrder'].append(handler)

    def add_on_trade(self, handler: Callable[[Trade], None]) -> None:
        """Subscribe to trade events"""
        self._handlers['OnTrade'].append(handler)

    def add_on_trans_reply(self, handler: Callable[[TransactionReply], None]) -> None:
        """Subscribe to transaction reply events"""
        self._handlers['OnTransReply'].append(handler)


    def remove_on_account_balance(self, handler):
        if handler in self._handlers['OnAccountBalance']:
            self._handlers['OnAccountBalance'].remove(handler)

    def remove_on_account_position(self, handler: Callable[[AccountPosition], None]) -> None:
        if handler in self._handlers['OnAccountPosition']:
            self._handlers['OnAccountPosition'].remove(handler)

    def remove_on_all_trade(self, handler: Callable[[AllTrade], None]) -> None:
        if handler in self._handlers['OnAllTrade']:
            self._handlers['OnAllTrade'].remove(handler)

    def remove_on_clean_up(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        if handler in self._handlers['OnCleanUp']:
            self._handlers['OnCleanUp'].remove(handler)

    def remove_on_close(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        if handler in self._handlers['OnClose']:
            self._handlers['OnClose'].remove(handler)

    def remove_on_connected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        if handler in self._handlers['OnConnected']:
            self._handlers['OnConnected'].remove(handler)

    def remove_on_depo_limit(self, handler: Callable[[DepoLimitEx], None]) -> None:
        if handler in self._handlers['OnDepoLimit']:
            self._handlers['OnDepoLimit'].remove(handler)

    def remove_on_depo_limit_delete(self, handler: Callable[[DepoLimitDelete], None]) -> None:
        if handler in self._handlers['OnDepoLimitDelete']:
            self._handlers['OnDepoLimitDelete'].remove(handler)

    def remove_on_disconnected(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        if handler in self._handlers['OnDisconnected']:
            self._handlers['OnDisconnected'].remove(handler)

    def remove_on_firm(self, handler: Callable[[Firm], None]) -> None:
        if handler in self._handlers['OnFirm']:
            self._handlers['OnFirm'].remove(handler)

    def remove_on_futures_client_holding(self, handler: Callable[[FuturesClientHolding], None]) -> None:
        if handler in self._handlers['OnFuturesClientHolding']:
            self._handlers['OnFuturesClientHolding'].remove(handler)

    def remove_on_futures_limit_change(self, handler: Callable[[FuturesLimits], None]) -> None:
        if handler in self._handlers['OnFuturesLimitChange']:
            self._handlers['OnFuturesLimitChange'].remove(handler)

    def remove_on_futures_limit_delete(self, handler: Callable[[FuturesLimitDelete], None]) -> None:
        if handler in self._handlers['OnFuturesLimitDelete']:
            self._handlers['OnFuturesLimitDelete'].remove(handler)

    def remove_on_money_limit(self, handler: Callable[[MoneyLimitEx], None]) -> None:
        if handler in self._handlers['OnMoneyLimit']:
            self._handlers['OnMoneyLimit'].remove(handler)

    def remove_on_money_limit_delete(self, handler: Callable[[MoneyLimitDelete], None]) -> None:
        if handler in self._handlers['OnMoneyLimitDelete']:
            self._handlers['OnMoneyLimitDelete'].remove(handler)

    def remove_on_order(self, handler: Callable[[Order], None]) -> None:
        if handler in self._handlers['OnOrder']:
            self._handlers['OnOrder'].remove(handler)

    def remove_on_param(self, handler: Callable[[Param], None]) -> None:
        if handler in self._handlers['OnParam']:
            self._handlers['OnParam'].remove(handler)

    def remove_on_quote(self, handler: Callable[[OrderBook], None]) -> None:
        if handler in self._handlers['OnQuote']:
            self._handlers['OnQuote'].remove(handler)

    def remove_on_stop(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        if handler in self._handlers['OnStop']:
            self._handlers['OnStop'].remove(handler)

    def remove_on_stop_order(self, handler: Callable[[StopOrder], None]) -> None:
        if handler in self._handlers['OnStopOrder']:
            self._handlers['OnStopOrder'].remove(handler)

    def remove_on_trade(self, handler: Callable[[Trade], None]) -> None:
        if handler in self._handlers['OnTrade']:
            self._handlers['OnTrade'].remove(handler)

    def remove_on_trans_reply(self, handler: Callable[[TransactionReply], None]) -> None:
        if handler in self._handlers['OnTransReply']:
            self._handlers['OnTransReply'].remove(handler)


    def remove_handler(self, event_name: str, handler: Callable) -> None:
        """Remove event handler"""
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)

    def clear_handlers(self, event_name: Optional[Dict[str, Any]] = None) -> None:
        """Clear event handlers"""
        if event_name:
            if event_name in self._handlers:
                self._handlers[event_name].clear()
        else:
            for handlers in self._handlers.values():
                handlers.clear()

    async def _fire_event(self, event_name: str, data: Any) -> None:
        """Fire event to all registered handlers"""
        if event_name in self._handlers:
            for handler in self._handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    # Log error but don't stop other handlers
                    print(f"Error in event handler {handler}: {e}")

    async def handle_event_data(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Handle incoming event data from QUIK"""
        try:
            if event_name == 'OnAccountBalance':
                accBal = AccountBalance.from_dict(event_data)
                await self._fire_event('OnAccountBalance', accBal)

            elif event_name == 'OnAccountPosition':
                accPos = AccountPosition.from_dict(event_data)
                await self._fire_event('OnAccountPosition', accPos)

            elif event_name == 'OnAllTrade':
                trade = AllTrade.from_dict(event_data)
                trade.lua_timestamp = self.created_time()
                await self._fire_event('OnAllTrade', trade)

            elif event_name == 'OnCleanUp':
                await self._fire_event('OnCleanUp', event_data)

            elif event_name == 'OnClose':
                await self._fire_event('OnClose', event_data)

            elif event_name == 'OnConnected':
                await self._fire_event('OnConnected', event_data)

            elif event_name == 'OnDepoLimit':
                dLimit = DepoLimitEx.from_dict(event_data)
                await self._fire_event('OnDepoLimit', dLimit)

            elif event_name == 'OnDepoLimitDelete':
                dLimitDel = DepoLimitDelete.from_dict(event_data)
                await self._fire_event('OnDepoLimitDelete', dLimitDel)

            elif event_name == 'OnDisconnected':
                await self._fire_event('OnDisconnected', event_data)

            elif event_name == 'OnFirm':
                firm = Firm.from_dict(event_data)
                await self._fire_event('OnFirm', firm)

            elif event_name == 'OnFuturesClientHolding':
                futPos = FuturesClientHolding.from_dict(event_data)
                await self._fire_event('OnFuturesClientHolding', futPos)

            elif event_name == 'OnFuturesLimitChange':
                futLimit = FuturesLimits.from_dict(event_data)
                await self._fire_event('OnFuturesLimitChange', futLimit)

            elif event_name == 'OnFuturesLimitDelete':
                limDel = FuturesLimitDelete.from_dict(event_data)
                await self._fire_event('OnFuturesLimitDelete', limDel)

            elif event_name == 'OnInit':
                #  Этот callback никогда не будет вызван так как на момент получения вызова OnInit в lua скрипте
                #  соединение с библиотекой QuikSharp не будет еще установлено. То есть этот callback не имеет смысла.
                pass

            elif event_name == 'OnMoneyLimit':
                mLimit = MoneyLimitEx.from_dict(event_data)
                await self._fire_event('OnMoneyLimit', mLimit)

            elif event_name == 'OnMoneyLimitDelete':
                mLimitDel = MoneyLimitDelete.from_dict(event_data)
                await self._fire_event('OnMoneyLimitDelete', mLimitDel)

            elif event_name == 'OnNegDeal':
                pass

            elif event_name == 'OnNegTrade':
                pass

            elif event_name == 'OnOrder':
                order = Order.from_dict(event_data)
                order.lua_timestamp = self.created_time()
                await self._fire_event('OnOrder', order)
                corellation_id = str(order.trans_id)
                #region Totally untested code or handling manual transactions
                if self.service.storage is not None and not self.service.storage.exists(str(order.trans_id)) :
                    corellation_id = "manual:" + str(order.order_num) +":" + corellation_id
                    fakeTrans = Transaction()
                    fakeTrans.is_manual = True
                    fakeTrans.brokerref = corellation_id
                    self.service.storage.save(corellation_id, fakeTrans)
                #endregion
                tr = self.service.storage.load(corellation_id)
                if tr is not None:
                    tr = Transaction(tr)
                    tr.on_order_call(order)

            elif event_name == 'OnParam':
                data = Param.from_dict(event_data)
                await self._fire_event('OnParam', data)

            elif event_name == 'OnQuote':
                quote = OrderBook.from_dict(event_data)
                quote.lua_timestamp = self.created_time()
                await self._fire_event('OnQuote', quote)

            elif event_name == 'OnStop':
                await self._fire_event('OnStop', event_data)

            elif event_name == 'OnStopOrder':
                order = StopOrder.from_dict(event_data)
                await self._fire_event('OnStopOrder', order)
                corellation_id = str(order.trans_id)
                #region Totally untested code or handling manual transactions
                if self.service.storage is not None and not self.service.storage.exists(str(order.trans_id)) :
                    corellation_id = "manual:" + str(order.order_num) +":" + corellation_id
                    fakeTrans = Transaction()
                    fakeTrans.is_manual = True
                    ## TODO map order properties back to transaction
                    ## ideally, make C# property names consistent (Lua names are set as JSON.NET properties via an attribute)

                    fakeTrans.brokerref = corellation_id
                    self.service.storage.save(corellation_id, fakeTrans)
                #endregion
                tr = self.service.storage.load(corellation_id)
                if tr is not None:
                    tr = Transaction(tr)
                    tr.on_order_call(order)

            elif event_name == 'OnTrade':
                trade = Trade.from_dict(event_data)
                trade.lua_timestamp = self.created_time()
                await self._fire_event('OnTrade', trade)

            elif event_name == 'OnTransReply':
                trans_reply = TransactionReply.from_dict(event_data)
                trans_reply.lua_timestamp = self.created_time()
                await self._fire_event('OnTransReply', trans_reply)

            elif event_name == 'NewCandle':
                candle = Candle.from_dict(event_data)
                candle.lua_timestamp = self.created_time()
                self.service.candles.raise_new_candle_event(candle)

        except Exception as e:
            print(f"Error handling event {event_name}: {e}")

    def created_time(self) -> int:
        """Get current time in milliseconds"""
        now = datetime.now()
        delta = now - self.EPOCH
        return int(delta.total_seconds() * 1000)
