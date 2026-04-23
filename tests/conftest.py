import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def game_module():
    module_path = Path(__file__).resolve().parents[1] / "code" / "reverse_turing_test.py"
    spec = importlib.util.spec_from_file_location("reverse_turing_test", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
