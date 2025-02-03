from dataclasses import dataclass, field
from typing import Any, Protocol

from dynamic_expressions.nodes import Node


class EmptyContext(Protocol): ...


@dataclass
class ExecutionContext:
    cache: dict[Node, Any] = field(default_factory=dict)
