import sys  # noqa: A005

if sys.platform == "win32":
    from winsound import SND_ASYNC, SND_FILENAME, Beep, PlaySound  # noqa: F401 # type: ignore[reportUnusedImport]
else:

    def Beep(frequency: int, duration: int) -> None:  # noqa: D103, N802
        pass

    def PlaySound(sound: str, flags: int) -> None:  # noqa: D103, N802
        pass

    SND_FILENAME = 0xDEADBEEF
    SND_ASYNC = 0xDEADBEEF
