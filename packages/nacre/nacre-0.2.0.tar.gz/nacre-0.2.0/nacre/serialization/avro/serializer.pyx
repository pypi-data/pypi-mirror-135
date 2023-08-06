from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.datetime cimport nanos_to_millis
from nautilus_trader.model.events.account cimport AccountState
from nautilus_trader.serialization.base cimport _OBJECT_TO_DICT_MAP

from nacre.serialization.base cimport AsyncSerializer
from nacre.serialization.avro.implementations import account_state
from nacre.serialization.avro.patch_registry import AsyncMessageSerializer
from nacre.serialization.avro.patch_registry import AsyncSchemaRegistryClient
from nacre.serialization.avro.schema import NAUTILUS_AVRO_SCHEMA


_AVRO_TO_DICT_MAP = {
    AccountState: account_state.serialize,
}

_AVRO_TO_SUBJECT_MAP = {
    AccountState: "events.snapshot-value",
}


cdef class AvroSerializer(AsyncSerializer):
    def __init__(self, schema_registry: str):
        self._client = AsyncSchemaRegistryClient(schema_registry)
        self._async_serializer = AsyncMessageSerializer(self._client)

    async def serialize(self, object obj) -> bytes:
        Condition.not_none(obj, "obj")

        cls = type(obj)
        obj_name = type(obj).__name__

        delegate = _AVRO_TO_DICT_MAP.get(cls)
        if delegate is None:
            delegate = _OBJECT_TO_DICT_MAP.get(obj_name)
        if delegate is None:
            raise TypeError(f"Cannot serialize object `{cls}`.")

        obj_dict = delegate(obj)
        schema = NAUTILUS_AVRO_SCHEMA.get(cls)
        if schema is None:
            raise TypeError(f"Cannot get schema for class `{cls}`")

        subject = _AVRO_TO_SUBJECT_MAP.get(cls)
        if subject is None:
            raise TypeError(f"Cannot get subject for class `{cls}`")

        ts_event = obj_dict.get("ts_event")
        if ts_event is not None:
            obj_dict["ts_event"] = nanos_to_millis(ts_event)
        ts_init = obj_dict.get("ts_init")
        if ts_init is not None:
            obj_dict["ts_init"] = nanos_to_millis(ts_init)

        return await self._async_serializer.encode_record_with_schema(subject, schema, obj_dict)

    async def deserialize(self, obj_bytes: bytes) -> object:
        pass

    async def stop(self):
        await self._client.session.aclose()
