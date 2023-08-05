import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Binance
import QuantConnect.Brokerages.Binance.Messages
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Generic

QuantConnect_Brokerages_Binance__EventContainer_Callable = typing.TypeVar("QuantConnect_Brokerages_Binance__EventContainer_Callable")
QuantConnect_Brokerages_Binance__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Brokerages_Binance__EventContainer_ReturnType")


class BinanceWebSocketWrapper(QuantConnect.Brokerages.WebSocketClientWrapper):
    """Wrapper class for a Binance websocket connection"""

    @property
    def ConnectionId(self) -> str:
        """The unique Id for the connection"""
        ...

    @property
    def ConnectionHandler(self) -> QuantConnect.Brokerages.IConnectionHandler:
        """The handler for the connection"""
        ...

    def __init__(self, connectionHandler: QuantConnect.Brokerages.IConnectionHandler) -> None:
        """Initializes a new instance of the BinanceWebSocketWrapper class."""
        ...


class BinanceBrokerage(QuantConnect.Brokerages.BaseWebsocketsBrokerage, QuantConnect.Interfaces.IDataQueueHandler):
    """Binance utility methods"""

    @property
    def TickLocker(self) -> System.Object:
        """
        Locking object for the Ticks list in the data queue handler
        
        This field is protected.
        """
        ...

    @property
    def IsConnected(self) -> bool:
        ...

    @typing.overload
    def __init__(self) -> None:
        """Constructor for brokerage"""
        ...

    @typing.overload
    def __init__(self, apiKey: str, apiSecret: str, restApiUrl: str, webSocketBaseUrl: str, algorithm: QuantConnect.Interfaces.IAlgorithm, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Constructor for brokerage
        
        :param apiKey: api key
        :param apiSecret: api secret
        :param restApiUrl: The rest api url
        :param webSocketBaseUrl: The web socket base url
        :param algorithm: the algorithm instance is required to retrieve account type
        :param aggregator: the aggregator for consolidating ticks
        :param job: The live job packet
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was submitted for cancellation, false otherwise.
        """
        ...

    def Connect(self) -> None:
        """Creates wss connection"""
        ...

    def Disconnect(self) -> None:
        """Closes the websockets connection"""
        ...

    def Dispose(self) -> None:
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """Gets all open positions"""
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """Gets the total account cash balance for specified account type"""
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """Gets all orders not yet closed"""
        ...

    def OnMessage(self, sender: typing.Any, e: QuantConnect.Brokerages.WebSocketMessage) -> None:
        """
        Wss message handler
        
        This method is protected.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        ...

    @typing.overload
    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: typing.Callable[[System.Object, System.EventArgs], None]) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    @typing.overload
    def Subscribe(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> bool:
        """
        Not used
        
        This method is protected.
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...


class BinanceBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory method to create binance Websockets brokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """provides brokerage connection data"""
        ...

    def __init__(self) -> None:
        """Factory constructor"""
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """Create the Brokerage instance"""
        ...

    def Dispose(self) -> None:
        """Not required"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        The brokerage model
        
        :param orderProvider: The order provider
        """
        ...


class BinanceOrderSubmitEventArgs(System.Object):
    """Represents a binance submit order event data"""

    @property
    def BrokerId(self) -> str:
        """Original brokerage id"""
        ...

    @BrokerId.setter
    def BrokerId(self, value: str):
        """Original brokerage id"""
        ...

    @property
    def Order(self) -> QuantConnect.Orders.Order:
        """The lean order"""
        ...

    @Order.setter
    def Order(self, value: QuantConnect.Orders.Order):
        """The lean order"""
        ...

    def __init__(self, brokerId: str, order: QuantConnect.Orders.Order) -> None:
        """
        Order Event Constructor.
        
        :param brokerId: Binance order id returned from brokerage
        :param order: Order for this order placement
        """
        ...


class BinanceRestApiClient(System.Object, System.IDisposable):
    """Binance REST API implementation"""

    @property
    def OrderSubmit(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Brokerages.Binance.BinanceOrderSubmitEventArgs], None], None]:
        """Event that fires each time an order is filled"""
        ...

    @OrderSubmit.setter
    def OrderSubmit(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Brokerages.Binance.BinanceOrderSubmitEventArgs], None], None]):
        """Event that fires each time an order is filled"""
        ...

    @property
    def OrderStatusChanged(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Orders.OrderEvent], None], None]:
        """Event that fires each time an order is filled"""
        ...

    @OrderStatusChanged.setter
    def OrderStatusChanged(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Orders.OrderEvent], None], None]):
        """Event that fires each time an order is filled"""
        ...

    @property
    def Message(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Brokerages.BrokerageMessageEvent], None], None]:
        """Event that fires when an error is encountered in the brokerage"""
        ...

    @Message.setter
    def Message(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Brokerages.BrokerageMessageEvent], None], None]):
        """Event that fires when an error is encountered in the brokerage"""
        ...

    @property
    def KeyHeader(self) -> str:
        """Key Header"""
        ...

    @property
    def ApiSecret(self) -> str:
        """
        The api secret
        
        This field is protected.
        """
        ...

    @ApiSecret.setter
    def ApiSecret(self, value: str):
        """
        The api secret
        
        This field is protected.
        """
        ...

    @property
    def ApiKey(self) -> str:
        """
        The api key
        
        This field is protected.
        """
        ...

    @ApiKey.setter
    def ApiKey(self, value: str):
        """
        The api key
        
        This field is protected.
        """
        ...

    @property
    def SessionId(self) -> str:
        """Represents UserData Session listen key"""
        ...

    @SessionId.setter
    def SessionId(self, value: str):
        """Represents UserData Session listen key"""
        ...

    def __init__(self, symbolMapper: QuantConnect.Brokerages.SymbolPropertiesDatabaseSymbolMapper, securityProvider: QuantConnect.Securities.ISecurityProvider, apiKey: str, apiSecret: str, restApiUrl: str) -> None:
        """
        Initializes a new instance of the BinanceRestApiClient class.
        
        :param symbolMapper: The symbol mapper.
        :param securityProvider: The holdings provider.
        :param apiKey: The Binance API key
        :param apiSecret: The The Binance API secret
        :param restApiUrl: The Binance API rest url
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was submitted for cancellation, false otherwise.
        """
        ...

    def CreateListenKey(self) -> None:
        """Start user data stream"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """Gets all open positions"""
        ...

    def GetCashBalance(self) -> QuantConnect.Brokerages.Binance.Messages.AccountInformation:
        """Gets the total account cash balance for specified account type"""
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Binance.Messages.Kline]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Binance.Messages.OpenOrder]:
        """Gets all orders not yet closed"""
        ...

    def GetTickers(self) -> typing.List[QuantConnect.Brokerages.Binance.Messages.PriceTicker]:
        """Provides the current tickers price"""
        ...

    def OnMessage(self, e: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Event invocator for the Message event
        
        This method is protected.
        
        :param e: The error
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def SessionKeepAlive(self) -> bool:
        """Check User Data stream listen key is alive"""
        ...

    def StopSession(self) -> None:
        """Stops the session"""
        ...


class _EventContainer(typing.Generic[QuantConnect_Brokerages_Binance__EventContainer_Callable, QuantConnect_Brokerages_Binance__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Brokerages_Binance__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Brokerages_Binance__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Brokerages_Binance__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


