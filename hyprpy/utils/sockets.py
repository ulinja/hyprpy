"""Interfaces for UNIX socket operations with Hyprland's event and command sockets.

Hyprland offers two UNIX sockets:

1. `EventSocket <https://wiki.hyprland.org/IPC/#tmphyprhissocket2sock>`_: This socket broadcasts various events occurring in the Hyprland session, 
   e.g., windows or workspaces getting created or destroyed.
2. `CommandSocket <https://wiki.hyprland.org/IPC/#tmphyprhissocketsock>`_: This socket can be written to in order to influence Hyprland's behavior 
   or send queries about the current state.

More information can be found at https://wiki.hyprland.org/IPC/

Examples:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland()

    # For command socket
    cs = instance.command_socket
    response = cs.send_command("dispatch", flags=["--single-instance"], args=["exec", "kitty"])

    # For event socket
    es = instance.event_socket
    s = es.get_socket() # returns a connected socket object
    while True:
        bytes = s.recv(4096)
        print(bytes)
"""

from abc import ABC
from typing import List
from pathlib import PosixPath
import socket
import logging

from hyprpy.utils import assertions


log = logging.getLogger(__name__)


class SocketError(Exception):
    """Raised when a socket operation fails."""
    pass


class AbstractSocket(ABC):
    """Base class for concrete socket classes.

    Holds shared attributes of the specific socket types.
    """

    def __init__(self, signature: str):
        assertions.assert_is_nonempty_string(signature)
        #: The Hyperland Instance Signature
        self._signature = signature


class EventSocket(AbstractSocket):
    """Interface to Hyprland's event socket.

    This socket broadcasts events about the ongoing Hyprland session, such as
    windows or workspaces being created or destroyed.
    """

    #: Maximum time in seconds to wait for a socket connection
    connection_timeout_seconds: float = 1.0

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket2.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


    def get_socket(self):
        """Creates and returns a connection to the event socket.

        :return: A **connected** :class:`socket.socket` object.
        :rtype: socket.socket
        :raises: :class:`socket.SocketError` if the connection process takes too long.
        """

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.connection_timeout_seconds)
        try:
            s.connect(str(self.path_to_socket))
            s.settimeout(None)
            return s
        except TimeoutError as e:
            log.error(f"Failed to connect to event socket.")
            raise SocketError(f"Socket timed out: {e}")


class CommandSocket(AbstractSocket):
    """Interface to Hyprland's command socket.

    Provides the :meth:`CommandSocket.send_command` method, which can be used to send
    a wide range of commands, as explained in `the Hyprland wiki <https://wiki.hyprland.org/Configuring/Using-hyprctl>`_.
    """

    #: Maximum time in seconds to wait for socket connection and command response
    connection_timeout_seconds: float = 1.0

    def __init__(self, signature: str):
        super().__init__(signature)
        path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket.sock")
        if not path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {path_to_socket!r}.")
        self.path_to_socket = path_to_socket


    def send_command(self, command: str, flags: List[str] = [], args: List[str] = []) -> str:
        """Sends a command through the socket and returns the received response.

        The command syntax and options are the same as when using ``hyprctl``, but the ``hyprctl``
        part can be omitted. Read `the wiki entry <https://wiki.hyprland.org/Configuring/Using-hyprctl/>`_
        for more information.

        :param command: The command string.
        :param flags: Any flags to accompany the command.
        :param args: Arguments for the command.
        :return: Response from the socket.
        :raises: :class:`socket.SocketError` if a timeout occurs during the sending process.

        Example:

        .. code-block:: python

            response = command_socket.send_command("clients", flags=["-j"])
            # response contains JSON listing all Hyprland clients
        """

        assertions.assert_is_nonempty_string(command)
        for token in args + flags:
            assertions.assert_is_nonempty_string(token)

        message = " ".join(flags) + "/" + command
        if args:
            message += " " + " ".join(args)

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(self.connection_timeout_seconds)
            try:
                s.connect(str(self.path_to_socket))
                s.sendall(message.encode('utf-8'))
                return s.recv(4096).decode('utf-8')
            except TimeoutError as e:
                log.error(f"Failed to send command: {command=!r} {flags=} {args=}")
                raise SocketError(f"Socket timed out: {e}")
