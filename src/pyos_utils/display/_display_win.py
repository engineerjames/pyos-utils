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

        return [DisplayInfo(0, 0, 0)]
