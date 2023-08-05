""" This module implement Model model  """
from superwise.models.base import BaseModel


class Model(BaseModel):
    """ Model model class """

    def __init__(
        self,
        id=None,
        external_id=None,
        name=None,
        description=None,
        monitor_delay=None,
        time_units=None,
        is_archive=None,
        **kwargs
    ):
        """
        ### Description:

        Constructor for Model class

        ### Args:

        `id`: id of model

        `external_id`: external/secondary identifier, use it to map between your id and superwise

        `name`: name of model

        `description`: description for the model

        `monitor_delay`:

        `time_units`:

        `is_archive`:
        """
        self.external_id = external_id
        self.name = name
        self.id = id or None
        self.description = description
        self.monitor_delay = monitor_delay
        self.time_units = time_units
        self.is_archive = is_archive
