from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Finding:
    issue: str
    severity: str
    confidence: float
    protocol: str
    device: Optional[str] = None
    interface: Optional[str] = None
    evidence: List[str] = field(default_factory=list)
    details: Optional[str] = None


@dataclass
class AnalysisResult:
    filename: str
    findings: List[Finding]
    summary: str
    evidence: List[str]
    llm_response: Optional[str] = None
    recommended_commands: List[str] = field(default_factory=list)
    recommended_fix: Optional[str] = None
