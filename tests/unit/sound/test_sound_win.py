import sys
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from pyos_utils.sound._exceptions import OperationFailedError
from pyos_utils.sound._sound_win import WindowsSoundInterface


@pytest.fixture(autouse=True)
def mock_platform() -> Generator[None, None, None]:
    with patch.object(sys, "platform", "win32"):
        yield


@pytest.fixture
def windows_sound_interface(mocker: MockerFixture) -> WindowsSoundInterface:
    mock_devices = MagicMock()
    mock_interface = MagicMock()
    mock_interface.QueryInterface.return_value = MagicMock()

    mocker.patch("pyos_utils.sound.external.pycaw.AudioUtilities.GetSpeakers", return_value=mock_devices)

    return WindowsSoundInterface()


def test_play_beep(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    beep_mock = mocker.patch("pyos_utils.sound._sound_win.winsound.Beep")
    windows_sound_interface.play_beep()
    beep_mock.assert_called_once_with(1000, 250)


def test_play_beep_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    beep_mock = mocker.patch("pyos_utils.sound._sound_win.winsound.Beep")
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


def test_set_volume_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "SetMasterVolumeLevelScalar",
        side_effect=RuntimeError("Failed to get speakers"),
    )
    with pytest.raises(OperationFailedError):
        windows_sound_interface.set_volume(0.5)


def test_get_volume(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "GetMasterVolumeLevelScalar",
        return_value=0.5,
    )
    volume = windows_sound_interface.get_volume()
    assert volume == 0.5


def test_get_volume_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "GetMasterVolumeLevelScalar",
        side_effect=RuntimeError("Failed to get volume"),
    )

    with pytest.raises(OperationFailedError):
        windows_sound_interface.get_volume()


def test_mute(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    set_mute_mock = mocker.patch.object(windows_sound_interface._volume, "SetMute")
    windows_sound_interface.mute()
    set_mute_mock.assert_called_once_with(1, None)


def test_mute_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "SetMute",
        side_effect=RuntimeError("Failed to mute"),
    )

    with pytest.raises(OperationFailedError):
        windows_sound_interface.mute()


def test_unmute(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    set_mute_mock = mocker.patch.object(windows_sound_interface._volume, "SetMute")
    windows_sound_interface.unmute()

    set_mute_mock.assert_called_once_with(0, None)


def test_unmute_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "SetMute",
        side_effect=RuntimeError("Failed to mute"),
    )

    with pytest.raises(OperationFailedError):
        windows_sound_interface.unmute()


def test_get_mute_true(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(windows_sound_interface._volume, "GetMute", return_value=1)
    assert windows_sound_interface.get_mute() is True


def test_get_mute_false(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(windows_sound_interface._volume, "GetMute", return_value=0)
    assert windows_sound_interface.get_mute() is False


def test_get_mute_failure(windows_sound_interface: WindowsSoundInterface, mocker: MockerFixture) -> None:
    mocker.patch.object(
        windows_sound_interface._volume,
        "GetMute",
        side_effect=RuntimeError("Failed to mute"),
    )
    with pytest.raises(OperationFailedError):
        windows_sound_interface.get_mute()
