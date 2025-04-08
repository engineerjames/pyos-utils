from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyos_utils.sound._exceptions import OperationFailedError
from pyos_utils.sound._sound_linux import Backend
from pyos_utils.sound.linux_backends.wireplumber import WirePlumberInterface


@pytest.fixture(autouse=True)
def mock_backend_detection() -> Generator[None, None, None]:
    with patch("pyos_utils.sound._sound_linux.Backend._detect_backend", return_value=Backend.WIREPLUMBER):
        yield


@pytest.fixture
def wireplumber_interface() -> WirePlumberInterface:
    return WirePlumberInterface(Path("/usr/bin/wpctl"))


@pytest.fixture
def mock_subprocess_run() -> Generator[Mock, None, None]:
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        yield mock_run


def test_play_beep_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    with patch("shutil.which", return_value="/usr/bin/beep"):
        wireplumber_interface._beep_path = "/usr/bin/beep"
        wireplumber_interface.play_beep()
        mock_subprocess_run.assert_called_once_with(
            ["/usr/bin/beep", "-f", "1000", "-l", "250"],
            check=False,
            text=True,
            capture_output=True,
        )


def test_play_beep_command_not_found(wireplumber_interface: WirePlumberInterface) -> None:
    with patch("shutil.which", return_value=None), pytest.raises(FileNotFoundError):
        wireplumber_interface.play_beep()


def test_set_volume_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    wireplumber_interface.set_volume(0.5)
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "50%"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_set_volume_failure(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.returncode = 1
    mock_subprocess_run.return_value.stderr = "Error setting volume"
    with pytest.raises(OperationFailedError):
        wireplumber_interface.set_volume(0.5)


def test_get_volume_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.stdout = "Volume: 0.75"
    assert wireplumber_interface.get_volume() == 0.75


def test_get_volume_failure(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.returncode = 1
    mock_subprocess_run.return_value.stderr = "Error getting volume"
    with pytest.raises(OperationFailedError):
        wireplumber_interface.get_volume()


def test_mute_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    wireplumber_interface.mute()
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_unmute_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    wireplumber_interface.unmute()
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "0"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_get_mute_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.stdout = "Volume: 0.75 [MUTED]"
    assert wireplumber_interface.get_mute() is True


def test_play_sound_success(wireplumber_interface: WirePlumberInterface, mock_subprocess_run: Mock) -> None:
    with patch("shutil.which", return_value="/usr/bin/aplay"), patch.object(Path, "exists", return_value=True):
        wireplumber_interface._path_to_aplay = "/usr/bin/aplay"
        wireplumber_interface.play_sound(Path("test.wav"))
        mock_subprocess_run.assert_called_once_with(
            ["/usr/bin/aplay", "test.wav"],
            check=False,
            text=True,
            capture_output=True,
        )


def test_play_sound_aplay_not_found(wireplumber_interface: WirePlumberInterface) -> None:
    with (
        patch("shutil.which", return_value=None),
        patch.object(Path, "exists", return_value=True),
        pytest.raises(FileNotFoundError),
    ):
        wireplumber_interface.play_sound(Path("test.wav"))


def test_play_sound_file_not_found(wireplumber_interface: WirePlumberInterface) -> None:
    with patch.object(Path, "exists", return_value=False), pytest.raises(FileNotFoundError):
        wireplumber_interface.play_sound(Path("nonexistent.wav"))
