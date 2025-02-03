from dataclasses import dataclass


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
    operator: str
    left: Node
    right: Node


@dataclass(slots=True, frozen=True, kw_only=True, unsafe_hash=True)
class LiteralNode(Node):
    value: int | str
