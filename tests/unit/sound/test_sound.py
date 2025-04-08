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

        pyos_utils.sound.SoundInterfaceFactory.create_interface("unsupported_platform")
