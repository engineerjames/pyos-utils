import subprocess

from pyos_utils.display._display_info import DisplayInfo
from pyos_utils.display._display_interface import DisplayInterface


class WindowsDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        output = subprocess.run(
            [  # noqa: S607
                "wmic",
                "path",
                "Win32_VideoController",
                "get",
                "VideoModeDescription,VideoProcessor,MaxRefreshRate,MinRefreshRate,DeviceID",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse the output and return a list of DisplayInfo objects

        # Extract the display information from the output
        display_info: list[DisplayInfo] = []
        for line in output.stdout.split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 5:
                    display_info.append(
                        DisplayInfo(
                            width=int(parts[0]),
                            height=int(parts[1]),
                            depth=int(parts[2]),
                            fps=int(parts[3]),
                        )
                    )
        return display_info


# wmic path Win32_VideoController get VideoModeDescription,VideoProcessor,MaxRefreshRate,MinRefreshRate,DeviceID
# DeviceID          MaxRefreshRate  MinRefreshRate  Name                              VideoModeDescription
# VideoController1  143             29              NVIDIA GeForce RTX 4090           3840 x 2160 x 4294967296 colors
# VideoController2  32              32              Microsoft Remote Display Adapter  3456 x 2158 x 4294967296 colors
