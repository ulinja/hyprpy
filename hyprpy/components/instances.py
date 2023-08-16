"""The central :class:`Instance` class for interfacing with Hyprland.

This class acts as the root for accessing other components like workspaces, windows, and monitors,
and offers capabilities to listen to events and signals emitted by the underlying Hyprland system.
"""

from typing import List, Union
import json
import logging

from hyprpy.data.models import InstanceData
from hyprpy.components.windows import Window
from hyprpy.components.workspaces import Workspace
from hyprpy.components.monitors import Monitor
from hyprpy.utils import assertions, shell
from hyprpy.utils.sockets import CommandSocket, EventSocket
from hyprpy.utils.signals import Signal


log = logging.getLogger(__name__)


class Instance:
    """Represents an active Hyprland instance.

    The Instance class is a primary interface for interacting with the Hyprland system. It provides methods
    for accessing windows, workspaces, and monitors, as well as emitting signals based on events in the
    Hyprland environment.

    :seealso: :ref:`Components: The Instance <guide-instance>`
    """

    def __init__(self, signature: str = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')):
        data = InstanceData(signature=signature)

        #: `Instance signature <https://wiki.hyprland.org/IPC/#hyprland-instance-signature-his>`_ of the Hyprland instance.
        self.signature: str = data.signature

        #: The Hyprland event socket for this instance.
        self.event_socket: EventSocket = EventSocket(signature)
        #: The Hyprland command socket for this instance.
        self.command_socket: CommandSocket = CommandSocket(signature)

        #: Signal emitted when a new workspace gets created.
        self.signal_workspace_created: Signal = Signal(self)
        #: Signal emitted when an existing workspace gets destroyed.
        self.signal_workspace_destroyed: Signal = Signal(self)
        #: Signal emitted when the focus changes to another workspace.
        self.signal_active_workspace_changed: Signal = Signal(self)

        #: Signal emitted when a new window gets created.
        self.signal_window_created: Signal = Signal(self)
        #: Signal emitted when an existing window gets destroyed.
        self.signal_window_destroyed: Signal = Signal(self)
        #: Signal emitted when the focus changes to another window.
        self.signal_active_window_changed: Signal = Signal(self)


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"


    def get_windows(self) -> List['Window']:
        """Returns all :class:`~hyprpy.components.windows.Window`\\ s currently managed by the instance.
    
        :return: A list containing :class:`~hyprpy.components.windows.Window` objects.
        """

        windows_data = json.loads(self.command_socket.send_command('clients', flags=['-j']))
        return [Window(window_data, self) for window_data in windows_data]

    def get_window_by_address(self, address: str) -> Union['Window', None]:
        """Retrieves the :class:`~hyprpy.components.windows.Window` with the specified ``address``.

        The ``address`` must be a valid hexadecimal string.

        :return: The :class:`~hyprpy.components.windows.Window` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``address`` is not a string.
        :raises: :class:`ValueError` if ``address`` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in self.get_windows():
            if window.address_as_int == int(address, 16):
                return window

    def get_active_window(self) -> 'Window':
        """Returns the currently active :class:`~hyprpy.components.windows.Window`.
    
        :return: The currently active :class:`~hyprpy.components.windows.Window`.
        """

        window_data = json.loads(self.command_socket.send_command('activewindow', flags=['-j']))
        return Window(window_data, self)


    def get_workspaces(self) -> List['Workspace']:
        """Returns all :class:`~hyprpy.components.workspaces.Workspace`\\ s currently managed by the instance.
    
        :return: A list containing :class:`~hyprpy.components.workspaces.Workspace`\\ s.
        """

        workspaces_data = json.loads(self.command_socket.send_command('workspaces', flags=['-j']))
        return [Workspace(workspace_data, self) for workspace_data in workspaces_data]

    def get_workspace_by_id(self, id: int) -> Union['Workspace', None]:
        """Retrieves the :class:`~hyprpy.components.workspaces.Workspace` with the specified ``id``.

        :return: The :class:`~hyprpy.components.workspaces.Workspace` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``id`` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in self.get_workspaces():
            if workspace.id == id:
                return workspace

    def get_active_workspace(self) -> 'Workspace':
        """Retrieves the currently active :class:`~hyprpy.components.workspaces.Workspace`.

        :return: The currently active :class:`~hyprpy.components.workspaces.Workspace`.
        """

        workspace_data = json.loads(self.command_socket.send_command('activeworkspace', flags=['-j']))
        return Workspace(workspace_data, self)

    def get_workspace_by_name(self, name: int) -> Union['Workspace', None]:
        """Retrieves the :class:`~hyprpy.components.workspaces.Workspace` with the specified ``name``.

        :return: The :class:`~hyprpy.components.workspaces.Workspace` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``name`` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in self.get_workspaces():
            if workspace.name == name:
                return workspace

    
    def get_monitors(self) -> List['Monitor']:
        """Returns all :class:`~hyprpy.components.monitors.Monitor`\\ s currently managed by the instance.
    
        :return: A list containing :class:`~hyprpy.components.monitors.Monitor`\\ s.
        """

        monitors_data = json.loads(self.command_socket.send_command('monitors', flags=['-j']))
        return [Monitor(monitor_data, self) for monitor_data in monitors_data]

    def get_monitor_by_id(self, id: int) -> Union['Monitor', None]:
        """Retrieves the :class:`~hyprpy.components.monitors.Monitor` with the specified ``id``.

        :return: The :class:`~hyprpy.components.monitors.Monitor` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``id`` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in self.get_monitors():
            if monitor.id == id:
                return monitor

    def get_monitor_by_name(self, name: str) -> Union['Monitor', None]:
        """Retrieves the :class:`~hyprpy.components.monitors.Monitor` with the specified ``name``.

        :return: The :class:`~hyprpy.components.monitors.Monitor` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``name`` is not a string.
        :raises: :class:`ValueError` if ``name`` is an empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in self.get_monitors():
            if monitor.name == name:
                return monitor


    def watch(self) -> None:
        """Continuosly monitors the :class:`~hyprpy.utils.sockets.EventSocket` and emits appropriate :class:`~hyprpy.utils.signals.Signal`\\ s when events are detected.

        This is a blocking method which runs indefinitely.
        Signals are continuosly emitted, as soon as Hyprland events are detected.

        :seealso: :ref:`Components: Reacting to events <guide-events>`
        """

        def _handle_socket_data(data: str):
            signal_for_event = {
                'openwindow': self.signal_window_created,
                'closewindow': self.signal_window_destroyed,
                'activewindowv2': self.signal_active_window_changed,

                'createworkspace': self.signal_workspace_created,
                'destroyworkspace': self.signal_workspace_destroyed,
                'workspace': self.signal_active_workspace_changed,
            }

            lines = list(filter(lambda line: len(line) > 0, data.split('\n')))
            for line in lines:
                event_name, event_data = line.split('>>', maxsplit=1)

                # Pick the signal to emit based on the event's name
                if event_name not in signal_for_event:
                    continue
                signal = signal_for_event[event_name]
                if not signal._observers:
                    # If the signal has no observers, just exit
                    continue

                # We send specific data along with the signal, depending on the event
                if event_name == 'openwindow':
                    signal.emit(created_window_address=event_data.split(',')[0])
                elif event_name == 'closewindow':
                    signal.emit(destroyed_window_address=event_data)
                elif event_name == 'activewindowv2':
                    signal.emit(active_window_address=(None if event_data == ',' else event_data))

                elif event_name == 'createworkspace':
                    signal.emit(created_workspace_id=(int(event_data) if event_data != 'special' else -99))
                elif event_name == 'destroyworkspace':
                    signal.emit(destroyed_workspace_id=(int(event_data) if event_data != 'special' else -99))
                elif event_name == 'workspace':
                    signal.emit(active_workspace_id=(int(event_data) if event_data != 'special' else -99))


        try:
            self.event_socket.connect()

            while True:
                self.event_socket.wait()
                data = self.event_socket.read()
                _handle_socket_data(data)
        finally:
            self.event_socket.close()
