"""`Monitor` objects represent monitors in Hyprland."""

from typing import List

from hyprpy.data.models import MonitorData
from hyprpy.components import instances, workspaces

class Monitor:
    """Represents a monitor within Hyprland.

    The data attributes of a :class:`Monitor` instance map directly to the data attributes of the underlying
    :class:`~hyprpy.data.models.MonitorData` data model class.
    """

    def __init__(self, monitor_data: str, instance: 'instances.Instance'):
        self._data = MonitorData.model_validate(monitor_data)
        self._instance = instance

    def __getattr__(self, name):
        """Relays attribute access to the underlying :class:`~hyprpy.data.models.MonitorData` data model class."""

        if name == 'instance':
            return self._instance
        else:
            return getattr(self._data, name)

    @property
    def workspaces(self) -> List['workspaces.Workspace']:
        """Returns all :class:`~hyprpy.components.workspace.Workspace`\\ s on this monitor.

        :return: A list containing all :class:`~hyprpy.components.workspace.Workspace`\\ s on this monitor.
        """

        workspaces = []
        for workspace in self._instance.get_workspaces():
            if workspace.monitor_name == self._data.name:
                workspaces.append(workspace)
        return workspaces

    def __repr__(self):
        return f"<Monitor(id={self._data.id}, name={self._data.name!r}, width={self._data.width}, height={self._data.height})>"
