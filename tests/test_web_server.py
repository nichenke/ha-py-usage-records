"""Tests for the FastAPI web server"""

import json
import threading
import time

import pytest
import uvicorn
from requests import post
import logfire
from unittest import mock

from ha_usage_records.main import app
from .test_usage_records import SAMPLE

logfire.configure(send_to_logfire=True)


@pytest.fixture
def records_dir(tmp_path):
    """Fixture to create a temporary directory for records."""
    records_path = tmp_path / "records"
    records_path.mkdir()
    return records_path


@pytest.fixture(scope="module")
def web_server():
    """Pytest fixture for starting the server in a background thread."""
    # Configure the server to run on a specific port
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8080, log_level="error")
    server = uvicorn.Server(config=config)

    # Override server install_signal_handlers to do nothing
    server.install_signal_handlers = lambda: None

    # Create a thread to run the server
    thread = threading.Thread(target=server.run)
    thread.daemon = True  # Daemon thread will be killed when the main thread exits

    # Start the server
    thread.start()

    # Give the server time to start up
    time.sleep(1)

    # Provide the test with access to the running server
    yield server

    # Clean up using the proper shutdown method
    server.handle_exit(sig=None, frame=None)
    thread.join(timeout=1)


@pytest.mark.parametrize(
    "record_count,expected_count",
    [
        (1, 1),  # Single record test
        (2, 2),  # Multiple records test
    ],
    ids=["single_record", "multiple_records"],
)
def test_record_processing(web_server, record_count, expected_count):
    """Test processing records with parameterized count"""
    # pylint: disable=W0621,W0613

    # Parse the sample JSON
    sample_data = json.loads(SAMPLE)

    # Create array with the specified number of records
    records_array = [sample_data] * record_count

    # Send the array of records
    response = post(
        "http://localhost:8080/usage",
        json=records_array,
        headers={"Content-Type": "application/json"},
        timeout=5.0,  # Added timeout
    )

    assert response.status_code == 200

    # Check that we got back a dictionary with the count of records processed
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "records_processed" in response_data
    assert response_data["records_processed"] == expected_count


def test_middleware_record_storage(web_server, records_dir):
    """Test that the middleware correctly stores records in the records directory."""
    # pylint: disable=W0621,W0613

    # Mock the RECORDS_DIR with our temporary directory
    with mock.patch("ha_usage_records.main.RECORDS_DIR", records_dir):
        # Parse the sample JSON
        sample_data = json.loads(SAMPLE)
        records_array = [sample_data]

        # Send a request to trigger the middleware
        response = post(
            "http://localhost:8080/usage",
            json=records_array,
            headers={"Content-Type": "application/json"},
            timeout=5.0,
        )

        assert response.status_code == 200

        # Give the middleware a moment to write the file
        time.sleep(0.5)

        # Check that a file was created
        json_files = list(records_dir.glob("*.json"))
        assert len(json_files) == 1

        # Verify the file content
        with open(json_files[0], "r", encoding="utf-8") as f:
            stored_data = json.load(f)

        # The middleware should store the raw request body, which is an array of records
        assert isinstance(stored_data, list)
        assert len(stored_data) == 1

        # Verify key data points match what was sent
        assert stored_data[0]["id"] == sample_data["id"]
        assert stored_data[0]["imsi"] == sample_data["imsi"]
