from typing import Any

import pytest
from dynamic_expressions.serialization.pydantic import (
    BUILTIN_SCHEMAS,
    AllOfNodeSchema,
    AnyOfNodeSchema,
    LiteralNodeSchema,
    PydanticExpressionParser,
)


@pytest.fixture
def parser() -> PydanticExpressionParser:
    return PydanticExpressionParser(types=BUILTIN_SCHEMAS)


def test_parse(parser: PydanticExpressionParser) -> None:
    value = """{
  "type": "all-of",
  "expressions": [
    {
      "type": "any-of",
      "expressions": [
        {
          "type": "literal",
          "value": true
        }
      ]
    },
    {
      "type": "literal",
      "value": true
    }
  ]
}
    """
    result = parser.type_adapter.validate_json(value)
    assert result == AllOfNodeSchema[Any](
        type="all-of",
        expressions=(
            AnyOfNodeSchema(
                type="any-of",
                expressions=(LiteralNodeSchema(type="literal", value=True),),
            ),
            LiteralNodeSchema(type="literal", value=True),
        ),
    )


def test_dump(parser: PydanticExpressionParser) -> None:
    node = AllOfNodeSchema[Any](
        type="all-of",
        expressions=(
            AnyOfNodeSchema(
                type="any-of",
                expressions=(LiteralNodeSchema(type="literal", value=True),),
            ),
            LiteralNodeSchema(type="literal", value=True),
        ),
    )
    result = parser.type_adapter.dump_python(
        node,
        mode="json",
        warnings="none",
    )

    assert result == {
        "type": "all-of",
        "expressions": [
            {
                "type": "any-of",
                "expressions": [
                    {
                        "type": "literal",
                        "value": True,
                    },
                ],
            },
            {
                "type": "literal",
                "value": True,
            },
        ],
    }
