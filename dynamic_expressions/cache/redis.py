from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from redis.asyncio import Redis

from dynamic_expressions.cache.base import CacheExtension, CachePolicy
from dynamic_expressions.serialization import Serializer
from dynamic_expressions.types import EmptyContext

if TYPE_CHECKING:
    RedisClient = Redis[bytes]
else:
    RedisClient = Redis


class RedisCacheExtension[
    Context: EmptyContext,
](CacheExtension[Context]):
    def __init__(
        self,
        client: RedisClient,
        policies: Sequence[CachePolicy[Context]],
        default_serializer: Serializer[Any],
    ) -> None:
        self.policies = policies
        self.default_serializer = default_serializer
        self._client = client
        self._policy_cache = {}

    async def get_cache(self, key: str) -> bytes | None:
        return await self._client.get(name=key)

    async def set_cache(
        self,
        key: str,
        value: bytes,
        policy: CachePolicy[Context],
    ) -> None:
        await self._client.set(name=key, value=value, ex=policy.ttl)
