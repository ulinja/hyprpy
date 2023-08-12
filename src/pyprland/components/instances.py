from typing import Dict, List, Type, Union
import json
import logging

from pyprland.data.models import InstanceData
from pyprland.components import windows, workspaces, monitors
from pyprland.utils import assertions, shell, sockets, signals


log = logging.getLogger(__name__)


class Instance:

    def __init__(self, signature: str = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')):
        self._data = InstanceData(signature=signature)

        self.event_socket = sockets.EventSocket(signature)
        self.command_socket = sockets.CommandSocket(signature)

        self.signal_workspace_created = signals.Signal(self)
        self.signal_workspace_destroyed = signals.Signal(self)
        self.signal_active_workspace_changed = signals.Signal(self)

        self.signal_window_created = signals.Signal(self)
        self.signal_window_destroyed = signals.Signal(self)
        self.signal_active_window_changed = signals.Signal(self)


    def __getattr__(self, name):
        """The Instance class is a proxy for the underlying :class:`pyprland.data.models.InstanceData` class attributes.

        This is implemented by relaying attribute access to the underlying data model for all attributes
        which are not direct attributes of the class.
        """
        if name in [
            'event_socket', 'command_socket',
            'signal_workspace_created', 'signal_workspace_destroyed', 'signal_active_workspace_changed'
            'signal_window_created', 'signal_window_destroyed', 'signal_active_window_changed'
        ]:
            return getattr(self, name)
        else:
            return getattr(self._data, name)


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"


    def get_windows(self) -> List['windows.Window']:
        """Returns all :class:`pyprland.components.windows.Window`s currently managed by the Instance.
    
        :return: A list containing :class:`pyprland.components.windows.Window`s.
        """

        windows_data = json.loads(self.command_socket.send_command('clients', flags=['-j']))
        return [windows.Window(window_data, self) for window_data in windows_data]

    def get_window_by_address(self, address: str) -> Union['windows.Window', None]:
        """Retrieves the :class:`pyprland.components.windows.Window` with the specified :param:`address`.

        The :param:`address` must be a valid hexadecimal string.

        :return: The :class:`pyprland.components.windows.Window` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`address` is not a string.
        :raises :class:`ValueError`: If :param:`address` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in self.get_windows():
            if window.address_as_int == int(address, 16):
                return window


    def get_workspaces(self) -> List['workspaces.Workspace']:
        """Returns all :class:`pyprland.components.workspaces.Workspace`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.components.workspaces.Workspace`s.
        """

        workspaces_data = json.loads(self.command_socket.send_command('workspaces', flags=['-j']))
        return [workspaces.Workspace(workspace_data, self) for workspace_data in workspaces_data]

    def get_workspace_by_id(self, id: int) -> Union['workspaces.Workspace', None]:
        """Retrieves the :class:`pyprland.components.workspaces.Workspace` with the specified :param:`id`.

        :return: The :class:`pyprland.components.workspaces.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in self.get_workspaces():
            if workspace.id == id:
                return workspace

    def get_workspace_by_name(self, name: int) -> Union['workspaces.Workspace', None]:
        """Retrieves the :class:`pyprland.components.workspaces.Workspace` with the specified :param:`name`.

        :return: The :class:`pyprland.components.workspaces.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in self.get_workspaces():
            if workspace.name == name:
                return workspace

    
    def get_monitors(self) -> List['monitors.Monitor']:
        """Returns all :class:`pyprland.components.monitors.Monitor`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.components.monitors.Monitor`s.
        """

        monitors_data = json.loads(self.command_socket.send_command('monitors', flags=['-j']))
        return [monitors.Monitor(monitor_data, self) for monitor_data in monitors_data]

    def get_monitor_by_id(self, id: int) -> Union['monitors.Monitor', None]:
        """Retrieves the :class:`pyprland.components.monitors.Monitor` with the specified :param:`id`.

        :return: The :class:`pyprland.components.monitors.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in self.get_monitors():
            if monitor.id == id:
                return monitor

    def get_monitor_by_name(self, name: str) -> Union['monitors.Monitor', None]:
        """Retrieves the :class:`pyprland.components.monitors.Monitor` with the specified :param:`name`.

        :return: The :class:`pyprland.components.monitors.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        :raises :class:`ValueError`: If :param:`name` the empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in self.get_monitors():
            if monitor.name == name:
                return monitor


    def watch(self) -> None:
        """Continuosly monitors the Hyprland event socket and emits signals when events occur.

        This is a blocking method which runs indefinitely.
        Signals are continuosly emitted, as soon as Hyprland events are detected.
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
                    new_window = self.get_window_by_address(event_data.split(',')[0])
                    signal.emit(new_window=new_window)
                elif event_name == 'closewindow':
                    signal.emit(destroyed_window_address=event_data)
                elif event_name == 'activewindowv2':
                    active_window = None if event_data == ',' else self.get_window_by_address(event_data)
                    signal.emit(active_window=active_window)

                elif event_name == 'createworkspace':
                    new_workspace = self.get_workspace_by_id(int(event_data))
                    signal.emit(new_workspace=new_workspace)
                elif event_name == 'destroyworkspace':
                    signal.emit(destroyed_workspace_id=event_data)
                elif event_name == 'workspace':
                    active_workspace = self.get_workspace_by_id(int(event_data))
                    signal.emit(active_workspace=active_workspace)

        with self.event_socket.get_socket() as s:
            while True:
                data = s.recv(4096).decode('utf-8')
                _handle_socket_data(data)
