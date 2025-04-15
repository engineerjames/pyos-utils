# type: ignore  # noqa: PGH003
from AppKit import NSScreen

from pyos_utils.display._info import DisplayInfo
from pyos_utils.display._interface import DisplayInterface


class MacDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        displays: list[DisplayInfo] = []
        for s in NSScreen.screens():
            name = s.localizedName()
            rect = s.frame()
            width = rect.size.width
            height = rect.size.height
            desc = s.deviceDescription()
            depth = desc["NSDeviceBitsPerSample"]
            fps = s.maximumFramesPerSecond()

            display = DisplayInfo(
                name=name,
                width=width,
                height=height,
                depth=depth,
                fps=fps,
            )
            displays.append(display)

        return displays
