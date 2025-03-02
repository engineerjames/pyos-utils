from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from pyos_utils.sound._exceptions import OperationFailedError
from pyos_utils.sound._sound_mac import MacSoundInterface


@pytest.fixture
def mac_sound_interface(mocker: MockerFixture) -> MacSoundInterface:
    mocker.patch("pathlib.Path.exists", return_value=True)
    return MacSoundInterface()


@patch("subprocess.run")
def test_play_beep(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    mac_sound_interface.play_beep()
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "beep"],
        check=False,
        text=True,
    )


@patch("subprocess.run")
def test_play_beep_failure(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(OperationFailedError):
        mac_sound_interface.play_beep()


@patch("subprocess.run")
def test_set_volume(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    mac_sound_interface.set_volume(0.5)
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "set volume output volume 50"],
        check=False,
        text=True,
    )


@patch("subprocess.run")
def test_set_volume_failure(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(OperationFailedError):
        mac_sound_interface.set_volume(0.5)


@patch("subprocess.run")
def test_get_volume(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0, stdout="50")
    volume: float = mac_sound_interface.get_volume()
    assert volume == 0.5
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "output volume of (get volume settings)"],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("subprocess.run")
def test_get_volume_failure(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(OperationFailedError):
        mac_sound_interface.get_volume()


@patch("subprocess.run")
def test_mute(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    mac_sound_interface.mute()
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "set volume output muted true"],
        check=False,
        text=True,
    )


@patch("subprocess.run")
def test_mute_failed(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(OperationFailedError):
        mac_sound_interface.mute()


@patch("subprocess.run")
def test_unmute(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0)
    mac_sound_interface.unmute()
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "set volume output muted false"],
        check=False,
        text=True,
    )


@patch("subprocess.run")
def test_unmute_failed(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(OperationFailedError):
        mac_sound_interface.unmute()


@patch("subprocess.run")
def test_get_mute(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0, stdout="true")
    assert mac_sound_interface.get_mute() is True
    mock_run.assert_called_once_with(
        [str(mac_sound_interface._osascript_path), "-e", "output muted of (get volume settings)"],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("subprocess.run")
def test_get_mute_false(mock_run: MagicMock, mac_sound_interface: MacSoundInterface) -> None:
    mock_run.return_value = MagicMock(returncode=0, stdout="false")
    assert mac_sound_interface.get_mute() is False
