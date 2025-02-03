from typing import Literal

from pydantic import BaseModel, JsonValue, TypeAdapter


class Expression[T: str](BaseModel):
    type: T


class AnyOf(Expression[Literal["any_of"]]):
    expressions: tuple[JsonValue, ...]


class AllOf(Expression[Literal["all_of"]]):
    expressions: tuple[JsonValue, ...]


class BinaryExpression(Expression[Literal["binary"]]):
    operator: str
    left: JsonValue
    right: JsonValue


class LiteralExpression(Expression[Literal["literal"]]):
    value: int | str


type AnyExpression = AnyOf | AllOf | BinaryExpression | LiteralExpression


expression_adapter: TypeAdapter[AnyExpression] = TypeAdapter(AnyExpression)
