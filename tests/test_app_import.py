import importlib


def test_app_imports():
    module = importlib.import_module("app")
    assert module is not None
