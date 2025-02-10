import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import LiteralNode
from dynamic_expressions.types import EmptyContext


@pytest.mark.parametrize(
    "value",
    [1, 3.12, "abc"],
)
async def test_ok(
    value: object,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    node = LiteralNode(value=value)
    assert value == await dispatcher.visit(node, None)
