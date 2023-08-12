"""This module provides the `Monitor` class for interfacing with individual monitors in the Hyprland system.

For a broader overview of the component system in Pyprland, refer to :mod:`pyprland.components`.

:seealso: :mod:`pyprland.components`
"""

from typing import List

from pyprland.data.models import MonitorData
from pyprland.components import instances, workspaces

class Monitor:
    """Represents an individual monitor within the Hyprland system.

    The attributes of a `Monitor` instance map directly to the data attributes available in the underlying
    :class:`pyprland.data.models.MonitorData`.

    Attributes:
        workspaces (list): List of :class:`pyprland.components.workspaces.Workspace` objects available on this monitor.
    """

    def __init__(self, monitor_data: str, instance: 'instances.Instance'):
        self._data = MonitorData.model_validate(monitor_data)
        self._instance = instance

    def __getattr__(self, name):
        """Relay attribute access to the underlying :class:`pyprland.data.models.MonitorData` model class."""

        if name == 'instance':
            return self._instance
        else:
            return getattr(self._data, name)

    @property
    def workspaces(self) -> List['workspaces.Workspace']:
        """Returns all :class:`pyprland.components.workspace.Workspace`s on this monitor.

        :return: A list containing all :class:`pyprland.components.workspace.Workspace`s on this monitor.
        """

        workspaces = []
        for workspace in self._instance.get_workspaces():
            if workspace.monitor_name == self._data.name:
                workspaces.append(workspace)
        return workspaces

    def __repr__(self):
        return f"<Monitor(id={self._data.id}, name={self._data.name!r}, width={self._data.width}, height={self._data.height})>"
