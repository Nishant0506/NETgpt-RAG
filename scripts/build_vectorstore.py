from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag import RAGPipeline


if __name__ == "__main__":
    pipeline = RAGPipeline()
    pipeline.build_index()
    print("FAISS vector store built successfully.")
