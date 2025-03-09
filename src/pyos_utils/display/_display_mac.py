from AppKit import NSScreen

from pyos_utils.display._display_info import DisplayInfo
from pyos_utils.display._display_interface import DisplayInterface


class MacDisplayInterface(DisplayInterface):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        displays = []
        for s in NSScreen.screens():
            rect = s.frame()
            width = rect.size.width
            height = rect.size.height
            desc = s.deviceDescription()
            depth = desc["NSDeviceBitsPerSample"]
            fps = s.maximumFramesPerSecond()
            display = DisplayInfo(width, height, depth, fps)
            displays.append(display)

        return displays
