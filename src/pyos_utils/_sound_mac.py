import shutil
import subprocess
from pathlib import Path

from ._exceptions import BackendNotFoundError
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
        subprocess.run([str(self._osascript_path), "-e", "beep"], check=False)

    def set_volume(self, volume: float) -> None:
        """Set the volume of the sound (0.0 to 1.0)."""
        # Convert 0-1 range to 0-100
        volume_int = max(0, min(100, int(volume * 100)))  # Clamp value between 0 and 100
        subprocess.run([str(self._osascript_path), "-e", f"set volume output volume {volume_int}"], check=False)

    def get_volume(self) -> float:
        """Get the volume of the sound (returns 0.0 to 1.0)."""
        result = subprocess.run(
            [str(self._osascript_path), "-e", "output volume of (get volume settings)"],
            capture_output=True,
            text=True,
            check=False,
        )
        # Convert from 0-100 range to 0-1
        return float(result.stdout.strip()) / 100

    def mute(self) -> None:
        """Set the mute state of the sound."""
        subprocess.run([str(self._osascript_path), "-e", "set volume output muted true"], check=False)

    def unmute(self) -> None:
        """Unset the mute state of the sound."""
        subprocess.run([str(self._osascript_path), "-e", "set volume output muted false"], check=False)

    def get_mute(self) -> bool:
        """Get the mute state of the sound."""
        result = subprocess.run(
            [str(self._osascript_path), "-e", "output muted of (get volume settings)"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip().lower() == "true"
