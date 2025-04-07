import pytest
from pytest_mock import MockerFixture

from pyos_utils.sound._exceptions import OperationFailedError
from pyos_utils.sound.linux_backends.pulse import PulseAudioInterface


@pytest.fixture
def linux_sound_interface(mocker: MockerFixture) -> PulseAudioInterface:
    mocker.patch("pathlib.Path.exists", return_value=True)
    return PulseAudioInterface()


def test_play_beep(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    linux_sound_interface.play_beep()
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._beep_path), "-f", "1000", "-l", "250"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_play_beep_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to play beep sound"):
        linux_sound_interface.play_beep()


def test_set_volume(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    linux_sound_interface.set_volume(0.5)
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._pactl_path), "set-sink-volume", "@DEFAULT_SINK@", "50%"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_set_volume_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to set volume"):
        linux_sound_interface.set_volume(0.5)


def test_get_volume(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Volume: front-left: 65536 / 50% / -0.00 dB"
    volume = linux_sound_interface.get_volume()
    assert volume == 0.5
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._pactl_path), "get-sink-volume", "@DEFAULT_SINK@"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_get_volume_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to get volume"):
        linux_sound_interface.get_volume()


def test_mute(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    linux_sound_interface.mute()
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "1"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_mute_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to mute"):
        linux_sound_interface.mute()


def test_unmute(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    linux_sound_interface.unmute()
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._pactl_path), "set-sink-mute", "@DEFAULT_SINK@", "0"],
        check=False,
        text=True,
        capture_output=True,
    )


def test_unmute_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to unmute"):
        linux_sound_interface.unmute()


def test_get_mute_true(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Mute: yes"
    assert linux_sound_interface.get_mute() is True
    mock_run.assert_called_once_with(
        [str(linux_sound_interface._pactl_path), "get-sink-mute", "@DEFAULT_SINK@"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_get_mute_false(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Mute: no"
    assert linux_sound_interface.get_mute() is False


def test_get_mute_failure(mocker: MockerFixture, linux_sound_interface: PulseAudioInterface) -> None:
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(OperationFailedError, match="Failed to get mute state"):
        linux_sound_interface.get_mute()
