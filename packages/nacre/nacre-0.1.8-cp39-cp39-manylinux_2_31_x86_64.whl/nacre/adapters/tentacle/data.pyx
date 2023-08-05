import asyncio

import grpc

from nacre.rpc import tentacle_pb2
from nacre.rpc import tentacle_pb2_grpc

from nautilus_trader.cache.cache cimport Cache
from nautilus_trader.common.clock cimport LiveClock
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.live.data_client cimport LiveDataClient
from nautilus_trader.model.data.base cimport DataType
from nautilus_trader.model.identifiers cimport ClientId
from nautilus_trader.model.identifiers cimport TraderId
from nautilus_trader.msgbus.bus cimport MessageBus

from nacre.model.data.control_command cimport ControlCommand
from nacre.model.data.manual_order cimport ManualOrder
from nacre.model.data.manual_order cimport OrderParams


cdef class TentacleDataClient(LiveDataClient):

    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        grpc_endpoint not None,
        MessageBus msgbus not None,
        Cache cache not None,
        LiveClock clock not None,
        Logger logger not None,
    ):
        super().__init__(
            loop=loop,
            client_id=ClientId("Tentacle"), # hardcode for now
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            logger=logger,
            config={
                "name": "TentacleDataClient-Tentacle",
            }
        )

        self._channel = grpc.aio.insecure_channel(grpc_endpoint)
        self._stub = tentacle_pb2_grpc.TentacleStub(self._channel)

        self._watch_manual_order_task = None
        self._watch_control_command_task = None

    cpdef void _start(self) except *:
        self._log.info("Connecting...")

        self._loop.create_task(self._connect())

    async def _connect(self):
        # self._watch_manual_order_task = self._loop.create_task(self._watch_manual_order)
        # self._watch_control_command_task = self._loop.create_task(self._watch_control_command)

        self.is_connected = True
        self._log.info("Connected.")

    cpdef void _stop(self) except *:
        self._loop.create_task(self._disconnect())

    async def _disconnect(self):
        self._log.info("Disconnecting...")

        # Cancel residual tasks
        if self._watch_manual_order_task and not self._watch_manual_order_task.cancelled():
            self._watch_manual_order_task.cancel()
        if self._watch_control_command_task and not self._watch_control_command_task.cancelled():
            self._watch_control_command_task.cancel()

        # Ensure grpc closed
        self._log.info("Closing GRPC channel(s)...")
        await self._channel.close()

        self.is_connected = False
        self._log.info("Disconnected.")

    cpdef void _reset(self) except *:
        if self.is_connected:
            self._log.error("Cannot reset a connected data client.")
            return

    cpdef void _dispose(self) except *:
        if self.is_connected:
            self._log.error("Cannot dispose a connected data client.")
            return

    async def _watch_manual_order(self, str trader_id):
        cdef OrderParams op
        cdef ManualOrder manual_order
        cdef list orders
        try:
            while True:
                try:
                    tentacle_trader_id = tentacle_pb2.Trader(id=trader_id)
                    manual_order_stream = self._stub.SubscribeManualOrder(tentacle_trader_id)

                    async for manual_order_pb in manual_order_stream:

                        orders = []
                        for order_params_pb in manual_order_pb.orders:
                            op = OrderParams(
                                instrument_id=order_params_pb.instrument_id,
                                amount=order_params_pb.amount,
                                price=order_params_pb.price,
                                stop_price=order_params_pb.stop_price,
                                twap_interval=order_params_pb.twap_interval,
                                twap_slice_amount=order_params_pb.twap_slice_amount,
                            )
                            orders.append(op)

                        manual_order = ManualOrder(orders)
                        self._on_manual_order(manual_order)
                except grpc.aio.UsageError as ex:
                    self._log.error(f"GRPC error {ex}")
                    # TODO: handle other error
        except asyncio.CancelledError as ex:
            self._log.debug(f"Cancelled `_watch_manual_order` for {self.client_id}.")
        except Exception as ex:
            self._log.exception(ex)

    async def _watch_control_command(self, str trader_id):
        pass

    cdef void _on_manual_order(self, ManualOrder manual_order) except *:
        self._handle_data(manual_order)

    cpdef void subscribe(self, DataType data_type) except *:
        if data_type.type == ManualOrder:
            trader_id = data_type.metadata.get("trader_id")
            self.subscribe_manual_order(trader_id)
        elif data_type.type == ControlCommand:
            trader_id = data_type.metadata.get("trader_id")
            self.subscribe_control_command(trader_id)


    cdef void subscribe_manual_order(self, str trader_id) except *:
        Condition.not_none(trader_id, "trader_id")

        # TODO: check if subscribe more than once
        self._watch_manual_order_task = self._loop.create_task(
            self._watch_manual_order(trader_id=trader_id),
        )

        self._log.info(f"Subscribed to tentacle <ManualOrder> data.")

    cdef void subscribe_control_command(self, str trader_id) except *:
        Condition.not_none(trader_id, "trader_id")

        # TODO: check if subscribe more than once
        self._watch_control_command_task = self._loop.create_task(
            self._watch_control_command(trader_id=trader_id),
        )

        self._log.info(f"Subscribed to tentacle <ControlCommand> data.")
