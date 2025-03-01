import sys

if sys.platform == "win32":
    import comtypes  # noqa: F401
else:
    CLSCTX_ALL = 0xDEADBEEF
