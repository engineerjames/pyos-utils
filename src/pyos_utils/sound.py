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
set_volume = _interface.set_volume
get_volume = _interface.get_volume
mute = _interface.mute
unmute = _interface.unmute
get_mute = _interface.get_mute

# Type verification
_impl: SoundInterface = _interface
