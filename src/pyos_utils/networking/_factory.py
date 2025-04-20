import sys

from ._interface import NetworkInterface


class NetworkInterfaceFactory:
    @staticmethod
    def create_interface(platform: str = sys.platform) -> NetworkInterface:
        """Create a display interface based on the specified platform."""
        if platform == "darwin":
            from ._mac import MacNetworkInterface

            return MacNetworkInterface()
        if platform == "win32":
            from ._win import WindowsNetworkInterface

            return WindowsNetworkInterface()
        if platform == "linux":
            from ._linux import LinuxNetworkInterface

            return LinuxNetworkInterface()

        msg = f"Platform {platform} is not supported"
        raise NotImplementedError(msg)
