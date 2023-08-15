""":class:`Window` objects represent individual windows in Hyprland."""

from hyprpy.data.models import WindowData
from hyprpy.components import instances, workspaces
from hyprpy.components.common import ParentNotFoundException


class Window:
    """Represents a window in the Hyprland compositor."""

    def __init__(self, window_data: dict, instance: 'instances.Instance'):
        data = WindowData.model_validate(window_data)

        #: String representation of a hexadecimal number, unique identifier for the window.
        self.address: str = data.address
        #: Unknown.
        self.is_mapped: bool = data.is_mapped
        #: Unknown.
        self.is_hidden: bool = data.is_hidden
        #: Absolute X-coordinate of the window on the monitor (in pixels).
        self.position_x: int = data.position_x
        #: Absolute Y-coordinate of the window on the monitor (in pixels).
        self.position_y: int = data.position_y
        #: Width of the window (in pixels).
        self.width: int = data.width
        #: Height of the window (in pixels).
        self.height: int = data.height
        #: Numeric ID of the workspace which the window is on.
        self.workspace_id: int = data.workspace_id
        #: Name of the workspace which the window is on.
        self.workspace_name: str = data.workspace_name
        #: Whether or not this is a floating window.
        self.is_floating: bool = data.is_floating
        #: Numeric ID of the monitor which the window is on.
        self.monitor_id: int = data.monitor_id
        #: Window manager class assigned to this window.
        self.wm_class: str = data.wm_class
        #: Current title of the window.
        self.title: str = data.title
        #: Window manager class when the window was created.
        self.initial_wm_class: str = data.initial_wm_class
        #: Title when the window was created.
        self.initial_title: str = data.initial_title
        #: Process ID of the process the window is assigned to.
        self.pid: int = data.pid
        #: Whether or not the window is using xwayland to be displayed.
        self.is_xwayland: bool = data.is_xwayland
        #: Unknown.
        self.is_pinned: bool = data.is_pinned
        #: Whether or not the window is in fullscreen mode.
        self.is_fullscreen: bool = data.is_fullscreen
        #: Unknown.
        self.fullscreen_mode: int = data.fullscreen_mode
        #: Unknown.
        self.is_fake_fullscreen: bool = data.is_fake_fullscreen

        #: The :class:`~hyprpy.components.instances.Instance` managing this window.
        self._instance = instance


    @property
    def workspace(self) -> 'workspaces.Workspace':
        """The :class:`~hyprpy.components.workspace.Workspace` which this window is in."""

        workspace = self._instance.get_workspace_by_id(self.workspace_id)
        if not workspace:
            raise ParentNotFoundException(f"Parent workspace {self.workspace_id=} not found.")
        return workspace


    @property
    def address_as_int(self) -> int:
        """The integer representation of the window's :attr:`~hyprpy.data.models.WindowData.address` property."""

        return int(self.address, 16)


    def __repr__(self):
        max_title_length = 24
        title_repr = self.title if len(self.title) <= max_title_length else self.title[:max_title_length-3] + "..."
        return f"<Window(address={self.address!r}, wm_class={self.wm_class!r}, title={title_repr!r})>"
