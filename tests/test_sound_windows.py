from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from pyos_utils._exceptions import OperationFailedError
from pyos_utils._sound_win import WindowsSoundInterface


@pytest.fixture
def windows_sound_interface(mocker: MockerFixture) -> WindowsSoundInterface:
    mock_devices = MagicMock()
    mock_interface = MagicMock()
    mock_interface.QueryInterface.return_value = MagicMock()

    mocker.patch("pyos_utils.external.pycaw.AudioUtilities.GetSpeakers", return_value=mock_devices)

    return WindowsSoundInterface()


def test_play_beep(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    beep_mock = mocker.patch("pyos_utils._sound_win.winsound.Beep")
    windows_sound_interface.play_beep()
    beep_mock.assert_called_once_with(1000, 250)


def test_play_beep_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    beep_mock = mocker.patch("pyos_utils._sound_win.winsound.Beep")
    beep_mock.side_effect = RuntimeError("Beep failed")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.play_beep()


def test_set_volume(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    set_volume_mock = mocker.patch.object(windows_sound_interface._volume, "SetMasterVolumeLevelScalar")
    windows_sound_interface.set_volume(0.5)
    set_volume_mock.assert_called_once_with(0.5, None)


def test_set_volume_out_of_range_max(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    set_volume_mock = mocker.patch.object(windows_sound_interface._volume, "SetMasterVolumeLevelScalar")
    windows_sound_interface.set_volume(1.5)
    set_volume_mock.assert_called_once_with(1.0, None)


def test_set_volume_out_of_range_min(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    set_volume_mock = mocker.patch.object(windows_sound_interface._volume, "SetMasterVolumeLevelScalar")
    windows_sound_interface.set_volume(-0.5)
    set_volume_mock.assert_called_once_with(0.0, None)


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_set_volume_failure(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_audio.GetSpeakers.side_effect = RuntimeError("Failed to get speakers")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.set_volume(0.5)


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_get_volume(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_session = MagicMock()
    mock_session.SimpleAudioVolume.MasterVolume = 0.5
    mock_audio.GetSpeakers.return_value = mock_session
    volume = windows_sound_interface.get_volume()
    assert volume == 0.5


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_get_volume_failure(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_audio.GetSpeakers.side_effect = RuntimeError("Failed to get speakers")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.get_volume()


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_mute(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_session = MagicMock()
    mock_audio.GetSpeakers.return_value = mock_session
    windows_sound_interface.mute()
    assert mock_session.SimpleAudioVolume.Mute is True


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_mute_failure(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_audio.GetSpeakers.side_effect = RuntimeError("Failed to get speakers")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.mute()


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_unmute(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_session = MagicMock()
    mock_audio.GetSpeakers.return_value = mock_session
    windows_sound_interface.unmute()
    assert mock_session.SimpleAudioVolume.Mute is False


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_unmute_failure(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_audio.GetSpeakers.side_effect = RuntimeError("Failed to get speakers")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.unmute()


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_get_mute(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_session = MagicMock()
    mock_session.SimpleAudioVolume.Mute = True
    mock_audio.GetSpeakers.return_value = mock_session
    assert windows_sound_interface.get_mute() is True


@patch("pyos_utils._sound_windows.pycaw.AudioUtilities")
def test_get_mute_failure(mock_audio: MagicMock, windows_sound_interface: WindowsSoundInterface) -> None:
    mock_audio.GetSpeakers.side_effect = RuntimeError("Failed to get speakers")
    with pytest.raises(OperationFailedError):
        windows_sound_interface.get_mute()
