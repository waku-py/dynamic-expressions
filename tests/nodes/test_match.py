import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import CaseNode, LiteralNode, MatchNode
from dynamic_expressions.types import EmptyContext


async def test_ok(dispatcher: VisitorDispatcher[EmptyContext]) -> None:
    return_value = 5
    node = MatchNode(
        cases=(
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=1),
            ),
            CaseNode(
                expression=LiteralNode(value=True),
                value=LiteralNode(value=return_value),
            ),
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=3),
            ),
        ),
    )
    assert return_value == await dispatcher.visit(node, None)


async def test_default_ok(dispatcher: VisitorDispatcher[EmptyContext]) -> None:
    return_value = 5
    node = MatchNode(
        cases=(
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=1),
            ),
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=2),
            ),
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=3),
            ),
        ),
        default=LiteralNode(value=return_value),
    )
    assert return_value == await dispatcher.visit(node, None)


async def test_default_err(dispatcher: VisitorDispatcher[EmptyContext]) -> None:
    node = MatchNode(
        cases=(
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=1),
            ),
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=2),
            ),
            CaseNode(
                expression=LiteralNode(value=False),
                value=LiteralNode(value=3),
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="MatchCase doesn't find CaseNode with the appropriate expression",
    ):
        await dispatcher.visit(node, None)


async def test_case_without_match_err(
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    node = CaseNode(
        expression=LiteralNode(value=False),
        value=LiteralNode(value=1),
    )

    with pytest.raises(
        ValueError,
        match="Use CaseNode only in MatchNode",
    ):
        await dispatcher.visit(node, None)
