import abc
import contextlib
import dataclasses
from collections.abc import AsyncIterator, Callable, MutableMapping, Sequence
from datetime import timedelta
from typing import Any

from dynamic_expressions.extensions import OnVisitExtension
from dynamic_expressions.nodes import Node
from dynamic_expressions.serialization import Serializer
from dynamic_expressions.types import EmptyContext, ExecutionContext


@dataclasses.dataclass(slots=True, kw_only=True)
class CachePolicy[Context: EmptyContext]:
    types: tuple[type[Node], ...]
    key: Callable[[Node, Context], str]
    ttl: timedelta
    serializer: Serializer[Any] | None = None


class CacheExtension[
    Context: EmptyContext,
](OnVisitExtension[Context]):
    policies: Sequence[CachePolicy[Context]]
    default_serializer: Serializer[Any]
    _policy_cache: MutableMapping[type[Node], CachePolicy[Context] | None]

    @contextlib.asynccontextmanager
    async def on_visit(
        self,
        *,
        node: Node,
        provided_context: Context,
        execution_context: ExecutionContext,
    ) -> AsyncIterator[None]:
        policy = self._get_policy(node)

        if policy is None or node in execution_context.cache:
            yield
            return

        key = policy.key(node, provided_context)
        serializer = policy.serializer or self.default_serializer
        cached_value = await self.get_cache(key)
        if cached_value is not None:
            execution_context.cache[node] = serializer.deserialize(cached_value)

        yield

        if (
            node in execution_context.cache
            and cached_value != execution_context.cache[node]
        ):
            await self.set_cache(
                key=key,
                value=serializer.serialize(execution_context.cache[node]),
                policy=policy,
            )

    def _get_policy(self, node: Node) -> CachePolicy[Context] | None:
        node_cls = type(node)
        if node_cls in self._policy_cache:
            return self._policy_cache[node_cls]

        self._policy_cache[node_cls] = next(
            (policy for policy in self.policies if isinstance(node, policy.types)),
            None,
        )
        return self._policy_cache[node_cls]

    @abc.abstractmethod
    async def get_cache(self, key: str) -> Any | None: ...  # noqa: ANN401

    @abc.abstractmethod
    async def set_cache(
        self,
        key: str,
        value: Any,  # noqa: ANN401
        policy: CachePolicy[Context],
    ) -> None: ...
