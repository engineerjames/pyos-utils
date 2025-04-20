from collections.abc import Callable

from ._factory import NetworkInterfaceFactory
from ._interface import NetworkInterface

get_network: Callable[..., NetworkInterface] = NetworkInterfaceFactory.create_interface

__all__ = [
    "NetworkInterface",
    "get_network",
]
