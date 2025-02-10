import abc
from collections.abc import Sequence
from typing import Any, Literal, Union, overload

from pydantic import BaseModel, ConfigDict, TypeAdapter

from dynamic_expressions.nodes import (
    AllOfNode,
    AnyOfNode,
    BinaryExpressionNode,
    LiteralNode,
    Node,
)
from dynamic_expressions.types import BinaryExpressionOperator

from ._serialization import Serializer


class NodeSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    @abc.abstractmethod
    def to_node(self) -> Node: ...


class AnyOfNodeSchema[T: NodeSchema](NodeSchema):
    type: Literal["any-of"]
    expressions: tuple[T, ...]

    def to_node(self) -> AnyOfNode:
        return AnyOfNode(expressions=tuple(expr.to_node() for expr in self.expressions))


class AllOfNodeSchema[T: NodeSchema](NodeSchema):
    type: Literal["all-of"]
    expressions: tuple[T, ...]

    def to_node(self) -> AllOfNode:
        return AllOfNode(expressions=tuple(expr.to_node() for expr in self.expressions))


class BinaryExpressionNodeSchema[T: NodeSchema](NodeSchema):
    type: Literal["binary"]
    operator: BinaryExpressionOperator
    left: T
    right: T

    def to_node(self) -> BinaryExpressionNode:
        return BinaryExpressionNode(
            operator=self.operator,
            left=self.left.to_node(),
            right=self.right.to_node(),
        )


class LiteralNodeSchema[T](NodeSchema):
    type: Literal["literal"]
    value: int | str | bool

    def to_node(self) -> LiteralNode:
        return LiteralNode(value=self.value)


BUILTIN_SCHEMAS: Sequence[type[NodeSchema]] = [
    AnyOfNodeSchema,
    AllOfNodeSchema,
    BinaryExpressionNodeSchema,
    LiteralNodeSchema,
]


class PydanticExpressionParser:
    def __init__(self, types: Sequence[type[NodeSchema]]) -> None:
        self._types = list(types)
        self._needs_rebuild = True
        self._type_adapter: TypeAdapter[NodeSchema] | None = None

    def add_type(self, cls: type[NodeSchema]) -> None:
        self._types.append(cls)

    @property
    def type_adapter(self) -> TypeAdapter[NodeSchema]:
        if self._needs_rebuild or self._type_adapter is None:
            union = Union[tuple(model["union"] for model in self._types)]  # type: ignore[valid-type,index]  # noqa: UP007
            self._type_adapter = TypeAdapter(union)

        return self._type_adapter


class PydanticSerializer[T](Serializer[T]):
    @overload
    def __init__(self, instance_of: type[T]) -> None: ...

    @overload
    def __init__(self, instance_of: Any) -> None: ...  # noqa: ANN401

    def __init__(self, instance_of: Any) -> None:
        self._type_adapter = TypeAdapter[T](instance_of)

    def serialize(self, value: T) -> bytes:
        return self._type_adapter.dump_json(value, by_alias=True)

    def deserialize(self, value: bytes) -> T:
        return self._type_adapter.validate_json(value, strict=True)
