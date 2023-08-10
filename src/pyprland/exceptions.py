"""Exceptions raised when something unexpected happens."""


class NonZeroStatusException(Exception):
    """Raised when a shell invocation returns a non-zero exit status."""
    pass


class ParseError(Exception):
    """Raised when a parsing attempt is unsuccessful."""
