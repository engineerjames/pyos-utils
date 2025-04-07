import subprocess

from pyos_utils.display._display_info import DisplayInfo
from pyos_utils.display._display_interface import DisplayInterface
from pyos_utils.display._display_utilities import get_bit_depth_from_colors


class WindowsDisplayInterface(DisplayInterface):
    NUMBER_OF_COLUMNS = 5

    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        output = subprocess.run(
            [  # noqa: S607
                "wmic",
                "path",
                "Win32_VideoController",
                "get",
                "CurrentRefreshRate,DeviceID,VideoModeDescription,VideoProcessor",
                "/format:csv",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse the output and return a list of DisplayInfo objects

        # Extract the display information from the output
        display_info: list[DisplayInfo] = []
        for row in [line for line in output.stdout.split("\n") if line]:
            # Skip the header row
            if "DeviceID" in row:
                continue

            # Split the row into columns, and skip the first column (Node).
            # Unsure why Powershell adds this, but it does.
            parts = row.split(",")[1:]

            fps = int(parts[0])
            name = parts[3]
            width = int(parts[2].split("x")[0])
            height = int(parts[2].split("x")[1])
            depth = int(parts[2].split("x")[2].split(" ")[1])

            depth = get_bit_depth_from_colors(depth)

            display_info.append(
                DisplayInfo(
                    name=name,
                    width=width,
                    height=height,
                    depth=depth,
                    fps=fps,
                ),
            )
        return display_info


# wmic path Win32_VideoController get VideoModeDescription,VideoProcessor,MaxRefreshRate,MinRefreshRate,DeviceID
# DeviceID          MaxRefreshRate  MinRefreshRate  Name                              VideoModeDescription
# VideoController1  143             29              NVIDIA GeForce RTX 4090           3840 x 2160 x 4294967296 colors
# VideoController2  32              32              Microsoft Remote Display Adapter  3456 x 2158 x 4294967296 colors
