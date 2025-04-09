"""Tests for the FastAPI web server"""

import json
import threading
import time

import pytest
import uvicorn
from requests import post

import logfire

from ha_usage_records.main import app
from .test_usage_records import SAMPLE

logfire.configure(send_to_logfire=True)


@pytest.fixture(scope="module")
def web_server():
    """Pytest fixture for starting the server in a background thread."""
    # Configure the server to run on a specific port
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
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
        "http://localhost:8000/usage",
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
