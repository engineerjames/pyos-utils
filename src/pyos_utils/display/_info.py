from dataclasses import dataclass


@dataclass
class DisplayInfo:
    name: str | None = None
    """ The name of the display. This is usually the name of the graphics card. """

    width: int | None = None
    """ The width of the display in pixels. """

    height: int | None = None
    """ The height of the display in pixels. """

    depth: int | None = None
    """ The color depth of the display in bits. """

    fps: int | None = None
    """ The current refresh rate of the display in frames per second. """

    def __str__(self) -> str:
        return f"Name: {self.name}, Width: {self.width}, Height: {self.height}, Depth: {self.depth}, FPS: {self.fps}"
