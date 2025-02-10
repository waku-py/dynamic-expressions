import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import AnyOfNode, BinaryExpressionNode, LiteralNode
from dynamic_expressions.types import EmptyContext


@pytest.mark.parametrize(
    "node",
    [
        AnyOfNode(
            expressions=(
                LiteralNode(value=True),
                LiteralNode(value=True),
                LiteralNode(value=True),
            ),
        ),
        AnyOfNode(
            expressions=(
                BinaryExpressionNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=1),
                ),
                LiteralNode(value=True),
            ),
        ),
        AnyOfNode(
            expressions=(
                BinaryExpressionNode(
                    operator="=",
                    left=BinaryExpressionNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                    right=BinaryExpressionNode(
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
    node: AnyOfNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    assert await dispatcher.visit(node, None)


@pytest.mark.parametrize(
    "node",
    [
        AnyOfNode(
            expressions=(
                LiteralNode(value=False),
                LiteralNode(value=False),
                LiteralNode(value=False),
            ),
        ),
        AnyOfNode(
            expressions=(
                BinaryExpressionNode(
                    operator=">",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=2),
                ),
                LiteralNode(value=False),
            ),
        ),
        AnyOfNode(
            expressions=(
                BinaryExpressionNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=2),
                ),
                LiteralNode(value=False),
            ),
        ),
        AnyOfNode(
            expressions=(
                BinaryExpressionNode(
                    operator="!=",
                    left=BinaryExpressionNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                    right=BinaryExpressionNode(
                        operator="=",
                        left=LiteralNode(value=1),
                        right=LiteralNode(value=1),
                    ),
                ),
            ),
        ),
    ],
)
async def test_negative(
    node: AnyOfNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    assert not await dispatcher.visit(node, None)
