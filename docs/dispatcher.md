Dispatcher is the resolver for a node.

The dispatcher takes a node and a context, where the node is an expression, the context is the input parameters for the expression. As an example, we can implement a role model and pass the user as the context.

You can easily override the behavior for a node by overriding the visitor for the node in `__init__` in `VisitorDispatcher`.

::: dynamic_expressions.dispatcher.VisitorDispatcher
