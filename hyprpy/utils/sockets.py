"""Interfaces for UNIX socket operations with Hyprland's event and command sockets.

Hyprland offers two UNIX sockets:

1. `EventSocket <https://wiki.hyprland.org/IPC/#tmphyprhissocket2sock>`_: This socket broadcasts various events occurring in the Hyprland session, 
   e.g., windows or workspaces getting created or destroyed.
2. `CommandSocket <https://wiki.hyprland.org/IPC/#tmphyprhissocketsock>`_: This socket can be written to in order to influence Hyprland's behavior 
   or send queries about the current state.

Hyprpy uses standard library `sockets <https://docs.python.org/3/library/socket.html>`_ for socket operations.

Examples:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland()

    # Connect the socket, wait for an event to occur, print the event data and close the socket.
    instance.event_socket.connect()
    instance.event_socket.wait()
    data = instance.even_socket.read()
    print(data)
    instance.event_socket.close()

    # Send a command
    instance.command_socket.send_command("dispatch", flags=["--single-instance"], args=["exec", "kitty"])
"""

from abc import ABC
from typing import List
from pathlib import PosixPath
import select, socket
import logging

from hyprpy.utils import assertions


log = logging.getLogger(__name__)


class SocketError(Exception):
    """Raised when a socket operation fails."""
    pass


class AbstractSocket(ABC):
    """Base class for concrete socket classes.

    Provides attributes and methods common between :class:`~EventSocket`
    and :class:`~CommandSocket`.

    Upon initialization, the underlying :class:`~socket.socket` object is *not* created.
    Users must explicitly call :meth:`~AbstractSocket.connect` prior
    to using the :class:`~socket.socket`, and should call :meth:`~AbstractSocket.close`
    aftwerwards.
    """

    def __init__(self, signature: str):
        assertions.assert_is_nonempty_string(signature)
        #: The Hyprland Instance Signature.
        self._signature: str = signature
        #: Filesystem path to the socket file.
        self._path_to_socket: PosixPath
        #: The underlying :class:`socket.socket` object.
        self._socket: socket.socket | None = None


    def connect(self, timeout: int | float | None = 1) -> None:
        """Creates and connects the :class:`~socket.socket`.

        If a ``timeout`` is set, its value specifies the number of seconds to wait until
        the connection is established. If the connection cannot be established within the
        specified ``timeout`` period, a :class:`SocketError` is raised. The default
        ``timeout`` is 1 second.

        Once created, the :class:`~socket.socket` is put into non-blocking mode (regardless
        of the specified ``timeout``).

        :param timeout: Maximum number of seconds to wait for a connection to be established until
            a :class:`~SocketError` is raised. If ``timeout`` is ``None``, the call blocks indefinitely
            until a connection is established.
        :raises: :class:`~SocketError` if the :class:`~socket.socket` has already been connected, or if the
            connection attempt takes longer than ``timeout`` seconds.
        """

        if self._socket:
            raise SocketError("Attempted to connect a socket which was already connected.")
        if timeout is not None:
            assertions.assert_is_float_or_int(timeout)

        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._socket.connect(str(self._path_to_socket))
        self._socket.setblocking(False)


    def close(self) -> None:
        """Disconnects and closes the :class:`~socket.socket`.

        :raises: :class:`~SocketError` if the :class:`~socket.socket` has already been disconnected.
        """

        if not self._socket:
            raise SocketError("Attempted to close a socket which was not created.")
        self._socket.close()
        self._socket = None


    def send(self, data: str) -> None:
        """Sends ``data`` into the :class:`~socket.socket`.

        :raises: :class:`~SocketError` if the :class:`~socket.socket` is not connected.
        """

        if not self._socket:
            raise SocketError("Attempted to send data to a socket which was not connected.")
        assertions.assert_is_string(data)

        self._socket.sendall(data.encode('UTF-8'))


    def wait(self, timeout: int | float | None = None) -> None:
        """Waits a maximum of ``timeout`` seconds until data has arrived at the :class:`~socket.socket`.

        Calling this method avoids using active waiting to wait for socket data.

        :param timeout: The maximum number of seconds to wait for data until a :class:`~SocketError` is raised.
            If ``timeout`` is ``None``, wait indefinitely until data is ready to be retrieved.
        :raises: :class:`~SocketError` if the :class:`~socket.socket` is not connected, or if the specified
            ``timeout`` was reached..
        """

        if not self._socket:
            raise SocketError("Attempted to wait for data on a socket which was not connected.")

        read_ready, _, _ = select.select([self._socket], [], [], timeout)
        if not read_ready:
            raise SocketError(f"Waiting socket timed out after {timeout} seconds.")

    def read(self) -> str:
        """Immediately retrieves all data from the :class:`~socket.socket` and returns it.

        :return: The data received from the :class:`~socket.socket` as a string. If the socket
            does not contain any data, returns an empty string.
        :raises: :class:`~SocketError` if the :class:`~socket.socket` is not connected.
        """

        if not self._socket:
            raise SocketError("Attempted to receive data from a socket which was not connected.")

        data = bytearray()
        while True:
            try:
                data_chunk = self._socket.recv(4096)
                if data_chunk:
                    data += data_chunk
                else:
                    break
            except BlockingIOError as e:
                if e.errno == 11:
                    break
                else:
                    raise SocketError(f"Failed to read from socket: {e}")

        return data.decode('UTF-8')


class EventSocket(AbstractSocket):
    """Interface to Hyprland's event socket.

    This socket broadcasts events about the ongoing Hyprland session, such as
    windows or workspaces being created or destroyed.
    """

    def __init__(self, signature: str):
        super().__init__(signature)
        self._path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket2.sock")
        if not self._path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {self._path_to_socket!r}.")


class CommandSocket(AbstractSocket):
    """Interface to Hyprland's command socket.

    Provides the :meth:`CommandSocket.send_command` method, which can be used to send
    a wide range of commands, as explained in `the Hyprland wiki <https://wiki.hyprland.org/Configuring/Using-hyprctl>`_.
    """

    def __init__(self, signature: str):
        super().__init__(signature)
        self._path_to_socket = PosixPath(f"/tmp/hypr/{self._signature}/.socket.sock")
        if not self._path_to_socket.is_socket():
            raise FileNotFoundError(f"No socket found at {self._path_to_socket!r}.")


    def send_command(self, command: str, flags: List[str] = [], args: List[str] = []) -> str:
        """Sends a command through the socket and returns the received response.

        Contrary to the methods inherited from :class:`~AbstractSocket`, this method implicitly
        connects the socket prior to sending the command, and disconnects it afterwards.

        The command syntax and options are the same as when using ``hyprctl``, but the ``hyprctl``
        part can be omitted. Read `the wiki entry <https://wiki.hyprland.org/Configuring/Using-hyprctl/>`_
        for more information.

        :param command: The command string.
        :param flags: Any flags to accompany the command.
        :param args: Arguments for the command.
        :return: Response from the socket.
        :raises: :class:`~SocketError` if the :class:`~socket.socket` is already connected.
        :raises: :class:`TypeError` if ``command`` or any items in ``flags`` and ``args``
            are not strings.
        :raises: :class:`ValueError` if ``command`` or any items in ``flags`` and ``args``
            are empty strings.

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

        self.connect()
        self.send(message)
        self.wait(0.5)
        response = self.read()
        self.close()
        return response
