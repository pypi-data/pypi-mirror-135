from libc.stdint cimport int64_t

from typing import List, Optional

import pydantic

from cpython.datetime cimport timedelta
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.data.base cimport Data
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity


cdef class ManualOrder(Data):
    def __init__(
        self,
        list orders not None,
        int64_t ts_event=0,
        int64_t ts_init=0,
    ):
        super().__init__(ts_event, ts_init)
        self.orders = orders

cdef class OrderParams:

    def __init__(
        self,
        str instrument_id not None,
        str amount not None,
        str price = None,
        str stop_price = None,
        timedelta twap_interval = None,
        str twap_slice_amount = None,
    ):
        self.instrument_id = InstrumentId.from_str_c(instrument_id)

        if amount[0] == "-":
            self.amount = Quantity.from_str_c(amount[1:])
            self.order_side = OrderSide.SELL
        else:
            self.amount = Quantity.from_str_c(amount)
            self.order_side = OrderSide.BUY

        self.price = None
        self.stop_price = None
        self.twap_interval = None
        self.twap_slice_amount = None

        self.order_type = OrderType.MARKET

        if twap_interval is not None and twap_slice_amount is not None:
            self.twap_interval = twap_interval
            self.twap_slice_amount = Quantity.from_str_c(twap_slice_amount)
            self.order_type = OrderType.TWAP

        elif price is not None:
            self.price = Price.from_str_c(price)
            if stop_price is not None:
                self.stop_price = Price.from_str_c(stop_price)
                self.order_type = OrderType.STOP_LIMIT
            else:
                self.order_type = OrderType.LIMIT
        else:
            if stop_price is not None:
                self.stop_price = Price.from_str_c(stop_price)
                self.order_type = OrderType.STOP_MARKET
            else:
                self.order_type = OrderType.MARKET


class OrderParamsModel(pydantic.BaseModel):
    instrument_id: str
    amount: str
    price: Optional[str]
    stop_price: Optional[str]
    twap_interval: Optional[timedelta]
    twap_slice_amount: Optional[str]


class BatchOrderParamsModel(pydantic.BaseModel):
    orders: List[OrderParamsModel]
