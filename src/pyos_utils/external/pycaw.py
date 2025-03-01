import sys
from typing import Any

if sys.platform == "win32":
    import comtypes  # noqa: F401
else:

    class Volume:  # noqa: D101
        def SetMasterVolumeLevelScalar(self, *args: Any) -> None:  # noqa: ANN401, D102, N802
            pass

        def GetMasterVolumeLevelScalar(self, *args: Any) -> float:  # noqa: ANN401, ARG002, D102, N802
            return 0.5

        def SetMute(self, *args: Any) -> None:  # noqa: ANN401, D102, N802
            pass

        def GetMute(self) -> int:  # noqa: D102, N802
            return 0

    class Interface:  # noqa: D101
        def QueryInterface(self, *args: Any) -> Volume:  # noqa: ANN401, ARG002, D102, N802
            return Volume()

    class Device:  # noqa: D101
        def Activate(self, *args: Any) -> Interface:  # noqa: ANN401, ARG002, D102, N802
            return Interface()

    class AudioUtilities:  # noqa: D101
        @staticmethod
        def GetSpeakers() -> Device:  # noqa: D102, N802
            return Device()

    class IAudioEndpointVolume:  # noqa: D101
        _iid_: str = ""
