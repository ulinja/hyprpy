"""The list of signals emitted by hyprpy, which covers all `events sent by Hyprland <https://wiki.hyprland.org/IPC/#events-list>`_."""
import logging

from hyprpy.utils.signals import Signal


log = logging.getLogger(__name__)


class InstanceSignalCollection:
    """The collection of Hyprland signals emitted by an :attr:`~hyprpy.components.instances.Instance`."""

    def __init__(self):
        #: Emits the following Signal Data when a keyboard's layout is changed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================= ============ ===============================
        #:       Name              Type         Description
        #:       ================= ============ ===============================
        #:       ``keyboard_name`` :class:`str` Name of the keyboard
        #:       ``layout_name``   :class:`str` Name of the newly active layout
        #:       ================= ============ ===============================
        self.activelayout: Signal = Signal(self)

        #: Emits the following Signal Data when the special workspace on a monitor changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ======================== ====================================================================================================================================================================
        #:       Name               Type                     Description
        #:       ================== ======================== ====================================================================================================================================================================
        #:       ``workspace_name`` :class:`str` or ``None`` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace (``"special:special"``) if the special workspace was created, and ``None`` if it was destroyed
        #:       ``monitor_name``   :class:`str`             :attr:`~hyprpy.components.monitors.Monitor.name` of the monitor
        #:       ================== ======================== ====================================================================================================================================================================
        #:
        self.activespecial: Signal = Signal(self)

        #: Emits the following Signal Data when the special workspace on a monitor changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ======================== ====================================================================================================================================================================
        #:       Name               Type                     Description
        #:       ================== ======================== ====================================================================================================================================================================
        #:       ``workspace_id``   :class:`int` or ``None`` :attr:`~hyprpy.components.workspaces.Workspace.id` of the workspace (``-99``) if the special workspace was created, and ``None`` if it was destroyed
        #:       ``workspace_name`` :class:`str` or ``None`` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace (``"special:special"``) if the special workspace was created, and ``None`` if it was destroyed
        #:       ``monitor_name``   :class:`str`             :attr:`~hyprpy.components.monitors.Monitor.name` of the monitor
        #:       ================== ======================== ====================================================================================================================================================================
        #:
        self.activespecialv2: Signal = Signal(self)

        #: Emits the following Signal Data when the active window is changed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================ ============ =================================================================================
        #:       Name             Type         Description
        #:       ================ ============ =================================================================================
        #:       ``window_class`` :class:`str` The newly active window's :attr:`~hyprpy.components.windows.Window.wm_class`
        #:       ``window_title`` :class:`str` Name of the newly active window's :attr:`~hyprpy.components.windows.Window.title`
        #:       ================ ============ =================================================================================
        self.activewindow: Signal = Signal(self)

        #: Emits the following Signal Data when the active window is changed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ===========================================================================
        #:       Name               Type         Description
        #:       ================== ============ ===========================================================================
        #:       ``window_address`` :class:`str` The newly active Window's :attr:`~hyprpy.components.windows.Window.address`
        #:       ================== ============ ===========================================================================
        self.activewindowv2: Signal = Signal(self)

        #: Emits the following Signal Data when a window's floating state changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= ===============================================================
        #:       Name               Type          Description
        #:       ================== ============= ===============================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the window
        #:       ``is_floating``    :class:`bool` ``True`` if the window is floating, and ``False`` otherwise
        #:       ================== ============= ===============================================================
        self.changefloatingmode: Signal = Signal(self)

        #: Emits the following Signal Data when a layerSurface is unmapped:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ============= ============ ===========
        #:       Name          Type         Description
        #:       ============= ============ ===========
        #:       ``namespace`` :class:`str` Unknown.
        #:       ============= ============ ===========
        self.closelayer: Signal = Signal(self)

        #: Emits the following Signal Data when a window is closed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ======================================================================
        #:       Name               Type         Description
        #:       ================== ============ ======================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the closed window
        #:       ================== ============ ======================================================================
        self.closewindow: Signal = Signal(self)

        #: Emitted upon a completed config reload.
        #:
        #: Does not emit any Signal Data.
        self.configreloaded: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is created:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =============================================================================
        #:       Name               Type         Description
        #:       ================== ============ =============================================================================
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the created workspace
        #:       ================== ============ =============================================================================
        self.createworkspace: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is created:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =============================================================================
        #:       Name               Type         Description
        #:       ================== ============ =============================================================================
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the created workspace
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the created workspace
        #:       ================== ============ =============================================================================
        self.createworkspacev2: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is destroyed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ===============================================================================
        #:       Name               Type         Description
        #:       ================== ============ ===============================================================================
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the destroyed workspace
        #:       ================== ============ ===============================================================================
        self.destroyworkspace: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is destroyed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ===============================================================================
        #:       Name               Type         Description
        #:       ================== ============ ===============================================================================
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the destroyed workspace
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the destroyed workspace
        #:       ================== ============ ===============================================================================
        self.destroyworkspacev2: Signal = Signal(self)

        #: Emits the following Signal Data when the active monitor changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ==================================================================================
        #:       Name               Type         Description
        #:       ================== ============ ==================================================================================
        #:       ``monitor_name``   :class:`str` :attr:`~hyprpy.components.monitors.Monitor.name` of the newly active monitor
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the newly active workspace
        #:       ================== ============ ==================================================================================
        self.focusedmon: Signal = Signal(self)

        #: Emits the following Signal Data when the active monitor changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =======================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =======================================================================================
        #:       ``monitor_name``   :class:`str` :attr:`~hyprpy.components.monitors.Monitor.name` of the newly active monitor
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the workspace which is now active
        #:       ================== ============ =======================================================================================
        self.focusedmonv2: Signal = Signal(self)

        #: Emits the following Signal Data when the fullscreen state of any window changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================= ============= ===========================================================================================
        #:       Name              Type          Description
        #:       ================= ============= ===========================================================================================
        #:       ``is_fullscreen`` :class:`bool` ``True`` if fullscreen mode was activated, and ``False`` if fullscreen mode was deactivated
        #:       ================= ============= ===========================================================================================
        self.fullscreen: Signal = Signal(self)

        #: Emits the following Signal Data when ``ignoregrouplock`` is toggled:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ============================= ============= ==================================================================================
        #:       Name                          Type          Description
        #:       ============================= ============= ==================================================================================
        #:       ``ignore_group_lock_enabled`` :class:`bool` ``True`` if ``ignoregrouplock`` was activated, and ``False`` if it was deactivated
        #:       ============================= ============= ==================================================================================
        self.ignoregrouplock: Signal = Signal(self)

        #: Emits the following Signal Data when ``lockgroups`` is toggled:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ======================= ============= =============================================================================
        #:       Name                    Type          Description
        #:       ======================= ============= =============================================================================
        #:       ``lock_groups_enabled`` :class:`bool` ``True`` if ``lockgroups`` was activated, and ``False`` if it was deactivated
        #:       ======================= ============= =============================================================================
        self.lockgroups: Signal = Signal(self)

        #: Emits the following Signal Data when an external app requests a window to be minimized:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= ===================================================================
        #:       Name               Type          Description
        #:       ================== ============= ===================================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the window
        #:       ``is_minimized``   :class:`bool` ``True`` if the window should be minimized, and ``False`` otherwise
        #:       ================== ============= ===================================================================
        self.minimized: Signal = Signal(self)

        #: Emits the following Signal Data when a monitor is added:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================ ============ ============================================================================
        #:       Name              Type        Description
        #:       ================ ============ ============================================================================
        #:       ``monitor_name`` :class:`str`  :attr:`~hyprpy.components.monitors.Monitor.name` of the newly added monitor
        #:       ================ ============ ============================================================================
        self.monitoradded: Signal = Signal(self)

        #: Emits the following Signal Data when a monitor is added:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ======================= ============ ==================================================================================
        #:       Name                    Type         Description
        #:       ======================= ============ ==================================================================================
        #:       ``monitor_id``          :class:`int` :attr:`~hyprpy.components.monitors.Monitor.id` of the newly added monitor
        #:       ``monitor_name``        :class:`str` :attr:`~hyprpy.components.monitors.Monitor.name` of the newly added monitor
        #:       ``monitor_description`` :class:`str` :attr:`~hyprpy.components.monitors.Monitor.description` of the newly added monitor
        #:       ======================= ============ ==================================================================================
        self.monitoraddedv2: Signal = Signal(self)

        #: Emits the following Signal Data when a monitor is removed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================ ============ ========================================================================
        #:       Name              Type        Description
        #:       ================ ============ ========================================================================
        #:       ``monitor_name`` :class:`str`  :attr:`~hyprpy.components.monitors.Monitor.name` of the removed monitor
        #:       ================ ============ ========================================================================
        self.monitorremoved: Signal = Signal(self)

        #: Emits the following Signal Data when a window is merged into a group:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ======================================================================
        #:       Name               Type         Description
        #:       ================== ============ ======================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the merged window
        #:       ================== ============ ======================================================================
        self.moveintogroup: Signal = Signal(self)

        #: Emits the following Signal Data when a window is removed from a group:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =======================================================================
        #:       Name               Type         Description
        #:       ================== ============ =======================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the removed window
        #:       ================== ============ =======================================================================
        self.moveoutofgroup: Signal = Signal(self)

        #: Emits the following Signal Data when a window is moved to a workspace:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =============================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =============================================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the window which was moved
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace the window was moved to
        #:       ================== ============ =============================================================================================
        self.movewindow: Signal = Signal(self)

        #: Emits the following Signal Data when a window is moved to a workspace:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =============================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =============================================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the window which was moved
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace the window was moved to
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the workspace the window was moved to
        #:       ================== ============ =============================================================================================
        self.movewindowv2: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is moved to a different monitor:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =================================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =================================================================================================
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace which was moved
        #:       ``monitor_name``   :class:`str` :attr:`~hyprpy.components.monitors.Monitor.name` of the monitor which the workspace was moved to
        #:       ================== ============ =================================================================================================
        self.moveworkspace: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is moved to a different monitor:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =================================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =================================================================================================
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the workspace which was moved
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace which was moved
        #:       ``monitor_name``   :class:`str` :attr:`~hyprpy.components.monitors.Monitor.name` of the monitor which the workspace was moved to
        #:       ================== ============ =================================================================================================
        self.moveworkspacev2: Signal = Signal(self)

        #: Emits the following Signal Data when a layerSurface is mapped:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ===========
        #:       Name               Type         Description
        #:       ================== ============ ===========
        #:       ``namespace``      :class:`str` Unknown.
        #:       ================== ============ ===========
        self.openlayer: Signal = Signal(self)

        #: Emits the following Signal Data when a window is opened:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ====================================================================================================
        #:       Name               Type         Description
        #:       ================== ============ ====================================================================================================
        #:       ``window_address`` :class:`str` :attr:`~hyprpy.components.windows.Window.address` of the opened window
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace on which the window was opened
        #:       ``window_class``   :class:`str` The opened window's :attr:`~hyprpy.components.windows.Window.wm_class`
        #:       ``window_title``   :class:`str` Name of the opened window's :attr:`~hyprpy.components.windows.Window.title`
        #:       ================== ============ ====================================================================================================
        self.openwindow: Signal = Signal(self)

        #: Emits the following Signal Data when a window is pinned or unpinned:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= ===============================================================================
        #:       Name               Type          Description
        #:       ================== ============= ===============================================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the pinned/unpinned window
        #:       ``is_pinned``      :class:`bool` ``True`` if the window was pinned, and ``False`` if it was unpinned.
        #:       ================== ============= ===============================================================================
        self.pin: Signal = Signal(self)

        #: Emits the following Signal Data when a workspace is renamed:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ =====================================================================================
        #:       Name               Type         Description
        #:       ================== ============ =====================================================================================
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the workspace which was renamed
        #:       ``new_name``       :class:`str` New :attr:`~hyprpy.components.workspaces.Workspace.name` of the workspace
        #:       ================== ============ =====================================================================================
        self.renameworkspace: Signal = Signal(self)

        #: Emits the following Signal Data when the screencopy state of a client changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ====================== ============= ==========================================================================================================
        #:       Name                   Type          Description
        #:       ====================== ============= ==========================================================================================================
        #:       ``screencast_enabled`` :class:`bool` ``True`` if the screencast was enabled, and ``False`` if it was disabled
        #:       ``screencast_type``    :class:`str`  ``"MONITOR"`` if the screencast was enabled for a monitor, and ``"WINDOW"`` if it was enabled for a window
        #:       ====================== ============= ==========================================================================================================
        self.screencast: Signal = Signal(self)

        #: Emits the following Signal Data when a keybind submap changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       =============== ======================== =======================================================================
        #:       Name            Type                     Description
        #:       =============== ======================== =======================================================================
        #:       ``submap_name`` :class:`str` or ``None`` Name of the new submap, or ``None`` if the default submap is now active
        #:       =============== ======================== =======================================================================
        self.submap: Signal = Signal(self)

        #: Emits the following Signal Data when the togglegroup command is used:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ==================== ============= ===================================================================================================
        #:       Name                 Type          Description
        #:       ==================== ============= ===================================================================================================
        #:       ``group_is_active``  :class:`bool` ``True`` if the group was created, and ``False`` if it was destroyed
        #:       ``window_addresses`` ``list[str]`` :class:`list` of :attr:`~hyprpy.components.windows.Window.address`\ es of the windows in the group
        #:       ==================== ============= ===================================================================================================
        self.togglegroup: Signal = Signal(self)

        #: Emits the following Signal Data when a window requests an urgent state:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= =======================================================================================
        #:       Name               Type          Description
        #:       ================== ============= =======================================================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the window requesting urgent state
        #:       ================== ============= =======================================================================================
        self.urgent: Signal = Signal(self)

        #: Emits the following Signal Data when the title of a window changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= ===================================================================================
        #:       Name               Type          Description
        #:       ================== ============= ===================================================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the window whose title changed
        #:       ================== ============= ===================================================================================
        self.windowtitle: Signal = Signal(self)

        #: Emits the following Signal Data when the title of a window changes:
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============= ===================================================================================
        #:       Name               Type          Description
        #:       ================== ============= ===================================================================================
        #:       ``window_address`` :class:`str`  :attr:`~hyprpy.components.windows.Window.address` of the window whose title changed
        #:       ``window_title``   :class:`str`  :attr:`~hyprpy.components.windows.Window.title` of the window whose title changed
        #:       ================== ============= ===================================================================================
        self.windowtitlev2: Signal = Signal(self)

        #: Emits the following Signal Data when the active workspace changes (ignores mouse movements):
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ==================================================================================
        #:       Name               Type         Description
        #:       ================== ============ ==================================================================================
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the newly active workspace
        #:       ================== ============ ==================================================================================
        self.workspace: Signal = Signal(self)

        #: Emits the following Signal Data when the active workspace changes (ignores mouse movements):
        #:
        #:    .. table::
        #:       :widths: auto
        #:       :align: left
        #:
        #:       ================== ============ ==================================================================================
        #:       Name               Type         Description
        #:       ================== ============ ==================================================================================
        #:       ``workspace_name`` :class:`str` :attr:`~hyprpy.components.workspaces.Workspace.name` of the newly active workspace
        #:       ``workspace_id``   :class:`int` :attr:`~hyprpy.components.workspaces.Workspace.id` of the newly active workspace
        #:       ================== ============ ==================================================================================
        self.workspacev2: Signal = Signal(self)

    def _handle_socket_data(self, data: str) -> None:
        """Parses a line of IPC socket data to fire the appropriate Signal.

        Identifies the signal to emit, then parses the event data and emits the signal.
        """
        event_name, event_data = data.split('>>', maxsplit=1)

        try:
            signal: Signal = getattr(self, event_name)
        except AttributeError:
            log.error(f"Failed to resolve signal: unrecognized IPC event '{event_name}'")
            return
        try:
            signal_data_parser = getattr(self, f"_parse_{event_name}")
        except AttributeError:
            log.error(f"Failed to resolve signal parser: unrecognized IPC event '{event_name}'")
            return

        # If the signal has no observers, do nothing
        if not signal._observers:
            return

        try:
            signal_data: dict = signal_data_parser(event_data)
        except Exception as e:
            log.error(f"{type(e).__name__} while parsing signal data for '{event_name}': {e}")
            return

        signal.emit(**signal_data)

    def _parse_activelayout(self, data: str) -> dict:
        keyboard_name, layout_name = data.split(",", maxsplit=1)
        return {
            "keyboard_name": keyboard_name,
            "layout_name": layout_name,
        }

    def _parse_activespecial(self, data: str) -> dict:
        workspace_name, monitor_name = data.split(",", maxsplit=1)
        return {
            "workspace_name": workspace_name or None,
            "monitor_name": monitor_name,
        }

    def _parse_activespecialv2(self, data: str) -> dict:
        workspace_id, workspace_name, monitor_name = data.split(",", maxsplit=2)
        return {
            "workspace_id": int(workspace_id) if workspace_id else None,
            "workspace_name": workspace_name or None,
            "monitor_name": monitor_name,
        }

    def _parse_activewindow(self, data: str) -> dict:
        window_class, window_title = data.split(",", maxsplit=1)
        return {
            "window_class": window_class,
            "window_title": window_title,
        }

    def _parse_activewindowv2(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_changefloatingmode(self, data: str) -> dict:
        window_address, is_floating = data.split(",")
        return {
            "window_address": window_address,
            "is_floating": bool(int(is_floating)),
        }

    def _parse_closelayer(self, data: str) -> dict:
        return {
            "namespace": data,
        }

    def _parse_closewindow(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_configreloaded(self, data: str) -> dict:
        return {}

    def _parse_createworkspace(self, data: str) -> dict:
        return {
            "workspace_name": data,
        }

    def _parse_createworkspacev2(self, data: str) -> dict:
        workspace_id, workspace_name = data.split(",", maxsplit=1)
        return {
            "workspace_id": int(workspace_id),
            "workspace_name": workspace_name,
        }

    def _parse_destroyworkspace(self, data: str) -> dict:
        return {
            "workspace_name": data,
        }

    def _parse_destroyworkspacev2(self, data: str) -> dict:
        workspace_id, workspace_name = data.split(",", maxsplit=1)
        return {
            "workspace_id": int(workspace_id),
            "workspace_name": workspace_name,
        }

    def _parse_focusedmon(self, data: str) -> dict:
        monitor_name, workspace_name = data.split(",", maxsplit=1)
        return {
            "monitor_name": monitor_name,
            "workspace_name": workspace_name,
        }

    def _parse_focusedmonv2(self, data: str) -> dict:
        monitor_name, workspace_id = data.rsplit(",", maxsplit=1)
        return {
            "monitor_name": monitor_name,
            "workspace_id": int(workspace_id),
        }

    def _parse_fullscreen(self, data: str) -> dict:
        return {
            "is_fullscreen": bool(int(data)),
        }

    def _parse_ignoregrouplock(self, data: str) -> dict:
        return {
            "ignore_group_lock_enabled": bool(int(data)),
        }

    def _parse_lockgroups(self, data: str) -> dict:
        return {
            "lock_groups_enabled": bool(int(data)),
        }

    def _parse_minimized(self, data: str) -> dict:
        window_address, is_minimized = data.split(",")
        return {
            "window_address": window_address,
            "is_minimized": bool(int(is_minimized)),
        }

    def _parse_monitoradded(self, data: str) -> dict:
        return {
            "monitor_name": data,
        }

    def _parse_monitoraddedv2(self, data: str) -> dict:
        monitor_id, monitor_name, monitor_description = data.split(",", maxsplit=2)
        return {
            "monitor_id": int(monitor_id),
            "monitor_name": monitor_name,
            "monitor_description": monitor_description,
        }

    def _parse_monitorremoved(self, data: str) -> dict:
        return {
            "monitor_name": data,
        }

    def _parse_moveintogroup(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_moveoutofgroup(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_movewindow(self, data: str) -> dict:
        window_address, workspace_name = data.split(",", maxsplit=1)
        return {
            "window_address": window_address,
            "workspace_name": workspace_name,
        }

    def _parse_movewindowv2(self, data: str) -> dict:
        window_address, _other = data.split(",", maxsplit=1)
        workspace_id, workspace_name = _other.rsplit(",", maxsplit=1)
        return {
            "window_address": window_address,
            "workspace_id": int(workspace_id),
            "workspace_name": workspace_name,
        }

    def _parse_moveworkspace(self, data: str) -> dict:
        workspace_name, monitor_name = data.rsplit(",", maxsplit=1)
        return {
            "workspace_name": workspace_name,
            "monitor_name": monitor_name,
        }

    def _parse_moveworkspacev2(self, data: str) -> dict:
        workspace_id, _other = data.split(",", maxsplit=1)
        workspace_name, monitor_name = _other.rsplit(",", maxsplit=1)
        return {
            "workspace_id": int(workspace_id),
            "workspace_name": workspace_name,
            "monitor_name": monitor_name,
        }

    def _parse_openlayer(self, data: str) -> dict:
        return {
            "namespace": data,
        }

    def _parse_openwindow(self, data: str) -> dict:
        window_address, workspace_name, window_class, window_title = data.split(",", maxsplit=3)
        return {
            "window_address": window_address,
            "workspace_name": workspace_name,
            "window_class": window_class,
            "window_title": window_title,
        }

    def _parse_pin(self, data: str) -> dict:
        window_address, is_pinned = data.split(",")
        return {
            "window_address": window_address,
            "is_pinned": bool(int(is_pinned)),
        }

    def _parse_renameworkspace(self, data: str) -> dict:
        workspace_id, new_name = data.split(",", maxsplit=1)
        return {
            "workspace_id": int(workspace_id),
            "new_name": new_name,
        }

    def _parse_screencast(self, data: str) -> dict:
        screencast_enabled, _screencast_type_numeric = data.split(",")
        screencast_type = "MONITOR" if int(_screencast_type_numeric) == 0 else "WINDOW"
        return {
            "screencast_enabled": bool(int(screencast_enabled)),
            "screencast_type": screencast_type,
        }

    def _parse_submap(self, data: str) -> dict:
        return {
            "submap_name": data or None,
        }

    def _parse_togglegroup(self, data: str) -> dict:
        group_is_active, window_addresses = data.split(",", maxsplit=1)
        return {
            "group_is_active": bool(int(group_is_active)),
            "window_addresses": window_addresses.split(","),
        }

    def _parse_urgent(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_windowtitle(self, data: str) -> dict:
        return {
            "window_address": data,
        }

    def _parse_windowtitlev2(self, data: str) -> dict:
        window_address, window_title = data.split(",", maxsplit=1)
        return {
            "window_address": window_address,
            "window_title": window_title,
        }

    def _parse_workspace(self, data: str) -> dict:
        return {
            "workspace_name": data,
        }

    def _parse_workspacev2(self, data: str) -> dict:
        workspace_id, workspace_name = data.rsplit(",", maxsplit=1)
        return {
            "workspace_name": workspace_name,
            "workspace_id": int(workspace_id),
        }
