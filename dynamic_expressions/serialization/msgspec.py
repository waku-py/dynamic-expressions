from typing import Any

import msgspec

from ._serialization import Serializer


class MsgSpecSerializer[T](Serializer[T]):
    def __init__(self, instance_of: type[T]) -> None:
        self.instance_of = instance_of

    def serialize(self, value: T) -> bytes:
        return msgspec.json.encode(value)

    def deserialize(self, value: bytes) -> T:
        return msgspec.json.decode(value, type=self.instance_of)


class MsgSpecScalarSerializer(Serializer[Any]):
    def serialize(self, value: Any) -> bytes:  # noqa: ANN401
        return msgspec.json.encode(value)

    def deserialize(self, value: bytes) -> Any:  # noqa: ANN401
        return msgspec.json.decode(value)
