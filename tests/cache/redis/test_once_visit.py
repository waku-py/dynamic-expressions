from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import AllOfNode, BinaryExpressionNode, LiteralNode
from dynamic_expressions.types import EmptyContext
from dynamic_expressions.visitors import AllOfVisitor


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
                BinaryExpressionNode(
                    operator="=",
                    left=LiteralNode(value=1),
                    right=LiteralNode(value=1),
                ),
                LiteralNode(value=True),
            ),
        ),
        AllOfNode(
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
@pytest.mark.redis
async def test_ok(
    node: AllOfNode,
    dispatcher: VisitorDispatcher[EmptyContext],
) -> None:
    result1 = cast("bool", await dispatcher.visit(node, None))
    with patch.object(
        AllOfVisitor,
        AllOfVisitor.visit.__name__,
        AsyncMock(return_value=not result1),
    ):
        result2 = await dispatcher.visit(node, None)

    assert result1 == result2
