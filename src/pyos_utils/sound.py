import sys

from ._sound_interface import SoundInterface

if sys.platform == "darwin":
    from ._sound_mac import MacSoundInterface as _PlatformSoundInterface
elif sys.platform == "win32":
    from ._sound_win import WindowsSoundInterface as _PlatformSoundInterface
elif sys.platform == "linux":
    from ._sound_linux import LinuxSoundInterface as _PlatformSoundInterface
else:
    msg = f"Platform {sys.platform} is not supported"
    raise NotImplementedError(msg)

# Create singleton instance
_interface = _PlatformSoundInterface()

# Export the interface methods: TODO -- Add a test to ensure all methods are exported
play_beep = _interface.play_beep
play_alert = _interface.play_alert

# Type verification
_impl: SoundInterface = _interface
