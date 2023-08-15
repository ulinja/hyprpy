# Hyprpy

[Hyprpy](https://github.com/ulinja/hyprpy) is a library that provides python bindings for the [Hyprland](https://hyprland.org/) wayland compositor.

With Hyprpy you can very easily retrieve information about windows, workspaces and monitors
in a running Hyprland instance.
It also offers an event monitor, allowing you to write your own callback functions which
execute in response to Hyprland events.

Hyprpy uses unix sockets to communicate with Hyprland, making it **fast** and **efficient**.

Please [check out the documentation](https://hyprpy.lobbes.dev)!
Hyprpy is fully typed and extensively documented. Happy hacking :sunglasses:

## Quickstart

### Installation

```bash
pip install hyprpy
```

### Usage examples

```python
from hyprpy import Hyprland

instance = Hyprland()


# Fetch active window and display information:
window = instance.get_active_window()
print(window.wm_class)
print(window.width)
print(window.position_x)


# Print information about the windows on the active workspace
workspace = instance.get_active_workspace()
for window in workspace.windows:
    print(f"{window.address}: {window.title} [{window.wm_class}]")


# Get the resolution of the first monitor
monitor = instance.get_monitor_by_id(0)
if monitor:
    print(f"{monitor.width} x {monitor.height}")


# Get all windows currently on the special workspace
special_workspace = instance.get_workspace_by_name("special")
if special_workspace:
    special_windows = special_workspace.windows
    for window in special_windows:
        print(window.title)


# Show a desktop notification every time we switch to workspace 6
from hyprpy.utils.shell import run_or_fail

def workspace_changed(sender, **kwargs):
    current_workspace = kwargs.get('active_workspace')
    if current_workspace.id == 6:
        run_or_fail(["notify-send", "We are on workspace 6."])

instance.signal_active_workspace_changed.connect(workspace_changed)
instance.watch()
```

## Development

Hyprpy is in active development! Please file an issue if you find any bugs or have a feature request.

Your contributions are greatly appreciated.

### Roadmap

- [ ] dispatchers for components
- [ ] ???
