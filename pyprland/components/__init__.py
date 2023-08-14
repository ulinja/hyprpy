"""Pyprland components represent all the moving parts of a running Hyprland instance.
They allow us to retrieve information about the compositor in real time.

Pyprland handles four component types:

* :mod:`~pyprland.components.instances`
* :mod:`~pyprland.components.monitors`
* :mod:`~pyprland.components.workspaces`
* :mod:`~pyprland.components.windows`

Let's get started, and go through some examples.

.. _guide-instance:

The Instance
------------

To retrieve a component, we first have to get the current Hyprland instance:

.. code-block:: python

    from pyprland.components.instances import Instance

    # Get the current instance
    instance = Instance()

We can also use the shorthand alias ``Hyprland``, which looks slightly nicer:

.. code-block:: python

    from pyprland import Hyprland

    instance = Hyprland()

By default, Pyprland reads the ``$HYPRLAND_INSTANCE_SIGNATURE`` environment variable to find the `Hyprland Instance Signature <https://wiki.hyprland.org/IPC/#hyprland-instance-signature-his>`_.
If the environment variable is unset because we are in an SSH session, or if we want to access a second
Hyprland instance running on our system, we can specify its value manually:

.. code-block:: python

    from pyprland import Hyprland

    instance = Hyprland("v0.25.0_1691941479")

.. _guide-component-data:

Reading component data
----------------------

Now that we have our instance, we can query it for components.
Components have *data attributes*, which allow us to access information about them.
Let's grab the first window we can find and print some information about it:

.. code-block:: python

    from pyprland import Hyprland

    instance = Hyprland()

    window = instance.get_windows()[0]
    print(window)
    # Output: "<Window(address='0x1981f40', wm_class='kitty', title='python ~/d/p/src')>"
    print(window.width)
    # Output: 1258
    print(window.wm_class)
    # Output: 'firefox'

Here, we queried the instance for all windows, and just grabbed the first one for the sake of demonstration.
We printed the window's ``width`` and ``wm_class`` data attributes, which tell us the current
width and display class of the window.

Windows, workspaces and monitors have a wide range of useful data attributes.
For a complete list of data attributes for each type of component, refer to the
:ref:`data model class API <api-data-model-classes>`, which defines the underlying data model
for Pyprland components.

.. note:: Component data attributes are **read-only**.
    Writing new values into them will not raise an exception, but will also have no effect on Hyprland's actual state.

Accessing related components
----------------------------

Components provide intuitive access to their parent and/or child components:

.. code-block:: python

    from pyprland import Hyprland

    instance = Hyprland()
    window = instance.get_windows()[0]

    print(window.workspace)
    # Output: "<Workspace(id=1, name='1')>"
    print(window.workspace.window_count)
    # Output: 1

For a given :class:`~pyprland.components.windows.Window`, we can access the :class:`~pyprland.components.workspaces.Workspace`
it is on through its :attr:`~pyprland.components.windows.Window.workspace` property.
For a workspace, we can access all of its windows through its :attr:`~pyprland.components.workspaces.Workspace.windows` property,
or the :attr:`~pyprland.components.workspaces.Workspace.monitor` it is on, and so forth.
This is similar to object relational mappers (ORMs) you may be familiar with, such as the Django ORM.

.. note:: Accessing related components involves an underlying socket read & write operation.
    Because Hyprland manages socket operations synchronously, performing many relational
    lookups in quick succession may impact its performance, leading to lags or, in the worst case, freezing.

.. _guide-events:

Reacting to events
------------------

Besides access to other components, the :class:`~pyprland.components.instances.Instance`
class provides the :meth:`~pyprland.components.instances.Instance.watch` method, which
monitors Hyprland for events and emits a specific :class:`~pyprland.utils.signals.Signal`
whenever an event occurs. By connecting our own callback functions to these signals,
we can execute python code dynamically, in response to changes in Hyprland's state:

.. code-block:: python

    from pyprland import Hyprland
    from pyprland.utils.shell import run_or_fail

    instance = Hyprland()

    # Define a callback function
    def workspace_changed(sender, **kwargs):
       run_or_fail(["notify-send", "Workspace Changed"])

    # Connect the callback function to the signal
    instance.signal_active_workspace_changed.connect(workspace_changed)

    # Start watching for hyprland events
    instance.watch()

In this example, we defined our own callback function called ``workspace_changed``.
The function executes a shell command, ``notify-send``, with ``"Workspace Changed"`` as an argument.
We used a helper function called :func:`~pyprland.utils.shell.run_or_fail` here to run the shell command,
but the body of our callback function can be any valid python code.

Then, we *connected* our callback function to the Instance's :attr:`~pyprland.components.instances.Instance.signal_active_workspace_changed`
signal and, finally, we called the Instance's :meth:`~pyprland.components.instances.Instance.watch` method.

The :meth:`~pyprland.components.instances.Instance.watch` method runs indefinitely, but executes our callback
function whenever the underlying signal is emitted.
In this case, we get a desktop notification whenever we switch to another workspace.

.. attention:: The signal callback function signature **must** be ``(sender, **kwargs)``.

Dispatched signals include some data about the event which triggered them.
The data can be retrieved from the `**kwargs` in our callback function:

.. code-block:: python

    from pyprland import Hyprland
    from pyprland.utils.shell import run_or_fail

    instance = Hyprland()

    def workspace_changed(sender, **kwargs):
       # Retrieve the newly active workspace from the signal's data
       active_workspace = kwargs.get('active_workspace')
       run_or_fail(["notify-send", "Workspace Changed", f"Workspace is now {active_workspace.id}"])

    instance.signal_active_workspace_changed.connect(workspace_changed)
    instance.watch()

Building on the previous example, our desktop notification now also includes the ID of the workspace we
switched to.

The following table shows a list of available signals, and the data they send to the callback function:

.. list-table:: Instance Signals
   :widths: 30 40 30
   :header-rows: 1

   * - Event
     - Signal
     - Signal Data
   * - A workspace was created
     - :attr:`~pyprland.components.instances.Instance.signal_workspace_created`
     - ``new_workspace``: the newly created :class:`~pyprland.components.workspaces.Workspace`
   * - A workspace was destroyed
     - :attr:`~pyprland.components.instances.Instance.signal_workspace_destroyed`
     - ``destroyed_workspace_id``: ID of the destroyed workspace (integer)
   * - The active workspace changed
     - :attr:`~pyprland.components.instances.Instance.signal_active_workspace_changed`
     - ``active_workspace``: the now active :class:`~pyprland.components.workspaces.Workspace`
   * - A window was created
     - :attr:`~pyprland.components.instances.Instance.signal_window_created`
     - ``new_window``: the newly created :class:`~pyprland.components.windows.Window`
   * - A window was destroyed
     - :attr:`~pyprland.components.instances.Instance.signal_window_destroyed`
     - ``destroyed_window_address``: hexadecimal address of the destroyed window
   * - The active window changed
     - :attr:`~pyprland.components.instances.Instance.signal_active_window_changed`
     - ``active_window``: the now active :class:`~pyprland.components.windows.Window`


.. note:: The :meth:`~pyprland.components.instances.Instance.watch` method is a blocking operation that runs 
   indefinitely.

Using signals in conjunction with :meth:`~pyprland.components.instances.Instance.watch` is much more efficient
than polling, because Pyprland watches `Hyprland's event socket <https://wiki.hyprland.org/IPC/#tmphyprhissocket2sock>`_
directly, saving on CPU time and I/O operations.

Component state
---------------

When we instantiate a component object (for example a :class:`~pyprland.components.workspaces.Workspace`)
in Pyprland, its data attributes reflect its *current* state in Hyprland.
As time passes and things happen in Hyprland, the object's attributes may no longer reflect its actual
state in the compositor. There is no synchronization of state between a Pyprland component its real-world counterpart.

.. attention:: With the exception of the :class:`~pyprland.components.instances.Instance` object,
    **do not re-use component objects after their state may have changed**.

Instead, we should use instantiated component objects immediately, and discard them once we have the information we need:

.. code-block:: python

    from pyprland import Hyprland

    instance = Hyprland()

    workspace_3 = instance.get_workspace_by_id(3)
    if workspace_3 and workspace_3.window_count > 2:
        ... # do some stuff

    ... # time passes, things happen

    # Don't do this:
    for window in workspace_3:
        ...
        # The windows on workspace_3, and the workspace itself may have changed

    # Instead, reinstantiate the workspace using the instance object:
    workspace_3 = instance.get_workspace_by_id(3)
    if workspace_3:
        for window in workspace_3.windows:
            ... # do some other stuff

The :class:`~pyprland.components.instances.Instance` object's data attributes won't change unless
you restart Hyprland, so it is generally safe to re-use. For other components, if you suspect that
the component's state has changed since it has been instantiated, it is better to overwrite it
with a fresh copy.

"""
