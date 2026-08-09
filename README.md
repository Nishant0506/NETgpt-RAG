# NetGPT

NetGPT is a local, privacy-friendly network troubleshooting assistant that combines rule-based log analysis, a FAISS-backed RAG knowledge base, and optional Ollama-based reasoning to help users explain and troubleshoot common networking issues from uploaded logs and configuration files.

## Features

- Upload logs and configuration text files for analysis
- Parse common network events such as OSPF, BGP, DHCP, VLAN, and STP issues
- Extract evidence from uploaded content
- Retrieve relevant networking knowledge from a local FAISS index
- Generate an AI-assisted explanation using Ollama when available
- Download a basic PDF troubleshooting report
- Store an analysis history in JSON

## Architecture

- Streamlit UI for dashboard, log analysis, knowledge base, chat, history, reports, and settings
- Python parser and analyzer for evidence extraction
- FAISS + sentence-transformers knowledge retrieval
- Ollama LLM integration for explanation generation
- JSON-based analysis history

## Folder structure

- app.py – Streamlit entry point
- src/ – parser, analyzer, RAG, LLM, history, and report modules
- data/knowledge_base/ – local networking knowledge documents
- data/sample_logs/ – example logs for testing
- tests/ – parser, analyzer, RAG, history, pipeline, and app import tests
- scripts/build_vectorstore.py – rebuild the local FAISS index

## Installation

1. Create and activate a virtual environment
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Start Ollama locally if you want AI explanations:
   - `ollama serve`
4. Pull a model if needed:
   - `ollama pull llama3.2`
5. Build the FAISS index:
   - `python scripts/build_vectorstore.py`

## Run the app

- `streamlit run app.py`

## Run tests

- `pytest`

## Example input

A sample log file is available at data/sample_logs/ospf.log.

## Limitations

- The current parser is rule-based and focused on common evidence patterns.
- PDF upload parsing is basic and intended for text extraction scenarios.
- The Ollama integration is best-effort and gracefully falls back when the service is unavailable.
