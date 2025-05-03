import abc
import operator
from collections.abc import Callable, Mapping
from typing import Any, ClassVar, Protocol

from dynamic_expressions.nodes import (
    AllOfNode,
    AnyOfNode,
    BinaryExpressionNode,
    CaseNode,
    CoalesceNode,
    LiteralNode,
    MatchNode,
    Node,
)
from dynamic_expressions.types import BinaryExpressionOperator, EmptyContext


class Dispatch[TContext: EmptyContext](Protocol):
    async def __call__(self, node: Node, context: TContext) -> Any: ...  # noqa: ANN401


class Visitor[TNode: Node, TContext: EmptyContext]:
    @abc.abstractmethod
    async def visit(
        self,
        *,
        node: TNode,
        dispatch: Dispatch[TContext],
        context: TContext,
    ) -> Any: ...  # noqa: ANN401


class AnyOfVisitor(Visitor[AnyOfNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: AnyOfNode,
        dispatch: Dispatch[EmptyContext],
        context: object,
    ) -> bool:
        for expr in node.expressions:
            value = await dispatch(expr, context)
            if value:
                return True
        return False


class AllOfVisitor(Visitor[AllOfNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: AllOfNode,
        dispatch: Dispatch[EmptyContext],
        context: EmptyContext,
    ) -> bool:
        for expr in node.expressions:
            value = await dispatch(expr, context)
            if not value:
                return False
        return True


class BinaryExpressionVisitor(Visitor[BinaryExpressionNode, EmptyContext]):
    operator_mapping: ClassVar[
        Mapping[BinaryExpressionOperator, Callable[[Any, Any], bool]]
    ] = {
        "=": operator.eq,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "!=": operator.ne,
        "in": operator.contains,
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "//": operator.floordiv,
        "^": operator.pow,
    }

    async def visit(
        self,
        *,
        node: BinaryExpressionNode,
        dispatch: Dispatch[EmptyContext],
        context: EmptyContext,
    ) -> bool:
        left = await dispatch(node.left, context)
        right = await dispatch(node.right, context)

        operator_callable = self.operator_mapping.get(node.operator)
        if operator_callable is None:
            msg = f"Unknown operator '{node.operator}'"
            raise ValueError(msg)
        return operator_callable(left, right)


class LiteralVisitor(Visitor[LiteralNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: LiteralNode,
        dispatch: Dispatch[EmptyContext],  # noqa: ARG002
        context: EmptyContext,  # noqa: ARG002
    ) -> Any:  # noqa: ANN401
        return node.value


class CoalesceVisitor(Visitor[CoalesceNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: CoalesceNode,
        dispatch: Dispatch[EmptyContext],
        context: EmptyContext,
    ) -> Any:  # noqa: ANN401
        for item in node.items:
            node_result = await dispatch(item, context)
            if node_result:
                return node_result
        return None


class CaseVisitor(Visitor[CaseNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: CaseNode,  # noqa: ARG002
        dispatch: Dispatch[EmptyContext],  # noqa: ARG002
        context: EmptyContext,  # noqa: ARG002
    ) -> Any:  # noqa: ANN401
        msg = "Use CaseNode only in MatchNode"
        raise ValueError(msg)


class MatchVisitor(Visitor[MatchNode, EmptyContext]):
    async def visit(
        self,
        *,
        node: MatchNode,
        dispatch: Dispatch[EmptyContext],
        context: EmptyContext,
    ) -> Any:  # noqa: ANN401
        for case_ in node.cases:
            if await dispatch(case_.expression, context):
                return await dispatch(case_.value, context)
        if node.default is not None:
            return await dispatch(node.default, context)

        msg = "MatchCase doesn't find CaseNode with the appropriate expression"
        raise ValueError(msg)
