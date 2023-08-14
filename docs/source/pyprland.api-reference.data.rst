.. _api-data:

Data API
========

This is the component data reference, where you will all the available data attributes for the different
components.

Pyprland retrieves data about Hyprland components by talking to Hyprland's :class:`~pyprland.utils.sockets.CommandSocket`.
The data retrieved from the socket arrives as JSON.
This JSON data needs to be parsed, validated, and converted into python objects with proper
attribute names.

Pyprland leverages `Pydantic <https://docs.pydantic.dev/latest/>`_ under the hood
to parse socket data into python objects.
This enables automatic model validation and serialization/deserialization of data,
based purely on class structure and type annotations.

.. _api-data-model-classes:

Data model classes
------------------

.. automodule:: pyprland.data.models
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: model_config, model_fields

Data model background
---------------------

.. automodule:: pyprland.data
   :members:
   :undoc-members:
   :show-inheritance:

Component Data validators
-------------------------

.. automodule:: pyprland.data.validators
   :members:
   :undoc-members:
   :show-inheritance:
