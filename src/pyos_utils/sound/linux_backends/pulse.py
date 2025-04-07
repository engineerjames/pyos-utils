import shutil
import subprocess
from pathlib import Path

from pyos_utils.sound import _sound_utilities
from pyos_utils.sound._exceptions import OperationFailedError
from pyos_utils.sound._sound_interface import SoundInterface


class PulseAudioInterface(SoundInterface):
    def __init__(self, path_to_ctl: Path) -> None:
        """Initialize the Linux sound interface."""
        self._pactl_path = path_to_ctl

        self._beep_path = shutil.which("beep")

    def play_beep(self) -> None:
        """Play a beep sound using system beep."""
        completed_process = subprocess.run(
            [str(self._beep_path), "-f", "1000", "-l", "250"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to play beep sound: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def set_volume(self, volume: float) -> None:
        """Set the system volume (0.0 to 1.0)."""
        volume = _sound_utilities.normalize_sound(volume)
        volume_percent = int(volume * 100)
        completed_process = subprocess.run(
            [str(self._pactl_path), "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to set volume: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def get_volume(self) -> float:
        """Get the system volume (returns 0.0 to 1.0)."""
        completed_process = subprocess.run(
            [str(self._pactl_path), "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True,
            text=True,
            check=False,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to get volume: {completed_process.stderr}"
            raise OperationFailedError(error_message)

        # Parse the volume percentage from output like: "Volume: front-left: 65536 / 100% / -0.00 dB"
        for line in completed_process.stdout.split("\n"):
            if "Volume:" in line and "%" in line:
                percent = int(line.split("%")[0].split()[-1])
                return percent / 100.0

        raise OperationFailedError("Failed to parse volume output")  # noqa: EM101, TRY003

    def mute(self) -> None:
        """Mute the system audio."""
        completed_process = subprocess.run(
            [str(self._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "1"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to mute: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def unmute(self) -> None:
        """Unmute the system audio."""
        completed_process = subprocess.run(
            [str(self._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "0"],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to unmute: {completed_process.stderr}"
            raise OperationFailedError(error_message)

    def get_mute(self) -> bool:
        """Get the system mute state."""
        completed_process = subprocess.run(
            [str(self._pactl_path), "get-sink-mute", "@DEFAULT_SINK@"],
            capture_output=True,
            text=True,
            check=False,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to get mute state: {completed_process.stderr}"
            raise OperationFailedError(error_message)

        return "yes" in completed_process.stdout.lower()

    def play_sound(self, path: Path) -> None:
        """Play a sound file."""
        if not path.exists():
            error_message = f"Sound file not found: {path}"
            raise FileNotFoundError(error_message)

        completed_process = subprocess.run(
            [str(self._pactl_path), "play-file", str(path)],
            check=False,
            text=True,
        )

        if completed_process.returncode != 0:
            error_message = f"Failed to play sound: {completed_process.stderr}"
            raise OperationFailedError(error_message)
