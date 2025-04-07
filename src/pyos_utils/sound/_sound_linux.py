import shutil
import subprocess
from enum import Enum
from pathlib import Path

from ._exceptions import BackendNotFoundError
from ._sound_interface import SoundInterface
from .linux_backends.pulse import PulseAudioInterface
from .linux_backends.wireplumber import WirePlumberInterface


class Backend(str, Enum):
    """Enum for Linux sound backends."""

    WIREPLUMBER = "wireplumber"
    PULSE = "pulse"
    UNKNOWN = "unknown"

    @staticmethod
    def _detect_backend() -> tuple["Backend", Path | None]:
        """Detect the sound backend on Linux."""
        pactl_path = shutil.which("pactl")
        if pactl_path:
            # Check if PulseAudio is running
            try:
                subprocess.run([pactl_path, "info"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                pass
            else:
                return Backend.PULSE, Path(pactl_path)

        wpctl_path = shutil.which("wpctl")
        if wpctl_path:
            # Check if WirePlumber is running
            try:
                subprocess.run([wpctl_path, "status"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                pass
            else:
                return Backend.WIREPLUMBER, Path(wpctl_path)

        return Backend.UNKNOWN, None

    @staticmethod
    def get_interface() -> SoundInterface:
        """Get the sound interface for the backend."""
        backend, backend_exe = Backend._detect_backend()

        if backend == Backend.PULSE and backend_exe is not None:
            return PulseAudioInterface(backend_exe)
        if backend == Backend.WIREPLUMBER and backend_exe is not None:
            return WirePlumberInterface(backend_exe)

        msg = f"Unsupported backend: {backend}"
        raise BackendNotFoundError(msg)


class LinuxSoundInterface(SoundInterface):
    def __init__(self) -> None:
        """Initialize the Linux sound interface."""
        self.backend_interface = Backend.get_interface()

    def play_beep(self) -> None:
        """Play a beep sound using system beep."""
        self.backend_interface.play_beep()

    def set_volume(self, volume: float) -> None:
        """Set the system volume (0.0 to 1.0)."""
        self.backend_interface.set_volume(volume)

    def get_volume(self) -> float:
        """Get the system volume (returns 0.0 to 1.0)."""
        return self.backend_interface.get_volume()

    def mute(self) -> None:
        """Mute the system audio."""
        self.backend_interface.mute()

    def unmute(self) -> None:
        """Unmute the system audio."""
        self.backend_interface.unmute()

    def get_mute(self) -> bool:
        """Get the system mute state."""
        return self.backend_interface.get_mute()

    def play_sound(self, path: Path) -> None:
        """Play a sound file."""
        self.backend_interface.play_sound(path)
