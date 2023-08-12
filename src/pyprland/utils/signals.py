from typing import Callable, List

from pyprland.utils import assertions


class Signal():

    def __init__(self, sender: object):
        self._observers: List[Callable] = []
        self._sender = sender


    def connect(self, callback: Callable) -> None:
        """Connects the specified :param:`callback` to this :class:`Signal`.

        :raises :class:`TypeError`: if :param:`callback` is not callable.
        :raises :class:`ValueError`: if :param:`callback` does not accept keyword arguments.
        """

        assertions.assert_is_callable_and_has_first_param_sender(callback)
        assertions.assert_is_callable_and_accepts_kwargs(callback)

        self._observers.append(callback)


    def disconnect(self, callback: Callable) -> None:
        """Disconnects the specified :param:`callback` from this :class:`Signal`.

        :raises :class:`ValueError`: if the specified callback is not in the list of observers.
        """

        self._observers.remove(callback)


    def emit(self, **kwargs) -> None:
        """Notifies all observers by calling their callback functions."""

        for callback in self._observers:
            callback(self._sender, **kwargs)
