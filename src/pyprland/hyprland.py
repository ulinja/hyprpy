"""
hyprland
========

This module provides the `Hyprland` class, which serves as the primary interface 
to interact with the Hyprland environment. It offers methods to fetch various entities 
like `Instance`, `Window`, `Workspace`, and `Monitor`.

The entities store information about themselves in their attributes.
For more information, take a peek at the :module:`pyprland.models` module.

Usage Examples
--------------

1. Fetch all windows:

.. code-block:: python

    from pyprland import Hyprland

    windows = Hyprland.get_windows()
    for window in windows:
        print(window.wm_class)

4. Retrieve all workspaces:

.. code-block:: python

    workspaces = Hyprland.get_workspaces()
    for workspace in workspaces:
        print(workspace)

4. Get all managed monitors:

.. code-block:: python

    monitors = Hyprland.get_monitors()
    for monitor in monitors:
        print(monitor)

3. Get all windows currently on the special workspace

.. code-block:: python

    special_workspace = Hyprland.get_workspace_by_name("special")
    # alternatively: special_workspace = Hyprland.get_workspace_by_id(-99)

    if special_workspace is not None:
        special_windows = special_workspace.windows
        for window in special_windows:
            print(window.title)

5. Check whether workspace number 5 currently exists

.. code-block:: python

    workspace = Hyprland.get_workspace_by_id(5)
    if workspace:
        return true

7. Get the resolution of the first monitor

.. code-block:: python

    monitor = Hyprland.get_monitor_by_id(0)
    if monitor:
        print(f"{monitor.width} x {monitor.height}")

Main Methods
------------

- :meth:`Hyprland.get_instance`
- :meth:`Hyprland.get_windows`
- :meth:`Hyprland.get_window_by_address`
- :meth:`Hyprland.get_workspaces`
- :meth:`Hyprland.get_workspace_by_id`
- :meth:`Hyprland.get_workspace_by_name`
- :meth:`Hyprland.get_monitors`
- :meth:`Hyprland.get_monitor_by_id`
- :meth:`Hyprland.get_monitor_by_name`

For the following classes and their attributes, refer to the :module:`pyprland.models` module:
- :class:`pyprland.models.Instance`: describes the Hyprland instance
- :class:`pyprland.models.Window`: describes a Window (a.k.a. client)
- :class:`pyprland.models.Workspace`: describes a Workspace
- :class:`pyprland.models.Monitor`: describes a Monitor

Exceptions:
    Various exceptions might be raised based on context, including:
    - :class:`pyprland.exceptions.EnvironmentException`: if you invoke this library outside of a Hyprland environment.
    - :class:`pyprland.exceptions.NonZeroStatusException`: if the `hyprctl` command fails for some reason.
    - :class:`TypeError`
    - :class:`ValueError`
"""

from typing import List
import json

from pyprland.utils import shell, assertions
from pyprland.models import Instance, Monitor, Workspace, Window


class Hyprland:

    @classmethod
    def get_instance(cls) -> Instance:
        """Returns the currently running :class:`pyprland.models.instance.Instance`.

        :return: The current :class:`pyprland.models.instance.Instance` of Hyprland.
        :raises :class:`pyprland.exceptions.EnvironmentException`: If executed outside of a Hyprland environment.
        """

        return Instance.get()


    @classmethod
    def get_windows(cls) -> List[Window]:
        """Returns all :class:`pyprland.models.window.Window` currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.window.Window`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        windows_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'clients'])[0])
        return [Window.model_validate(window_dict) for window_dict in windows_json]

    @classmethod
    def get_window_by_address(cls, address: str) -> Window | None:
        """Retrieves the :class:`pyprland.models.window.Window` with the specified :param:`address`.

        The :param:`address` must be a valid hexadecimal string.
        :return: The :class:`pyprland.models.window.Window` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`address` is not a string.
        :raises :class:`ValueError`: If :param:`address` is not a valid hexadecimal string.
        """

        assertions.assert_is_hexadecimal_string(address)
        for window in cls.get_windows():
            if window.address_as_int == int(address, 16):
                return window


    @classmethod
    def get_workspaces(cls) -> List[Workspace]:
        """Returns all :class:`pyprland.models.workspace.Workspace`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.workspace.Workspace`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        workspaces_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'workspaces'])[0])
        return [Workspace.model_validate(workspace_dict) for workspace_dict in workspaces_json]

    @classmethod
    def get_workspace_by_id(cls, id: int) -> Workspace | None:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`id`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for workspace in cls.get_workspaces():
            if workspace.id == id:
                return workspace

    @classmethod
    def get_workspace_by_name(cls, name: int) -> Workspace | None:
        """Retrieves the :class:`pyprland.models.workspace.Workspace` with the specified :param:`name`.

        :return: The :class:`pyprland.models.workspace.Workspace` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        """

        assertions.assert_is_string(name)
        for workspace in cls.get_workspaces():
            if workspace.name == name:
                return workspace

    
    @classmethod
    def get_monitors(cls) -> List[Monitor]:
        """Returns all :class:`pyprland.models.monitor.Monitor`s currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.monitor.Monitor`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        monitors_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'monitors'])[0])
        return [Monitor.model_validate(monitor_dict) for monitor_dict in monitors_json]

    @classmethod
    def get_monitor_by_id(cls, id: int) -> Monitor | None:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`id`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`id` is not an integer.
        """

        assertions.assert_is_int(id)
        for monitor in cls.get_monitors():
            if monitor.id == id:
                return monitor

    @classmethod
    def get_monitor_by_name(cls, name: str) -> Monitor | None:
        """Retrieves the :class:`pyprland.models.monitor.Monitor` with the specified :param:`name`.

        :return: The :class:`pyprland.models.monitor.Monitor` if it exists, or `None` otherwise.
        :raises :class:`TypeError`: If :param:`name` is not a string.
        :raises :class:`ValueError`: If :param:`name` the empty string.
        """

        assertions.assert_is_nonempty_string(name)
        for monitor in cls.get_monitors():
            if monitor.name == name:
                return monitor
