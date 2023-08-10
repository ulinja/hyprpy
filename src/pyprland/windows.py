"""Interface for Hyprland windows."""

import logging
import json
from typing import List

from pyprland.utils import assertions, shell
from pyprland.exceptions import ParseError


log = logging.getLogger(__name__)


class Window:
    def __init__(
        self,
        address: str,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        workspace_id: int,
        workspace_name: str,
        monitor_id: int,
        pid: int,
        wm_class: str,
        title: str,
        initial_wm_class: str,
        initial_title: str,
        fullscreen_mode: int,
        is_floating: bool,
        is_fullscreen: bool,
        is_hidden: bool,
        is_xwayland: bool,
        is_fake_fullscreen: bool,
        is_mapped: bool,
        is_pinned: bool,
    ):
        assertions.assert_is_hexadecimal_string(address)

        for value in [
            position_x,
            position_y,
            width,
            height,
            workspace_id,
            monitor_id,
            pid,
            fullscreen_mode
        ]:
            assertions.assert_is_int(value)

        for value in [
            wm_class,
            title,
            initial_wm_class,
            initial_title,
            workspace_name
        ]:
            assertions.assert_is_string(value)

        for value in [
            is_floating,
            is_fullscreen,
            is_hidden,
            is_xwayland,
            is_fake_fullscreen,
            is_mapped,
            is_pinned,
        ]:
            assertions.assert_is_bool(value)

        self.address = address
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.monitor_id = monitor_id
        self.pid = pid
        self.wm_class = wm_class
        self.title = title
        self.initial_wm_class = initial_wm_class
        self.initial_title = initial_title
        self.is_floating = is_floating
        self.is_fullscreen = is_fullscreen
        self.is_hidden = is_hidden
        self.is_xwayland = is_xwayland
        self.is_fake_fullscreen = is_fake_fullscreen
        self.is_mapped = is_mapped
        self.is_pinned = is_pinned
        self.fullscreen_mode = fullscreen_mode

    @classmethod
    def _from_json(cls, json_str: str) -> List['Window']:
        # I am repeating `log.error` and `raise ParseError` often
        # here because my linter complains about unbound values
        # if I try to refactor it into a function.

        try:
            data = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            log.error(f"Error while parsing windows from JSON: {json_str}")
            raise ParseError("Invalid JSON.")

        if not isinstance(data, list):
            log.error(f"Error while parsing windows from JSON: {json_str}")
            raise ParseError(f"Expected a list but got {type(data)}")

        windows = []

        for item in data:
            try:
                address = item["address"]
                position_x, position_y = item["at"]
                width, height = item["size"]
                workspace_id = item["workspace"]["id"]
                workspace_name = item["workspace"]["name"]
                monitor_id = item["monitor"]
                pid = item["pid"]
                wm_class = item["class"]
                title = item["title"]
                initial_wm_class = item["initialClass"]
                initial_title = item["initialTitle"]
                fullscreen_mode = item["fullscreenMode"]
                is_floating = item["floating"]
                is_fullscreen = item["fullscreen"]
                is_hidden = item["hidden"]
                is_xwayland = item["xwayland"]
                is_fake_fullscreen = item["fakeFullscreen"]
                is_mapped = item["mapped"]
                is_pinned = item["pinned"]

            except ValueError as e:
                log.error(f"Error while parsing windows from JSON: {item}")
                raise ParseError(f"Unexpected JSON structure (value error): {e}")
            except KeyError as e:
                log.error(f"Error while parsing windows from JSON: {item}")
                raise ParseError(f"Unexpected JSON structure (missing key): {e}")

            try:
                windows.append(cls(
                    address=address,
                    position_x=position_x,
                    position_y=position_y,
                    width=width,
                    height=height,
                    workspace_id=workspace_id,
                    workspace_name=workspace_name,
                    monitor_id=monitor_id,
                    pid=pid,
                    wm_class=wm_class,
                    title=title,
                    initial_wm_class=initial_wm_class,
                    initial_title=initial_title,
                    fullscreen_mode=fullscreen_mode,
                    is_floating=is_floating,
                    is_fullscreen=is_fullscreen,
                    is_hidden=is_hidden,
                    is_xwayland=is_xwayland,
                    is_fake_fullscreen=is_fake_fullscreen,
                    is_mapped=is_mapped,
                    is_pinned=is_pinned
                ))
            except TypeError as e:
                log.error(f"Error while parsing windows from JSON: {item}")
                raise ParseError(f"Unexpected JSON format (type mismatch): {e}")
            except ValueError as e:
                log.error(f"Error while parsing windows from JSON: {item}")
                raise ParseError(f"Unexpected JSON format (value error): {e}")

        return windows


    @property
    def id_as_int(self) -> int:
        return int(self.address, 16)
