from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dynamic_expressions.types import BinaryExpressionOperator


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class Node: ...


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class AnyOfNode(Node):
    expressions: tuple[Node, ...]


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class AllOfNode(Node):
    expressions: tuple[Node, ...]


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class BinaryNode(Node):
    operator: BinaryExpressionOperator
    left: Node
    right: Node


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class LiteralNode(Node):
    value: Any
