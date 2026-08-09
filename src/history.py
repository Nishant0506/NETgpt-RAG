import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .config import HISTORY_DIR


class HistoryStore:
    def __init__(self, history_dir: str = HISTORY_DIR):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.history_dir / "history.json"

    def load(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def save(self, entry: Dict[str, Any]) -> None:
        history = self.load()
        history.append(entry)
        self.file_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def delete(self, index: int) -> None:
        history = self.load()
        if 0 <= index < len(history):
            del history[index]
            self.file_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def export(self) -> str:
        return json.dumps(self.load(), indent=2)

    def create_entry(self, filename: str, findings: List[Dict[str, Any]], summary: str) -> Dict[str, Any]:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "filename": filename,
            "detected_issues": [item["issue"] for item in findings],
            "severity": "HIGH" if any(item["severity"] == "HIGH" for item in findings) else "MEDIUM",
            "confidence": max(item["confidence"] for item in findings) if findings else 0.0,
            "summary": summary,
        }
