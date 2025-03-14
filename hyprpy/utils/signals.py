"""A basic implementation of the observer pattern for emitting signals and connecting 
listeners to them, similar to the Django signals framework.

This module allows objects to declare signals that other parts of the application can
connect callbacks to. When the signal is emitted, all connected callbacks are executed.

Example:

.. code-block:: python

    from hyprpy.utils.signals import Signal

    class MyClass:
        def __init__(self):
            self.my_signal = Signal(sender=self)

        def perform_action(self):
            self.my_signal.emit(info="Action performed!")

    def my_callback(sender, **kwargs):
        print(f"{sender} says: {kwargs['info']}")

    obj = MyClass()
    obj.my_signal.connect(my_callback)
    obj.perform_action()
    # Output: <MyClass object at 0x...> says: Action performed!

:seealso: :ref:`Components: Reacting to events <guide-events>`

"""

from typing import Callable, List
import logging

from hyprpy.utils import assertions


log = logging.getLogger(__name__)


class Signal():
    """A signal that can have multiple observers (callbacks) connected to it.

    Each time the signal is emitted, all connected callbacks are executed.
    When instantiating a signal, the sending object (sender) **must** be passed to
    the signal's constructor.

    :param sender: The source object sending the signal.
    :type sender: :class:`object`

    Example:

    .. code-block:: python

        class MyClass:
            def __init__(self):
                self.my_signal = Signal(sender=self)

            def do_something(self):
                self.my_signal.emit(action="something_done")

        obj = MyClass()
    """

    def __init__(self, sender: object):
        self._observers: List[Callable] = []
        self._sender: object = sender


    def connect(self, callback: Callable) -> None:
        """Connects the specified ``callback`` to this :class:`Signal`.

        The callback signature **must** contain ``sender`` as the positional argument,
        followed by ``**kwargs``.

        :param callback: The callback function to be connected to this signal.
        :type callback: :class:`Callable`
        :raises: :class:`TypeError` if ``callback`` is not callable.
        :raises: :class:`ValueError` if the first positional argument of ``callback`` is not ``sender``.
        :raises: :class:`ValueError` if ``callback`` does not accept keyword arguments.

        Example:

        .. code-block:: python

            def my_callback(sender, **kwargs):
                print(sender, kwargs)

            obj.signal.connect(my_callback)
        """

        assertions.assert_is_callable_and_has_first_param_sender(callback)
        assertions.assert_is_callable_and_accepts_kwargs(callback)

        self._observers.append(callback)


    def disconnect(self, callback: Callable) -> None:
        """Disconnects the specified ``callback`` from this :class:`Signal`.

        This is useful if you want to limit how often a callback should be executed.

        :param callback: The callback function to be disconnected.
        :type callback: :class:`Callable`
        :raises: :class:`ValueError` if the specified callback is not in the list of observers.

        Example:

        .. code-block:: python

            def my_callback(sender, **kwargs):
                print(sender, kwargs)

            obj.signal.connect(my_callback)
            ...
            # some time later
            ...
            signal.disconnect(my_callback)
        """

        self._observers.remove(callback)


    def emit(self, **kwargs) -> None:
        """Emits the signal, notifying all observers by calling their callback functions.

        Any information to be sent to the observers should be provided as keyword arguments to
        this method.

        :param \\**kwargs: Keyword arguments that will be passed to each callback.
        :type \\**kwargs: :class:`dict[str, any]`

        Example:

        .. code-block:: python

            def my_callback(sender, **kwargs):
                print(kwargs['message'])

            obj.signal.connect(my_callback)
            ...
            obj.signal.emit(message="Hello from sender!")
        """

        for callback in self._observers:
            callback(self._sender, **kwargs)


class DeprecatedSignal(Signal):
    """Behaves just like a normal :class:`~hyprpy.utils.signals.Signal`, but logs deprecation warnings to the console.

    A warning message is printed to the log whenever this Signal's methods are invoked.

    :param sender: The source object sending the signal.
    :type sender: :class:`object`
    :param message: The warning message to log when this Signal gets used. This should be an informative deprecation warning.
    :type message: :class:`str`
    """

    def __init__(self, sender: object, message: str):
        super().__init__(sender)
        self.message = message
        log.warning(self.message)


    def connect(self, callback: Callable) -> None:
        super().connect(callback)
        log.warning(self.message)


    def disconnect(self, callback: Callable) -> None:
        super().disconnect(callback)
        log.warning(self.message)

    def emit(self, **kwargs) -> None:
        super().emit(**kwargs)
        log.warning(self.message)
