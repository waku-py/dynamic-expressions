from typing import Any, Literal, Union

from pydantic import BaseModel, ConfigDict, TypeAdapter

from dynamic_expressions.types import BinaryExpressionOperator


class NodeSchema[T](BaseModel):
    model_config = ConfigDict(strict=True)


class AnyOfNodeSchema[T](NodeSchema[T]):
    type: Literal["any-of"]
    expressions: tuple[T, ...]


class AllOfNodeSchema[T](NodeSchema[T]):
    type: Literal["all-of"]
    expressions: tuple[T, ...]


class BinaryExpressionNodeSchema[T](NodeSchema[T]):
    type: Literal["binary"]
    operator: BinaryExpressionOperator
    left: T
    right: T


class LiteralNodeSchema[T](NodeSchema[T]):
    type: Literal["literal"]
    value: int | str | bool


BUILTIN_SCHEMAS: list[type[NodeSchema[Any]]] = [
    AnyOfNodeSchema,
    AllOfNodeSchema,
    BinaryExpressionNodeSchema,
    LiteralNodeSchema,
]


class PydanticExpressionParser:
    def __init__(self, types: list[type[NodeSchema[Any]]]) -> None:
        self._types = types
        self._needs_rebuild = True
        self._type_adapter: TypeAdapter[NodeSchema[Any]] | None = None

    def add_type(self, cls: type[NodeSchema[Any]]) -> None:
        self._types.append(cls)

    @property
    def type_adapter(self) -> TypeAdapter[NodeSchema[Any]]:
        if self._needs_rebuild or self._type_adapter is None:
            union = Union[tuple(model["union"] for model in self._types)]  # type: ignore[valid-type,index]  # noqa: UP007
            self._type_adapter = TypeAdapter(union)

        return self._type_adapter
