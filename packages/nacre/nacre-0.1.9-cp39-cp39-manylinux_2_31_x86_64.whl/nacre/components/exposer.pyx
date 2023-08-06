import asyncio

import orjson
import pydantic

from libc.stdint cimport int64_t

from json.decoder import JSONDecodeError
from typing import Dict, Optional, Union

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from prometheus_async import aio

from nautilus_trader.cache.cache cimport Cache
from nautilus_trader.common.clock cimport LiveClock
from nautilus_trader.common.component cimport Component
from nautilus_trader.common.logging cimport CMD
from nautilus_trader.common.logging cimport REQ
from nautilus_trader.common.logging cimport SENT
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.data.messages cimport DataCommand
from nautilus_trader.data.messages cimport Subscribe
from nautilus_trader.model.c_enums.price_type cimport PriceType
from nautilus_trader.model.data.base cimport DataType
from nautilus_trader.model.data.base cimport GenericData
from nautilus_trader.model.data.tick cimport QuoteTick
from nautilus_trader.model.data.tick cimport TradeTick
from nautilus_trader.model.events.account cimport AccountState
from nautilus_trader.model.identifiers cimport ClientId
from nautilus_trader.model.identifiers cimport ComponentId
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.identifiers cimport Symbol
from nautilus_trader.model.identifiers cimport Venue
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport BaseDecimal
from nautilus_trader.msgbus.bus cimport MessageBus
from nautilus_trader.serialization.base cimport _OBJECT_TO_DICT_MAP

from nacre.model.data.manual_order cimport ManualOrder
from nacre.model.data.manual_order cimport OrderParams

from nacre.model.data.manual_order import BatchOrderParamsModel
from nacre.model.data.manual_order import OrderParamsModel

from nacre.metrics.metric_manager cimport MetricManager
from nacre.model.data.tick cimport MarkTick
from nacre.model.report_position cimport ReportedAccount


class ExposerConfig(pydantic.BaseModel):
    host: str = "localhost"
    port: int = 8080


def default(obj):
    if isinstance(obj, BaseDecimal):
        return str(obj.as_decimal())
    raise TypeError


cdef class Exposer(Component):
    """
    Expose
    """
    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        MessageBus msgbus not None,
        Cache cache not None,
        LiveClock clock not None,
        Logger logger not None,
        config: Optional[ExposerConfig] = None,
    ):
        if config is None:
            config = ExposerConfig()
        Condition.type(config, ExposerConfig, "config")
        super().__init__(
            msgbus=msgbus,
            clock=clock,
            logger=logger,
            config=config.dict(),
        )

        self._loop = loop
        self._cache = cache

        self.is_running = False

        self._run_http_server_task = None
        self._runner = None
        self._metric_manager = MetricManager()

        # Required subscriptions
        self._msgbus.subscribe(topic="data.quotes*", handler=self.update_quote_tick, priority=10)
        self._msgbus.subscribe(topic=f"data.<MarkTick>*", handler=self.update_generic_data, priority=10)
        self._msgbus.subscribe(topic="data.trades*", handler=self.update_trade_tick, priority=10)
        self._msgbus.subscribe(topic="reported.*", handler=self.update_report_position, priority=10)

    # -- ABSTRACT METHODS ------------------------------------------------------------------------------

    cpdef void _on_start(self) except *:
        if not self._loop.is_running():
            self._log.warning("Started when loop is not running.")

        self.is_running = True

        self._run_http_server_task = self._loop.create_task(self._run())
        self._log.info(f"Scheduled {self._run_http_server_task}")

    cpdef void _on_stop(self) except *:
        if self.is_running:
            self.is_running = False

        self._loop.create_task(self._stop_server())

    # -- ACTION IMPLEMENTATIONS ------------------------------------------------------------------------

    cpdef void _start(self) except *:
        # Do nothing else for now
        self._on_start()

    cpdef void _stop(self) except *:
        # Do nothing else for now
        self._on_stop()

    cpdef void _reset(self) except *:
        pass

    cpdef void _dispose(self) except *:
        pass
        # Nothing to dispose for now

    async def _run(self):
        self._log.info(f"HTTP server starting...")

        app = web.Application()
        app.add_routes([

            # General
            web.get('/health', self._expose_health),
            web.get('/metrics', aio.web.server_stats),
        ])

        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(
            self._runner,
            self._config.get("host"),
            self._config.get("port"),
        )

        await site.start()
        self._log.info(f"HTTP server started")

    async def _stop_server(self):
        if self._runner:
            await self._runner.shutdown()
        self._log.info(f"HTTP server stopped")

    async def _expose_health(self, request):
        return web.json_response({"status": "OK"})

    cpdef void update_generic_data(self, GenericData data) except *:
        if data.data_type.type == MarkTick:
            self._metric_manager.apply_mark_tick(data.data)

    cpdef void update_quote_tick(self, QuoteTick tick) except *:
        self._metric_manager.apply_quote_tick(tick)

    cpdef void update_trade_tick(self, TradeTick tick) except *:
        self._metric_manager.apply_trade_tick(tick)

    cpdef void update_report_position(self, ReportedAccount account) except *:
        self._metric_manager.apply_report_position(account)
