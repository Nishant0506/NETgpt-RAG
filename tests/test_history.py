from src.history import HistoryStore


def test_history_store_round_trip(tmp_path):
    store = HistoryStore(history_dir=str(tmp_path))
    entry = store.create_entry("sample.log", [{"issue": "OSPF Neighbor Down", "severity": "HIGH", "confidence": 0.92}], "OSPF issue found")
    store.save(entry)
    history = store.load()
    assert len(history) == 1
    assert history[0]["filename"] == "sample.log"
