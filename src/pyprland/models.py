"""
Models for Hyprland Objects
===========================

This module provides classes representing objects in the Hyprland wayland compositor:

- :class:`pyprland.models.Window`: Represents individual windows.
- :class:`pyprland.models.Workspace`: Represents workspaces.
- :class:`pyprland.models.Monitor`: Represents monitors.
- :class:`pyprland.models.Instance`: Represents the current Hyprland instance.

These models are designed to be instantiated by parsing the JSON output from the `hyprctl` command-line utility.
In order to validate the JSON inputs (type safety and format), and to give the object properties more pythonic
names, Pydantic is used heavily.

The :module:`pyprland.hyprland` handles running `hyprctl` for you in its provided convenience functions, so you shouldn't need to 
instantiate these objects yourself. However, they provide read-access to all dynamic properties of your Hyprland instance.
The instantiated objects not only store their intrinsic attributes (e.g., dimensions, IDs, names), but also provide properties
to access related objects. For instance:

- A window's associated workspace can be accessed using the :attr:`pyprland.models.Window.workspace` property.
- A workspace's list of contained windows can be accessed via the :attr:`pyprland.models.Workspace.windows` property.

For completeness, here is an example of how to instantiate objects from JSON:

Examples:
---------

.. code-block:: python

    import json

    from pyprland.utils import shell
    from pyprland.models import Window, Workspace


    # Use `hyperctl` to get the list of all windows
    json_string = shell.run_or_fail(['hyprctl', '-j', 'clients'])[0]
    windows_list = json.loads(json_string)

    # Instantiate a window using the `Window` class
    first_window = Window.model_validate(windows_list[0])

    # Use the instantiated `Window` object to get the `Workspace` which the window is in
    workspace = window.workspace

"""

from typing import List

from pydantic import BaseModel, Field, AliasPath

from pyprland.utils import shell
from pyprland.validators.common import HexString, NonEmptyString
from pyprland.exceptions import ParentNotFoundException


class Window(BaseModel):
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

    
    @property
    def workspace(self) -> 'Workspace':
        """Returns the :class:`pyprland.models.workspace.Workspace` which this window is in.

        :return: The :class:`pyprland.models.workspace.Workspace` this window is on.
        """

        from pyprland.hyprland import Hyprland
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


class Workspace(BaseModel):
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


    @property
    def monitor(self) -> 'Monitor':
        """Returns the :class:`pyprland.models.monitor.Monitor` which this workspace is on.

        :return: The :class:`pyprland.models.monitor.Monitor` this workspace is on.
        """

        from pyprland.hyprland import Hyprland
        monitor = Hyprland.get_monitor_by_name(self.monitor_name)
        if not monitor:
            raise ParentNotFoundException(f"Parent monitor {self.monitor_name=!r} not found.")
        return monitor


    @property
    def windows(self) -> List[Window]:
        """Returns all :class:`pyprland.models.window.Window`s on this workspace.

        :return: A list containing all :class:`pyprland.models.window.Window`s on this workspace.
        """

        from pyprland.hyprland import Hyprland
        windows = []
        for window in Hyprland.get_windows():
            if window.workspace_id == self.id:
                windows.append(window)
        return windows


    @property
    def last_window_address_as_int(self) -> int:
        """Returns the integer representation of the window's `last_window_address` property."""

        return int(self.last_window_address, 16)


    def __repr__(self):
        return f"<Workspace(id={self.id}, name={self.name!r})>"


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

        from pyprland.hyprland import Hyprland
        workspaces = []
        for workspace in Hyprland.get_workspaces():
            if workspace.monitor_name == self.name:
                workspaces.append(workspace)
        return workspaces


    def __repr__(self):
        return f"<Monitor(id={self.id}, name={self.name!r}, width={self.width}, height={self.height})>"


class Instance(BaseModel):
    """Represents an instance of Hyprland.

    This class is not fully implemented yet. It will be used in the future to access the Hyprland IPC sockets.

    Attributes:
        signature (str): Hyprland instance signature of the current instance.
    """

    signature: NonEmptyString


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"


    @classmethod
    def get(cls):
        """Retrieves the current Hyprland instance."""

        instance_signature = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')
        return cls.model_validate({'signature': instance_signature})
