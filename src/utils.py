from io import BytesIO
from pathlib import Path
from typing import List

from pypdf import PdfReader


def read_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def supported_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in {".txt", ".log", ".cfg", ".conf", ".pdf"}


def extract_text_from_bytes(data: bytes, filename: str) -> str:
    if not supported_extension(filename):
        return ""
    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""
    return data.decode("utf-8", errors="ignore")
