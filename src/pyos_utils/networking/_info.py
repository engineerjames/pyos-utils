from dataclasses import dataclass


@dataclass
class NetworkInfo:
    name: str | None = None
    """ The name of the display. This is usually the name of the graphics card. """
