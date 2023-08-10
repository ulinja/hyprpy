"""Pydantic model representing Hyprland monitors.

This module provides a way to query Hyprland monitors. The monitor objects are
constructed by parsing the output from the `hyprctl` command-line utility.

Classes:
    Monitor: Represents a monitor, and contains all available information about it.
"""

from typing import List

from pydantic import AliasPath, BaseModel, Field

from pyprland.models.workspace import Workspace
from pyprland.hyprland import Hyprland


class Monitor(BaseModel):
    """Represents a Monitor in the Hyprland wayland compositor.

    The class allows reading of monitor attributes.

    Attributes:
        id (int): Numeric ID of the monitor.
        name (str): Name of the monitor.
        make (str): Manufacturer's name.
        model (str): Model number of the monitor.
        description (str): Composite string of `make`, `name` and `model`.
        serial (str): Unknown.
        width (int): Width of the monitor (in pixels).
        height (int): Height of the monitor (in pixels).
        refresh_rate (float): Refresh rate of the monitor (in Hz).
        position_x (int): Unknown.
        position_y (int): Unknown.
        active_workspace_id (int): Numeric ID of the workspace currently active on the monitor.
        active_workspace_name (str): Assigned name of the workspace currently active on the monitor.
        reserved (List[int]): Unknown.
        scale (float): Unknown.
        transform (int): Unknown.
        is_focused (bool): Whether or not the currently focused window is on this monitor.
        uses_dpms (bool): Whether or not the monitor uses DPMS.
        vrr (bool): Unknown.
    """
    id: int
    name: str
    description: str
    make: str
    model: str
    serial: str
    width: int
    height: int
    refresh_rate: float = Field(..., alias="refreshRate")
    position_x: int = Field(..., alias="x")
    position_y: int = Field(..., alias="y")
    active_workspace_id: int = Field(..., validation_alias=AliasPath("activeWorkspace", "id"))
    active_workspace_name: str = Field(..., validation_alias=AliasPath("activeWorkspace", "name"))
    reserved: List[int]
    scale: float
    transform: int
    is_focused: bool = Field(..., alias="focused")
    uses_dpms: bool = Field(..., alias="dpmsStatus")
    vrr: bool


    @property
    def workspaces(self) -> List[Workspace]:
        """Returns all :class:`pyprland.models.workspace.Workspace`s on this monitor.

        :return: A list containing all :class:`pyprland.models.workspace.Workspace`s on this monitor.
        """

        workspaces = []
        for workspace in Hyprland.get_workspaces():
            if workspace.monitor_name == self.name:
                workspaces.append(workspace)
        return workspaces


    def __repr__(self):
        return f"<Monitor(id={self.id}, name={self.name!r}, width={self.width}, height={self.height})>"
