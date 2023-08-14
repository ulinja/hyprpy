"""Utilities for shell-related operations."""

import logging
import os
from typing import Tuple
import subprocess

import hyprpy.utils.assertions as assertions


log = logging.getLogger(__name__)


class NonZeroStatusException(Exception):
    """Raised when a shell invocation returns a non-zero exit status."""


class EnvironmentException(Exception):
    """Raised when an expected environment variable could not be found."""


def run_or_fail(command: list[str]) -> Tuple[str, str]:
    """Runs the specified ``command`` successfully and returns its output, or raises an exception.

    Each command token must be an item in the ``command`` list. Each token is treated as a contiguous
    string by the shell (even if it contains whitespace).

    Example:

    .. code-block:: python

        from hyprpy.utils.shell import run_or_fail

        cmd = ['echo', 'Hello world!']
        response = run_or_fail(cmd)
        print(response)[0]
        # Output: 'Hello world!\\n'
        print(response)[1]
        # Output: ''

    :param command: The command to run, as a list of string tokens.
    :return: A tuple containing the command's output on stdout and stderr respectively.
    :raises: :class:`NonZeroStatusException` if the invoked command returned a non-zero exit status.
    :raises: :class:`TypeError` if ``command`` is not a list of strings.
    :raises: :class:`ValueError` if ``command`` is an empty list.
    """

    if not isinstance (command, list):
        log.error(f"Failed to parse command: {command}")
        raise TypeError("Command must be a list of string tokens.")
    for token in command:
        if not isinstance(token, str):
            log.error(f"Failed to parse command: {command}")
            raise TypeError("Command tokens must be strings.")
    if len(command) == 0:
        log.error(f"Failed to parse command: {command}")
        raise ValueError("Command cannot be without tokens.")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.SubprocessError as e:
        raise NonZeroStatusException(str(e))

    return (result.stdout, result.stderr)


def get_env_var_or_fail(name: str) -> str:
    """Retrieves the value of the environment variable ``name`` or raises an exception if it is undefined.

    :param name: Name of the environment variable to retrieve.
    :return: The current value of the environment variable.
    :raises: :class:`EnvironmentException` if the specified environment variable is undefined.
    :raises: :class:`TypeError` if ``name`` is not a string.
    :raises: :class:`ValueError` if ``name`` is an empty string.
    """

    assertions.assert_is_nonempty_string(name)
    value = os.getenv(name, None)
    if value is None:
        raise EnvironmentException(f"Environment variable '{name}' is undefined.")
    return value
