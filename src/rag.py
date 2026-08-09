from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from .config import KNOWLEDGE_BASE_DIR, VECTORSTORE_DIR


class RAGPipeline:
    def __init__(self, persist_dir: str = VECTORSTORE_DIR):
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = None

    def build_index(self) -> None:
        docs = self._load_documents()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
        chunks = splitter.split_documents(docs)
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(self.persist_dir)

    def load_index(self) -> None:
        self.vectorstore = FAISS.load_local(self.persist_dir, self.embeddings, allow_dangerous_deserialization=True)

    def retrieve(self, query: str, k: int = 4) -> List[str]:
        if self.vectorstore is None:
            self.load_index()
        result = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in result]

    def _load_documents(self) -> List[Document]:
        documents: List[Document] = []
        for path in Path(KNOWLEDGE_BASE_DIR).glob("*.txt"):
            documents.append(Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name}))
        return documents
