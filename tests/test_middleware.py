from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.middlewares import OnVisitMiddleware
from dynamic_expressions.nodes import (
    AllOfNode,
    AnyOfNode,
    BinaryExpressionNode,
    CaseNode,
    CoalesceNode,
    LiteralNode,
    MatchNode,
    Node,
)
from dynamic_expressions.types import EmptyContext
from dynamic_expressions.visitors import (
    AllOfVisitor,
    AnyOfVisitor,
    BinaryExpressionVisitor,
    CaseVisitor,
    CoalesceVisitor,
    Dispatch,
    LiteralVisitor,
    MatchVisitor,
)


@dataclass
class Result:
    value: object


class WrapResultMiddleware(OnVisitMiddleware[EmptyContext]):
    async def on_visit(
        self,
        node: Node,
        context: EmptyContext,
        call_next: Dispatch[EmptyContext],
    ) -> Any:  # noqa: ANN401
        return Result(await call_next(node, context))


class AdderMiddleware(OnVisitMiddleware[EmptyContext]):
    def __init__(self, suffix: str) -> None:
        self._suffix = suffix

    async def on_visit(
        self,
        node: Node,
        context: EmptyContext,
        call_next: Dispatch[EmptyContext],
    ) -> Any:  # noqa: ANN401
        return await call_next(node, context) + self._suffix


class EarlyReturnMiddleware(OnVisitMiddleware[EmptyContext]):
    def __init__(self, return_value: object, return_if: Callable[[Node], bool]) -> None:
        self._return_value = return_value
        self._return_if = return_if

    async def on_visit(
        self,
        node: Node,
        context: EmptyContext,
        call_next: Dispatch[EmptyContext],
    ) -> Any:  # noqa: ANN401
        if self._return_if(node):
            return self._return_value
        return await call_next(node, context)


def create_dispatcher(
    middlewares: Sequence[OnVisitMiddleware[EmptyContext]],
) -> VisitorDispatcher[EmptyContext]:
    return VisitorDispatcher[EmptyContext](
        visitors={
            AllOfNode: AllOfVisitor(),
            AnyOfNode: AnyOfVisitor(),
            BinaryExpressionNode: BinaryExpressionVisitor(),
            LiteralNode: LiteralVisitor(),
            CoalesceNode: CoalesceVisitor(),
            CaseNode: CaseVisitor(),
            MatchNode: MatchVisitor(),
        },
        middlewares=middlewares,
    )


async def test_wrap_middleware() -> None:
    dispatcher = create_dispatcher([WrapResultMiddleware()])
    node = LiteralNode(value="string")

    result = await dispatcher.visit(node, context=None)

    assert isinstance(result, Result)
    assert result.value == node.value


async def test_middleware_ordering() -> None:
    suffix = "abc"
    dispatcher = create_dispatcher(
        [AdderMiddleware(char) for char in suffix],
    )
    node = LiteralNode(value="string")

    result = await dispatcher.visit(node, context=None)

    assert result == node.value + suffix[::-1]


async def test_early_return_from_middleware() -> None:
    dispatcher = create_dispatcher(
        [
            EarlyReturnMiddleware(
                return_value=None,
                return_if=lambda node: (
                    isinstance(node, LiteralNode) and node.value == 1
                ),
            )
        ],
    )

    result = await dispatcher.visit(LiteralNode(value=1), context=None)
    assert result is None

    result = await dispatcher.visit(LiteralNode(value=2), context=None)
    assert result is not None
