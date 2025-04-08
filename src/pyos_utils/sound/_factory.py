import sys

from ._sound_interface import SoundInterface
from ._sound_linux import LinuxSoundInterface
from ._sound_mac import MacSoundInterface
from ._sound_win import WindowsSoundInterface


class SoundInterfaceFactory:
    @staticmethod
    def create_interface(platform: str = sys.platform) -> SoundInterface:
        if platform == "darwin":
            return MacSoundInterface()
        if platform == "win32":
            return WindowsSoundInterface()
        if platform == "linux":
            return LinuxSoundInterface()

        msg = f"Platform {platform} is not supported"
        raise NotImplementedError(msg)
