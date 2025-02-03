from collections.abc import Mapping
from typing import Any

from dynamic_expressions.schemas import (
    AllOf,
    AnyOf,
    BinaryExpression,
    LiteralExpression,
    expression_adapter,
)
from dynamic_expressions.nodes import (
    AllOfNode,
    AnyOfNode,
    BinaryNode,
    LiteralNode,
    Node,
)
from dynamic_expressions.visitors import (
    AllOfVisitor,
    AnyOfVisitor,
    BinaryExpressionVisitor,
    LiteralVisitor,
    Visitor,
)


def parse_expression(expression: Any) -> Node:  # noqa: ANN401
    expression_ = expression_adapter.validate_python(expression)
    match expression_:
        case LiteralExpression():
            return LiteralNode(value=expression_.value)
        case BinaryExpression():
            return BinaryNode(
                operator=expression_.operator,
                left=parse_expression(expression_.left),
                right=parse_expression(expression_.right),
            )
        case AllOf():
            return AllOfNode(
                expressions=tuple(
                    parse_expression(exp) for exp in expression_.expressions
                ),
            )
        case AnyOf():
            return AnyOfNode(
                expressions=tuple(
                    parse_expression(exp) for exp in expression_.expressions
                ),
            )


def get_default_visitors() -> Mapping[type[Node], Visitor[Any, Any]]:
    return {
        LiteralNode: LiteralVisitor(),
        BinaryNode: BinaryExpressionVisitor(),
        AnyOfNode: AnyOfVisitor(),
        AllOfNode: AllOfVisitor(),
    }
