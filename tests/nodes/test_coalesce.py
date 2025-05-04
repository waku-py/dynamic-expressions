import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import CoalesceNode, LiteralNode
from dynamic_expressions.types import EmptyContext


@pytest.mark.parametrize(
    "value",
    [1, 3.12, "abc"],
)
async def test_ok(
    value: object,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    node = CoalesceNode(
        items=(
            LiteralNode(value=None),
            LiteralNode(value=value),
            LiteralNode(value=None),
        ),
    )
    assert value == await dispatcher.visit(node, None)


async def test_return_none(dispatcher: VisitorDispatcher[EmptyContext]) -> None:
    node = CoalesceNode(
        items=(
            LiteralNode(value=None),
            LiteralNode(value=None),
            LiteralNode(value=None),
        ),
    )
    assert await dispatcher.visit(node, None) is None
