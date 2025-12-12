from collections.abc import Sequence
from typing import Any, Protocol

from dynamic_expressions.nodes import Node
from dynamic_expressions.types import EmptyContext
from dynamic_expressions.visitors import Dispatch, Visitor


class OnVisitMiddleware[Context: EmptyContext](Protocol):
    async def on_visit(
        self,
        node: Node,
        context: Context,
        call_next: Dispatch[Context],
    ) -> Any: ...  # noqa: ANN401


class MiddlewareStack[Context: EmptyContext]:
    def __init__(
        self,
        middlewares: Sequence[OnVisitMiddleware[Context]],
        visitor: Visitor[Any, Context],
        dispatch: Dispatch[Context],
    ) -> None:
        self._middlewares = middlewares
        self._visitor = visitor
        self._dispatch = dispatch
        self._index = 0

    async def call(
        self,
        node: Node,
        context: Context,
    ) -> Any:  # noqa: ANN401
        if self._index >= len(self._middlewares):
            return await self._visitor.visit(
                node=node,
                dispatch=self._dispatch,
                context=context,
            )

        middleware = self._middlewares[self._index]
        self._index += 1
        return await middleware.on_visit(
            node=node,
            context=context,
            call_next=self.call,
        )
