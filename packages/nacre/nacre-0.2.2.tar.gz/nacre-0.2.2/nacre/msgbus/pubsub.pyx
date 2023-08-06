import asyncio
from typing import Any, Callable

from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.common.queue cimport Queue
from nautilus_trader.model.identifiers cimport TraderId


cdef class PubSub:
    _sentinel = None

    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        TraderId trader_id not None,
        Logger logger not None,
    ):

        self._log = LoggerAdapter(component_name=type(self).__name__, logger=logger)
        self._log.info("INITIALIZED.")

        self.trader_id = trader_id
        self._loop = loop
        self._queue = Queue(maxsize=10000)  # hardcoded for now

        self._run_queues_task = None
        self.is_running = False

    def get_run_queue_task(self) -> asyncio.Task:
        return self._run_queues_task

    cpdef int qsize(self) except *:
        return self._queue.qsize()

    cpdef bint check_connected(self) except *:
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef bint check_disconnected(self) except *:
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef void start(self) except *:
        if not self._loop.is_running():
            self._log.warning("Started when loop is not running.")

        self.is_running = True  # Queues will continue to process

        # Run queue
        self._run_queues_task = self._loop.create_task(self._run())

        self._log.debug(f"Scheduled {self._run_queues_task}")

        self._on_start()

    cpdef void stop(self) except *:
        if self.is_running:
            self.is_running = False
            self._enqueue_sentinels()

        self._on_stop()

    cpdef void dispose(self) except *:
        pass

    cpdef void _on_start(self) except *:
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef void _on_stop(self) except *:
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef void kill(self) except *:
        self._log.warning("Killing pusub...")
        if self._run_queues_task:
            self._log.debug("Canceling run_queues_task...")
            self._run_queues_task.cancel()
        if self.is_running:
            self.is_running = False  # Avoids sentinel messages for queues
            self.stop()

    cpdef void publish(self, str topic, msg) except *:
        message = (topic, msg,)
        try:
            self._queue.put_nowait(message)
        except asyncio.QueueFull:
            self._log.warning(
                f"Blocking on `_queue.put` as message_queue full at "
                f"{self._queue.qsize()} items.",
            )
            self._loop.create_task(self._queue.put(message))  # Blocking until qsize reduces

    cpdef void subscribe(self, str topic, handler: Callable[[Any], None]) except *:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef void unsubscribe(self, str topic, handler: Callable[[Any], None]) except *:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _run(self):
        self._log.debug(
            f"Message queue processing starting (qsize={self.qsize()})...",
        )
        cdef object message
        cdef str topic
        try:
            while self.is_running:
                message = await self._queue.get()
                if message is None:  # Sentinel message (fast C-level check)
                    continue         # Returns to the top to check `self.is_running`
                else:
                    topic, msg = message
                    await self._handle_publish(topic, msg)

        except asyncio.CancelledError:
            if not self._queue.empty():
                self._log.warning(
                    f"Running canceled with {self.qsize()} message(s) on queue.",
                )
            else:
                self._log.debug(
                    f"Message queue processing stopped (qsize={self.qsize()}).",
                )

        self._log.debug(
            f"Message queue exit (qsize={self.qsize()})...",
        )

    cdef void _enqueue_sentinels(self) except *:
        self._queue.put_nowait(self._sentinel)
        self._log.debug(f"Sentinel message placed on message queue.")

    async def _handle_publish(self, str topic, object msg):
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef bint can_handle(self, str topic) except *:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover
