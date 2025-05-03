from collections.abc import AsyncIterator
from datetime import timedelta

import pytest
from dynamic_expressions.cache import CachePolicy
from dynamic_expressions.cache.redis import RedisCacheExtension, RedisClient
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
from dynamic_expressions.serialization.msgspec import MsgSpecScalarSerializer
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
from testcontainers.redis import AsyncRedisContainer  # type: ignore[import-untyped]


@pytest.fixture(scope="session")
def redis_image() -> str:
    return "valkey/valkey:8.0.1-bookworm"


@pytest.fixture(scope="session")
async def redis_container(redis_image: str) -> AsyncIterator[RedisClient]:
    with AsyncRedisContainer(image=redis_image) as redis_container:
        yield redis_container


@pytest.fixture
async def redis(redis_container: AsyncRedisContainer) -> AsyncIterator[RedisClient]:
    async with await redis_container.get_async_client() as client:
        yield client
        await client.flushall()


@pytest.fixture
def dispatcher(redis: RedisClient) -> VisitorDispatcher[EmptyContext]:
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
        extensions=[
            RedisCacheExtension(
                client=redis,
                policies=[
                    CachePolicy[EmptyContext](
                        types=(
                            AllOfNode,
                            AnyOfNode,
                            BinaryExpressionNode,
                            LiteralNode,
                        ),
                        key=lambda node, _: str(hash(node)),
                        ttl=timedelta(seconds=1),
                    ),
                ],
                default_serializer=MsgSpecScalarSerializer(),
            ),
        ],
    )
