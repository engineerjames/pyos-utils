import subprocess

from pyos_utils.display._display_info import DisplayInfo
from pyos_utils.display._display_interface import DisplayInterface


class WindowsDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        _ = subprocess.run(
            ["wmic", "path", "Win32_VideoController", "get", "Name"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )

        return [DisplayInfo(0, 0, 0, 0)]


# PS C:\Users\jarmes> wmic path Win32_VideoController
# get Name,VideoModeDescription,VideoProcessor,MaxRefreshRate,MinRefreshRate,DeviceID
# DeviceID          MaxRefreshRate  MinRefreshRate  Name                              VideoModeDescription
# VideoController1  143             29              NVIDIA GeForce RTX 4090           3840 x 2160 x 4294967296 colors
# VideoController2  32              32              Microsoft Remote Display Adapter  3456 x 2158 x 4294967296 colors
