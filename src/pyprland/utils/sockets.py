"""Interfaces for unix socket operations."""

from abc import ABC
from typing import List
from pathlib import PosixPath
import socket
import logging

from pyprland.utils import assertions


log = logging.getLogger(__name__)


class AbstractSocket(ABC):

    def __init__(self, signature: str):
        assertions.assert_is_nonempty_string(signature)
        self._signature = signature


class EventSocket(AbstractSocket):

    conncection_timeout_seconds: float = 0.5

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket2.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


class CommandSocket(AbstractSocket):

    conncection_timeout_seconds: float = 0.5

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


    def send_command(self, command: str, args: List[str] = [], flags: List[str] = []) -> str | None:
        assertions.assert_is_nonempty_string(command)
        for token in args + flags:
            assertions.assert_is_nonempty_string(token)

        message = " ".join(flags) + "/" + command
        if args:
            message += " " + " ".join(args)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(self.conncection_timeout_seconds)
            try:
                s.connect(str(self.path_to_socket))
                s.sendall(message.encode('ascii'))
                return s.recv(4096).decode('ascii')
            except TimeoutError:
                log.error("Failed to send command: socket connection timeout.")
