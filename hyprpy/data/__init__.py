"""The `data` module provides Pydantic-based data model classes designed for defining 
the data structure, validation, and serialization/deserialization of the various 
Hyprland components. These model classes act as the central point of data transformation, 
ensuring that data retrieved from Hyprland is correctly structured and validated.

Utility:
    Through `Pydantic <https://docs.pydantic.dev/latest/>`_, the library offers
    a robust mechanism for parsing, validating, and serializing JSON data.
    The source of this JSON data is primarily the :class:`~hyprpy.utils.sockets.CommandSocket`
    which interacts with Hyprland to retrieve current state and event information.

    Notably, these data models not only handle validation but also perform renaming of 
    JSON properties to provide a more Pythonic interface.

Serialization:
    The instantiated data model objects are easily serializable back into JSON, providing 
    flexibility in both consuming Hyprland data and in using it for further operations.

Example:

    .. code-block:: python

        >>> from hyprpy.data.models import WindowData

        >>> # Output from `hyprctl -j clients` for example
        >>> window_json_str = '''
            {
                "address": "0x1981f40",
                "mapped": true,
                "hidden": false,
                "at": [11, 11],
                "size": [1344, 746],
                "workspace": {
                    "id": 1,
                    "name": "1"
                },
                "floating": false,
                "monitor": 0,
                "class": "kitty",
                "title": "python ~/d/p/src",
                "initialClass": "kitty",
                "initialTitle": "fish",
                "pid": 1782,
                "xwayland": false,
                "pinned": false,
                "fullscreen": false,
                "fullscreenMode": 0,
                "fakeFullscreen": false,
                "grouped": [],
                "swallowing": null
            }
            '''

        >>> # Deserialize and validate JSON, creating an object
        >>> window_data = WindowData.model_validate_json(window_json_str)

        >>> # Access window data properties
        >>> window_data.pid
        1782
        >>> window_data.floating
        False

        >>> # Serialize back into JSON
        >>> print(window_data.model_dump_json(indent=2))
        {
          "address": "0x1981f40",
          "is_mapped": true,
          "is_hidden": false,
          "position_x": 11,
          "position_y": 11,
          "width": 1344,
          "height": 746,
          "workspace_id": 1,
          "workspace_name": "1",
          "is_floating": false,
          "monitor_id": 0,
          "wm_class": "kitty",
          "title": "python ~/d/p/src",
          "initial_wm_class": "kitty",
          "initial_title": "fish",
          "pid": 1782,
          "is_xwayland": false,
          "is_pinned": false,
          "is_fullscreen": false,
          "fullscreen_mode": 0,
          "is_fake_fullscreen": false
        }
"""
