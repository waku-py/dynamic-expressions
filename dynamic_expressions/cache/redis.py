from collections.abc import Callable, Sequence
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from redis.asyncio import Redis as RedisLib

from dynamic_expressions.cache.base import CacheExtension, CachePolicy
from dynamic_expressions.nodes import Node
from dynamic_expressions.types import EmptyContext

if TYPE_CHECKING:
    Redis = RedisLib[bytes]
else:
    Redis = RedisLib


class RedisCacheExtension[
    Context: EmptyContext,
](CacheExtension[Context]):
    def __init__(
        self,
        key: Callable[[Node, Context], str],
        types: Sequence[type[Node]],
        client: Redis,
        ttl: timedelta,
    ) -> None:
        self.types = tuple(types)
        self.key = key
        self._client = client
        self._ttl = ttl
        self._policy_cache = {}

    async def get_cache(self, key: str) -> Any | None:  # noqa: ANN401
        return await self._client.get(name=key)

    async def set_cache(
        self,
        key: str,
        value: Any,  # noqa: ANN401
        policy: CachePolicy[Context],
    ) -> None:
        await self._client.set(name=key, value=value, ex=policy.ttl)
