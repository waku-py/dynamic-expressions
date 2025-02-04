import uuid
from dataclasses import dataclass

import pytest
from dynamic_expressions.serialization.msgspec import (
    MsgSpecScalarSerializer,
    MsgSpecSerializer,
)


@dataclass
class SomeModel:
    id: int


@pytest.mark.parametrize(
    ("instance", "type_"),
    [
        (SomeModel(id=1), SomeModel),
        ([], list[SomeModel]),
        ([SomeModel(id=1), SomeModel(id=1)], list[SomeModel]),
        (uuid.uuid4(), uuid.UUID),
        ([uuid.uuid4()], list[uuid.UUID]),
    ],
)
def test_serialize_instance(
    instance: object,
    type_: type[object],
) -> None:
    serializer = MsgSpecSerializer(type_)

    serialized = serializer.serialize(instance)
    deserialized = serializer.deserialize(serialized)

    assert instance == deserialized


@pytest.mark.parametrize(
    "object_",
    [1, 3.12, True, "str", [1, 2, 3], [1, "2", 3]],
)
def test_serialize_scalar(object_: object) -> None:
    serializer = MsgSpecScalarSerializer()

    serialized = serializer.serialize(object_)
    deserialized = serializer.deserialize(serialized)

    assert object_ == deserialized
