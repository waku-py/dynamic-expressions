import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import BinaryNode, LiteralNode
from dynamic_expressions.types import EmptyContext

random_numbers: list[LiteralNode] = [
    LiteralNode(value=0),
    LiteralNode(value=1),
    LiteralNode(value=3),
    LiteralNode(value=100),
    LiteralNode(value=-1),
    LiteralNode(value=-3),
    LiteralNode(value=-100),
]


@pytest.mark.parametrize("left", random_numbers)
@pytest.mark.parametrize("right", random_numbers)
async def test_add(
    left: LiteralNode,
    right: LiteralNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    node = BinaryNode(operator="+", left=left, right=right)
    assert await dispatcher.visit(node, None) == (left.value + right.value)


@pytest.mark.parametrize("left", random_numbers)
@pytest.mark.parametrize("right", random_numbers)
async def test_eq(
    left: LiteralNode,
    right: LiteralNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    node = BinaryNode(operator="=", left=left, right=right)
    assert await dispatcher.visit(node, None) == (left.value == right.value)
