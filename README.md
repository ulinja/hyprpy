# Pyprland

Pyprland is a library providing python bindings for the [Hyprland](https://hyprland.org/) wayland compositor.

Currently, the interface to Hyprland is read-only: you can get information about windows, workspaces and so on.
I will add IPC functionality soon, used to *send commands to*/*listen to events from* Hyprland via unix sockets.

## Quickstart

**Dependencies**:
- Python 3.7 or later
- [Pydantic 2.1](https://docs.pydantic.dev/2.1/)

If you want to use pip:

```bash
pip install -r requirements.txt
```

> I'll add a proper python package later, when the project is a bit more mature (and tested.)

### Usage examples

```python
from pyprland import Hyprland


# Fetch all windows:
windows = Hyprland.get_windows()
for window in windows:
    print(window.wm_class)


# Retrieve all workspaces:
workspaces = Hyprland.get_workspaces()
for workspace in workspaces:
    print(workspace)


# Get all managed monitors:
monitors = Hyprland.get_monitors()
for monitor in monitors:
    print(monitor)


# Get all windows currently on the special workspace
special_workspace = Hyprland.get_workspace_by_name("special")
# alternatively: special_workspace = Hyprland.get_workspace_by_id(-99)
if special_workspace is not None:
    special_windows = special_workspace.windows
    for window in special_windows:
        print(window.title)


# Check whether workspace number 5 currently exists
workspace = Hyprland.get_workspace_by_id(5)
if workspace:
    return true


# Get the resolution of the first monitor
monitor = Hyprland.get_monitor_by_id(0)
if monitor:
    print(f"{monitor.width} x {monitor.height}")
```

Pyprland is thoroughly documented. Take a peek at the [./src/pyprland/hyprland.py](hyprland) and [./src/pyprland/models.py](models) modules for more information.
