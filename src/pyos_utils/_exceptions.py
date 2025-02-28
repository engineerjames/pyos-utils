class BackendNotFoundError(Exception):
    """
    Exception raised when no suitable audio backend can be found.

    This exception is raised when the system is unable to locate or initialize
    any of the supported audio backend libraries (e.g., pyaudio, sounddevice).
    """
