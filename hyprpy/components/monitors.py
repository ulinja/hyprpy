"""`Monitor` objects represent monitors in Hyprland."""

from typing import List

from hyprpy.data.models import MonitorData
from hyprpy.components import instances, workspaces

class Monitor:
    """Represents a monitor within Hyprland."""

    def __init__(self, monitor_data: str, instance: 'instances.Instance'):
        data = MonitorData.model_validate(monitor_data)

        #: Numeric ID of the monitor.
        self.id: int = data.id
        #: Name of the monitor.
        self.name: str = data.name
        #: Manufacturer's name.
        self.description: str = data.description
        #: Model number of the monitor.
        self.make: str = data.make
        #: Composite string of `make`, `name` and `model`.
        self.model: str = data.model
        #: Unknown.
        self.serial: str = data.serial
        #: Width of the monitor (in pixels).
        self.width: int = data.width
        #: Height of the monitor (in pixels).
        self.height: int = data.height
        #: Refresh rate of the monitor (in Hz).
        self.refresh_rate: float = data.refresh_rate
        #: Unknown.
        self.position_x: int = data.position_x
        #: Unknown.
        self.position_y: int = data.position_y
        #: Numeric ID of the workspace currently active on the monitor.
        self.active_workspace_id: int = data.active_workspace_id
        #: Assigned name of the workspace currently active on the monitor.
        self.active_workspace_name: str = data.active_workspace_name
        #: Unknown.
        self.reserved: List[int] = data.reserved
        #: Unknown.
        self.scale: float = data.scale
        #: Unknown.
        self.transform: int = data.transform
        #: Whether or not the currently focused window is on this monitor.
        self.is_focused: bool = data.is_focused
        #: Whether or not the monitor uses DPMS.
        self.uses_dpms: bool = data.uses_dpms
        #: Unknown.
        self.vrr: bool = data.vrr

        #: The :class:`~hyprpy.components.instances.Instance` managing this monitor.
        self._instance = instance


    @property
    def workspaces(self) -> List['workspaces.Workspace']:
        """All :class:`~hyprpy.components.workspace.Workspace`\\ s located on this monitor."""

        workspaces = []
        for workspace in self._instance.get_workspaces():
            if workspace.monitor_name == self.name:
                workspaces.append(workspace)
        return workspaces


    def __repr__(self):
        return f"<Monitor(id={self.id}, name={self.name!r}, width={self.width}, height={self.height})>"
