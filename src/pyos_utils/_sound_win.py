import winsound

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from ._exceptions import BackendNotFoundError
from ._sound_interface import SoundInterface


class WindowsSoundInterface(SoundInterface):
    def __init__(self) -> None:
        """Initialize the Windows sound interface using pycaw."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self._volume = interface.QueryInterface(IAudioEndpointVolume)
        except Exception as e:
            error_msg = f"Failed to initialize Windows audio: {e}"
            raise BackendNotFoundError(error_msg) from e

    def play_beep(self) -> None:
        """Play a beep sound using Windows API."""
        winsound.Beep(1000, 250)  # 1000Hz for 250ms

    def set_volume(self, volume: float) -> None:
        """Set the system volume (0.0 to 1.0)."""
        # pycaw uses a range from -65.25 to 0.0 in dB
        # Convert linear 0-1 to proper dB range
        if not 0.0 <= volume <= 1.0:
            volume = max(0.0, min(1.0, volume))
        self._volume.SetMasterVolumeLevelScalar(volume, None)

    def get_volume(self) -> float:
        """Get the system volume (returns 0.0 to 1.0)."""
        return self._volume.GetMasterVolumeLevelScalar()

    def mute(self) -> None:
        """Mute the system audio."""
        self._volume.SetMute(1, None)

    def unmute(self) -> None:
        """Unmute the system audio."""
        self._volume.SetMute(0, None)

    def get_mute(self) -> bool:
        """Get the system mute state."""
        return bool(self._volume.GetMute())
