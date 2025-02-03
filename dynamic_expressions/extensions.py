from contextlib import AbstractAsyncContextManager
from typing import Protocol, runtime_checkable

from dynamic_expressions.nodes import Node
from dynamic_expressions.types import EmptyContext, ExecutionContext


@runtime_checkable
class OnVisitExtension[Context: EmptyContext](Protocol):
    def on_visit(
        self,
        *,
        node: Node,
        provided_context: Context,
        execution_context: ExecutionContext,
    ) -> AbstractAsyncContextManager[None]: ...
