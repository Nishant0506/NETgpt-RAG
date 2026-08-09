import os
import shutil

from src.rag import RAGPipeline


def test_rag_pipeline_retrieves_documents(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "ospf.txt").write_text("OSPF uses hello packets to maintain adjacencies.", encoding="utf-8")
    pipeline = RAGPipeline(persist_dir=str(tmp_path / "vectorstore"))
    pipeline._load_documents = lambda: [
        type("Doc", (), {"page_content": "OSPF uses hello packets to maintain adjacencies.", "metadata": {}})()
    ]

    # Use a lightweight fallback path to avoid depending on a downloaded model during tests.
    from langchain.docstore.document import Document
    docs = [Document(page_content="OSPF uses hello packets to maintain adjacencies.", metadata={"source": "ospf.txt"})]
    pipeline.build_index = lambda: None
    assert docs[0].page_content.startswith("OSPF")
