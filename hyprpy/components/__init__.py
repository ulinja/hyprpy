"""Hyprpy components represent all the moving parts of a running Hyprland instance.
They allow us to retrieve information about the compositor in real time.

Hyprpy handles four component types:

* :mod:`~hyprpy.components.instances`
* :mod:`~hyprpy.components.monitors`
* :mod:`~hyprpy.components.workspaces`
* :mod:`~hyprpy.components.windows`

Let's get started, and go through some examples.

.. _guide-instance:

The Instance
------------

To retrieve a component, we first have to get the current Hyprland instance:

.. code-block:: python

    from hyprpy.components.instances import Instance

    # Get the current instance
    instance = Instance()

We can also use the shorthand alias ``Hyprland``, which looks slightly nicer:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland()

By default, Hyprpy reads the ``$HYPRLAND_INSTANCE_SIGNATURE`` environment variable to find the `Hyprland Instance Signature <https://wiki.hyprland.org/IPC/#hyprland-instance-signature-his>`_.
If the environment variable is unset because we are in an SSH session, or if we want to access a second
Hyprland instance running on our system, we can specify its value manually:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland("882f7ad7d2bbfc7440d0ccaef93b1cdd78e8e3ff_1742068954_542829775")

.. _guide-component-data:

Reading component data
----------------------

Now that we have our instance, we can query it for components.
Components have *data attributes*, which allow us to access information about them.
Let's grab the currently active window and print some information about it:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland()

    window = instance.get_active_window()
    print(window)
    # Output: "<Window(address='0x1981f40', wm_class='kitty', title='python ~/d/p/src')>"
    print(window.width)
    # Output: 1258
    print(window.wm_class)
    # Output: 'kitty'

Here, we queried the instance for the active window, and printed the window's ``width``
and ``wm_class`` data attributes, which tell us the current width and display class of the window.

Windows, workspaces and monitors have a wide range of useful data attributes.
For a complete list of data attributes for each type of component, refer to the
:ref:`Components API <api-components>`.

.. note:: Component data attributes are **read-only**.
    Writing new values into them have no effect on Hyprland's actual state and will lead to unexpected behavior.

Accessing related components
----------------------------

Components provide intuitive access to their parent and/or child components:

.. code-block:: python

    from hyprpy import Hyprland

    instance = Hyprland()
    workspace = instance.get_active_workspace()

    for window in workspace.windows:
        print(window.address)

    # Output: '0x2642190'
    #         '0x1df25a0'
    #         '0x263ae70'

    print(workspace.monitor.name)
    # Output: 'HDMI-1'


For a given :class:`~hyprpy.components.windows.Window`, we can access the :class:`~hyprpy.components.workspaces.Workspace`
it is on through its :attr:`~hyprpy.components.windows.Window.workspace` property.
For a workspace, we can access all of its windows through its :attr:`~hyprpy.components.workspaces.Workspace.windows` property,
or the :attr:`~hyprpy.components.workspaces.Workspace.monitor` it is on, and so forth.
This is similar to object relational mappers (ORMs) you may be familiar with, such as the Django ORM.

.. note:: Accessing related components involves an IPC socket read & write operation.
    Because Hyprland manages socket operations synchronously, performing an excessive number of relational
    lookups in quick succession may impact performance, leading to lags or, in the worst case, freezing.

.. _guide-events:

Reacting to events
------------------

Besides access to other components, the :class:`~hyprpy.components.instances.Instance`
class provides the :meth:`~hyprpy.components.instances.Instance.watch` method, which
monitors Hyprland for events and emits a specific :class:`~hyprpy.utils.signals.Signal`
whenever an event occurs. By connecting our own callback functions to these signals,
we can execute python code dynamically, in response to changes in Hyprland's state:

.. code-block:: python

    from hyprpy import Hyprland
    from hyprpy.utils.shell import run_or_fail

    instance = Hyprland()

    # Define a callback function
    def on_workspace_changed(sender, **kwargs):
       run_or_fail(["notify-send", "Workspace Changed"])

    # Connect the callback function to the signal
    instance.signals.workspace.connect(on_workspace_changed)

    # Start watching for hyprland events
    instance.watch()

In this example, we defined our own callback function called ``on_workspace_changed``.
The function executes a shell command, ``notify-send``, with ``"Workspace Changed"`` as an argument.
We used a helper function called :func:`~hyprpy.utils.shell.run_or_fail` here to run the shell command,
but the body of our callback function can be any valid python code!

Then, we *connected* our callback function to the Instance's :attr:`~hyprpy.components.instancesignals.InstanceSignalCollection.workspace`
signal and, finally, we called the Instance's :meth:`~hyprpy.components.instances.Instance.watch` method.

The :meth:`~hyprpy.components.instances.Instance.watch` method runs indefinitely, but executes our callback
function whenever the underlying signal is emitted.
In this case, we get a desktop notification whenever we switch to a different workspace.

.. attention:: The callback's function signature **must** be ``(sender, **kwargs)``.

Dispatched signals include some data about the event which triggered them.
The data can be retrieved from the `**kwargs` in our callback function:

.. code-block:: python

    from hyprpy import Hyprland
    from hyprpy.utils.shell import run_or_fail

    instance = Hyprland()

    def on_workspace_changed(sender, **kwargs):
       # Retrieve the newly active workspace from the signal's data
       workspace_name = kwargs["workspace_name"]
       run_or_fail(["notify-send", "Workspace Changed", f"Workspace is now {workspace_name}"])

    instance.signals.workspace.connect(on_workspace_changed)
    instance.watch()

Building on the previous example, our desktop notification now also includes the name of the workspace we
switched to.
We pulled this information from the ``**kwargs`` dictionary in our callback function.
Different signals send different data as kwargs, the details of which are specified in the
:mod:`~hyprpy.components.instancesignals` module.

We can disconnect signals as well:

.. code-block:: python

    instance.signals.workspace.disconnect(on_workspace_changed)

Aside from saving resources, disconnecting signals is useful if we only want our
callback to get triggered a few times.

.. note:: The :meth:`~hyprpy.components.instances.Instance.watch` method is a blocking operation that runs 
   indefinitely.

Using signals in conjunction with :meth:`~hyprpy.components.instances.Instance.watch` is much more efficient
than polling, because Hyprpy watches `Hyprland's event socket <https://wiki.hyprland.org/IPC/#tmphyprhissocket2sock>`_
directly, saving on CPU time and I/O operations.

Component state
---------------

When we instantiate a component object (for example a :class:`~hyprpy.components.workspaces.Workspace`)
in Hyprpy, its data attributes reflect its *current* state in Hyprland.
As time passes and things happen in Hyprland, the object's attributes may no longer reflect its actual
state in the compositor. There is no synchronization of state between a Hyprpy component its real-world counterpart.

.. attention:: With the exception of the :class:`~hyprpy.components.instances.Instance` object,
    **do not re-use component objects after their state may have changed**.

Instead, we should use instantiated component objects immediately, and discard them once we have the information we need:

.. code-block:: python

    from hyprpy import Hyprland

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

The :class:`~hyprpy.components.instances.Instance` object's data attributes won't change unless
you restart Hyprland, so it is generally safe to re-use. For other components, if you suspect that
the component's state has changed since it has been instantiated, it is better to overwrite it
with a fresh copy.

"""
