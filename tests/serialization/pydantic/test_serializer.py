import pytest
from dynamic_expressions.serialization.pydantic import PydanticSerializer
from pydantic import BaseModel


class SomeModel(BaseModel):
    id: int


@pytest.fixture
def serializer() -> PydanticSerializer[SomeModel | list[SomeModel]]:
    return PydanticSerializer[SomeModel | list[SomeModel]](
        instance_of=SomeModel | list[SomeModel]
    )


@pytest.mark.parametrize(
    "instance",
    [
        SomeModel(id=1),
        [],
        [SomeModel(id=1), SomeModel(id=1)],
    ],
)
def test_serialize_instance(
    instance: SomeModel | list[SomeModel],
    serializer: PydanticSerializer[SomeModel | list[SomeModel]],
) -> None:
    serialized = serializer.serialize(instance)
    deserialized = serializer.deserialize(serialized)

    assert instance == deserialized
