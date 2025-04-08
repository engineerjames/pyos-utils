import importlib
from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_backend_detection() -> Generator[None, None, None]:
    with patch(
        "pyos_utils.sound._sound_linux.Backend._detect_backend",
        return_value=("wireplumber", "/usr/bin/wpctl"),
    ):
        yield


def test_sound_interface_exists() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory

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
