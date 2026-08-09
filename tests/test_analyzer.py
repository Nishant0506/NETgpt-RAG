from src.network_analyzer import NetworkAnalyzer
from src.models import Finding


def test_analyzer_increases_confidence_for_ospf():
    analyzer = NetworkAnalyzer()
    findings = [Finding(issue="OSPF Neighbor Down", severity="HIGH", confidence=0.9, protocol="OSPF")]
    result = analyzer.analyze(findings)
    assert result[0].confidence >= 0.95
