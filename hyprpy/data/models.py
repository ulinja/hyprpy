"""Data classes used for parsing, validating and storing JSON output received
from the Hyprland command socket.

Classes:
    - :class:`WindowData`: data for Hyprland windows.
    - :class:`WorkspaceData`: data for Hyprland workspaces.
    - :class:`MonitorData`: data for Hyprland monitors.
    - :class:`InstanceData`: data for Hyprland instances.
"""

from typing import List

from pydantic import BaseModel, Field, AliasPath

from hyprpy.data.validators import HexString, NonEmptyString


class WindowData(BaseModel):
    """Deserialization and validation of ``hyprctl`` window (client) data."""

    #: String representation of a hexadecimal number, unique identifier for the window.
    address: HexString
    #: Unknown.
    is_mapped: bool = Field(..., alias="mapped")
    #: Unknown.
    is_hidden: bool = Field(..., alias="hidden")
    #: Absolute X-coordinate of the window on the monitor (in pixels).
    position_x: int = Field(..., validation_alias=AliasPath("at", 0))
    #: Absolute Y-coordinate of the window on the monitor (in pixels).
    position_y: int = Field(..., validation_alias=AliasPath("at", 1))
    #: Width of the window (in pixels).
    width: int = Field(..., validation_alias=AliasPath("size", 0))
    #: Height of the window (in pixels).
    height: int = Field(..., validation_alias=AliasPath("size", 1))
    #: Numeric ID of the workspace which the window is on.
    workspace_id: int = Field(..., validation_alias=AliasPath("workspace", "id"))
    #: Name of the workspace which the window is on.
    workspace_name: str = Field(..., validation_alias=AliasPath("workspace", "name"))
    #: Whether or not this is a floating window.
    is_floating: bool = Field(..., alias="floating")
    #: Numeric ID of the monitor which the window is on.
    monitor_id: int = Field(..., alias="monitor")
    #: Window manager class assigned to this window.
    wm_class: str = Field(..., alias="class")
    #: Current title of the window.
    title: str
    #: Window manager class when the window was created.
    initial_wm_class: str = Field(..., alias="initialClass")
    #: Title when the window was created.
    initial_title: str = Field(..., alias="initialTitle")
    #: Process ID of the process the window is assigned to.
    pid: int
    #: Whether or not the window is using xwayland to be displayed.
    is_xwayland: bool = Field(..., alias="xwayland")
    #: Unknown.
    is_pinned: bool = Field(..., alias="pinned")
    #: Whether or not the window is in fullscreen mode.
    is_fullscreen: bool = Field(..., alias="fullscreen")
    #: Unknown.
    fullscreen_mode: int = Field(..., alias="fullscreenMode")
    #: Unknown.
    is_fake_fullscreen: bool = Field(..., alias="fakeFullscreen")


class WorkspaceData(BaseModel):
    """Deserialization and validation of ``hyprctl`` workspace data."""

    #: Numeric ID of the workspace.
    id: int
    #: Name assigned to the workspace.
    name: str
    #: Name of the monitor which this workspace is on.
    monitor_name: str = Field(..., alias="monitor")
    #: Address string of the most recently active window on the workspace.
    last_window_address: HexString = Field(..., alias="lastwindow")
    #: Title of the most recently active window on the workspace.
    last_window_title: str = Field(..., alias="lastwindowtitle")
    #: Number of windows placed in the workspace.
    window_count: int = Field(..., alias="windows")
    #: True if at least one window in the workspace is in fullscreen mode.
    has_fullscreen: bool = Field(..., alias="hasfullscreen")


class MonitorData(BaseModel):
    """Deserialization and validation of ``hyprctl`` monitor data."""

    #: Numeric ID of the monitor.
    id: int
    #: Name of the monitor.
    name: str
    #: Manufacturer's name.
    description: str
    #: Model number of the monitor.
    make: str
    #: Composite string of `make`, `name` and `model`.
    model: str
    #: Unknown.
    serial: str
    #: Width of the monitor (in pixels).
    width: int
    #: Height of the monitor (in pixels).
    height: int
    #: Refresh rate of the monitor (in Hz).
    refresh_rate: float = Field(..., alias="refreshRate")
    #: Unknown.
    position_x: int = Field(..., alias="x")
    #: Unknown.
    position_y: int = Field(..., alias="y")
    #: Numeric ID of the workspace currently active on the monitor.
    active_workspace_id: int = Field(..., validation_alias=AliasPath("activeWorkspace", "id"))
    #: Assigned name of the workspace currently active on the monitor.
    active_workspace_name: str = Field(..., validation_alias=AliasPath("activeWorkspace", "name"))
    #: Unknown.
    reserved: List[int]
    #: Unknown.
    scale: float
    #: Unknown.
    transform: int
    #: Whether or not the currently focused window is on this monitor.
    is_focused: bool = Field(..., alias="focused")
    #: Whether or not the monitor uses DPMS.
    uses_dpms: bool = Field(..., alias="dpmsStatus")
    #: Unknown.
    vrr: bool


class InstanceData(BaseModel):
    """Deserialization and validation of ``hyprctl`` instance data."""

    #: `Instance signature <https://wiki.hyprland.org/IPC/#hyprland-instance-signature-his>`_ of the Hyprland instance.
    signature: NonEmptyString
