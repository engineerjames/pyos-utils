from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_platform_and_backend() -> Generator[None, None, None]:
    with (
        patch("sys.platform", "linux"),
        patch(
            "pyos_utils.sound._sound_linux.Backend._detect_backend",
            return_value=("wireplumber", "/usr/bin/wpctl"),
        ),
        patch("pyos_utils.sound._sound_linux.Backend.get_interface", return_value="mock_interface"),
    ):
        # Import the modules only after patching
        from pyos_utils.sound._factory import SoundInterfaceFactory  # type: ignore[reportUnusedImport]
        from pyos_utils.sound._sound_linux import Backend, LinuxSoundInterface  # type: ignore[reportUnusedImport]
        from pyos_utils.sound._sound_mac import MacSoundInterface  # type: ignore[reportUnusedImport]
        from pyos_utils.sound._sound_win import WindowsSoundInterface  # type: ignore[reportUnusedImport]

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
