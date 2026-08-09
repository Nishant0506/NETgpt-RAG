from src.log_parser import LogParser


def test_parser_detects_ospf_issue():
    parser = LogParser()
    text = "Router1 %OSPF-5-ADJCHG: Neighbor 10.0.0.2 changed from FULL to DOWN"
    findings = parser.parse(text)
    assert len(findings) >= 1
    assert findings[0].issue == "OSPF Neighbor Down"
    assert findings[0].protocol == "OSPF"


def test_parser_detects_dhcp_issue():
    parser = LogParser()
    text = "Switch1 DHCP failed to offer an address"
    findings = parser.parse(text)
    assert any(f.issue == "DHCP Failure" for f in findings)
