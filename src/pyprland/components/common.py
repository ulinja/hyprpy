"""Common classes, shared among different components."""


class ParentNotFoundException(Exception):
    """Raised when a component's parent could not be found.

    This exception may occur due to programming errors or race conditions, for example when
    a :class:`pyprland.components.windows.Window` knows the ID of the
    :class:`pyprland.components.workspaces.Workspace` it is on, but no workspace with that ID
    exists.
    """
