"""Utilities for invoking shell commands."""

import logging
from typing import Tuple
import subprocess

from pyprland.exceptions import NonZeroStatusException


log = logging.getLogger(__name__)


def run_or_fail(command: list[str]) -> Tuple[str, str]:
    """Runs the specified shell command successfully and returns its output, or raises an exception.

    :param command: The command to run, as a list of string tokens.
    :return: A tuple containing the command's output on stdout and stderr respectively.
    :raises pyprland.exceptions.shell.NonZeroStatusException: When the invoked command returned a non-zero
    exit status.
    :raises TypeError: When the input is not a list of strings.
    :raises ValueError: When the input list is empty.
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
