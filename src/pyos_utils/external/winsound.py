import sys  # noqa: A005

if sys.platform == "win32":
    import winsound  # noqa: F401
else:

    def Beep(frequency: int, duration: int) -> None:  # noqa: D103, N802
        pass
