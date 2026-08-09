from src.pipeline import AnalysisPipeline
from src.history import HistoryStore


def test_analysis_pipeline_returns_summary_and_history(tmp_path):
    store = HistoryStore(history_dir=str(tmp_path))
    pipeline = AnalysisPipeline(history_store=store)
    result, entry = pipeline.run("sample.log", "Router1 %OSPF-5-ADJCHG: Neighbor 10.0.0.2 changed from FULL to DOWN")
    assert result.filename == "sample.log"
    assert result.summary
    assert entry["filename"] == "sample.log"
