Hyprpy
------

`Hyprpy <https://github.com/ulinja/hyprpy>`_ is a library which provides python bindings
for the `Hyprland <https://hyprland.org/>`_ window compositor.
With Hyprpy, you can retrieve information about windows, workspaces and monitors in realtime
and react to Hyprland events dynamically using pure Python.

Hyprpy communicates with Hyprland using unix sockets, making it *fast* and *efficient*.
It also provides a versatile and resource-friendly signalling interface. With it,
you can write python callbacks for Hyprland events.

.. attention:: Check out the :ref:`guide <guide>` for a demonstration of Hyprpy.

Getting started
---------------

To get started, install Hyprpy:

.. code-block:: bash

    pip install hyprpy

and follow along with the :ref:`guide <guide>`, or dive straight into the extensive :ref:`API reference <api>`
if you're feeling adventurous!

.. toctree::
   :maxdepth: 2

   hyprpy.components
   hyprpy.api-reference.components
   hyprpy.api-reference.utils
   hyprpy.api-reference.data


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
