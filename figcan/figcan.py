"""Fig Can - Simple Python Configuration Management
"""
from collections.abc import Mapping as BaseMapping
from copy import deepcopy
from typing import Any, Iterator, Union


class Configuration(BaseMapping):
    """Configuration container
    """
    def __init__(self, base_config: dict):
        self._data = deepcopy(base_config)

    def apply(self, config: dict) -> None:
        """Apply additional configuration from a dictionary

        This will look for dictionary items that exist in the base_config any apply their values on the current
        configuration object
        """
        pass

    def apply_object(self, config: Any) -> None:
        """Apply additional configuration from any Python object

        This will look for object attributes that exist in the base_config and apply their values  on the current
        configuration object
        """
        pass

    def apply_flat(self, config: dict, namespace_separator: str = '_', prefix: Union[str, None] = None):
        """Apply additional configuration from a flattened dictionary

        This will look for dictionary items that match flattened keys from base_config and apply their values on the
        current configuration object.

        This can be useful for applying configuration from environment variables and flat configuration file formats
        such as INI files.
        """
        pass

    def __getitem__(self, k: str) -> Any:
        return self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)
