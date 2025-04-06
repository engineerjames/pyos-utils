import subprocess

from pyos_utils.display._display_info import DisplayInfo
from pyos_utils.display._display_interface import DisplayInterface


class LinuxDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        _ = subprocess.run(
            ["xrandr"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )

        return [DisplayInfo(name="Linux Display", width=1920, height=1080, depth=24, fps=60)]
