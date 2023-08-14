""":class:`Workspace` objects represent individual workspaces in Hyprland."""

from typing import List

from hyprpy.data.models import WorkspaceData
from hyprpy.components import instances, windows, monitors
from hyprpy.components.common import ParentNotFoundException


class Workspace:
    """Represents a workspace in Hyprland.

    The data attributes of a :class:`Workspace` map directly to the data attributes of the underlying
    :class:`~hyprpy.data.models.WorkspaceData` data class.
    """

    def __init__(self, workspace_data: dict, instance: 'instances.Instance'):
        self._data = WorkspaceData.model_validate(workspace_data)
        self._instance = instance

    def __getattr__(self, name):
        """Relays attribute access to the underlying :class:`~hyprpy.data.models.WorkspaceData` data model class."""

        if name == 'instance':
            return self._instance
        else:
            return getattr(self._data, name)

    @property
    def monitor(self) -> 'monitors.Monitor':
        """The :class:`~hyprpy.components.monitor.Monitor` this workspace is on.

        :return: The :class:`~hyprpy.components.monitor.Monitor` this workspace is on.
        """

        monitor = self._instance.get_monitor_by_name(self._data.monitor_name)
        if not monitor:
            raise ParentNotFoundException(f"Parent monitor {self._data.monitor_name=!r} not found.")
        return monitor

    @property
    def windows(self) -> List['windows.Window']:
        """The list of all :class:`~hyprpy.components.window.Window`\\ s on this workspace.

        :return: A list containing all :class:`~hyprpy.components.window.Window`\\ s on this workspace.
        """

        windows = []
        for window in self._instance.get_windows():
            if window.workspace_id == self.id:
                windows.append(window)
        return windows

    @property
    def last_window_address_as_int(self) -> int:
        """Returns the integer representation of the workspace's :attr:`~hyprpy.data.models.WorkspaceData.last_window_address` property."""

        return int(self._data.last_window_address, 16)


    def __repr__(self):
        return f"<Workspace(id={self.id}, name={self.name!r})>"
