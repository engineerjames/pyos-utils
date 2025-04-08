import importlib
from unittest.mock import patch

import pytest

from pyos_utils.sound._factory import SoundInterfaceFactory


def test_sound_interface_exists() -> None:
    assert SoundInterfaceFactory.create_interface("win32") is not None


def test_unsupported_platform() -> None:
    with patch("sys.platform", "unsupported"), pytest.raises(NotImplementedError):  # noqa: PT012
        import pyos_utils.sound

        importlib.reload(pyos_utils.sound)


def test_sound_interface_exports() -> None:
    from pyos_utils import sound
    from pyos_utils.sound._sound_interface import SoundInterface

    # Get all the methods of the SoundInterface as a list of strings:
    methods = [method for method in dir(SoundInterface) if not method.startswith("_")]

    for m in methods:
        assert hasattr(sound, m)
