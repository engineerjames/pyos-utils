import subprocess

from pyos_utils.display._display_interface import DisplayInterface


class LinuxDisplayInterface(DisplayInterface):
    def get_info(self) -> str:
        """Get the display information."""
        completed_process = subprocess.run(
            ["xrandr"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )

        return completed_process.stdout
