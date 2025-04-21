import json
import subprocess
from typing import Any

from pyos_utils.networking._info import NetworkInfo
from pyos_utils.networking._interface import NetworkInterface


class LinuxNetworkInterface(NetworkInterface):
    """Linux implementation of the NetworkInterface."""

    def get_info(self) -> list[NetworkInfo]:
        """Get the network information."""
        interfaces: list[NetworkInfo] = []

        # Get list of all network interfaces using ip addr, JSON output
        cmd: list[str] = ["ip", "-j", "addr"]
        try:
            output: str = subprocess.check_output(cmd).decode()
        except subprocess.CalledProcessError:
            return interfaces

        # Parse the JSON output
        json_data: list[dict[str, Any]] = []
        try:
            json_data = json.loads(output)
        except json.JSONDecodeError:
            return interfaces

        # Iterate over each interface
        for interface in json_data:
            current_name: str = "Unknown"
            current_interface: str = interface["ifname"]
            ip_match: str = interface["addr_info"][0].get("local")
            is_active: bool | None = "UP" in interface["flags"]

            if current_interface.startswith("wlan"):
                current_name = f"Wireless {current_interface}"
            elif current_interface.startswith(("eth", "enp", "eno", "ens", "en")):
                current_name = f"Ethernet {current_interface}"
            elif current_interface.startswith("lo"):
                current_name = f"Loopback {current_interface}"

            # Add the interface information to the list
            interfaces.append(
                NetworkInfo(
                    name=current_name,
                    device_name=current_interface,
                    ip_address=ip_match,
                    is_active=is_active,
                ),
            )

        return interfaces
