import shutil
import subprocess
from pathlib import Path

from ._exceptions import BackendNotFoundError
from ._sound_interface import SoundInterface


class LinuxSoundInterface(SoundInterface):
    def __init__(self) -> None:
        """Initialize the Linux sound interface using pactl."""
        self._pactl_path = Path("/usr/bin/pactl").resolve()
        self._beep_path = Path("/usr/bin/beep").resolve()

        if not self._pactl_path.exists():
            pactl_str = shutil.which("pactl")
            if pactl_str is None:
                raise BackendNotFoundError("pactl not found")
            self._pactl_path = Path(pactl_str)

        if not self._beep_path.exists():
            beep_str = shutil.which("beep")
            if beep_str is None:
                self._beep_path = None  # Fall back to print('\a') if beep not available
            else:
                self._beep_path = Path(beep_str)

    def play_beep(self) -> None:
        """Play a beep sound using system beep."""
        if self._beep_path:
            subprocess.run(
                [str(self._beep_path), "-f", "1000", "-l", "250"],
                check=False,
            )
        else:
            print("\a", flush=True)  # Fallback to terminal bell

    def set_volume(self, volume: float) -> None:
        """Set the system volume (0.0 to 1.0)."""
        volume = max(0.0, min(1.0, volume))
        volume_percent = int(volume * 100)
        subprocess.run(
            [str(self._pactl_path), "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"],
            check=False,
        )

    def get_volume(self) -> float:
        """Get the system volume (returns 0.0 to 1.0)."""
        result = subprocess.run(
            [str(self._pactl_path), "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True,
            text=True,
            check=False,
        )
        # Parse the volume percentage from output like: "Volume: front-left: 65536 / 100% / -0.00 dB"
        for line in result.stdout.split("\n"):
            if "Volume:" in line and "%" in line:
                percent = int(line.split("%")[0].split()[-1])
                return percent / 100.0
        return 0.0

    def mute(self) -> None:
        """Mute the system audio."""
        subprocess.run(
            [str(self._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "1"],
            check=False,
        )

    def unmute(self) -> None:
        """Unmute the system audio."""
        subprocess.run(
            [str(self._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "0"],
            check=False,
        )

    def get_mute(self) -> bool:
        """Get the system mute state."""
        result = subprocess.run(
            [str(self._pactl_path), "get-sink-mute", "@DEFAULT_SINK@"],
            capture_output=True,
            text=True,
            check=False,
        )
        return "yes" in result.stdout.lower()
