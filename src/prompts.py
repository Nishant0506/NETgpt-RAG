def build_prompt(question: str, finding, rag_context: list[str]) -> str:
    evidence = "\n".join(finding.evidence) if finding else "No evidence"
    return f"""You are a network troubleshooting assistant.

User question: {question}

Detected issue: {finding.issue if finding else 'Unknown'}
Evidence from log:
{evidence}

Retrieved knowledge:
{chr(10).join(rag_context)}

Instructions:
- Do not invent evidence.
- Clearly distinguish confirmed evidence from possible causes.
- Provide: Problem Summary, Evidence, Likely Root Cause, Troubleshooting Steps, Recommended Cisco Commands, Recommended Fix, Confidence Explanation.
"""
