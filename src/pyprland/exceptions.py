"""Exceptions raised when something unexpected happens."""


class NonZeroStatusException(Exception):
    """Raised when a shell invocation returns a non-zero exit status."""
    pass


class EnvironmentException(Exception):
    """Raised when an expected environment variable could not be found."""


class ParentNotFoundException(Exception):
    """Raised when an object's parent could not be found.

    This exception should only ever occur due to a programming error, for example when
    a :class:`pyprland.models.window.Window` knows the ID of the workspace it is on, but
    no workspace with that ID exists in the list of all workspaces.
    """
