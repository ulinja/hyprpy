from typing import List

from pydantic import BaseModel, Field, AliasPath

from pyprland.data.validators import HexString, NonEmptyString


class WindowData(BaseModel):
    """Represents a window (also called client) in the Hyprland wayland compositor.

    The class allows reading of various window attributes, from the address and window dimensions to more specific attributes like
    `is_fullscreen` and `is_pinned`.

    Attributes:
        address (str): String representation of a hexadecimal number, unique identifier for the window.
        is_mapped (bool): Unknown.
        is_hidden (bool): Unknown.
        position_x (int): Absolute X-coordinate of the window on the monitor (in pixels).
        position_y (int): Absolute Y-coordinate of the window on the monitor (in pixels).
        width (int): Width of the window (in pixels).
        height (int): Height of the window (in pixels).
        workspace_id (int): Numeric ID of the workspace which the window is on.
        workspace_name (int): Name of the workspace which the window is on.
        is_floating (bool): Whether or not this is a floating window.
        monitor_id (int): Numeric ID of the monitor which the window is on.
        wm_class (str): Window manager class assigned to this window.
        title (str): Current title of the window.
        initial_wm_class (str): Window manager class when the window was created.
        initial_title (str): Title when the window was created.
        pid (int): Process ID of the process the window is assigned to.
        is_xwayland (bool): Whether or not the window is using xwayland to be displayed.
        is_pinned (bool): Unknown.
        is_fullscreen (bool): Whether or not the window is in fullscreen mode.
        fullscreen_mode (int): Unknown.
        is_fake_fullscreen (bool): Unknown.
    """
    address: HexString
    is_mapped: bool = Field(..., alias="mapped")
    is_hidden: bool = Field(..., alias="hidden")
    position_x: int = Field(..., validation_alias=AliasPath("at", 0))
    position_y: int = Field(..., validation_alias=AliasPath("at", 1))
    width: int = Field(..., validation_alias=AliasPath("size", 0))
    height: int = Field(..., validation_alias=AliasPath("size", 1))
    workspace_id: int = Field(..., validation_alias=AliasPath("workspace", "id"))
    workspace_name: str = Field(..., validation_alias=AliasPath("workspace", "name"))
    is_floating: bool = Field(..., alias="floating")
    monitor_id: int = Field(..., alias="monitor")
    wm_class: str = Field(..., alias="class")
    title: str
    initial_wm_class: str = Field(..., alias="initialClass")
    initial_title: str = Field(..., alias="initialTitle")
    pid: int
    is_xwayland: bool = Field(..., alias="xwayland")
    is_pinned: bool = Field(..., alias="pinned")
    is_fullscreen: bool = Field(..., alias="fullscreen")
    fullscreen_mode: int = Field(..., alias="fullscreenMode")
    is_fake_fullscreen: bool = Field(..., alias="fakeFullscreen")


class WorkspaceData(BaseModel):
    """Represents a workspace in the Hyprland wayland compositor.

    The class allows reading of workspace attributes.

    Attributes:
        id (int): Numeric ID of the workspace.
        name (str): Name assigned to the workspace.
        monitor_name (str): Name of the monitor which this workspace is on.
        last_window_address (str): Address string of the most recently active window on the workspace.
        last_window_title (str): Title of the most recently active window on the workspace.
        window_count (int): Number of windows placed in the workspace.
        has_fullscreen (bool): True if at least one window in the workspace is in fullscreen mode.
    """
    id: int
    name: str
    monitor_name: str = Field(..., alias="monitor")
    last_window_address: HexString = Field(..., alias="lastwindow")
    last_window_title: str = Field(..., alias="lastwindowtitle")
    window_count: int = Field(..., alias="windows")
    has_fullscreen: bool = Field(..., alias="hasfullscreen")


class MonitorData(BaseModel):
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


class InstanceData(BaseModel):
    """Represents an instance of Hyprland.

    This class is not fully implemented yet. It will be used in the future to access the Hyprland IPC sockets.

    Attributes:
        signature (str): Hyprland instance signature of the current instance.
    """

    signature: NonEmptyString
