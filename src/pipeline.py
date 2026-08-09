from typing import Any, Dict, List, Optional, Tuple

from .history import HistoryStore
from .llm import OllamaClient
from .log_parser import LogParser
from .models import AnalysisResult, Finding
from .network_analyzer import NetworkAnalyzer
from .prompts import build_prompt
from .rag import RAGPipeline


class AnalysisPipeline:
    def __init__(self, history_store: Optional[HistoryStore] = None):
        self.history_store = history_store or HistoryStore()

    def run(self, filename: str, text: str, question: str = "Summarize the network issue") -> Tuple[AnalysisResult, Dict[str, Any]]:
        parser = LogParser()
        findings = parser.parse(text)
        analyzer = NetworkAnalyzer()
        findings = analyzer.analyze(findings)

        rag = RAGPipeline()
        try:
            rag_context = rag.retrieve(question, k=4)
        except Exception:
            rag_context = []

        primary_finding = findings[0] if findings else Finding(
            issue="No clear issue detected",
            severity="LOW",
            confidence=0.0,
            protocol="Unknown",
            evidence=["No strong evidence found in the uploaded content."],
            details="The uploaded content did not clearly indicate a network issue.",
        )

        prompt = build_prompt(question, primary_finding, rag_context)
        llm = OllamaClient()
        llm_response = llm.generate(prompt)

        summary = self._build_summary(findings, primary_finding)
        recommended_commands = self._recommend_commands(primary_finding)
        recommended_fix = self._recommend_fix(primary_finding)

        result = AnalysisResult(
            filename=filename,
            findings=findings or [primary_finding],
            summary=summary,
            evidence=[e for f in findings or [primary_finding] for e in f.evidence],
            llm_response=llm_response,
            recommended_commands=recommended_commands,
            recommended_fix=recommended_fix,
        )

        entry = self.history_store.create_entry(
            filename,
            [{"issue": finding.issue, "severity": finding.severity, "confidence": finding.confidence} for finding in result.findings],
            summary,
        )
        self.history_store.save(entry)
        return result, entry

    def _build_summary(self, findings: List[Finding], primary_finding: Finding) -> str:
        if not findings:
            return "No clear issue was detected from the uploaded content."
        issue_names = ", ".join(f.issue for f in findings)
        return f"Detected network issues: {issue_names}. The strongest finding is {primary_finding.issue}."

    def _recommend_commands(self, finding: Finding) -> List[str]:
        mapping = {
            "OSPF": ["show ip ospf neighbor", "show ip ospf interface", "show ip protocols"],
            "BGP": ["show ip bgp summary", "show ip bgp neighbors", "show log"],
            "VLAN": ["show vlan brief", "show interfaces trunk", "show spanning-tree summary"],
            "DHCP": ["show ip dhcp binding", "show ip dhcp server statistics", "show running-config | section dhcp"],
            "STP": ["show spanning-tree summary", "show spanning-tree detail", "show interfaces status"],
        }
        return mapping.get(finding.protocol, ["show interfaces status", "show ip interface brief", "show running-config"])

    def _recommend_fix(self, finding: Finding) -> str:
        if finding.protocol == "OSPF":
            return "Restore the affected interface or correct the neighbor adjacency, authentication, or MTU mismatch."
        if finding.protocol == "BGP":
            return "Verify reachability to the peer, review session parameters, and check the BGP neighbor states."
        if finding.protocol == "DHCP":
            return "Verify the DHCP scope, server reachability, and interface configuration for the affected subnet."
        return "Confirm the evidence, inspect the affected interface or protocol state, and apply the smallest corrective change supported by the logs."
