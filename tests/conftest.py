"""Common pytest fixtures for all tests"""

from pathlib import Path
import pytest


@pytest.fixture
def sample_json_path():
    """Fixture that returns the path to the sample data file"""
    test_data_dir = Path(__file__).parent / "testdata"
    test_data_dir.mkdir(exist_ok=True)
    return test_data_dir / "sample.json"


@pytest.fixture
def sample_data(sample_json_path):
    """Fixture that provides the sample JSON data as a string"""
    with open(sample_json_path, "r", encoding="utf-8") as f:
        return f.read()
