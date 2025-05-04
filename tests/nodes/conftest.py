import pytest
from dynamic_expressions.dispatcher import VisitorDispatcher
from dynamic_expressions.nodes import (
    AllOfNode,
    AnyOfNode,
    BinaryExpressionNode,
    CaseNode,
    CoalesceNode,
    LiteralNode,
    MatchNode,
)
from dynamic_expressions.types import EmptyContext
from dynamic_expressions.visitors import (
    AllOfVisitor,
    AnyOfVisitor,
    BinaryExpressionVisitor,
    CaseVisitor,
    CoalesceVisitor,
    LiteralVisitor,
    MatchVisitor,
)


@pytest.fixture
def dispatcher() -> VisitorDispatcher[EmptyContext]:
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
    )
