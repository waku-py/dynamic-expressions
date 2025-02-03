import functools
from collections.abc import Mapping, Sequence
from contextlib import AsyncExitStack
from typing import Any

from dynamic_expressions.extensions import (
    OnVisitExtension,
)
from dynamic_expressions.nodes import Node
from dynamic_expressions.types import EmptyContext, ExecutionContext
from dynamic_expressions.visitors import Visitor


class VisitorDispatcher[Context: EmptyContext]:
    def __init__(
        self,
        visitors: Mapping[type[Node], Visitor[Any, Context]],
        extensions: Sequence[OnVisitExtension[Context]] = (),
    ) -> None:
        self._visitors = visitors
        self._on_visit_exts = extensions

    async def visit(
        self,
        node: Node,
        context: Context,
    ) -> Any:  # noqa: ANN401
        execution_context = ExecutionContext()
        return await self._visit(
            node=node,
            context=context,
            execution_context=execution_context,
        )

    async def _visit(
        self,
        node: Node,
        context: Context,
        execution_context: ExecutionContext,
    ) -> Any:  # noqa: ANN401
        async with AsyncExitStack() as stack:
            for ext in self._on_visit_exts:
                await stack.enter_async_context(
                    ext.on_visit(
                        node=node,
                        provided_context=context,
                        execution_context=execution_context,
                    )
                )

            if node in execution_context.cache:
                return execution_context.cache[node]

            visitor = self._visitors[type(node)]
            result = await visitor.visit(
                node=node,
                context=context,
                dispatch=functools.partial(
                    self._visit,
                    execution_context=execution_context,
                ),
            )
            execution_context.cache[node] = result
            return result
