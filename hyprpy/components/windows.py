""":class:`Window` objects represent individual windows in Hyprland."""

from hyprpy.data.models import WindowData
from hyprpy.components import instances, workspaces
from hyprpy.components.common import ParentNotFoundException


class Window:
    """Represents a window in the Hyprland compositor.

    The data attributes of a :class:`Window` instance map directly to the data attributes of the underlying
    :class:`~hyprpy.data.models.WindowData`.
    """

    def __init__(self, window_data: dict, instance: 'instances.Instance'):
        self._data = WindowData.model_validate(window_data)
        self._instance = instance

    def __getattr__(self, name):
        """Relays data attribute access to the underlying :class:`~hyprpy.data.models.WindowData` data model class."""

        if name == 'instance':
            return self._instance
        else:
            return getattr(self._data, name)
    
    @property
    def workspace(self) -> 'workspaces.Workspace':
        """The :class:`~hyprpy.components.workspace.Workspace` which this window is in.

        :return: The :class:`~hyprpy.components.workspace.Workspace` this window is on.
        """

        workspace = self._instance.get_workspace_by_id(self._data.workspace_id)
        if not workspace:
            raise ParentNotFoundException(f"Parent workspace {self._data.workspace_id=} not found.")
        return workspace

    @property
    def address_as_int(self) -> int:
        """Returns the integer representation of the window's :attr:`~hyprpy.data.models.WindowData.address` property."""

        return int(self._data.address, 16)

    def __repr__(self):
        max_title_length = 24
        title_repr = self._data.title if len(self._data.title) <= max_title_length else self._data.title[:max_title_length-3] + "..."
        return f"<Window(address={self._data.address!r}, wm_class={self._data.wm_class!r}, title={title_repr!r})>"
