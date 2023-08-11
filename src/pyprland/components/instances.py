from typing import Dict, List, Type, Union
import json

from pyprland.data.models import InstanceData
from pyprland.components import windows, workspaces, monitors
from pyprland.utils import assertions, shell, sockets


class Instance:

    def __init__(self, signature: str = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')):
        self._data = InstanceData(signature=signature)
        self.event_socket = sockets.EventSocket(signature)
        self.command_socket = sockets.CommandSocket(signature)

    def __getattr__(self, name):
        if name == 'event_socket':
            return self.event_socket
        elif name == 'command_socket':
            return self.command_socket
        else:
            return getattr(self._data, name)


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"


    def get_windows(self) -> List['windows.Window']:
        """Returns all :class:`pyprland.models.window.Window` currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.window.Window`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        windows_data = json.loads(self.command_socket.send_command('clients', flags=['-j']))
        return [windows.Window(window_data, self) for window_data in windows_data]

    def get_window_by_address(self, address: str) -> Union['windows.Window', None]:
        """Retrieves the :class:`pyprland.models.window.Window` with the specified :param:`address`.

        The :param:`address` must be a valid hexadecimal string.
        :return: The :class:`pyprland.models.window.Window` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`address` is not a string.
        :raises :class:`ValueError`: If :param:`address` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in self.get_windows():
            if window.address_as_int == int(address, 16):
                return window


    def get_workspaces(self) -> List['workspaces.Workspace']:
        """Returns all :class:`pyprland.models.workspace.Workspace`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.workspace.Workspace`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        workspaces_data = json.loads(self.command_socket.send_command('workspaces', flags=['-j']))
        return [workspaces.Workspace(workspace_data, self) for workspace_data in workspaces_data]

    def get_workspace_by_id(self, id: int) -> Union['workspaces.Workspace', None]:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`id`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in self.get_workspaces():
            if workspace.id == id:
                return workspace

    def get_workspace_by_name(self, name: int) -> Union['workspaces.Workspace', None]:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`name`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in self.get_workspaces():
            if workspace.name == name:
                return workspace

    
    def get_monitors(self) -> List['monitors.Monitor']:
        """Returns all :class:`pyprland.models.monitor.Monitor`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.monitor.Monitor`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        monitors_data = json.loads(self.command_socket.send_command('monitors', flags=['-j']))
        return [monitors.Monitor(monitor_data, self) for monitor_data in monitors_data]

    def get_monitor_by_id(self, id: int) -> Union['monitors.Monitor', None]:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`id`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in self.get_monitors():
            if monitor.id == id:
                return monitor

    def get_monitor_by_name(self, name: str) -> Union['monitors.Monitor', None]:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`name`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        :raises :class:`ValueError`: If :param:`name` the empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in self.get_monitors():
            if monitor.name == name:
                return monitor
