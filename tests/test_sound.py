import importlib
import sys
from unittest.mock import patch

import pytest

from pyos_utils.sound import _interface


def test_sound_interface_exists() -> None:
    assert _interface is not None


@pytest.mark.parametrize("platform", ["darwin", "win32", "linux"])
def test_supported_platforms(platform: str) -> None:
    our_sys_platform = sys.platform
    with patch("sys.platform", platform), patch("pathlib.Path.exists", return_value=True):
        # If we're not runing on Windows, and the platform is Windows, we should get a ModuleNotFoundError
        # as we haven't installed the Windows specific dependencies
        if our_sys_platform != "win32" and platform == "win32":
            with pytest.raises(ModuleNotFoundError):  # noqa: PT012
                import pyos_utils.sound

                importlib.reload(pyos_utils.sound)
        else:
            import pyos_utils.sound

            importlib.reload(pyos_utils.sound)


def test_unsupported_platform() -> None:
    with patch("sys.platform", "unsupported"), pytest.raises(NotImplementedError):  # noqa: PT012
        import pyos_utils.sound

        importlib.reload(pyos_utils.sound)


def test_sound_interface_exports() -> None:
    from pyos_utils import sound
    from pyos_utils._sound_interface import SoundInterface

    # Get all the methods of the SoundInterface as a list of strings:
    methods = [method for method in dir(SoundInterface) if not method.startswith("_")]

    for m in methods:
        assert hasattr(sound, m)
