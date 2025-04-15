import sys

from ._interface import SoundInterface


class SoundInterfaceFactory:
    @staticmethod
    def create_interface(platform: str = sys.platform) -> SoundInterface:
        """Create a sound interface based on the specified platform."""
        if platform == "darwin":
            from ._mac import MacSoundInterface

            return MacSoundInterface()
        if platform == "win32":
            from ._win import WindowsSoundInterface

            return WindowsSoundInterface()
        if platform == "linux":
            from ._linux import LinuxSoundInterface

            return LinuxSoundInterface()

        msg = f"Platform {platform} is not supported"
        raise NotImplementedError(msg)
