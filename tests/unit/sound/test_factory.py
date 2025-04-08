from collections.abc import Generator
from unittest.mock import patch

import pytest

from pyos_utils.sound._factory import SoundInterfaceFactory
from pyos_utils.sound._sound_linux import Backend, LinuxSoundInterface
from pyos_utils.sound._sound_mac import MacSoundInterface
from pyos_utils.sound._sound_win import WindowsSoundInterface


@pytest.fixture(autouse=True)
def mock_backend_detection() -> Generator[None, None, None]:
    with patch(
        "pyos_utils.sound._sound_linux.Backend._detect_backend",
        return_value=(Backend.WIREPLUMBER, "/usr/bin/wpctl"),
    ):
        yield


def test_create_interface_linux() -> None:
    interface = SoundInterfaceFactory.create_interface("linux")
    assert isinstance(interface, LinuxSoundInterface)


def test_create_interface_mac() -> None:
    interface = SoundInterfaceFactory.create_interface("darwin")
    assert isinstance(interface, MacSoundInterface)


def test_create_interface_windows() -> None:
    interface = SoundInterfaceFactory.create_interface("win32")
    assert isinstance(interface, WindowsSoundInterface)


def test_create_interface_unsupported() -> None:
    with pytest.raises(NotImplementedError):
        SoundInterfaceFactory.create_interface("unsupported_platform")
