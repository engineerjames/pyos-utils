from typing import Protocol

from pyos_utils.display._info import DisplayInfo


class DisplayInterface(Protocol):
    def get_info(self) -> list[DisplayInfo]:
        """Get the display information."""
        ...
