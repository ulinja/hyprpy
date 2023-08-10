"""Exceptions raised when something unexpected happens."""


class NonZeroStatusException(Exception):
    """Raised when a shell invocation returns a non-zero exit status."""
    pass


class EnvironmentException(Exception):
    """Raised when an expected environment variable could not be found."""
