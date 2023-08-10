"""Pydantic model representing Hyprland windows (a.k.a. clients).

This module provides a way to query Hyprland window objects (clients). The window objects are
primarily constructed by parsing the output from the `hyprctl` command-line utility, which provides detailed
information about the state of windows managed by Hyprland.

Typical usage involves instantiating a `Window` object by deserializing JSON data obtained from `hyprctl`.

Classes:
    Window: Represents a window (client), and contains all available information about the window.
"""

from pydantic import BaseModel, Field, AliasPath

from pyprland.validators.common import HexString
from pyprland.models.workspace import Workspace
from pyprland.hyprland import Hyprland
from pyprland.exceptions import ParentNotFoundException


class Window(BaseModel):
    """Represents a window or client in the Hyprland wayland compositor.

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

    
    @property
    def workspace(self) -> Workspace:
        """Returns the :class:`pyprland.models.workspace.Workspace` which this window is in.

        :return: The :class:`pyprland.models.workspace.Workspace` this window is on.
        """

        workspace = Hyprland.get_workspace_by_id(self.workspace_id)
        if not workspace:
            raise ParentNotFoundException(f"Parent workspace {self.workspace_id=} not found.")
        return workspace


    @property
    def address_as_int(self) -> int:
        """Returns the integer representation of the window's `address` property."""

        return int(self.address, 16)


    def __repr__(self):
        max_title_length = 24
        title_repr = self.title if len(self.title) <= max_title_length else self.title[:max_title_length-3] + "..."
        return f"<Window(address={self.address!r}, wm_class={self.wm_class!r}, title={title_repr!r})>"
