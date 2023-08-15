.. _api-data:

Data Models
===========

Hyprpy retrieves data about Hyprland components by talking to Hyprland's :class:`~hyprpy.utils.sockets.CommandSocket`.
The data retrieved from the socket arrives as JSON.
This JSON data needs to be parsed, validated, and converted into python objects with proper
attribute names.

Hyprpy leverages `Pydantic <https://docs.pydantic.dev/latest/>`_ under the hood
to parse socket data into python objects.
This enables automatic model validation and serialization/deserialization of data,
based purely on class structure and type annotations.

.. _api-data-model-classes:

Data model classes
------------------

.. automodule:: hyprpy.data.models
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: model_config, model_fields

Data model background
---------------------

.. automodule:: hyprpy.data
   :members:
   :undoc-members:
   :show-inheritance:

Component Data validators
-------------------------

.. automodule:: hyprpy.data.validators
   :members:
   :undoc-members:
   :show-inheritance:
