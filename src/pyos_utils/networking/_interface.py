from typing import Protocol

from pyos_utils.networking._info import NetworkInfo


class NetworkInterface(Protocol):
    def get_info(self) -> list[NetworkInfo]:
        """Get the display information."""
        ...
