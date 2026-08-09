from typing import List
from .models import Finding


class NetworkAnalyzer:
    def analyze(self, findings: List[Finding]) -> List[Finding]:
        if not findings:
            return []

        for finding in findings:
            if finding.issue == "OSPF Neighbor Down" and finding.confidence < 0.95:
                finding.confidence = 0.95
            elif finding.issue == "BGP Neighbor Down" and finding.confidence < 0.9:
                finding.confidence = 0.9

        return findings
