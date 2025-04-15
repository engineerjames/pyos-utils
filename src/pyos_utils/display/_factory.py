import sys

from ._interface import DisplayInterface


class DisplayInterfaceFactory:
    @staticmethod
    def create_interface(platform: str = sys.platform) -> DisplayInterface:
        """Create a display interface based on the specified platform."""
        if platform == "darwin":
            from ._mac import MacDisplayInterface

            return MacDisplayInterface()
        if platform == "win32":
            from ._win import WindowsDisplayInterface

            return WindowsDisplayInterface()
        if platform == "linux":
            from ._linux import LinuxDisplayInterface

            return LinuxDisplayInterface()

        msg = f"Platform {platform} is not supported"
        raise NotImplementedError(msg)
