from AppKit import NSScreen

from pyos_utils.display._display_interface import DisplayInterface


class MacDisplayInterface(DisplayInterface):
    def get_info(self) -> str:
        """Get the display information."""
        rect = NSScreen.mainScreen().frame()
        width = rect.size.width
        height = rect.size.height
        return f"Width: {width}, Height: {height}"
