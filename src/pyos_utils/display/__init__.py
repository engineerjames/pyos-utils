import sys

from ._display_interface import DisplayInterface

if sys.platform == "darwin":
    from ._display_mac import MacDisplayInterface as _PlatformDisplayInterface
elif sys.platform == "win32":
    from ._display_win import WindowsDisplayInterface as _PlatformDisplayInterface
elif sys.platform == "linux":
    from ._display_linux import LinuxDisplayInterface as _PlatformDisplayInterface
else:
    msg = f"Platform {sys.platform} is not supported"
    raise NotImplementedError(msg)

# Create singleton instance
_interface = _PlatformDisplayInterface()

# Export the interface methods:
get_info = _interface.get_info

# Type verification
_impl: DisplayInterface = _interface
