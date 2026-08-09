import os
import streamlit as st
from pathlib import Path

from src.config import KNOWLEDGE_BASE_DIR
from src.pipeline import AnalysisPipeline
from src.history import HistoryStore
from src.report_generator import ReportGenerator
from src.utils import extract_text_from_bytes, supported_extension

st.set_page_config(page_title="NetGPT", page_icon="🌐", layout="wide")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = AnalysisPipeline(history_store=HistoryStore())

st.sidebar.title("NetGPT")
st.sidebar.write("Local network troubleshooting assistant")
page = st.sidebar.radio("Navigation", ["Dashboard", "Log Analysis", "RAG Knowledge Base", "AI Chat", "Analysis History", "Reports", "Settings"])

if page == "Dashboard":
    st.title("Dashboard")
    history = HistoryStore().load()
    total_analyses = len(history)
    problems_detected = sum(len(item.get("detected_issues", [])) for item in history)
    critical_issues = sum(1 for item in history if item.get("severity") == "HIGH")
    high_severity_issues = sum(1 for item in history if item.get("severity") in {"HIGH", "MEDIUM"})
    st.metric("Total analyses", total_analyses)
    st.metric("Problems detected", problems_detected)
    st.metric("Critical issues", critical_issues)
    st.metric("High severity issues", high_severity_issues)
    st.write("Use the Log Analysis page to upload a log and inspect findings.")

elif page == "Log Analysis":
    st.title("Log Analysis")
    uploaded_file = st.file_uploader("Upload a text, log, cfg, conf, or PDF file", type=["txt", "log", "cfg", "conf", "pdf"])
    if uploaded_file is not None:
        if not supported_extension(uploaded_file.name):
            st.error("Unsupported file type. Please upload a .txt, .log, .cfg, .conf, or .pdf file.")
        else:
            file_bytes = uploaded_file.getvalue()
            text = extract_text_from_bytes(file_bytes, uploaded_file.name)
            st.text_area("Uploaded content", text or "No readable text could be extracted from the uploaded file.", height=200)
            if st.button("Analyze"):
                result, entry = st.session_state.pipeline.run(uploaded_file.name, text or "")
            st.success("Analysis complete")
            st.subheader("Detected Issues")
            for finding in result.findings:
                st.write(f"- {finding.issue} [{finding.severity}] confidence={finding.confidence:.2f}")
            st.subheader("Evidence")
            for evidence in result.evidence:
                st.write(f"• {evidence}")
            st.subheader("AI Explanation")
            st.write(result.llm_response or "No LLM response available")
            st.subheader("Recommended Commands")
            st.write(result.recommended_commands)
            st.subheader("Recommended Fix")
            st.write(result.recommended_fix)

            report = ReportGenerator().build_pdf({
                "filename": result.filename,
                "summary": result.summary,
                "findings": [{"issue": f.issue, "severity": f.severity} for f in result.findings],
            })
            st.download_button("Download PDF Report", report, file_name="netgpt_report.pdf", mime="application/pdf")

elif page == "RAG Knowledge Base":
    st.title("RAG Knowledge Base")
    for path in sorted(Path(KNOWLEDGE_BASE_DIR).glob("*.txt")):
        st.subheader(path.stem)
        st.write(path.read_text(encoding="utf-8"))

elif page == "AI Chat":
    st.title("AI Troubleshooting Chat")
    question = st.text_input("Ask a follow-up question")
    if st.button("Send") and question:
        st.write(f"You asked: {question}")
        st.write("This demo uses the latest analysis context and retrieved knowledge to guide the response.")

elif page == "Analysis History":
    st.title("Analysis History")
    store = HistoryStore()
    history = store.load()
    if history:
        search_term = st.text_input("Search history")
        filtered_history = [item for item in history if search_term.lower() in str(item).lower()] if search_term else history
        if filtered_history:
            selected = st.selectbox("Select an entry", range(len(filtered_history)), format_func=lambda i: filtered_history[i].get("filename", f"Entry {i + 1}"))
            if st.button("Delete selected"):
                store.delete(history.index(filtered_history[selected]))
                st.experimental_rerun()
            if st.button("Export history"):
                st.download_button("Download JSON", store.export(), file_name="history.json", mime="application/json")
            for item in filtered_history:
                st.write(item)
        else:
            st.write("No matching history entries.")
    else:
        st.write("No history yet.")

elif page == "Reports":
    st.title("Reports")
    st.write("Generate and download a PDF report from the Log Analysis page.")

elif page == "Settings":
    st.title("Settings")
    st.text_input("Ollama base URL", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    st.text_input("Ollama model", os.getenv("OLLAMA_MODEL", "llama3.2"))
    st.write("The app will use the local Ollama server when available.")
