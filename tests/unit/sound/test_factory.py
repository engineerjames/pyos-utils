from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_backend_detection() -> Generator[None, None, None]:
    with patch(
        "pyos_utils.sound._linux.Backend._detect_backend",
        return_value=("wireplumber", "/usr/bin/wpctl"),
    ):
        yield


def test_create_interface_linux() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._linux import LinuxSoundInterface

    interface = SoundInterfaceFactory.create_interface("linux")
    assert isinstance(interface, LinuxSoundInterface)


def test_create_interface_mac() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._mac import MacSoundInterface

    # Mock shutil.which to return a valid path
    with patch("shutil.which", return_value="/usr/bin/osascript"), patch("pathlib.Path.exists", return_value=True):
        interface = SoundInterfaceFactory.create_interface("darwin")
        assert isinstance(interface, MacSoundInterface)


def test_create_interface_windows() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._win import WindowsSoundInterface

    interface = SoundInterfaceFactory.create_interface("win32")
    assert isinstance(interface, WindowsSoundInterface)


def test_create_interface_unsupported() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory

    with pytest.raises(NotImplementedError):
        SoundInterfaceFactory.create_interface("unsupported_platform")
