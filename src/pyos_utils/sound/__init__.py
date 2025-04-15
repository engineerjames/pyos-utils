from collections.abc import Callable

from ._factory import SoundInterfaceFactory
from ._sound_interface import SoundInterface

get_sound: Callable[..., SoundInterface] = SoundInterfaceFactory.create_interface

__all__ = [
    "SoundInterface",
    "get_sound",
]
