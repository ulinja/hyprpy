"""Interfaces for hyprland."""

from typing import List
import json

from pyprland.utils import shell, assertions
from pyprland.models import Instance, Monitor, Workspace, Window


class Hyprland:

    @classmethod
    def get_instance(cls) -> Instance:
        """Returns the currently running :class:`pyprland.models.instance.Instance`.

        :return: The current :class:`pyprland.models.instance.Instance` of Hyprland.
        :raises :class:`pyprland.exceptions.EnvironmentException`: If executed outside of a Hyprland environment.
        """

        return Instance.get()


    @classmethod
    def get_windows(cls) -> List[Window]:
        """Returns all :class:`pyprland.models.window.Window` currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.window.Window`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        windows_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'clients'])[0])
        return [Window.model_validate(window_dict) for window_dict in windows_json]

    @classmethod
    def get_window_by_address(cls, address: str) -> Window | None:
        """Retrieves the :class:`pyprland.models.window.Window` with the specified :param:`address`.

        The :param:`address` must be a valid hexadecimal string.
        :return: The :class:`pyprland.models.window.Window` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`address` is not a string.
        :raises :class:`ValueError`: If :param:`address` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in cls.get_windows():
            if window.address_as_int == int(address, 16):
                return window


    @classmethod
    def get_workspaces(cls) -> List[Workspace]:
        """Returns all :class:`pyprland.models.workspace.Workspace`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.workspace.Workspace`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        workspaces_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'workspaces'])[0])
        return [Workspace.model_validate(workspace_dict) for workspace_dict in workspaces_json]

    @classmethod
    def get_workspace_by_id(cls, id: int) -> Workspace | None:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`id`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in cls.get_workspaces():
            if workspace.id == id:
                return workspace

    @classmethod
    def get_workspace_by_name(cls, name: int) -> Workspace | None:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`name`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in cls.get_workspaces():
            if workspace.name == name:
                return workspace

    
    @classmethod
    def get_monitors(cls) -> List[Monitor]:
        """Returns all :class:`pyprland.models.monitor.Monitor`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.monitor.Monitor`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        monitors_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'monitors'])[0])
        return [Monitor.model_validate(monitor_dict) for monitor_dict in monitors_json]

    @classmethod
    def get_monitor_by_id(cls, id: int) -> Monitor | None:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`id`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in cls.get_monitors():
            if monitor.id == id:
                return monitor

    @classmethod
    def get_monitor_by_name(cls, name: str) -> Monitor | None:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`name`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        :raises :class:`ValueError`: If :param:`name` the empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in cls.get_monitors():
            if monitor.name == name:
                return monitor
