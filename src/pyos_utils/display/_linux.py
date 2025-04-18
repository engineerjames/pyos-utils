import re
import subprocess
from subprocess import CompletedProcess
from typing import Any

from pyos_utils.display._info import DisplayInfo
from pyos_utils.display._interface import DisplayInterface


class LinuxDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        result: CompletedProcess[str] = subprocess.run(
            ["xrandr", "--listactivemonitors"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )

        displays: list[DisplayInfo] = []

        # Skip the first line which contains "Monitors: N"
        for line in result.stdout.splitlines()[1:]:
            # Format: " 0: +*HDMI-1 1920/527x1080/296+0+0  HDMI-1"  # noqa: ERA001
            match: re.Match[str] | None = re.search(r"^\s*(\d+):\s+\+\*?(\S+)\s+(\d+)/\d+x(\d+)/\d+", line)
            if match:
                screen_index: int = int(match.group(1))
                name: str | Any = match.group(2)
                width: int = int(match.group(3))
                height: int = int(match.group(4))

                # Get refresh rate with a separate command
                rate_result: CompletedProcess[str] = subprocess.run(
                    ["xrandr", "--properties", "--screen", f"{screen_index}"],  # noqa: S607
                    capture_output=True,
                    text=True,
                    check=True,
                )
                fps: float | None = None
                for rate_line in rate_result.stdout.splitlines():
                    # * Indicates the current setting
                    # + Indicates the preferred setting
                    if "*" in rate_line:
                        rate_match: re.Match[str] | None = re.search(r"([\d.]+)\*", rate_line)
                        if rate_match:
                            fps = float(rate_match.group(1))
                            break

                displays.append(
                    DisplayInfo(
                        name=name,
                        width=width,
                        height=height,
                        depth=None,  # Most X11 displays use 24-bit color, TODO: Actually pull this value
                        fps=round(number=fps) if fps else None,
                    ),
                )

        return displays
