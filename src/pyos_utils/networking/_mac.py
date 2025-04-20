import re
import subprocess
from re import Match
from typing import Any

from pyos_utils.networking._info import NetworkInfo
from pyos_utils.networking._interface import NetworkInterface


class MacNetworkInterface(NetworkInterface):
    """Mac implementation of the NetworkInterface."""

    def get_info(self) -> list[NetworkInfo]:
        """Get the display information for all network interfaces."""
        interfaces: list[Any] = []

        # Get list of all hardware ports
        cmd: list[str | Any] = ["networksetup", "-listallhardwareports"]
        output: str = subprocess.check_output(cmd).decode()

        # Parse the output to get interface names and device names
        ports: list[str] = output.split(sep="\n\n")
        for port in ports:
            if not port.strip():
                continue

            name_match: Match[str] | None = re.search(r"Hardware Port: ([^(]+)", port)
            device_match: Match[str] | None = re.search(r"Device: (.*)", port)

            if name_match and device_match:
                name: str | Any = name_match.group(1).strip()
                device: str | Any = device_match.group(1).strip()

                # Get IP address using ifconfig
                try:
                    cmd = ["ifconfig", device]
                    ifconfig_output: str = subprocess.check_output(cmd).decode()
                    ip_match: Match[str] | None = re.search(r"inet ([\d.]+)", ifconfig_output)
                    ip: str | Any = ip_match.group(1) if ip_match else None

                    interfaces.append(NetworkInfo(name=name, device_name=device, ip_address=ip))
                except subprocess.CalledProcessError:
                    continue

        return interfaces


if __name__ == "__main__":
    mac_interface = MacNetworkInterface()
    network_info = mac_interface.get_info()
    for info in network_info:
        print(f"Name: {info.name}, IP Address: {info.ip_address}")
