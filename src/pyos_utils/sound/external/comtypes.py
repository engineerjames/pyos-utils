import sys

if sys.platform == "win32":
    from comtypes import CLSCTX_ALL  # noqa: F401 # type: ignore[reportUnusedImport]
else:
    CLSCTX_ALL = 0xDEADBEEF
