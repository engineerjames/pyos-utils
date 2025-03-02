from pathlib import Path

from . import _sound_utilities
from ._exceptions import BackendNotFoundError, OperationFailedError
from ._sound_interface import SoundInterface
from .external import comtypes, pycaw, winsound


class WindowsSoundInterface(SoundInterface):
    def __init__(self) -> None:
        """Initialize the Windows sound interface using pycaw."""
        try:
            devices = pycaw.AudioUtilities.GetSpeakers()
            interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
            self._volume = interface.QueryInterface(pycaw.IAudioEndpointVolume)
        except Exception as e:
            error_msg = f"Failed to initialize Windows audio: {e}"
            raise BackendNotFoundError(error_msg) from e

    def play_beep(self) -> None:
        """Play a beep sound using Windows API."""
        try:
            winsound.Beep(1000, 250)  # 1000Hz for 250ms
        except Exception as e:
            error_msg = f"Failed to play beep sound: {e}"
            raise OperationFailedError(error_msg) from e

    def set_volume(self, volume: float) -> None:
        """Set the system volume (0.0 to 1.0)."""
        # pycaw uses a range from -65.25 to 0.0 in dB
        # Convert linear 0-1 to proper dB range
        try:
            volume = _sound_utilities.normalize_sound(volume)
            self._volume.SetMasterVolumeLevelScalar(volume, None)
        except Exception as e:
            error_msg = f"Failed to set Windows volume: {e}"
            raise OperationFailedError(error_msg) from e

    def get_volume(self) -> float:
        """Get the system volume (returns 0.0 to 1.0)."""
        try:
            return self._volume.GetMasterVolumeLevelScalar()
        except Exception as e:
            error_msg = f"Failed to get Windows volume: {e}"
            raise OperationFailedError(error_msg) from e

    def mute(self) -> None:
        """Mute the system audio."""
        try:
            self._volume.SetMute(1, None)
        except Exception as e:
            error_msg = f"Failed to mute Windows audio: {e}"
            raise OperationFailedError(error_msg) from e

    def unmute(self) -> None:
        """Unmute the system audio."""
        try:
            self._volume.SetMute(0, None)
        except Exception as e:
            error_msg = f"Failed to unmute Windows audio: {e}"
            raise OperationFailedError(error_msg) from e

    def get_mute(self) -> bool:
        """Get the system mute state."""
        try:
            return bool(self._volume.GetMute())
        except Exception as e:
            error_msg = f"Failed to get Windows mute state: {e}"
            raise OperationFailedError(error_msg) from e

    def play_sound(self, path: Path) -> None:
        """Play a sound file."""
        if not path.exists():
            error_msg = f"Sound file not found: {path}"
            raise FileNotFoundError(error_msg)

        try:
            winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            error_msg = f"Failed to play sound file: {e}"
            raise OperationFailedError(error_msg) from e
