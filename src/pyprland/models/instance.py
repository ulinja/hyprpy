"""Pydantic model representing a Hyprland instance."""

from pydantic import BaseModel

from pyprland.validators.common import NonEmptyString
from pyprland.utils import shell


class Instance(BaseModel):
    signature: NonEmptyString


    def __repr__(self):
        return f"<Instance(signature={self.signature!r})>"


    @classmethod
    def get(cls):
        """Retrieves the current Hyprland instance."""

        instance_signature = shell.get_env_var_or_fail('HYPRLAND_INSTANCE_SIGNATURE')
        return cls.model_validate({'signature': instance_signature})
