"""Utility functions for type- and sanity checking."""

from typing import Any
import inspect


def assert_is_bool(value: Any) -> None:
    """Raises an exception if ``value`` is not a boolean.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not a boolean.
    """

    if not isinstance(value, bool):
        raise TypeError(f"Expected the input to be a bool but got a '{type(value)}'.")


def assert_is_int(value: Any) -> None:
    """Raises an exception if ``value`` is not an integer.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not a integer.
    """

    if not isinstance(value, int):
        raise TypeError(f"Expected the input to be an integer but got a '{type(value)}'.")


def assert_is_string(value: Any) -> None:
    """Raises an exception if ``value`` is not a string.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not a string.
    """

    if not isinstance(value, str):
        raise TypeError(f"Expected the input to be a string but got a '{type(value)}'.")


def assert_is_nonempty_string(value: Any) -> None:
    """Raises an exception if ``value`` is not a string of length >= 1.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not a string.
    :raises: :class:`ValueError` if ``value`` is an empty string.
    """

    assert_is_string(value)

    if not len(value) > 0:
        raise ValueError(f"Input string cannot be empty.")


def assert_is_hexadecimal_string(value: Any) -> None:
    """Raises an exception if ``value`` is not a valid string representation of a hexadecimal number.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not a string.
    :raises: :class:`ValueError` if ``value`` is empty, or not a valid hexadecimal string.
    """

    assert_is_nonempty_string(value)
    try:
        int(value, 16)
    except ValueError:
        raise ValueError(f"Invalid characters in hexadecimal string: '{value}'")


def assert_is_callable(value: Any) -> None:
    """Raises an exception if ``value`` is not callable.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not callable.
    """

    if not callable(value):
        raise TypeError("Object is not callable.")


def assert_is_callable_and_has_first_param_sender(value: Any) -> None:
    """Raises an exception if ``value` is not a callable which has ``sender`` as its first positional argument.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not callable.
    :raises: :class:`ValueError` if ``value` does not accept ``sender`` as its first positional argument.
    """

    assert_is_callable(value)

    sig = inspect.signature(value)
    params = list(sig.parameters)
    
    if len(params) == 0 or params[0] != 'sender':
        raise ValueError("Callable must accept 'sender' as the first parameter.")


def assert_is_callable_and_accepts_kwargs(value: Any) -> None:
    """Raises an exception if ``value`` is not a callable which accepts keyword arguments.

    :param value: The input to check.
    :raises: :class:`TypeError` if ``value`` is not callable.
    :raises: :class:`ValueError` if ``value`` does not accept keyword arguments.
    """

    assert_is_callable(value)

    def _get_func_parameters(func, remove_first):
        parameters = tuple(inspect.signature(func).parameters.values())
        if remove_first:
            parameters = parameters[1:]
        return parameters

    def _get_callable_parameters(meth_or_func):
        is_method = inspect.ismethod(meth_or_func)
        func = meth_or_func.__func__ if is_method else meth_or_func
        return _get_func_parameters(func, remove_first=is_method)

    if not any(p for p in _get_callable_parameters(value) if p.kind == p.VAR_KEYWORD):
        raise ValueError("Function must accept keyword arguments (**kwargs).")
