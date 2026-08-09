import re
from typing import List
from .models import Finding


class LogParser:
    def parse(self, text: str) -> List[Finding]:
        findings: List[Finding] = []
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            if "OSPF" in line and "DOWN" in line:
                findings.append(Finding(
                    issue="OSPF Neighbor Down",
                    severity="HIGH",
                    confidence=0.92,
                    protocol="OSPF",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="OSPF adjacency changed to down."
                ))
            elif "BGP" in line and "down" in line.lower():
                findings.append(Finding(
                    issue="BGP Neighbor Down",
                    severity="HIGH",
                    confidence=0.88,
                    protocol="BGP",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="BGP session is down."
                ))
            elif "interface" in line.lower() and "down" in line.lower():
                findings.append(Finding(
                    issue="Interface Failure",
                    severity="HIGH",
                    confidence=0.9,
                    protocol="Interface",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="An interface reported a failure state."
                ))
            elif "VLAN" in line and "blocked" in line.lower():
                findings.append(Finding(
                    issue="VLAN Issue",
                    severity="MEDIUM",
                    confidence=0.8,
                    protocol="VLAN",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="VLAN activity indicates a topology issue."
                ))
            elif "DHCP" in line and "failed" in line.lower():
                findings.append(Finding(
                    issue="DHCP Failure",
                    severity="HIGH",
                    confidence=0.87,
                    protocol="DHCP",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="DHCP lease or offer failed."
                ))
            elif "STP" in line and "topology" in line.lower():
                findings.append(Finding(
                    issue="STP Topology Change",
                    severity="MEDIUM",
                    confidence=0.78,
                    protocol="STP",
                    device=self._extract_device(line),
                    interface=self._extract_interface(line),
                    evidence=[line],
                    details="STP detected a topology change."
                ))

        return findings

    def _extract_device(self, line: str) -> str | None:
        match = re.search(r"([A-Za-z0-9._-]+)", line)
        return match.group(1) if match else None

    def _extract_interface(self, line: str) -> str | None:
        match = re.search(r"(GigabitEthernet[0-9/.-]+|FastEthernet[0-9/.-]+|Ethernet[0-9/.-]+)", line)
        return match.group(1) if match else None
