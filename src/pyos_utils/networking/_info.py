from dataclasses import dataclass


@dataclass
class NetworkInfo:
    name: str | None = None
    """ The name of the network adapter. Example: Wi-Fi, Ethernet, etc."""

    ip_address: str | None = None
    """ The IP address of the network adapter."""

    device_name: str | None = None
    """ The device name of the network adapter. Example: en0, eth0, wlan0, etc."""
