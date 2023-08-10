"""General validators used for pydantic type annotations."""

from typing_extensions import Annotated

from pydantic import AfterValidator


def non_empty_string(value: str) -> str:
    assert len(value) > 0, f"Expected a non-empty string."
    return value

NonEmptyString = Annotated[str, AfterValidator(non_empty_string)]


def valid_hex_string(value: str) -> str:
    int(value, 16)
    return value

HexString = Annotated[str, AfterValidator(valid_hex_string), AfterValidator(non_empty_string)]
