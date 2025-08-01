"""The central :class:`Instance` class for interfacing with Hyprland.

This class acts as the root for accessing other components like workspaces, windows, and monitors,
and offers capabilities to listen to events and signals emitted by the underlying Hyprland system.
"""

from typing import List, Union
import json
import logging

from hyprpy.components.instancesignals import InstanceSignalCollection
from hyprpy.components.monitors import Monitor
from hyprpy.components.windows import Window
from hyprpy.components.workspaces import Workspace
from hyprpy.data.models import InstanceData
from hyprpy.utils import assertions, shell
from hyprpy.utils.signals import DeprecatedSignal, Signal
from hyprpy.utils.sockets import CommandSocket, EventSocket


log = logging.getLogger(__name__)


class Instance:
    """Represents an active Hyprland instance.

    The Instance class is a primary interface for interacting with the Hyprland system. It provides methods
    for accessing windows, workspaces, and monitors, as well as emitting signals based on events in the
    Hyprland environment.

    :seealso: :ref:`Components: The Instance <guide-instance>`
    """

    def __init__(self, signature: str | None = None):
        if signature is None:
            signature = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')
        data = InstanceData(signature=signature)

        #: `Instance signature <https://wiki.hyprland.org/IPC/#hyprland-instance-signature-his>`_ of the Hyprland instance.
        self.signature: str = data.signature

        #: The Hyprland event socket for this instance.
        self.event_socket: EventSocket = EventSocket(signature)
        #: The Hyprland command socket for this instance.
        self.command_socket: CommandSocket = CommandSocket(signature)
        #: The :class:`~hyprpy.components.instancesignals.InstanceSignalCollection` for this instance.
        self.signals: InstanceSignalCollection = InstanceSignalCollection()

        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.createworkspace`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when a new workspace gets created.
        #: Sends ``created_workspace_id``, the :attr:`~hyprpy.components.workspaces.Workspace.id` of the created workspace, as signal data.
        self.signal_workspace_created: Signal = DeprecatedSignal(
            self,
            "Instance.signal_workspace_created",
            "Instance.signals.createworkspace"
        )
        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.destroyworkspace`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when an existing workspace gets destroyed.
        #: Sends ``destroyed_workspace_id``, the :attr:`~hyprpy.components.workspaces.Workspace.id` of the destroyed workspace, as signal data.
        self.signal_workspace_destroyed: Signal = DeprecatedSignal(
            self,
            "Instance.signal_workspace_destroyed",
            "Instance.signals.destroyworkspace"
        )
        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.workspace`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when the focus changes to another workspace.
        #: Sends ``active_workspace_id``, the :attr:`~hyprpy.components.workspaces.Workspace.id` of the now active workspace, as signal data.
        self.signal_active_workspace_changed: Signal = DeprecatedSignal(
            self,
            "Instance.signal_active_workspace_changed",
            "Instance.signals.workspace"
        )
        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.openwindow`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when a new window gets created.
        #: Sends ``created_window_address``, the :attr:`~hyprpy.components.windows.Window.address` of the newly created window, as signal data.
        self.signal_window_created: Signal = DeprecatedSignal(
            self,
            "Instance.signal_window_created",
            "Instance.signals.openwindow"
        )
        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.closewindow`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when an existing window gets destroyed.
        #: Sends ``destroyed_window_address``, the :attr:`~hyprpy.components.windows.Window.address` of the destroyed window, as signal data.
        self.signal_window_destroyed: Signal = DeprecatedSignal(
            self,
            "Instance.signal_window_destroyed",
            "Instance.signals.closewindow"
        )
        #: .. admonition:: |:no_entry_sign:| **Deprecated since v0.2.0**
        #:
        #:    This signal has been moved to :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.activewindow`
        #:    and will be removed in future versions of hyprpy.
        #:
        #: Signal emitted when the focus changes to another window.
        #: Sends ``active_window_address``, the :attr:`~hyprpy.components.windows.Window.address` of the now active window, as signal data.
        self.signal_active_window_changed: Signal = DeprecatedSignal(
            self,
            "Instance.signal_active_window_changed",
            "Instance.signals.activewindowv2"
        )


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"

    def dispatch(self, arguments: list[str]) -> Union[str, None]:
        """Runs a generic dispatcher command with the given arguments and returns ``None`` on success or a string indicating errors.

        See the `Hyprland Wiki <https://wiki.hyprland.org/Configuring/Dispatchers/>`_ for a list
        of available commands.

        Example:

        .. code-block:: python

            from hyprpy import Hyprland

            instance = Hyprland()
            instance.dispatch(["cyclenext", "prev"])

        :param arguments: A list of strings containing the arguments of the dispatch command.
        :type arguments: list[str]
        :return: `None` if the command succeeded, otherwise a string indicating errors.
        :rtype: str or None
        """

        dispatch_response = self.command_socket.send_command('dispatch', flags=['-j'], args=arguments)
        dispatch_error = dispatch_response if dispatch_response != 'ok' else None
        return dispatch_error


    def get_windows(self) -> List['Window']:
        """Returns all :class:`~hyprpy.components.windows.Window`\\ s currently managed by the instance.

        :return: A list containing :class:`~hyprpy.components.windows.Window` objects.
        """

        windows_data = json.loads(self.command_socket.send_command('clients', flags=['-j']))
        return [Window(window_data, self) for window_data in windows_data]

    def get_window_by_address(self, address: str) -> Union['Window', None]:
        """Retrieves the :class:`~hyprpy.components.windows.Window` with the specified ``address``.

        The ``address`` must be a valid hexadecimal string.

        :return: The :class:`~hyprpy.components.windows.Window` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``address`` is not a string.
        :raises: :class:`ValueError` if ``address`` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in self.get_windows():
            if window.address_as_int == int(address, 16):
                return window

    def get_active_window(self) -> 'Window':
        """Returns the currently active :class:`~hyprpy.components.windows.Window`.

        :return: The currently active :class:`~hyprpy.components.windows.Window`.
        """

        window_data = json.loads(self.command_socket.send_command('activewindow', flags=['-j']))
        return Window(window_data, self)


    def get_workspaces(self) -> List['Workspace']:
        """Returns all :class:`~hyprpy.components.workspaces.Workspace`\\ s currently managed by the instance.

        :return: A list containing :class:`~hyprpy.components.workspaces.Workspace`\\ s.
        """

        workspaces_data = json.loads(self.command_socket.send_command('workspaces', flags=['-j']))
        return [Workspace(workspace_data, self) for workspace_data in workspaces_data]

    def get_workspace_by_id(self, id: int) -> Union['Workspace', None]:
        """Retrieves the :class:`~hyprpy.components.workspaces.Workspace` with the specified ``id``.

        :return: The :class:`~hyprpy.components.workspaces.Workspace` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``id`` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in self.get_workspaces():
            if workspace.id == id:
                return workspace

    def get_active_workspace(self) -> 'Workspace':
        """Retrieves the currently active :class:`~hyprpy.components.workspaces.Workspace`.

        :return: The currently active :class:`~hyprpy.components.workspaces.Workspace`.
        """

        workspace_data = json.loads(self.command_socket.send_command('activeworkspace', flags=['-j']))
        return Workspace(workspace_data, self)

    def get_workspace_by_name(self, name: str) -> Union['Workspace', None]:
        """Retrieves the :class:`~hyprpy.components.workspaces.Workspace` with the specified ``name``.

        :return: The :class:`~hyprpy.components.workspaces.Workspace` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``name`` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in self.get_workspaces():
            if workspace.name == name:
                return workspace


    def get_monitors(self) -> List['Monitor']:
        """Returns all :class:`~hyprpy.components.monitors.Monitor`\\ s currently managed by the instance.

        :return: A list containing :class:`~hyprpy.components.monitors.Monitor`\\ s.
        """

        monitors_data = json.loads(self.command_socket.send_command('monitors', flags=['-j']))
        return [Monitor(monitor_data, self) for monitor_data in monitors_data]

    def get_monitor_by_id(self, id: int) -> Union['Monitor', None]:
        """Retrieves the :class:`~hyprpy.components.monitors.Monitor` with the specified ``id``.

        :return: The :class:`~hyprpy.components.monitors.Monitor` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``id`` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in self.get_monitors():
            if monitor.id == id:
                return monitor

    def get_monitor_by_name(self, name: str) -> Union['Monitor', None]:
        """Retrieves the :class:`~hyprpy.components.monitors.Monitor` with the specified ``name``.

        :return: The :class:`~hyprpy.components.monitors.Monitor` if it exists, or ``None`` otherwise.
        :raises: :class:`TypeError` if ``name`` is not a string.
        :raises: :class:`ValueError` if ``name`` is an empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in self.get_monitors():
            if monitor.name == name:
                return monitor

    def watch(self) -> None:
        """Continuosly monitors the :class:`~hyprpy.utils.sockets.EventSocket` and emits appropriate :class:`~hyprpy.utils.signals.Signal`\\ s when events are detected.

        This is a blocking method which runs indefinitely.
        Signals are continuosly emitted, as soon as Hyprland events are detected.

        :seealso: :ref:`Components: Reacting to events <guide-events>`
        """

        _deprecated_signal_for_event = {
            'openwindow': self.signal_window_created,
            'closewindow': self.signal_window_destroyed,
            'activewindowv2': self.signal_active_window_changed,

            'createworkspace': self.signal_workspace_created,
            'destroyworkspace': self.signal_workspace_destroyed,
            'workspace': self.signal_active_workspace_changed,
        }

        def _deprecated_handle_socket_data(event_name: str, event_data: str):
            signal = _deprecated_signal_for_event[event_name]
            if not signal._observers:
                return

            if event_name == 'openwindow':
                signal.emit(created_window_address=event_data.split(',')[0])
            elif event_name == 'closewindow':
                signal.emit(destroyed_window_address=event_data)
            elif event_name == 'activewindowv2':
                signal.emit(active_window_address=(None if event_data == ',' else event_data))

            elif event_name == 'createworkspace':
                signal.emit(created_workspace_id=(int(event_data) if event_data not in ['special', 'special:special'] else -99))
            elif event_name == 'destroyworkspace':
                signal.emit(destroyed_workspace_id=(int(event_data) if event_data not in ['special', 'special:special'] else -99))
            elif event_name == 'workspace':
                signal.emit(active_workspace_id=(int(event_data) if event_data not in ['special', 'special:special'] else -99))

        def _handle_socket_data(data: str):
            lines = list(filter(lambda line: len(line) > 0, data.split('\n')))
            for line in lines:
                event_name, event_data = line.split('>>', maxsplit=1)
                if event_name in _deprecated_signal_for_event:
                    _deprecated_handle_socket_data(event_name, event_data)
                self.signals._handle_socket_data(line)

        try:
            self.event_socket.connect()

            while True:
                self.event_socket.wait()
                data = self.event_socket.read()
                _handle_socket_data(data)
        finally:
            self.event_socket.close()
