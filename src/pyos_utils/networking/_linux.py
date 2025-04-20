from pyos_utils.networking._info import NetworkInfo
from pyos_utils.networking._interface import NetworkInterface


class LinuxNetworkInterface(NetworkInterface):
    """Linux implementation of the NetworkInterface."""

    def get_info(self) -> list[NetworkInfo]:
        """Get the display information."""
        return []
