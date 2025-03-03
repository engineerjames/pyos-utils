import subprocess

from pyos_utils.display._display_interface import DisplayInterface


class WindowsDisplayInterface(DisplayInterface):
    def get_info(self) -> str:
        """Get the display information."""
        completed_process = subprocess.run(
            ["wmic", "path", "Win32_VideoController", "get", "Name"],
            capture_output=True,
            text=True,
            check=True,
        )

        return completed_process.stdout
