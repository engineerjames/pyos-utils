import re
import subprocess
from re import Match
from typing import Any

from pyos_utils.networking._info import NetworkInfo
from pyos_utils.networking._interface import NetworkInterface


class MacNetworkInterface(NetworkInterface):
    """Mac implementation of the NetworkInterface."""

    def get_info(self) -> list[NetworkInfo]:
        """Get the network information for all network interfaces."""
        interfaces: list[NetworkInfo] = []

        # Get list of all hardware ports
        cmd: list[str] = ["networksetup", "-listallhardwareports"]
        output: str = subprocess.check_output(cmd).decode()

        # Parse the output to get interface names and device names
        lines: list[str] = [o for o in output.split(sep="\n") if o]
        for i, line in enumerate(lines):
            if "Hardware Port" not in line:
                continue

            # Extract hardware port name and device name
            # Example line: "Hardware Port: Wi-Fi (AirPort)"
            # Example line: "Device: en0"
            # Example line: "Ethernet Address: 00:00:00:00:00:00"
            name_match: Match[str] | None = re.search(r"Hardware Port: ([^(]+)", line)
            device_match: Match[str] | None = re.search(r"Device: (.*)", lines[i + 1])

            if name_match and device_match:
                name: str = name_match.group(1).strip()
                device: str = device_match.group(1).strip()

                # Get IP address using ifconfig
                try:
                    cmd = ["ifconfig", device]
                    ifconfig_output: str = subprocess.check_output(cmd).decode()
                    ip_match: Match[str] | None = re.search(r"inet ([\d.]+)", ifconfig_output)
                    active_match = re.search(r"status: (active|inactive)", ifconfig_output)
                    is_active: bool | Any = active_match.group(1) == "active" if active_match else None
                    ip: str | Any = ip_match.group(1) if ip_match else None

                    interfaces.append(
                        NetworkInfo(
                            name=name,
                            device_name=device,
                            ip_address=ip,
                            is_active=is_active,
                        ),
                    )
                except subprocess.CalledProcessError:
                    continue

        return interfaces
