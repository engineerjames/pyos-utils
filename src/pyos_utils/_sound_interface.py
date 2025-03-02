from pathlib import Path
from typing import Protocol


class SoundInterface(Protocol):
    def play_beep(self) -> None:
        """Play a beep sound."""
        ...

    def set_volume(self, volume: float) -> None:
        """Set the volume of the sound."""
        ...

    def get_volume(self) -> float:
        """Get the volume of the sound."""
        ...

    def mute(self) -> None:
        """Set the mute state of the sound."""
        ...

    def unmute(self) -> None:
        """Unset the mute state of the sound."""
        ...

    def get_mute(self) -> bool:
        """Get the mute state of the sound."""
        ...

    def play_sound(self, path: Path) -> None:
        """Play a sound file."""
        ...
