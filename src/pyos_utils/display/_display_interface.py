from typing import Protocol


class DisplayInterface(Protocol):
    def get_info(self) -> str:
        """Get the display information."""
        ...
