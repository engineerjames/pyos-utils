from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

patch("pyos_utils.sound._factory.SoundInterfaceFactory.create_interface")

from pyos_utils.sound._exceptions import OperationFailedError  # noqa: E402
from pyos_utils.sound.linux_backends.pulse import PulseAudioInterface  # noqa: E402


@pytest.fixture
def pulse_interface() -> PulseAudioInterface:
    return PulseAudioInterface(Path("/usr/bin/pactl"))


@pytest.fixture
def mock_subprocess_run() -> Generator[Mock, None, None]:
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        yield mock_run


def test_play_beep_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    with patch("shutil.which", return_value="/usr/bin/beep"):
        pulse_interface._beep_path = "/usr/bin/beep"
        pulse_interface.play_beep()
        mock_subprocess_run.assert_called_once_with(
            ["/usr/bin/beep", "-f", "1000", "-l", "250"],
            check=False,
            text=True,
            capture_output=True,
        )


def test_play_beep_command_not_found(pulse_interface: PulseAudioInterface) -> None:
    with patch("shutil.which", return_value=None), pytest.raises(FileNotFoundError):
        pulse_interface.play_beep()


def test_set_volume_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    pulse_interface.set_volume(0.5)
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/pactl", "set-sink-volume", "@DEFAULT_SINK@", "50%"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_set_volume_failure(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.returncode = 1
    mock_subprocess_run.return_value.stderr = "Error setting volume"
    with pytest.raises(OperationFailedError):
        pulse_interface.set_volume(0.5)


def test_get_volume_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.stdout = "Volume: front-left: 65536 / 75% / -0.00 dB"
    assert pulse_interface.get_volume() == 0.75


def test_get_volume_failure(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.returncode = 1
    mock_subprocess_run.return_value.stderr = "Error getting volume"
    with pytest.raises(OperationFailedError):
        pulse_interface.get_volume()


def test_mute_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    pulse_interface.mute()
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_unmute_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    pulse_interface.unmute()
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_get_mute_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    mock_subprocess_run.return_value.stdout = "Mute: yes"
    assert pulse_interface.get_mute() is True


def test_play_sound_success(pulse_interface: PulseAudioInterface, mock_subprocess_run: Mock) -> None:
    with patch.object(Path, "exists", return_value=True):
        pulse_interface.play_sound(Path("test.wav"))
        mock_subprocess_run.assert_called_once_with(
            ["/usr/bin/pactl", "play-file", "test.wav"],
            check=False,
            text=True,
            capture_output=True,
        )


def test_play_sound_file_not_found(pulse_interface: PulseAudioInterface) -> None:
    with patch.object(Path, "exists", return_value=False), pytest.raises(FileNotFoundError):
        pulse_interface.play_sound(Path("nonexistent.wav"))
