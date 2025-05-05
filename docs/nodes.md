## Node
Node is a class that stores the expression parameters.
All nodes must be hashable.
You can inherit from a base class `dynamic_expressions.nodes.Node`


## Visitor
Visitor is a class that stores behavior for the concrete node.


## Built-in nodes and visitors


### Literal
Literal - constant value in the expression.

::: dynamic_expressions.nodes.LiteralNode
::: dynamic_expressions.visitors.LiteralVisitor


### Any Of
Sequence of the nodes. Returns True if at least one element equals True, else is False

::: dynamic_expressions.nodes.AnyOfNode
::: dynamic_expressions.visitors.AnyOfVisitor


### All Of
Sequence of the nodes. Returns True if all elements equal True, else is False

::: dynamic_expressions.nodes.AllOfNode
::: dynamic_expressions.visitors.AllOfVisitor


### Binary Expression
Binary operator. See the available operation in `dynamic_expressions.types.BinaryExpressionOperator`
::: dynamic_expressions.nodes.BinaryExpressionNode
::: dynamic_expressions.visitors.BinaryExpressionVisitor


### Coalesce
Analogue SQL Coalesce. Returns the first non null item
::: dynamic_expressions.nodes.CoalesceNode
::: dynamic_expressions.visitors.CoalesceVisitor


### Match
Match case operator.
Returns the first value for which the expression returns true
::: dynamic_expressions.nodes.MatchNode
::: dynamic_expressions.visitors.MatchVisitor


### Case
Use only in Match operator
::: dynamic_expressions.nodes.CaseNode
::: dynamic_expressions.visitors.CaseVisitor
