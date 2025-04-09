import pytest
import time
import threading
import uvicorn
from ha_usage_records.main import app
from .test_usage_records import SAMPLE

from requests import put


@pytest.fixture(scope="module")
def web_server():
    """Pytest fixture for starting the server in a background thread."""
    # Configure the server to run on a specific port
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config=config)

    # Create a thread to run the server
    thread = threading.Thread(target=server.run)
    thread.daemon = True  # Daemon thread will be killed when the main thread exits

    # Start the server
    thread.start()

    # Give the server time to start up
    time.sleep(1)

    # Provide the test with access to the running server
    yield server

    # Clean up (though daemon thread will be killed automatically)
    server.should_exit = True
    thread.join(timeout=1)


def test_web_request(web_server):
    """test web request"""
    response = put("http://localhost:8000/usage", data=SAMPLE)
    assert response.status_code == 200
    assert response.json() == {
        "record.id": 1234567890,
        "record.start_timestamp": "2021-08-09T12:59:05Z",
    }
    print(response)
