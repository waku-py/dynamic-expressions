import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import AllOfNode, AnyOfNode, BinaryNode, LiteralNode
from dynamic_expressions.types import EmptyContext
from dynamic_expressions.visitors import (
    AllOfVisitor,
    AnyOfVisitor,
    BinaryExpressionVisitor,
    LiteralVisitor,
)


@pytest.fixture
def dispatcher() -> VisitorDispatcher[EmptyContext]:
    return VisitorDispatcher[EmptyContext](
        visitors={
            AllOfNode: AllOfVisitor(),
            AnyOfNode: AnyOfVisitor(),
            BinaryNode: BinaryExpressionVisitor(),
            LiteralNode: LiteralVisitor(),
        },
    )
