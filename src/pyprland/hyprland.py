"""Interfaces for hyprland."""

from typing import List
import json

from pyprland.models.window import Window
from pyprland.models.instance import Instance
from pyprland.utils import shell


class Hyprland:

    @staticmethod
    def get_instance() -> Instance:
        """Returns the currently running :class:`pyprland.models.instance.Instance`.

        :return: The current :class:`pyprland.models.instance.Instance` of Hyprland.
        :raises :class:`pyprland.exceptions.EnvironmentException`: If executed outside of a Hyprland environment.
        """

        return Instance.get()


    @staticmethod
    def get_windows() -> List[Window]:
        """Returns all :class:`pyprland.models.window.Window` currently managed by Hyprland.
    
        :return: A list containing :class:`pyprland.models.window.Window`s.
        :raises :class:`pyprland.exceptions.NonZeroStatusException`: if `hyperctl` failed to execute.
        """

        windows_json = json.loads(shell.run_or_fail(['hyprctl', '-j', 'clients'])[0])
        return [Window.model_validate(window_dict) for window_dict in windows_json]
