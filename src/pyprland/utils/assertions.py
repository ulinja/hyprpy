"""Utility functions for type and sanity checking."""

from typing import Any


def assert_is_bool(value: Any) -> None:
    """Raises an exception if the input is not a boolean.

    :param value: The input to check.
    :raises TypeError: When the input is not a boolean.
    """

    if not isinstance(value, bool):
        raise TypeError(f"Expected the input to be a bool but got a '{type(value)}'.")


def assert_is_int(value: Any) -> None:
    """Raises an exception if the input is not an integer.

    :param value: The input to check.
    :raises TypeError: When the input is not a integer.
    """

    if not isinstance(value, int):
        raise TypeError(f"Expected the input to be an integer but got a '{type(value)}'.")


def assert_is_string(value: Any) -> None:
    """Raises an exception if the input is not a string.

    :param value: The input to check.
    :raises TypeError: When the input is not a string.
    """

    if not isinstance(value, str):
        raise TypeError(f"Expected the input to be a string but got a '{type(value)}'.")


def assert_is_nonempty_string(value: Any) -> None:
    """Raises an exception if the input is not a string of length >= 1.

    :param value: The input to check.
    :raises TypeError: When the input is not a string.
    :raises ValueError: When the input is an empty string.
    """

    assert_is_string(value)

    if not len(value) > 0:
        raise ValueError(f"Input string cannot be empty.")


def assert_is_hexadecimal_string(value: Any) -> None:
    """Raises an exception if the input is not a valid string representation of a hexadecimal number.

    :param value: The input to check.
    :raises TypeError: When the input is not a string.
    :raises ValueError: When the input is empty, or not a valid hexadecimal string.
    """

    assert_is_nonempty_string(value)
    try:
        int(value, 16)
    except ValueError:
        raise ValueError(f"Invalid characters in hexadecimal string: '{value}'")
