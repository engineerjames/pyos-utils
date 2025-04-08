from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_backend_detection() -> Generator[None, None, None]:
    from pyos_utils.sound._sound_linux import Backend

    with patch(
        "pyos_utils.sound._sound_linux.Backend._detect_backend",
        return_value=(Backend.WIREPLUMBER, "/usr/bin/wpctl"),
    ):
        yield


def test_create_interface_linux() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._sound_linux import LinuxSoundInterface

    interface = SoundInterfaceFactory.create_interface("linux")
    assert isinstance(interface, LinuxSoundInterface)


def test_create_interface_mac() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._sound_mac import MacSoundInterface

    interface = SoundInterfaceFactory.create_interface("darwin")
    assert isinstance(interface, MacSoundInterface)


def test_create_interface_windows() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory
    from pyos_utils.sound._sound_win import WindowsSoundInterface

    interface = SoundInterfaceFactory.create_interface("win32")
    assert isinstance(interface, WindowsSoundInterface)


def test_create_interface_unsupported() -> None:
    from pyos_utils.sound._factory import SoundInterfaceFactory

    with pytest.raises(NotImplementedError):
        SoundInterfaceFactory.create_interface("unsupported_platform")
