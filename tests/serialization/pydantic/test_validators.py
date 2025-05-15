from collections.abc import Callable, Collection, Iterator
from typing import Any

import pytest
from dynamic_expressions.serialization.pydantic import (
    BUILTIN_SCHEMAS,
    AnyOfNodeSchema,
    PydanticExpressionParser,
)


@pytest.fixture
def parser() -> PydanticExpressionParser:
    return PydanticExpressionParser(types=BUILTIN_SCHEMAS)


@pytest.mark.parametrize(
    "collection_factory",
    [list, tuple],
)
def test_ensure_tuple_validator_validate_python(
    collection_factory: Callable[[Iterator[Any]], Collection[Any]],
    parser: PydanticExpressionParser,
) -> None:
    raw_node = {
        "type": "any-of",
        "expressions": collection_factory(
            {"type": "literal", "value": i} for i in range(10)
        ),
    }

    node = parser.type_adapter.validate_python(raw_node)

    assert isinstance(node, AnyOfNodeSchema)
    assert isinstance(node.expressions, tuple)


def test_ensure_tuple_validator_validate_json(
    parser: PydanticExpressionParser,
) -> None:
    data = """
{
    "type": "any-of",
    "expressions": [
        {
            "type": "literal",
            "value": 1
        },
        {
            "type": "literal",
            "value": 2
        }
    ]
}
"""
    node = parser.type_adapter.validate_json(data)

    assert isinstance(node, AnyOfNodeSchema)
    assert isinstance(node.expressions, tuple)
