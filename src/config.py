import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
VECTORSTORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "knowledge_base")
SAMPLE_LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_logs")
HISTORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "history")
