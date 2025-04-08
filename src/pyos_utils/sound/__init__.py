import sys

from ._exceptions import BackendNotFoundError, OperationFailedError
from ._factory import SoundInterfaceFactory

# Create singleton instance using factory
_interface = SoundInterfaceFactory.create_interface(sys.platform)

# Export the interface methods:
play_beep = _interface.play_beep
play_sound = _interface.play_sound
set_volume = _interface.set_volume
get_volume = _interface.get_volume
mute = _interface.mute
unmute = _interface.unmute
get_mute = _interface.get_mute

__all__ = [
    "BackendNotFoundError",
    "OperationFailedError",
    "get_mute",
    "get_volume",
    "mute",
    "play_beep",
    "play_sound",
    "set_volume",
    "unmute",
]
