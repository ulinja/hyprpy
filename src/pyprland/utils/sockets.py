"""Interfaces for unix socket operations."""

from abc import ABC
from typing import List
from pathlib import PosixPath
import socket
import logging

from pyprland.utils import assertions


log = logging.getLogger(__name__)


class SocketError(Exception):
    """Raised when a socket operation fails."""
    pass


class AbstractSocket(ABC):

    def __init__(self, signature: str):
        assertions.assert_is_nonempty_string(signature)
        self._signature = signature


class EventSocket(AbstractSocket):

    conncection_timeout_seconds: float = 1.0

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket2.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


    def get_socket(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.conncection_timeout_seconds)
        try:
            s.connect(str(self.path_to_socket))
            s.settimeout(None)
            return s
        except TimeoutError as e:
            log.error(f"Failed to connect to event socket.")
            raise SocketError(f"Socket timed out: {e}")


class CommandSocket(AbstractSocket):

    conncection_timeout_seconds: float = 1.0

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


    def send_command(self, command: str, flags: List[str] = [], args: List[str] = []) -> str:
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
                s.sendall(message.encode('utf-8'))
                return s.recv(4096).decode('utf-8')
            except TimeoutError as e:
                log.error(f"Failed to send command: {command=!r} {flags=} {args=}")
                raise SocketError(f"Socket timed out: {e}")
