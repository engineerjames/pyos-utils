import sys
from typing import Any

if sys.platform == "win32":
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # noqa: F401 # type: ignore[reportUnusedImport]
else:

    class Volume:
        def SetMasterVolumeLevelScalar(self, *args: Any) -> None:  # noqa: ANN401, D102, N802
            pass

        def GetMasterVolumeLevelScalar(self, *args: Any) -> float:  # noqa: ANN401, ARG002, D102, N802
            return 0.5

        def SetMute(self, *args: Any) -> None:  # noqa: ANN401, D102, N802
            pass

        def GetMute(self) -> int:  # noqa: D102, N802
            return 0

    class Interface:
        def QueryInterface(self, *args: Any) -> Volume:  # noqa: ANN401, ARG002, D102, N802
            return Volume()

    class Device:
        def Activate(self, *args: Any) -> Interface:  # noqa: ANN401, ARG002, D102, N802
            return Interface()

    class AudioUtilities:
        @staticmethod
        def GetSpeakers() -> Device:  # noqa: D102, N802
            return Device()

    class IAudioEndpointVolume:
        _iid_: str = ""
