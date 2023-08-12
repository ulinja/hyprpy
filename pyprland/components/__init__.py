"""
pyprland.components
~~~~~~~~~~~~~~~~~~~

This module provides the main interface to Hyprland components for library users.

Interface to Components
-----------------------
The components offer a high-level representation of various entities managed by Hyprland. Each component is modeled 
in a way that it reflects the current state in Hyprland. A component's data attributes, as defined in 
:mod:`pyprland.data`, can be accessed directly as properties of the component. 

Moreover, similar to object-relational-mappers, these components provide intuitive access to their parent and child 
components, encapsulating the hierarchical structure of entities in Hyprland.

Example:

.. code-block:: python

   from pyprland.components.instances import Instance

   # Get the current instance
   instance = Instance()
   print(repr(instance))
   # Output: "<Instance(signature='v0.25.0_1691839240')>"

   # Get a window and its properties
   window = instance.get_windows()[0]
   print(repr(window))
   # Output: "<Window(address='0x1981f40', wm_class='kitty', title='python ~/d/p/src')>"
   print(window.workspace)
   # Output: "<Workspace(id=1, name='1')>"
   print(window.workspace.window_count)
   # Output: 1

.. note:: Accessing a related component involves an underlying socket write and read. As Hyprland manages 
   these operations synchronously, performing many lookups in quick succession or over a prolonged period may result 
   in sluggish performance.

Special Components: The Instance
--------------------------------
The :class:`pyprland.components.instances.Instance` holds a special place among components. It acts as a gateway to all 
other components managed by its corresponding Hyprland instance. Besides direct access to data and relations, the 
Instance class provides a method :meth:`pyprland.components.instances.Instance.watch` to actively monitor Hyprland 
events.

As events are detected, appropriate :class:`pyprland.utils.signals.Signal` instances are emitted, which can trigger 
user-defined callback functions, enabling dynamic python code execution in response to changes in Hyprland's state.

.. list-table:: Instance Signals
   :widths: 30 40 30
   :header-rows: 1

   * - Signal Attribute
     - Emission Condition
     - Returned Keyword Arguments
   * - :attr:`pyprland.components.instances.Instance.signal_workspace_created`
     - New workspace creation
     - `new_workspace`: the newly created :class:`pyprland.components.workspaces.Workspace`
   * - :attr:`pyprland.components.instances.Instance.signal_workspace_destroyed`
     - Workspace destruction
     - `destroyed_workspace_id`: ID of the destroyed workspace (integer)
   * - :attr:`pyprland.components.instances.Instance.signal_active_workspace_changed`
     - Active workspace change
     - `active_workspace`: the now active :class:`pyprland.components.workspaces.Workspace`
   * - :attr:`pyprland.components.instances.Instance.signal_window_created`
     - New window creation
     - `new_window`: the newly created :class:`pyprland.components.windows.Window`
   * - :attr:`pyprland.components.instances.Instance.signal_window_destroyed`
     - Window destruction
     - `destroyed_window_address`: hexadecimal address of the destroyed window
   * - :attr:`pyprland.components.instances.Instance.signal_active_window_changed`
     - Active window change
     - `active_window`: the now active :class:`pyprland.components.windows.Window`

Library users can attach callback functions to these signals. When the associated event is detected in Hyprland, the 
callback is invoked. This system ensures immediate, efficient reactions to state changes in Hyprland without 
frequent polling.

Example:

.. code-block:: python

   # Shorthand for 'import pyprland.components.instances.Instance as Hyprland':
   from pyprland import Hyprland

   from pyprland.utils.shell import run_or_fail

   # Get the current instance
   instance = Hyprland()

   # Define a callback function
   # The function signature must be: (sender, **kwargs)
   def on_active_workspace_changed(sender, **kwargs):
       active_workspace = kwargs.get('active_workspace')
       run_or_fail(["notify-send", "Workspace Changed", f"Active workspace is now {active_workspace.id}"])
    
   # Connect the callback function to the signal
   instance.signal_active_workspace_changed.connect(on_active_workspace_changed)

   # Start watching for hyprland events
   instance.watch()

In this example, a desktop notification showing the current workspace is displayed (using `notify-send`) each
time the active workspace changes.

.. note:: The :meth:`pyprland.components.instances.Instance.watch` method is a blocking operation that runs 
   indefinitely. It avoids polling by monitoring the event socket.

"""
