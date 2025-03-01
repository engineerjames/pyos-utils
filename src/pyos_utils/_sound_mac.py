import shutil
import subprocess
from pathlib import Path

from . import _sound_utilities
from ._exceptions import BackendNotFoundError, OperationFailedError
from ._sound_interface import SoundInterface


class MacSoundInterface(SoundInterface):
    def __init__(self) -> None:
        super().__init__()

        self._osascript_path = Path("/usr/bin/osascript").resolve()

        if not self._osascript_path.exists():
            osascript_str = shutil.which("osascript")

            if osascript_str is None:
                error_msg = "osascript not found"
                raise BackendNotFoundError(error_msg)

            self._osascript_path = Path(osascript_str)

    def play_beep(self) -> None:
        """Play a beep sound."""
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", "beep"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to play beep sound: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def set_volume(self, volume: float) -> None:
        """Set the volume of the sound (0.0 to 1.0)."""
        volume = _sound_utilities.normalize_sound(volume)
        volume_int = int(volume * 100)  # Clamp value between 0 and 100
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", f"set volume output volume {volume_int}"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to set volume: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def get_volume(self) -> float:
        """Get the volume of the sound (returns 0.0 to 1.0)."""
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", "output volume of (get volume settings)"],
            capture_output=True,
            text=True,
            check=False,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to get volume: {completed_process.stderr}"
            raise OperationFailedError(error_message)

        # Convert from 0-100 range to 0-1
        return float(completed_process.stdout.strip()) / 100.0

    def mute(self) -> None:
        """Commands a muted state."""
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", "set volume output muted true"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to mute sound: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def unmute(self) -> None:
        """Unset the muted state."""
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", "set volume output muted false"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to unmute sound: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def get_mute(self) -> bool:
        """Get the mute state of the sound."""
        completed_process = subprocess.run(
            [str(self._osascript_path), "-e", "output muted of (get volume settings)"],
            capture_output=True,
            text=True,
            check=False,
        )
        return completed_process.stdout.strip().lower() == "true"
