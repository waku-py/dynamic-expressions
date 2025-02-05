import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import AllOfNode, BinaryNode, LiteralNode
from dynamic_expressions.types import EmptyContext


@pytest.mark.parametrize(
    "node",
    [
        AllOfNode(
            expressions=(
                LiteralNode(value=True),
                LiteralNode(value=True),
                LiteralNode(value=True),
            ),
        ),
        AllOfNode(
            expressions=(
                BinaryNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=1),
                ),
                LiteralNode(value=True),
            ),
        ),
        AllOfNode(
            expressions=(
                BinaryNode(
                    operator="=",
                    left=BinaryNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                    right=BinaryNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                ),
            ),
        ),
    ],
)
async def test_positive(
    node: AllOfNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    assert await dispatcher.visit(node, None)


@pytest.mark.parametrize(
    "node",
    [
        AllOfNode(
            expressions=(
                LiteralNode(value=True),
                LiteralNode(value=False),
                LiteralNode(value=True),
            ),
        ),
        AllOfNode(
            expressions=(
                BinaryNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=2),
                ),
                LiteralNode(value=True),
            ),
        ),
        AllOfNode(
            expressions=(
                BinaryNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=1),
                ),
                LiteralNode(value=False),
            ),
        ),
        AllOfNode(
            expressions=(
                BinaryNode(
                    operator="=",
                    left=BinaryNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                    right=BinaryNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=3),
                    ),
                ),
            ),
        ),
    ],
)
async def test_negative(
    node: AllOfNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    assert not await dispatcher.visit(node, None)
