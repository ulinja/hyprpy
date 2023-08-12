from typing import List

from pyprland.data.models import WorkspaceData
from pyprland.components import instances, windows, monitors
from pyprland.components.common import ParentNotFoundException


class Workspace:

    def __init__(self, workspace_data: dict, instance: 'instances.Instance'):
        self._data = WorkspaceData.model_validate(workspace_data)
        self._instance = instance

    def __getattr__(self, name):
        """Relay attribute access to the underlying :class:`pyprland.data.models.WorkspaceData` model class."""

        if name == 'instance':
            return self._instance
        else:
            return getattr(self._data, name)

    @property
    def monitor(self) -> 'monitors.Monitor':
        """Returns the :class:`pyprland.components.monitor.Monitor` which this workspace is on.

        :return: The :class:`pyprland.components.monitor.Monitor` this workspace is on.
        """

        monitor = self._instance.get_monitor_by_name(self._data.monitor_name)
        if not monitor:
            raise ParentNotFoundException(f"Parent monitor {self._data.monitor_name=!r} not found.")
        return monitor

    @property
    def windows(self) -> List['windows.Window']:
        """Returns all :class:`pyprland.components.window.Window`s on this workspace.

        :return: A list containing all :class:`pyprland.components.window.Window`s on this workspace.
        """

        windows = []
        for window in self._instance.get_windows():
            if window.workspace_id == self.id:
                windows.append(window)
        return windows

    @property
    def last_window_address_as_int(self) -> int:
        """Returns the integer representation of the window's `last_window_address` property."""

        return int(self._data.last_window_address, 16)


    def __repr__(self):
        return f"<Workspace(id={self.id}, name={self.name!r})>"
